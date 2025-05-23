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
import pyttsx3
from collections import deque, Counter

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

# Initialize sentiment classifier and TTS
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
tts = pyttsx3.init()
tts.setProperty('rate', 150)  # Speed of speech

# File setups
TRANSCRIPT_FILE = "voiceify_live_transcript.txt"

# History buffers
sentiment_history = deque(maxlen=3)  # For smoothing sentiment
recent_sentiments = deque(maxlen=5)  # For live trend display
session_data = []  # For summary: (timestamp, text, sentiment, score, feedback)

# Feedback templates based on sentiment
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

# Emoji mapping for sentiment trends
SENTIMENT_EMOJIS = {
    "POSITIVE": "🙂",
    "NEUTRAL": "😐",
    "NEGATIVE": "🙁"
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
        sentiment, score = "NEUTRAL", 0.5
    else:
        sentences = nltk.sent_tokenize(text)
        sentiments = [classifier(sentence)[0] for sentence in sentences]
        total_score = sum(s['score'] for s in sentiments) / len(sentiments)
        if any(s['label'] == "NEGATIVE" for s in sentiments) and total_score > 0.6:
            sentiment = "NEGATIVE"
            score = total_score
        elif all(s['label'] == "POSITIVE" for s in sentiments) and total_score > 0.8:
            sentiment = "POSITIVE"
            score = total_score
        else:
            sentiment = "NEUTRAL"
            score = total_score

    # Smooth sentiment with history
    sentiment_history.append((sentiment, score))
    if len(sentiment_history) > 1:
        avg_score = sum(s[1] for s in sentiment_history) / len(sentiment_history)
        sentiments = [s[0] for s in sentiment_history]
        if sentiments.count("NEUTRAL") >= len(sentiments) // 2:
            return "NEUTRAL", avg_score
        elif sentiments.count("NEGATIVE") > sentiments.count("POSITIVE"):
            return "NEGATIVE", avg_score
        elif sentiments.count("POSITIVE") > sentiments.count("NEGATIVE"):
            return "POSITIVE", avg_score

    return sentiment, score

def get_feedback(sentiment, score):
    feedback_list = FEEDBACK_TEMPLATES.get(sentiment, FEEDBACK_TEMPLATES["NEUTRAL"])
    return random.choice(feedback_list)

def speak_feedback(feedback):
    try:
        tts.say(feedback)
        tts.runAndWait()
        print(f"{Fore.CYAN}🎧 Feedback Spoken Aloud: “{feedback}”{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}TTS error: {e}{Style.RESET_ALL}")

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

def generate_trend_summary():
    if not recent_sentiments:
        print(f"{Fore.YELLOW}No sentiment data for trend summary.{Style.RESET_ALL}")
        return

    # Generate emoji trend
    trend_emojis = "".join(SENTIMENT_EMOJIS[sentiment] for sentiment in recent_sentiments)
    print(f"\n{Fore.MAGENTA}🧠 Sentiment Trend: {trend_emojis}{Style.RESET_ALL}")

    # Calculate percentages
    total = len(recent_sentiments)
    sentiment_counts = Counter(recent_sentiments)
    positive_pct = (sentiment_counts["POSITIVE"] / total) * 100
    neutral_pct = (sentiment_counts["NEUTRAL"] / total) * 100
    negative_pct = (sentiment_counts["NEGATIVE"] / total) * 100

    print(f"{Fore.MAGENTA}📊 Positive: {positive_pct:.0f}% | Neutral: {neutral_pct:.0f}% | Negative: {negative_pct:.0f}%{Style.RESET_ALL}")

def generate_journal_summary():
    if not session_data:
        print(f"{Fore.YELLOW}No data for journal summary.{Style.RESET_ALL}")
        return

    total_utterances = len(session_data)
    sentiments = [item[2] for item in session_data]
    scores = [item[3] for item in session_data]
    feedbacks = [item[4] for item in session_data]

    avg_score = sum(scores) / len(scores) if scores else 0
    most_common_mood = Counter(sentiments).most_common(1)[0][0]
    top_feedbacks = Counter(feedbacks).most_common(3)

    print(f"\n{Fore.CYAN}📝 Daily Journal Summary:{Style.RESET_ALL}")
    print(f"Total Utterances: {total_utterances}")
    print(f"Overall Sentiment Average: {avg_score:.2f}")
    print(f"Most Common Mood: {most_common_mood}")
    print("Top 3 Feedback Responses:")
    for feedback, count in top_feedbacks:
        print(f"- {feedback} (x{count})")
    print()

def continuous_listening():
    recognizer = sr.Recognizer()
    stop_event = threading.Event()
    input_queue = queue.Queue()
    last_speech_time = time.time()
    silence_threshold = 10
    inactivity_timeout = 120  # 2 minutes

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
        print("🎙️ Voiceify Live Plus: Real-time Emotion Feedback (Wispr Flow-Inspired)")
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
                    recent_sentiments.append(sentiment)
                    feedback = get_feedback(sentiment, score)
                    color = Fore.GREEN if sentiment == "POSITIVE" else Fore.RED if sentiment == "NEGATIVE" else Fore.YELLOW
                    print(f"{color}Sentiment: {sentiment} ({score:.2f}) - {feedback}{Style.RESET_ALL}")
                    speak_feedback(feedback)
                    session_data.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text, sentiment, score, feedback))
            else:
                current_time = time.time()
                if current_time - last_speech_time > silence_threshold:
                    print(f"{Fore.YELLOW}No speech detected for {silence_threshold} seconds. Still listening...{Style.RESET_ALL}")
                    last_speech_time = current_time
                if current_time - last_speech_time > inactivity_timeout:
                    print(f"{Fore.YELLOW}⏹️ No speech for 2 minutes. Stopping...{Style.RESET_ALL}")
                    stop_event.set()
                    break

            time.sleep(0.1)

    print(f"{Fore.GREEN}Listening stopped. Transcriptions saved to {TRANSCRIPT_FILE}.{Style.RESET_ALL}")
    generate_trend_summary()
    generate_journal_summary()

def main():
    print("🎙️ Voiceify Live Plus: Real-time Emotion Feedback (Wispr Flow-Inspired)")
    setup_files()
    try:
        continuous_listening()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Thanks for using Voiceify Live Plus! Transcriptions saved to {TRANSCRIPT_FILE}.{Style.RESET_ALL}")
        generate_trend_summary()
        generate_journal_summary()
        sys.exit(0)

if __name__ == "__main__":
    main()