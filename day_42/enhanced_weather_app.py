import requests
import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
from datetime import datetime
import json

# Optional voice features (install with: pip install pyttsx3 speechrecognition pyaudio)
try:
    import pyttsx3
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Voice features unavailable. Install: pip install pyttsx3 speechrecognition pyaudio")

# Weather API Configuration
API_KEY = "b4f314e071a5462a7586a41bf72a8fd1"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌤️ Smart Weather Dashboard")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Voice setup
        if VOICE_AVAILABLE:
            # Only initialize recognizer - create TTS engines as needed to avoid conflicts
            self.recognizer = sr.Recognizer()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main title
        title_font = font.Font(family="Arial", size=20, weight="bold")
        title_label = tk.Label(self.root, text="🌤️ Smart Weather Dashboard", 
                              font=title_font, bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#2c3e50')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter City:", bg='#2c3e50', fg='white', font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        self.city_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="Get Weather", command=self.get_weather,
                 bg='#3498db', fg='white', font=('Arial', 11), padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="5-Day Forecast", command=self.get_forecast,
                 bg='#e74c3c', fg='white', font=('Arial', 11), padx=20).pack(side=tk.LEFT, padx=5)
        
        if VOICE_AVAILABLE:
            tk.Button(buttons_frame, text="🎤 Voice Input", command=self.voice_input,
                     bg='#9b59b6', fg='white', font=('Arial', 11), padx=20).pack(side=tk.LEFT, padx=5)
        
        # Weather display frame
        self.weather_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=2)
        self.weather_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollable text widget for weather info
        self.weather_text = tk.Text(self.weather_frame, font=('Arial', 11), 
                                   bg='#ecf0f1', fg='#2c3e50', wrap=tk.WORD, 
                                   state=tk.DISABLED, height=25)
        
        scrollbar = tk.Scrollbar(self.weather_frame, orient=tk.VERTICAL, command=self.weather_text.yview)
        self.weather_text.configure(yscrollcommand=scrollbar.set)
        
        self.weather_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
    def display_text(self, text, speak=False):
        """Display text in the weather display area"""
        self.weather_text.config(state=tk.NORMAL)
        self.weather_text.delete(1.0, tk.END)
        self.weather_text.insert(tk.END, text)
        self.weather_text.config(state=tk.DISABLED)
        
        if speak and VOICE_AVAILABLE:
            threading.Thread(target=self.speak_text, args=(text,), daemon=True).start()
    
    def speak_text(self, text):
        """Convert text to speech"""
        try:
            # Clean text for speech (remove emojis and special characters)
            clean_text = ''.join(char for char in text if ord(char) < 128)
            
            # Create a fresh TTS engine for each speech to avoid conflicts
            tts = pyttsx3.init()
            tts.setProperty('rate', 150)
            tts.say(clean_text)
            tts.runAndWait()
            tts.stop()  # Clean shutdown
            del tts  # Free resources
            
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def voice_input(self):
        """Handle voice input for city name"""
        if not VOICE_AVAILABLE:
            messagebox.showwarning("Voice Unavailable", "Voice features not installed")
            return
        
        def listen():
            try:
                # Create a fresh microphone instance for each use
                mic = sr.Microphone()
                with mic as source:
                    self.display_text("🎤 Listening... Say a city name:")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Recognize speech outside the with block
                city = self.recognizer.recognize_google(audio)
                
                # Update UI in main thread
                self.root.after(0, lambda: self._update_city_and_fetch(city))
                
            except sr.WaitTimeoutError:
                self.root.after(0, lambda: self.display_text("❌ Voice input timeout. Please try again."))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.display_text("❌ Could not understand audio. Please try again."))
            except sr.RequestError as e:
                self.root.after(0, lambda: self.display_text(f"❌ Could not request results; {e}"))
            except Exception as e:
                self.root.after(0, lambda: self.display_text(f"❌ Voice input error: {e}"))
        
        threading.Thread(target=listen, daemon=True).start()
    
    def _update_city_and_fetch(self, city):
        """Helper method to update city entry and fetch weather (called from main thread)"""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city.title())
        self.get_weather()
    
    def get_current_weather(self, city):
        """Fetch current weather data"""
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return None
    
    def get_forecast_data(self, city):
        """Fetch 5-day forecast data"""
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        try:
            response = requests.get(FORECAST_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return None
    
    def get_weather_emoji(self, condition):
        """Get emoji for weather condition"""
        condition = condition.lower()
        emoji_map = {
            "clear": "☀️",
            "rain": "🌧️",
            "drizzle": "🌦️",
            "clouds": "☁️",
            "snow": "❄️",
            "thunderstorm": "⛈️",
            "mist": "🌫️",
            "fog": "🌫️",
            "haze": "🌫️"
        }
        return emoji_map.get(condition, "🌤️")
    
    def get_weather_suggestions(self, temp, condition, humidity, wind_speed):
        """Generate weather-based suggestions"""
        suggestions = []
        condition_lower = condition.lower()
        
        # Temperature suggestions
        if temp > 30:
            suggestions.append("🔥 It's quite hot! Stay hydrated and avoid prolonged sun exposure.")
        elif temp > 25:
            suggestions.append("☀️ Perfect weather for outdoor activities!")
        elif temp < 5:
            suggestions.append("🧥 Bundle up! It's very cold outside.")
        elif temp < 15:
            suggestions.append("🧥 Consider wearing a jacket or sweater.")
        
        # Weather condition suggestions
        if "rain" in condition_lower or "drizzle" in condition_lower:
            suggestions.append("☔ Don't forget your umbrella!")
        elif "thunderstorm" in condition_lower:
            suggestions.append("⚡ Stay indoors if possible - thunderstorm conditions!")
        elif "snow" in condition_lower:
            suggestions.append("❄️ Drive carefully and wear warm clothes!")
        elif "fog" in condition_lower or "mist" in condition_lower:
            suggestions.append("🌫️ Visibility might be low - drive safely!")
        
        # Humidity suggestions
        if humidity > 80:
            suggestions.append("💧 High humidity - you might feel sticky!")
        elif humidity < 30:
            suggestions.append("🏜️ Low humidity - consider using moisturizer!")
        
        # Wind suggestions
        if wind_speed > 10:
            suggestions.append("💨 It's quite windy - secure loose objects!")
        
        return suggestions
    
    def format_current_weather(self, data):
        """Format current weather data for display"""
        try:
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            visibility = data['visibility'] / 1000  # Convert to km
            wind_speed = data['wind']['speed']
            wind_direction = data['wind'].get('deg', 0)
            condition = data['weather'][0]['main']
            description = data['weather'][0]['description'].title()
            emoji = self.get_weather_emoji(condition)
            
            # Get suggestions
            suggestions = self.get_weather_suggestions(temp, condition, humidity, wind_speed)
            
            # Format display
            weather_info = f"""
🌍 CURRENT WEATHER FOR {city.upper()}, {country}
{'='*50}

{emoji} {description}

🌡️  TEMPERATURE
    Current: {temp}°C
    Feels like: {feels_like}°C

💨 WIND & ATMOSPHERE
    Wind Speed: {wind_speed} m/s
    Wind Direction: {wind_direction}°
    Humidity: {humidity}%
    Pressure: {pressure} hPa
    Visibility: {visibility:.1f} km

💡 SMART SUGGESTIONS:
"""
            
            for i, suggestion in enumerate(suggestions, 1):
                weather_info += f"    {i}. {suggestion}\n"
            
            if not suggestions:
                weather_info += "    Perfect conditions - enjoy your day! 😊\n"
            
            weather_info += f"\n📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            return weather_info
            
        except KeyError as e:
            return f"❌ Error formatting weather data: missing key {e}"
        except IndexError as e:
            return f"❌ Error formatting weather data: list index error {e}"
    
    def format_forecast(self, data):
        """Format 5-day forecast data for display"""
        try:
            city = data['city']['name']
            country = data['city']['country']
            
            forecast_info = f"""
🌍 5-DAY FORECAST FOR {city.upper()}, {country}
{'='*60}

"""
            
            # Group forecasts by day
            daily_forecasts = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(item)
            
            # Display first 5 days
            for i, (date, forecasts) in enumerate(list(daily_forecasts.items())[:5]):
                day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %d')
                
                # Get average values for the day
                temps = [f['main']['temp'] for f in forecasts]
                conditions = [f['weather'][0]['main'] for f in forecasts]
                humidity_vals = [f['main']['humidity'] for f in forecasts]
                wind_vals = [f['wind']['speed'] for f in forecasts]
                
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)
                most_common_condition = max(set(conditions), key=conditions.count)
                avg_humidity = sum(humidity_vals) / len(humidity_vals)
                avg_wind = sum(wind_vals) / len(wind_vals)
                
                emoji = self.get_weather_emoji(most_common_condition)
                
                forecast_info += f"""📅 {day_name}
    {emoji} {most_common_condition}
    🌡️  High: {max_temp:.1f}°C | Low: {min_temp:.1f}°C | Avg: {avg_temp:.1f}°C
    💧 Humidity: {avg_humidity:.0f}%
    💨 Wind: {avg_wind:.1f} m/s

"""
            
            # Add general forecast suggestions
            forecast_info += """💡 WEEKLY OUTLOOK TIPS:
    • Check daily before heading out
    • Weather can change quickly
    • Plan outdoor activities for clear days
    • Keep an umbrella handy during rainy periods

"""
            forecast_info += f"📅 Forecast generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            return forecast_info
            
        except (KeyError, IndexError) as e:
            return f"❌ Error parsing forecast data: {e}"
    
    def get_weather(self):
        """Get current weather for entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        self.display_text("🔄 Fetching weather data...")
        
        def fetch_weather():
            data = self.get_current_weather(city)
            
            if data and data.get('cod') == 200:
                weather_info = self.format_current_weather(data)
                self.display_text(weather_info, speak=True)
            else:
                error_msg = data.get('message', 'Unknown error') if data else 'No data received'
                error_text = f"❌ Error fetching weather data for '{city}':\n{error_msg}"
                self.display_text(error_text)
        
        threading.Thread(target=fetch_weather, daemon=True).start()
    
    def get_forecast(self):
        """Get 5-day forecast for entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        self.display_text("🔄 Fetching 5-day forecast...")
        
        def fetch_forecast():
            data = self.get_forecast_data(city)
            
            if data and data.get('cod') == '200':
                forecast_info = self.format_forecast(data)
                self.display_text(forecast_info, speak=True)
            else:
                error_msg = data.get('message', 'Unknown error') if data else 'No data received'
                error_text = f"❌ Error fetching forecast data for '{city}':\n{error_msg}"
                self.display_text(error_text)
        
        threading.Thread(target=fetch_forecast, daemon=True).start()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

# Console-based weather functions (original functionality)
def get_weather_console(city):
    """Console version of weather fetching"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_weather_console(data):
    """Console version of weather parsing"""
    try:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_condition = data['weather'][0]['main']
        return temp, humidity, wind_speed, weather_condition
    except (KeyError, IndexError):
        print("Error parsing weather data.")
        return None

def get_weather_emoji_console(condition):
    """Console version of emoji selection"""
    condition = condition.lower()
    if condition == "clear":
        return "😎"
    elif condition == "rain":
        return "🌧️"
    elif condition == "clouds":
        return "☁️"
    elif condition == "snow":
        return "❄️"
    elif condition == "thunderstorm":
        return "⚡"
    else:
        return ""

def console_mode():
    """Run the original console version"""
    print("🌤️ Welcome to the Live Weather Dashboard! 🌤️")
    city = input("Enter a city name: ").strip()
    data = get_weather_console(city)

    if data and data.get('cod') == 200:
        weather_info = parse_weather_console(data)
        if weather_info:
            temp, humidity, wind_speed, condition = weather_info
            emoji = get_weather_emoji_console(condition)
            print(f"\nWeather in {city.title()}: {emoji}")
            print(f"🌡️ Temperature: {temp}°C")
            print(f"☁️ Condition: {condition}")
            print(f"💧 Humidity: {humidity}%")
            print(f"🌬️ Wind Speed: {wind_speed} m/s")
        else:
            print("Could not parse weather data.")
    else:
        error_message = data.get('message', 'Unknown error') if data else 'No data received'
        print(f"Error fetching weather data for '{city}': {error_message}")

def main():
    """Main function to choose between GUI and console mode"""
    print("🌤️ Smart Weather App")
    print("1. Launch GUI Dashboard")
    print("2. Use Console Mode")
    
    try:
        choice = input("Choose mode (1 or 2): ").strip()
        
        if choice == "1":
            app = WeatherApp()
            app.run()
        elif choice == "2":
            console_mode()
        else:
            print("Invalid choice. Launching GUI by default...")
            app = WeatherApp()
            app.run()
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to console mode...")
        console_mode()

if __name__ == "__main__":
    main()