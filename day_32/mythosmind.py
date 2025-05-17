import speech_recognition as sr
from colorama import init, Fore
from oracle_wisdom import analyze_mood, select_deity, get_wisdom
from mythos_logger import save_journal
import os
import numpy as np
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
SOUND_FILE = os.path.join(AUDIO_DIR, "oracle_chant.wav")

def check_sound_file():
    """Check if the ambient sound file exists."""
    if not os.path.exists(SOUND_FILE):
        return False
    return True

def generate_fallback_sound():
    """Generate a softer, lower-frequency sine wave with fade effects as a fallback."""
    if not PYGAME_AVAILABLE:
        return None
    try:
        # Generate a 0.5-second 220 Hz sine wave (lower, calming tone)
        sample_rate = 44100
        duration = 0.5  # 0.5 seconds
        frequency = 220  # Hz (lower tone)
        volume = 0.3  # 30% volume to start
        samples = np.arange(int(duration * sample_rate))
        waveform = np.sin(2 * np.pi * frequency * samples / sample_rate) * 32767 * volume
        # Add fade-in and fade-out (first and last 10% of the duration)
        fade_length = int(0.1 * len(waveform))
        fade_in = np.linspace(0, 1, fade_length)
        fade_out = np.linspace(1, 0, fade_length)
        waveform[:fade_length] *= fade_in
        waveform[-fade_length:] *= fade_out
        waveform = waveform.astype(np.int16)
        # Convert to stereo by duplicating the channel
        stereo_waveform = np.stack((waveform, waveform), axis=1)
        sound = pygame.sndarray.make_sound(stereo_waveform)
        return sound
    except Exception as e:
        print(Fore.RED + f"⚠️ Error generating fallback sound: {e}")
        return None

def test_sound_playback(volume=0.5):
    """Test sound playback to confirm pygame is working."""
    if not PYGAME_AVAILABLE:
        print(Fore.YELLOW + "⚠️ Pygame not installed. Sound playback unavailable.")
        return False, None
    if not os.path.exists(SOUND_FILE):
        print(Fore.YELLOW + f"⚠️ Sound file '{SOUND_FILE}' not found.")
        print(Fore.YELLOW + "💡 Download a soothing .wav sound (e.g., mystical chant, wind chimes) from Pixabay (https://pixabay.com/sound-effects/)")
        print(Fore.YELLOW + "  and save as 'audio/oracle_chant.wav'. Ensure it's PCM, 16-bit, 44100 Hz.")
        print(Fore.YELLOW + "🔊 Using a fallback sound (soft tone) instead.")
        sound = generate_fallback_sound()
        if sound:
            sound.set_volume(volume)
            sound.play()
            print(Fore.CYAN + "🔊 You should hear a soft, low tone. Press Enter to continue.")
            input()
            sound.stop()
            return True, sound
        return False, None
    try:
        print(Fore.CYAN + "🔊 Testing sound playback...")
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        print(Fore.CYAN + "🔊 If you hear a sound, pygame is working. Press Enter to continue.")
        input()
        pygame.mixer.music.stop()
        return True, None
    except Exception as e:
        print(Fore.RED + f"⚠️ Error during sound test: {e}")
        print(Fore.RED + "💡 The WAV file might be incompatible. Convert it to PCM, 16-bit, 44100 Hz using CloudConvert (https://cloudconvert.com/wav-converter).")
        print(Fore.RED + "💡 Alternatively, download a new soothing .wav file (e.g., mystical chant) from Pixabay (https://pixabay.com/sound-effects/).")
        print(Fore.RED + "💡 Also check your audio device (speakers/headphones) in Windows Sound Settings.")
        print(Fore.YELLOW + "🔊 Using a fallback sound (soft tone) instead.")
        sound = generate_fallback_sound()
        if sound:
            sound.set_volume(volume)
            sound.play()
            print(Fore.CYAN + "🔊 You should hear a soft, low tone. Press Enter to continue.")
            input()
            sound.stop()
            return True, sound
        return False, None

def play_sound(volume=0.5, fallback_sound=None):
    """Play ambient sound if available, or use fallback sound."""
    if not PYGAME_AVAILABLE:
        print(Fore.YELLOW + "⚠️ Ambient sound unavailable (pygame not installed).")
        return False
    if fallback_sound:
        try:
            fallback_sound.set_volume(volume)
            fallback_sound.play(-1)  # Loop indefinitely
            return True
        except Exception as e:
            print(Fore.RED + f"⚠️ Error playing fallback sound: {e}")
            return False
    if not os.path.exists(SOUND_FILE):
        print(Fore.YELLOW + f"⚠️ Sound file '{SOUND_FILE}' not found. Skipping ambiance.")
        print(Fore.YELLOW + "💡 Download a soothing .wav sound (e.g., mystical chant, wind chimes) from Pixabay (https://pixabay.com/sound-effects/)")
        print(Fore.YELLOW + "  and save as 'audio/oracle_chant.wav'. Ensure it's PCM, 16-bit, 44100 Hz.")
        return False
    try:
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.set_volume(volume)  # Default volume 50%
        pygame.mixer.music.play(-1)  # Loop indefinitely
        return True
    except Exception as e:
        print(Fore.RED + f"⚠️ Error playing sound: {e}")
        print(Fore.RED + "💡 The WAV file might be incompatible. Convert it to PCM, 16-bit, 44100 Hz using CloudConvert (https://cloudconvert.com/wav-converter).")
        print(Fore.RED + "💡 Alternatively, download a new soothing .wav file (e.g., mystical chant) from Pixabay (https://pixabay.com/sound-effects/).")
        print(Fore.RED + "💡 Also check your audio device (speakers/headphones) in Windows Sound Settings.")
        return False

def adjust_volume(current_volume, fallback_sound=None):
    """Adjust sound volume."""
    print(Fore.WHITE + f"\n🎚️ Current volume: {int(current_volume * 100)}%")
    print(Fore.WHITE + "  (1) 25%  (2) 50%  (3) 75%  (4) 100%  (s) Skip")
    choice = input(Fore.WHITE + "Select volume (1-4, s to skip): ").lower()
    volume_map = {"1": 0.25, "2": 0.50, "3": 0.75, "4": 1.00}
    if choice in volume_map:
        new_volume = volume_map[choice]
        if PYGAME_AVAILABLE:
            if fallback_sound and pygame.mixer.get_busy():
                fallback_sound.set_volume(new_volume)
            elif pygame.mixer.music.get_busy():
                pygame.mixer.music.set_volume(new_volume)
        return new_volume
    return current_volume

def stop_sound(fallback_sound=None):
    """Stop ambient sound."""
    if PYGAME_AVAILABLE:
        if fallback_sound and pygame.mixer.get_busy():
            fallback_sound.stop()
        else:
            pygame.mixer.music.stop()

def record_question(max_retries=5):
    """Record spoken question with retry limit and fallback to text input."""
    recognizer = sr.Recognizer()
    retries = 0
    while retries < max_retries:
        with sr.Microphone() as source:
            print(Fore.CYAN + "🎙️ Ask your question, seeker...")
            print(Fore.CYAN + "🎤 Listening... (speak clearly, ensure your mic is on)")
            print(Fore.CYAN + "💡 Tip: If it fails to hear, check your mic settings, reduce noise, or ensure your mic is the default input device.")
            recognizer.adjust_for_ambient_noise(source, duration=3)  # Increased duration
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)  # Increased timeouts
            except sr.WaitTimeoutError:
                retries += 1
                print(Fore.RED + f"❌ Couldn’t hear you (attempt {retries}/{max_retries}). Try again!")
                continue
        
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            retries += 1
            print(Fore.RED + f"❌ Couldn’t hear you (attempt {retries}/{max_retries}). Try again!")
        except sr.RequestError as e:
            print(Fore.RED + f"❌ Speech recognition error: {e}. Check your internet connection.")
            return None
    
    # Fallback to text input after max retries
    print(Fore.YELLOW + f"⚠️ Speech recognition failed after {max_retries} attempts.")
    print(Fore.YELLOW + "💡 Let’s switch to typing your question instead.")
    return input(Fore.WHITE + "Type your question: ")

def main():
    deity = select_deity()
    print(Fore.MAGENTA + f"🧙‍♀️ You are now speaking to {deity['name']} – {deity['title']} {deity['emoji']}")
    
    # Ask if user wants to enable ambient sound
    print(Fore.WHITE + "\nWould you like to enable ambient sound? (y/n)")
    enable_sound = input(Fore.WHITE + "Choice (y/n): ").lower() == 'y'
    
    # Test sound playback if enabled
    sound_playing = False
    fallback_sound = None
    current_volume = 0.5  # Default volume
    if enable_sound:
        sound_playing, fallback_sound = test_sound_playback(current_volume)
        if sound_playing:
            current_volume = adjust_volume(current_volume, fallback_sound)
        # Start ambient sound if test passed
        if sound_playing:
            sound_playing = play_sound(current_volume, fallback_sound)
        else:
            print(Fore.YELLOW + "⚠️ Ambient sound disabled due to playback issues.")
            enable_sound = False
    
    while True:
        question = record_question()
        if not question:
            print(Fore.RED + "❌ No question received. Try again!")
            continue
        
        print(Fore.GREEN + f"\n🧠 Analyzing emotion...")
        mood, score = analyze_mood(question)
        wisdom = get_wisdom(mood, deity["name"])
        
        # Display results
        print(Fore.GREEN + f"📜 You asked: \"{question}\"")
        print(Fore.MAGENTA + f"😊 Mood Detected: {mood.capitalize()} (Confidence: {score:.2f})")
        print(Fore.YELLOW + "\n💬 Oracle Speaks:")
        print(Fore.YELLOW + f"\"{wisdom}\"")
        
        # Save to journal
        save_journal(question, mood, f"{deity['name']} ({deity['mythology']})", wisdom)
        print(Fore.GREEN + "\n📘 Entry saved to mythos_journal.json")
        
        # Continue or exit
        choice = input(Fore.WHITE + "\nWould you like to consult the Oracle again? (y/n): ").lower()
        if choice != 'y':
            print(Fore.CYAN + f"🌟 Farewell, seeker. May {deity['name']}'s wisdom guide you.")
            break
    
    if enable_sound:    
        stop_sound(fallback_sound)  # Stop sound on exit

if __name__ == "__main__":
    main()