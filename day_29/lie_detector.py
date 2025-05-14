import os
import speech_recognition as sr
from colorama import init, Fore
from lie_utils import analyze_sentiment, analyze_tempo, detect_filler_words
from truth_or_lie import guess_truth_or_lie
import threading
import time

# Initialize colorama for colored output
init()

def save_audio(audio, filename="temp.wav"):
    """Save audio to a WAV file."""
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())

def record_with_start_stop():
    """Record audio with manual start/stop control."""
    recognizer = sr.Recognizer()
    audio = None
    recording = False
    
    audio_data = None

    def record_audio():
        nonlocal audio_data, recording
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(Fore.YELLOW + "🔊 Recording started...")
            audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            recording = False
            print(Fore.YELLOW + "🛑 Recording stopped.")

    print(Fore.CYAN + "🎙️ Press Enter to start recording...")
    input()  # Wait for Enter to start
    recording = True
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()

    print(Fore.CYAN + "🎙️ Press Enter to stop recording...")
    input()  # Wait for Enter to stop
    recording = False
    record_thread.join()  # Wait for recording to finish

    if audio_data:
        try:
            text = recognizer.recognize_google(audio_data)
            return text, audio_data
        except sr.UnknownValueError:
            return None, None
        except sr.RequestError:
            return None, None
    return None, None

def main():
    print(Fore.CYAN + "🎉 Welcome to Lie Detector Lite! 🎉")
    print(Fore.YELLOW + "⚠️ This is just for fun, not a real lie detector!")
    
    while True:
        # Record and process audio with start/stop
        text, audio = record_with_start_stop()
        if not text or not audio:
            print(Fore.RED + "❌ Couldn’t understand you. Try again!")
            continue
        
        print(Fore.GREEN + f"\n🧠 Analyzing tone for: '{text}'...")
        
        # Save audio for tempo analysis
        save_audio(audio, "temp.wav")
        
        # Analyze components
        sentiment, sentiment_score = analyze_sentiment(text)
        tempo = analyze_tempo()
        has_fillers = detect_filler_words(text)
        
        # Display analysis
        print(Fore.MAGENTA + f"🧪 Emotion Detected: {sentiment.capitalize()} (Score: {sentiment_score:.2f})")
        print(Fore.MAGENTA + f"🌀 Speech Tempo: {tempo.capitalize()}")
        if has_fillers:
            print(Fore.MAGENTA + "🛑 Filler Words Detected (e.g., 'uh', 'um')")
        
        # Guess truth or lie
        verdict, feedback = guess_truth_or_lie(sentiment, sentiment_score, tempo, has_fillers)
        print(Fore.CYAN + f"\n🤔 Verdict: {verdict}")
        print(Fore.YELLOW + feedback)
        
        # Ask to continue
        choice = input(Fore.WHITE + "\nWant to try again? (y/n): ").lower()
        if choice != 'y':
            print(Fore.CYAN + "👋 Thanks for playing!")
            break
        
        # Clean up temp file
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")

if __name__ == "__main__":
    main()