import sys
import os
import logging
import threading
import queue
import time
from datetime import datetime
import speech_recognition as sr
from transformers import pipeline
from colorama import init, Fore, Style
import nltk
import tensorflow as tf
import random

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
tf.get_logger().setLevel('ERROR')

# Fix Unicode encoding for Windows PowerShell
sys.stdout.reconfigure(encoding='utf-8')

# Download NLTK data for sentence tokenization
nltk.download('punkt', quiet=True)

# Initialize colorama for colored terminal output
init()

# Initialize sentiment classifier
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# File setups
TRANSCRIPT_FILE = "voiceify_live_transcript.txt"

# Feedback templates based on sentiment (emoji-free for Windows compatibility)
FEEDBACK_TEMPLATES = {
    "POSITIVE": [
        "You sound happy! Keep it up!",
        "You’re radiating good vibes!",
        "That’s a cheerful tone—nice!"
    ],
    "NEGATIVE": [
        "Sounds like stress. Want to take a breath?",
        "Seems a bit tense. Everything okay?",
        "I sense some frustration. Need a break?"
    ],
    "NEUTRAL": [
        "You sound neutral. Maybe a bit tired?",
        "Feeling balanced—any big plans?",
        "You’re sounding calm. What’s up?"
    ]
}

def setup_files():
    if not os.path.exists(TRANSCRIPT_FILE):
        with open(TRANSCRIPT_FILE, 'w', encoding='utf-8') as f:
            f.write("Voiceify Live Transcriptions\n\n")

def save_transcription(text):
    with open(TRANSCRIPT_FILE, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")

def analyze_sentiment(text):
    if not text.strip() or len(text.split()) <= 3:
        return "NEUTRAL", 0.5
    sentences = nltk.sent_tokenize(text)
    sentiments = [classifier(sentence)[0] for sentence in sentences]
    total_score = sum(s['score'] for s in sentiments) / len(sentiments)
    if any(s['label'] == "NEGATIVE" for s in sentiments) and total_score > 0.6:
        return "NEGATIVE", total_score
    if all(s['label'] == "POSITIVE" for s in sentiments) and total_score > 0.8:
        return "POSITIVE", total_score
    return "NEUTRAL", total_score

def get_feedback(sentiment, score):
    feedback_list = FEEDBACK_TEMPLATES.get(sentiment, FEEDBACK_TEMPLATES["NEUTRAL"])
    return random.choice(feedback_list)

def transcribe_audio(audio, retries=3):
    if audio is None:
        return ""
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print(f"{Fore.YELLOW}Couldn’t understand the audio (attempt {attempt+1}/{retries}).{Style.RESET_ALL}")
        except sr.RequestError as e:
            print(f"{Fore.RED}Transcription error: {e}{Style.RESET_ALL}")
            return ""
    return ""

def listen_once(recognizer, source, duration=7):
    try:
        print("🎙️ Listening for up to 7 seconds...")
        audio = recognizer.listen(source, timeout=7, phrase_time_limit=duration)
        print("🎙️ Processing...")
        return audio
    except sr.WaitTimeoutError:
        return None
    except Exception as e:
        print(f"{Fore.RED}Error recording audio: {e}{Style.RESET_ALL}")
        return None

def continuous_listening():
    recognizer = sr.Recognizer()
    stop_event = threading.Event()
    input_queue = queue.Queue()
    last_speech_time = time.time()
    silence_threshold = 10

    def check_for_enter():
        input()
        stop_event.set()
        input_queue.put("stop")

    input_thread = threading.Thread(target=check_for_enter, daemon=True)
    input_thread.start()

    print("Adjusting for ambient noise... Please wait.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 200
        print("🎙️ Voiceify Live: Real-time Emotion Feedback (Wispr Flow-Inspired)")
        print("Speak anytime to get emotional feedback. Press Enter to stop...")

        while not stop_event.is_set():
            audio = listen_once(recognizer, source)
            if audio:
                text = transcribe_audio(audio)
                if text:
                    last_speech_time = time.time()
                    save_transcription(text)
                    print(f"\n{Fore.CYAN}Transcribed: {text}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Saved to {TRANSCRIPT_FILE}{Style.RESET_ALL}")
                    sentiment, score = analyze_sentiment(text)
                    feedback = get_feedback(sentiment, score)
                    color = Fore.GREEN if sentiment == "POSITIVE" else Fore.RED if sentiment == "NEGATIVE" else Fore.YELLOW
                    print(f"{color}Sentiment: {sentiment} ({score:.2f}) - {feedback}{Style.RESET_ALL}")
            else:
                if time.time() - last_speech_time > silence_threshold:
                    print(f"{Fore.YELLOW}No speech detected for {silence_threshold} seconds. Still listening...{Style.RESET_ALL}")
                    last_speech_time = time.time()
            time.sleep(0.1)

    print(f"{Fore.GREEN}Listening stopped. Transcriptions saved to {TRANSCRIPT_FILE}.{Style.RESET_ALL}")

def main():
    print("🎙️ Voiceify Live: Real-time Emotion Feedback (Wispr Flow-Inspired)")
    setup_files()
    try:
        continuous_listening()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Thanks for using Voiceify Live! Transcriptions saved to {TRANSCRIPT_FILE}.{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == "__main__":
    main()
