import speech_recognition as sr
from colorama import init, Fore
from mood_music import analyze_mood, get_music_for_mood
import os
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Initialize colorama
init()

# Get absolute path to the audio directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

def check_music_files():
    """Check if all music files exist at startup."""
    missing_files = []
    for mood, config in MOOD_CONFIG.items():
        track = config["track"]
        # Update track path to absolute
        config["track"] = os.path.join(AUDIO_DIR, os.path.basename(track))
        if not os.path.exists(config["track"]):
            missing_files.append(config["track"])
    return missing_files

def record_mood():
    """Record spoken mood."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.CYAN + "🎙️ Say how you feel today...")
        print(Fore.CYAN + "🎤 Listening... (speak clearly, ensure your mic is on, press Ctrl+C to cancel)")
        print(Fore.CYAN + "💡 Tip: If it fails to hear, check your mic settings or reduce background noise.")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Increased duration
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(Fore.RED + f"❌ Speech recognition error: {e}. Check your internet connection.")
        return None

def play_music(track, volume=0.5):
    """Play music track if pygame is available."""
    if not PYGAME_AVAILABLE:
        print(Fore.RED + "⚠️ Music playback unavailable (pygame not installed).")
        return False
    if not os.path.exists(track):
        print(Fore.RED + f"⚠️ Music file '{track}' not found. Skipping playback.")
        print(Fore.RED + "💡 Download royalty-free tracks from Pixabay (https://pixabay.com/music/) and save as:")
        print(Fore.RED + "  - audio/positive.mp3 (upbeat)")
        print(Fore.RED + "  - audio/neutral.mp3 (calm)")
        print(Fore.RED + "  - audio/negative.mp3 (soothing)")
        return False
    try:
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(volume)  # Set initial volume
        pygame.mixer.music.play()
        return True
    except Exception as e:
        print(Fore.RED + f"⚠️ Error playing music: {e}")
        return False

def adjust_volume(current_volume):
    """Adjust music volume."""
    print(Fore.WHITE + f"\n🎚️ Current volume: {int(current_volume * 100)}%")
    print(Fore.WHITE + "  (1) 25%  (2) 50%  (3) 75%  (4) 100%  (s) Skip")
    choice = input(Fore.WHITE + "Select volume (1-4, s to skip): ").lower()
    volume_map = {"1": 0.25, "2": 0.50, "3": 0.75, "4": 1.00}
    if choice in volume_map:
        new_volume = volume_map[choice]
        if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(new_volume)
        return new_volume
    return current_volume

def stop_music():
    """Stop music playback."""
    if PYGAME_AVAILABLE:
        pygame.mixer.music.stop()

# Import MOOD_CONFIG for checking files
from mood_music import MOOD_CONFIG

def main():
    print(Fore.CYAN + "🎵 Welcome to MoodMuse! Let your emotions sing! 🎧")
    
    # Check for missing music files at startup
    missing_files = check_music_files()
    if missing_files:
        print(Fore.YELLOW + "⚠️ Warning: The following music files are missing:")
        for f in missing_files:
            print(Fore.YELLOW + f"  - {f}")
        print(Fore.YELLOW + "Please add them to the 'audio/' folder to enable music playback.")
        print(Fore.YELLOW + "💡 Download royalty-free tracks from Pixabay (https://pixabay.com/music/).")
    
    last_track = None  # Track the last played music for replay
    current_volume = 0.5  # Default volume 50%
    
    while True:
        mood_text = record_mood()
        if not mood_text:
            print(Fore.RED + "❌ Couldn’t hear you. Try again!")
            continue
        
        print(Fore.GREEN + f"\n🧠 Analyzing emotion...")
        mood, score = analyze_mood(mood_text)
        music_config = get_music_for_mood(mood)
        
        # Display results
        print(Fore.GREEN + f"📜 You said: \"{mood_text}\"")
        print(Fore.MAGENTA + f"😊 Mood: {mood.capitalize()} (Score: {score:.2f})")
        print(Fore.YELLOW + f"🎧 Now playing: “{music_config['title']}” for your mood")
        print(Fore.YELLOW + f"✨ Tip: “{music_config['tip']}”")
        
        # Play music
        played = play_music(music_config["track"], current_volume)
        last_track = music_config["track"] if played else None
        
        # Adjust volume if music is playing
        if played:
            current_volume = adjust_volume(current_volume)
        
        # Ask to replay, try again, or exit
        print(Fore.WHITE + "\nWhat would you like to do?")
        print(Fore.WHITE + "  (r) Replay music  (y) Express another mood  (n) Exit")
        choice = input(Fore.WHITE + "Choice (r/y/n): ").lower()
        stop_music()  # Stop music before next action
        
        if choice == 'r' and last_track:
            print(Fore.YELLOW + f"🎧 Replaying: “{music_config['title']}”")
            played = play_music(last_track, current_volume)
            if played:
                current_volume = adjust_volume(current_volume)
            choice = input(Fore.WHITE + "\nWould you like to express another mood? (y/n): ").lower()
            stop_music()
        
        if choice != 'y':
            print(Fore.CYAN + "🌟 Thank you for sharing your emotions!")
            break

if __name__ == "__main__":
    main()