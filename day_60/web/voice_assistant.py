import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import random

class VoiceAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("🎙️ Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("✅ Ready to listen!")
        
        # Assistant name
        self.name = "Assistant"
        
        # Add callback for GUI integration
        self.speech_callback = None
    
    def set_speech_callback(self, callback):
        """Set callback function for GUI speech output"""
        self.speech_callback = callback
        
    def setup_voice(self):
        """Configure the voice settings"""
        voices = self.engine.getProperty('voices')
        # Try to set a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 {self.name}: {text}")
        # Call GUI callback if available
        if self.speech_callback:
            self.speech_callback(text)
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("🎧 Listening...")
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            print("🔄 Processing...")
            # Convert speech to text
            command = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout")
            return ""
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            self.speak("Sorry, I'm having trouble with speech recognition right now.")
            return ""
    
    def get_current_time(self):
        """Get current time and date"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"The current time is {time_str} on {date_str}"
    
    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            # Remove common words from the query
            query = query.replace("search for", "").replace("tell me about", "").replace("what is", "").strip()
            
            if not query:
                return "What would you like me to search for?"
            
            print(f"🔍 Searching Wikipedia for: {query}")
            # Get summary (2 sentences)
            summary = wikipedia.summary(query, sentences=2)
            return f"Here's what I found about {query}: {summary}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            # If multiple results, pick the first one
            try:
                summary = wikipedia.summary(e.options[0], sentences=2)
                return f"I found multiple results. Here's information about {e.options[0]}: {summary}"
            except:
                return f"I found multiple results for {query}. Could you be more specific?"
        except wikipedia.exceptions.PageError:
            return f"Sorry, I couldn't find any information about {query} on Wikipedia."
        except Exception as e:
            return f"Sorry, I encountered an error while searching: {str(e)}"
    
    def open_website(self, site):
        """Open websites in the default browser"""
        sites = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'reddit': 'https://www.reddit.com',
            'twitter': 'https://www.twitter.com',
            'facebook': 'https://www.facebook.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'amazon': 'https://www.amazon.com'
        }
        
        site = site.lower().strip()
        if site in sites:
            webbrowser.open(sites[site])
            return f"Opening {site.title()} for you!"
        else:
            # Try to open as a direct URL
            if 'www.' in site or '.com' in site:
                webbrowser.open(f"https://{site}")
                return f"Opening {site} for you!"
            else:
                return f"Sorry, I don't know how to open {site}. Try saying the full website name."
    
    def play_music(self):
        """Open music streaming service"""
        music_services = [
            'https://open.spotify.com',
            'https://music.youtube.com',
            'https://music.apple.com'
        ]
        
        # Open Spotify by default, or first available service
        webbrowser.open(music_services[0])
        return "Opening Spotify for you! Enjoy your music!"
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        return random.choice(jokes)
    
    def process_command(self, command):
        """Process voice commands and execute appropriate actions"""
        if not command:
            return
        
        # Greeting commands
        if any(word in command for word in ['hello', 'hi', 'hey']):
            greetings = [
                f"Hello! I'm your voice assistant. How can I help you today?",
                f"Hi there! What can I do for you?",
                f"Hey! I'm here to help. What do you need?"
            ]
            self.speak(random.choice(greetings))
        
        # Time and date commands
        elif any(word in command for word in ['time', 'date', 'today']):
            time_info = self.get_current_time()
            self.speak(time_info)
        
        # Wikipedia search commands
        elif any(word in command for word in ['search', 'tell me about', 'what is', 'who is']):
            result = self.search_wikipedia(command)
            self.speak(result)
        
        # Website opening commands
        elif 'open' in command:
            # Extract website name
            words = command.split()
            if 'open' in words:
                site_index = words.index('open') + 1
                if site_index < len(words):
                    site = ' '.join(words[site_index:])
                    result = self.open_website(site)
                    self.speak(result)
                else:
                    self.speak("What website would you like me to open?")
        
        # Music commands
        elif any(word in command for word in ['play music', 'music', 'song', 'spotify']):
            result = self.play_music()
            self.speak(result)
        
        # Joke commands
        elif any(word in command for word in ['joke', 'funny', 'laugh']):
            joke = self.tell_joke()
            self.speak(joke)
        
        # Exit commands
        elif any(word in command for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            farewell_messages = [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! It was nice talking with you!"
            ]
            self.speak(random.choice(farewell_messages))
            return False
        
        # Help commands
        elif 'help' in command:
            help_text = """Here are some things you can ask me to do:
            Say 'time' or 'date' for current time and date.
            Say 'search for' followed by a topic to search Wikipedia.
            Say 'open' followed by a website name to open websites.
            Say 'play music' to open Spotify.
            Say 'tell me a joke' for a random joke.
            Say 'goodbye' or 'exit' to quit."""
            self.speak(help_text)
        
        # Unknown command
        else:
            responses = [
                "I'm not sure how to help with that. Try saying 'help' to see what I can do.",
                "I didn't understand that command. Say 'help' to see available options.",
                "Sorry, I don't know how to do that yet. Ask me for help to see what I can do."
            ]
            self.speak(random.choice(responses))
        
        return True
    
    def run(self):
        """Main loop for the voice assistant"""
        print("🚀 Starting Voice Assistant...")
        print("=" * 50)
        
        # Welcome message
        welcome_msg = f"Hello! I'm your voice assistant. Say 'help' to see what I can do, or just start talking!"
        self.speak(welcome_msg)
        
        # Main interaction loop
        while True:
            try:
                command = self.listen()
                if command:
                    should_continue = self.process_command(command)
                    if should_continue is False:
                        break
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                self.speak("Sorry, I encountered an error. Let me try again.")
        
        print("👋 Voice Assistant stopped.")

def main():
    """Main function to run the voice assistant"""
    print("🎙️ Python Voice Assistant")
    print("=" * 30)
    
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Failed to start voice assistant: {e}")
        print("Make sure you have installed all required packages:")
        print("pip install pyttsx3 speechrecognition wikipedia pyaudio")

if __name__ == "__main__":
    main()
