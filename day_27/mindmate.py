import speech_recognition as sr
from transformers import pipeline
from datetime import datetime
import random
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Initialize recognizer and sentiment analysis pipeline
recognizer = sr.Recognizer()
sentiment_pipeline = pipeline("sentiment-analysis")

# Sample affirmations
affirmations = {
    "POSITIVE": [
        "You're capable of amazing things! Keep shining! ✨",
        "Today is a new day, full of possibilities! 🌟",
        "Believe in yourself—you've got this! 💪",
        "Your positivity is contagious! Keep it up! 😊"
    ],
    "NEGATIVE": [
        "Every day is a new beginning. Take a deep breath. 🌈",
        "Remember, even tough times pass. Stay strong! 💖",
        "You are resilient and capable of overcoming challenges. 🌻",
        "Believe in brighter days ahead. Keep faith! 🌞"
    ],
    "NEUTRAL": [
        "Maintain your balance and stay positive. 🌟",
        "Take a moment to breathe and center yourself. 🌬️",
        "Every mood is temporary. Embrace the present. 🌸",
        "Stay grounded and keep moving forward. 🚶‍♂️"
    ]
}

def listen_and_detect_mood():
    with sr.Microphone() as source:
        print(Fore.CYAN + "Listening... Please speak your thoughts.")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print(Fore.YELLOW + "Processing your input...")
            text = recognizer.recognize_google(audio)
            print(Fore.GREEN + f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print(Fore.RED + "Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print(Fore.RED + "Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(Fore.RED + f"API error: {e}")
    return None

def detect_mood(text):
    if not text:
        return "NEUTRAL"
    result = sentiment_pipeline(text)[0]
    label = result['label']
    if label == 'POSITIVE':
        return 'POSITIVE'
    elif label == 'NEGATIVE':
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'

def get_affirmation(mood):
    return random.choice(affirmations[mood])

def display_affirmation(mood):
    affirmation = get_affirmation(mood)
    emoji = {
        "POSITIVE": "😊",
        "NEGATIVE": "😢",
        "NEUTRAL": "🤔"
    }[mood]
    color = {
        "POSITIVE": Fore.GREEN,
        "NEGATIVE": Fore.RED,
        "NEUTRAL": Fore.YELLOW
    }[mood]
    print(color + f"\n{emoji} Here's an affirmation for you:\n{affirmation}\n")
    return affirmation

def save_favorite(affirmation):
    choice = input("Would you like to save this affirmation as a favorite? (y/n): ").lower()
    if choice == 'y':
        with open("favorites.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {affirmation}\n")
        print(Fore.MAGENTA + "Saved to favorites!\n")
    else:
        print("No worries!\n")

def main():
    print(Fore.MAGENTA + "🌟 Welcome to MindMate! Your Personal Affirmation Companion 🌟\n")
    while True:
        text = listen_and_detect_mood()
        if text:
            mood = detect_mood(text)
            print(Fore.CYAN + f"Detected mood: {mood}")
            affirmation = display_affirmation(mood)
            save_favorite(affirmation)
        else:
            print(Fore.RED + "Let's try again.\n")
        cont = input("Would you like another go? (y/n): ").lower()
        if cont != 'y':
            print(Fore.MAGENTA + "Take care! Remember, you're awesome. 💖")
            break

if __name__ == "__main__":
    main()