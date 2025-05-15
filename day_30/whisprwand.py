import speech_recognition as sr
from colorama import init, Fore
from mood_magic import analyze_mood, get_affirmation
from journal_logger import save_journal
import os

# Try importing pygame, but continue if not available
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Initialize colorama
init()

# Optional: Play a gentle chime sound (provide your own chime.wav)
CHIME_SOUND = "chime.wav"

def play_chime():
    """Play a gentle chime sound if available."""
    if PYGAME_AVAILABLE and os.path.exists(CHIME_SOUND):
        try:
            pygame.mixer.Sound(CHIME_SOUND).play()
        except:
            pass

def record_wish():
    """Record spoken wish."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.CYAN + "🎙️ Speak your wish...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def main():
    print(Fore.CYAN + "🪄 Welcome to WhisprWand! Speak your dreams! ✨")
    
    while True:
        wish = record_wish()
        if not wish:
            print(Fore.RED + "❌ Couldn’t hear your wish. Try again!")
            continue
        
        print(Fore.GREEN + f"\n🧠 Analyzing your emotion...")
        mood, score = analyze_mood(wish)
        affirmation = get_affirmation(mood)
        
        # Display results
        print(Fore.GREEN + f"📜 Your Wish: \"{wish}\"")
        print(Fore.MAGENTA + f"😊 Detected Mood: {mood.capitalize()} (Score: {score:.2f})")
        print(Fore.YELLOW + f"\n🌈 Whisper Logged!")
        print(Fore.YELLOW + f"✨ Magic Note: \"{affirmation}\"")
        
        # Save to journal
        save_journal(wish, mood, affirmation)
        print(Fore.GREEN + "📘 Saved to your Wish Journal!")
        
        # Play chime (optional)
        play_chime()
        
        # Continue or exit
        choice = input(Fore.WHITE + "\nWould you like to speak another dream? (y/n): ").lower()
        if choice != 'y':
            print(Fore.CYAN + "🌟 Thank you for sharing your wishes!")
            break

if __name__ == "__main__":
    main()