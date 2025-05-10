import requests

# my weather API key
API_KEY = "b4f314e071a5462a7586a41bf72a8fd1"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_weather(data):
    try:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_condition = data['weather'][0]['main']
        return temp, humidity, wind_speed, weather_condition
    except (KeyError, IndexError):
        print("Error parsing weather data.")
        return None

def get_weather_emoji(condition):
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

def main():
    print("🌤️ Welcome to the Live Weather Dashboard! 🌤️")
    city = input("Enter a city name: ").strip()
    data = get_weather(city)

    if data and data.get('cod') == 200:
        weather_info = parse_weather(data)
        if weather_info:
            temp, humidity, wind_speed, condition = weather_info
            emoji = get_weather_emoji(condition)
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

if __name__ == "__main__":
    main()