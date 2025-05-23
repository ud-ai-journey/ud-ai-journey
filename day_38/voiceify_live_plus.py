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
from googletrans import Translator
import pyperclip
import librosa
import soundfile as sf
import numpy as np
import tkinter as tk
from tkinter import scrolledtext

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

# Initialize sentiment classifier (using advanced emotion model), translator, and TTS
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
translator = Translator()
tts = pyttsx3.init()
tts.setProperty('rate', 150)  # Speed of speech

# File setups
TRANSCRIPT_FILE = "voiceify_live_transcript.txt"
TEMP_AUDIO_FILE = "temp_audio.wav"

# History buffers
sentiment_history = deque(maxlen=3)  # For smoothing sentiment
recent_sentiments = deque(maxlen=5)  # For live trend display
session_data = []  # For summary: (timestamp, text, sentiment, score, feedback, emotion)

# Feedback templates based on emotion
FEEDBACK_TEMPLATES = {
    "joy": [
        "You sound so joyful! Keep that positivity flowing!",
        "You’re radiating happiness—love it!",
        "That’s a cheerful vibe—nice one!"
    ],
    "anger": [
        "You sound a bit frustrated. Let’s take a deep breath, okay?",
        "I sense some tension. Want to talk it out?",
        "You seem upset—maybe a quick break could help?"
    ],
    "sadness": [
        "You sound a bit down. It’s okay to feel this way—want to take a moment?",
        "I sense some sadness. How about a mindfulness break?",
        "You seem a bit low. Let’s try to lift your spirits, okay?"
    ],
    "fear": [
        "You sound a bit anxious. Let’s pause and breathe together, okay?",
        "I sense some worry. Want to take a moment to relax?",
        "You seem a bit nervous—let’s try to calm those nerves."
    ],
    "love": [
        "You sound so loving! That warmth is amazing!",
        "You’re full of love today—beautiful to hear!",
        "That’s such a caring tone—keep spreading love!"
    ],
    "surprise": [
        "You sound surprised! What caught you off guard?",
        "I sense some excitement—something unexpected happen?",
        "You seem a bit shocked—what’s going on?"
    ]
}

# Simplified sentiment mapping for trends
EMOTION_TO_SENTIMENT = {
    "joy": "POSITIVE",
    "love": "POSITIVE",
    "surprise": "NEUTRAL",
    "sadness": "NEGATIVE",
    "anger": "NEGATIVE",
    "fear": "NEGATIVE"
}

# Emoji mapping for sentiment trends
SENTIMENT_EMOJIS = {
    "POSITIVE": "🙂",
    "NEUTRAL": "😐",
    "NEGATIVE": "🙁"
}

# ASCII emotion meter bar settings
METER_WIDTH = 20
METER_POSITIVE = "█" * METER_WIDTH
METER_NEUTRAL = "█" * (METER_WIDTH // 2)
METER_NEGATIVE = "█" * (METER_WIDTH // 4)

# Reflection templates based on sentiment
REFLECTION_TEMPLATES = {
    "POSITIVE": [
        "You seemed full of energy and positivity today! It sounds like you’re in a great place—keep that momentum going.",
        "You sounded really upbeat today. Maybe it’s been a good day? Keep spreading that positivity!"
    ],
    "NEGATIVE": [
        "You seemed a bit tense or down today. Maybe it was a long day? Remember to take breaks, breathe, and be kind to yourself.",
        "You sounded a bit low today. It’s okay to feel this way—give yourself some grace and take it one step at a time."
    ],
    "NEUTRAL": [
        "You sounded steady and introspective today. Perhaps you’re in a thoughtful or contemplative space. It’s okay to take things slow—progress happens in quiet moments too.",
        "You seemed balanced but maybe a bit tired today. It might be a good time to recharge and reflect."
    ]
}

# Expanded mindfulness tips based on sentiment
MINDFULNESS_TIPS = {
    "POSITIVE": [
        "Channel that energy—journal your wins!",
        "Share your positivity with someone today!",
        "Celebrate your joy with a small treat!"
    ],
    "NEUTRAL": [
        "A short walk might refresh your mind.",
        "Take a moment to set a small goal for the day.",
        "Try a quick stretch to re-energize."
    ],
    "NEGATIVE": [
        "Try deep breathing: Inhale 4s, hold 4s, exhale 4s.",
        "Write down one thing you’re grateful for to shift your focus.",
        "Listen to a calming song to soothe your mind.",
        "Take a moment to sip some water and reset.",
        "Close your eyes and visualize a peaceful place for a minute.",
        "Step outside for a quick breath of fresh air.",
        "Try a 1-minute stretch to release tension.",
        "Write down three things that made you smile recently."
    ]
}

# Mood quotes dictionary
MOOD_QUOTES = {
    "POSITIVE": [
        "Joy is not in things; it is in us.",
        "Happiness is the best makeup."
    ],
    "NEUTRAL": [
        "Stillness speaks more than noise.",
        "In the middle of difficulty lies opportunity."
    ],
    "NEGATIVE": [
        "Every day may not be good, but there’s good in every day.",
        "The darkest nights produce the brightest stars."
    ]
}

class VoiceifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voiceify Live Plus")
        self.root.geometry("600x500")

        # GUI elements
        self.label = tk.Label(root, text="Voiceify Live Plus: Real-time Emotion Feedback", font=("Arial", 14))
        self.label.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD, font=("Arial", 10))
        self.output_text.pack(pady=10)
        self.output_text.insert(tk.END, "Click 'Start Listening' to begin.\n")

        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening, font=("Arial", 12))
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED, font=("Arial", 12))
        self.stop_button.pack(pady=5)

        # Listening state
        self.stop_event = threading.Event()
        self.listening_thread = None

    def log_to_gui(self, message, color="black"):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()

    def start_listening(self):
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.log_to_gui("Adjusting for ambient noise... Please wait.")
        self.listening_thread = threading.Thread(target=continuous_listening, args=(self,))
        self.listening_thread.start()

    def stop_listening(self):
        self.stop_event.set()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_to_gui("Listening stopped.")

def setup_files():
    if not os.path.exists(TRANSCRIPT_FILE):
        with open(TRANSCRIPT_FILE, 'w', encoding='utf-8') as f:
            f.write("Voiceify Live Transcriptions\n\n")

def save_transcription(text):
    with open(TRANSCRIPT_FILE, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")
    # Copy to clipboard
    try:
        pyperclip.copy(text)
        return f"📋 Copied to clipboard: {text}"
    except Exception as e:
        return f"Clipboard error: {e}"

def translate_to_english(text):
    try:
        detected = translator.detect(text)
        if detected.lang != 'en':
            translated = translator.translate(text, dest='en')
            return translated.text, f"Translated from {detected.lang} to English: {translated.text}"
        return text, None
    except Exception as e:
        return text, f"Translation error: {e}"

def analyze_tone(audio):
    try:
        # Save audio to a temporary WAV file
        with open(TEMP_AUDIO_FILE, 'wb') as f:
            f.write(audio.get_wav_data())
        
        # Load audio with librosa
        y, sr = librosa.load(TEMP_AUDIO_FILE, sr=None)
        
        # Extract pitch (fundamental frequency) using librosa's piptrack
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Only consider non-zero pitches
                pitch_values.append(pitch)
        
        if not pitch_values:
            return 0.0, "No pitch detected."
        
        # Calculate average pitch
        avg_pitch = np.mean(pitch_values)
        
        # Normalize pitch to a 0-1 scale (assuming typical human speech range: 85 Hz to 255 Hz)
        normalized_pitch = (avg_pitch - 85) / (255 - 85)
        normalized_pitch = max(0, min(1, normalized_pitch))  # Clamp to 0-1
        
        return normalized_pitch, f"Tone Analysis - Average Pitch: {avg_pitch:.0f} Hz (Normalized: {normalized_pitch:.2f})"
    except Exception as e:
        return 0.0, f"Tone analysis error: {e}"
    finally:
        # Clean up temporary file
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)

def analyze_emotion(text, tone_factor):
    if not text.strip() or len(text.split()) <= 3:
        emotion, score = "surprise", 0.5
    else:
        sentences = nltk.sent_tokenize(text)
        emotions = [classifier(sentence)[0] for sentence in sentences]
        total_score = sum(e['score'] for e in emotions) / len(emotions)
        emotion_counts = Counter(e['label'] for e in emotions)
        most_common_emotion = emotion_counts.most_common(1)[0][0]
        emotion, score = most_common_emotion, total_score

    # Adjust score based on tone (high pitch can amplify positive or negative emotions)
    sentiment = EMOTION_TO_SENTIMENT.get(emotion, "NEUTRAL")
    if sentiment == "POSITIVE" and tone_factor > 0.7:
        score = min(1.0, score * 1.1)  # Boost positive emotion with high pitch
    elif sentiment == "NEGATIVE" and tone_factor > 0.7:
        score = min(1.0, score * 1.1)  # Boost negative emotion with high pitch
    elif tone_factor < 0.3:
        score = max(0.1, score * 0.9)  # Slightly reduce score for low pitch (calmer tone)

    # Smooth sentiment with history
    sentiment_history.append((sentiment, score))
    if len(sentiment_history) > 1:
        avg_score = sum(s[1] for s in sentiment_history) / len(sentiment_history)
        sentiments = [s[0] for s in sentiment_history]
        if sentiments.count("NEUTRAL") >= len(sentiments) // 2:
            return emotion, score, "NEUTRAL"
        elif sentiments.count("NEGATIVE") > sentiments.count("POSITIVE"):
            return emotion, score, "NEGATIVE"
        elif sentiments.count("POSITIVE") > sentiments.count("NEGATIVE"):
            return emotion, score, "POSITIVE"

    return emotion, score, sentiment

def get_feedback(emotion, score):
    feedback_list = FEEDBACK_TEMPLATES.get(emotion, FEEDBACK_TEMPLATES["surprise"])
    return random.choice(feedback_list)

def speak_feedback(feedback):
    try:
        tts.say(feedback)
        tts.runAndWait()
        return f"🎧 Feedback Spoken Aloud: “{feedback}”"
    except Exception as e:
        return f"TTS error: {e}"

def display_emotion_meter(sentiment, score):
    if sentiment == "POSITIVE":
        bar = METER_POSITIVE[:int(score * METER_WIDTH)]
    elif sentiment == "NEGATIVE":
        bar = METER_NEGATIVE[:int(score * METER_WIDTH // 4)]
    else:
        bar = METER_NEUTRAL[:int(score * METER_WIDTH // 2)]
    return f"Emotion Meter: [{bar:<{METER_WIDTH}}] ({score:.2f})"

def transcribe_audio(audio, retries=3):
    if audio is None:
        return "", "No audio captured."
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        try:
            text = recognizer.recognize_google(audio)
            return text, None
        except sr.UnknownValueError:
            return "", f"Couldn’t understand the audio (attempt {attempt+1}/{retries})."
        except sr.RequestError as e:
            return "", f"Transcription error: {e}"
    return "", "Failed to transcribe after retries."

def listen_once(recognizer, source, duration=7):
    try:
        print("🎙️ Listening for up to 7 seconds...")
        audio = recognizer.listen(source, timeout=7, phrase_time_limit=duration)
        print("🎙️ Processing...")
        return audio, None
    except sr.WaitTimeoutError:
        return None, "No speech detected within timeout."
    except Exception as e:
        return None, f"Error recording audio: {e}"

def generate_trend_summary():
    if not recent_sentiments:
        return "No sentiment data for trend summary."

    # Generate emoji trend
    trend_emojis = "".join(SENTIMENT_EMOJIS[sentiment] for sentiment in recent_sentiments)
    trend_summary = f"\n🧠 Sentiment Trend: {trend_emojis}\n"

    # Calculate percentages
    total = len(recent_sentiments)
    sentiment_counts = Counter(recent_sentiments)
    positive_pct = (sentiment_counts["POSITIVE"] / total) * 100
    neutral_pct = (sentiment_counts["NEUTRAL"] / total) * 100
    negative_pct = (sentiment_counts["NEGATIVE"] / total) * 100

    trend_summary += f"📊 Positive: {positive_pct:.0f}% | Neutral: {neutral_pct:.0f}% | Negative: {negative_pct:.0f}%\n"
    return trend_summary

def generate_reflection(sentiment, avg_score):
    reflection_list = REFLECTION_TEMPLATES.get(sentiment, REFLECTION_TEMPLATES["NEUTRAL"])
    return random.choice(reflection_list)

def get_mindfulness_tip(sentiment):
    tip_list = MINDFULNESS_TIPS.get(sentiment, MINDFULNESS_TIPS["NEUTRAL"])
    return random.choice(tip_list)

def get_mood_quote(sentiment):
    quote_list = MOOD_QUOTES.get(sentiment, MOOD_QUOTES["NEUTRAL"])
    return random.choice(quote_list)

def generate_journal_summary():
    if not session_data:
        return "No data for journal summary."

    total_utterances = len(session_data)
    sentiments = [item[5] for item in session_data]
    scores = [item[3] for item in session_data]
    feedbacks = [item[4] for item in session_data]

    avg_score = sum(scores) / len(scores) if scores else 0
    most_common_sentiment = Counter(sentiments).most_common(1)[0][0]
    top_feedbacks = Counter(feedbacks).most_common(3)

    summary = "\n📝 Daily Journal Summary:\n"
    summary += f"Total Utterances: {total_utterances}\n"
    summary += f"Average Sentiment: {avg_score:.2f}\n"
    summary += f"Most Common Mood: {most_common_sentiment}\n"
    summary += "\nTop 3 Feedbacks:\n"
    for feedback, count in top_feedbacks:
        summary += f"- {feedback} (x{count})\n"
    summary += "\n---\n"

    # Generate reflection, mindfulness tip, and mood quote
    reflection = generate_reflection(most_common_sentiment, avg_score)
    mindfulness_tip = get_mindfulness_tip(most_common_sentiment)
    mood_quote = get_mood_quote(most_common_sentiment)

    summary += f"\n💬 Reflection:\n> {reflection}\n"
    summary += f"\n🧘 Mindfulness Tip:\n> {mindfulness_tip}\n"
    summary += f"\n💡 Quote of the Day:\n> “{mood_quote}”\n"
    return summary

def continuous_listening(app):
    recognizer = sr.Recognizer()
    last_speech_time = time.time()
    silence_threshold = 10
    inactivity_timeout = 120  # 2 minutes

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 200
        app.log_to_gui("🎙️ Speak anytime to get emotional feedback...")

        while not app.stop_event.is_set():
            audio, error = listen_once(recognizer, source)
            if error:
                app.log_to_gui(error)
                print(error)

            if audio:
                # Analyze tone (pitch) before transcription
                tone_factor, tone_message = analyze_tone(audio)
                app.log_to_gui(tone_message)
                print(tone_message)

                text, transcribe_error = transcribe_audio(audio)
                if transcribe_error:
                    app.log_to_gui(transcribe_error)
                    print(transcribe_error)

                if text:
                    last_speech_time = time.time()
                    clipboard_message = save_transcription(text)
                    app.log_to_gui(f"Transcribed: {text}")
                    app.log_to_gui(f"Saved to {TRANSCRIPT_FILE}")
                    app.log_to_gui(clipboard_message)
                    print(f"\n{Fore.CYAN}Transcribed: {text}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Saved to {TRANSCRIPT_FILE}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{clipboard_message}{Style.RESET_ALL}")

                    # Translate text to English if needed
                    translated_text, translation_message = translate_to_english(text)
                    if translation_message:
                        app.log_to_gui(translation_message)
                        print(f"{Fore.YELLOW}{translation_message}{Style.RESET_ALL}")

                    # Analyze emotion and map to sentiment, adjusted by tone
                    emotion, score, sentiment = analyze_emotion(translated_text, tone_factor)
                    recent_sentiments.append(sentiment)

                    # Display emotion and feedback
                    feedback = get_feedback(emotion, score)
                    feedback_message = speak_feedback(feedback)
                    emotion_message = f"Emotion: {emotion.upper()} | Sentiment: {sentiment} ({score:.2f}) - {feedback}"
                    meter_message = display_emotion_meter(sentiment, score)
                    app.log_to_gui(emotion_message)
                    app.log_to_gui(meter_message)
                    app.log_to_gui(feedback_message)
                    print(f"{Fore.GREEN if sentiment == 'POSITIVE' else Fore.RED if sentiment == 'NEGATIVE' else Fore.YELLOW}{emotion_message}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN if sentiment == 'POSITIVE' else Fore.RED if sentiment == 'NEGATIVE' else Fore.YELLOW}{meter_message}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{feedback_message}{Style.RESET_ALL}")

                    # Save to session data (including emotion and sentiment)
                    session_data.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text, emotion, score, feedback, sentiment))
            else:
                current_time = time.time()
                if current_time - last_speech_time > silence_threshold:
                    app.log_to_gui(f"No speech detected for {silence_threshold} seconds. Still listening...")
                    print(f"{Fore.YELLOW}No speech detected for {silence_threshold} seconds. Still listening...{Style.RESET_ALL}")
                    last_speech_time = current_time
                if current_time - last_speech_time > inactivity_timeout:
                    app.log_to_gui("⏹️ No speech for 2 minutes. Stopping...")
                    print(f"{Fore.YELLOW}⏹️ No speech for 2 minutes. Stopping...{Style.RESET_ALL}")
                    app.stop_event.set()
                    break

            time.sleep(0.1)

    app.log_to_gui(f"Listening stopped. Transcriptions saved to {TRANSCRIPT_FILE}.")
    print(f"{Fore.GREEN}Listening stopped. Transcriptions saved to {TRANSCRIPT_FILE}.{Style.RESET_ALL}")
    trend_summary = generate_trend_summary()
    journal_summary = generate_journal_summary()
    app.log_to_gui(trend_summary)
    app.log_to_gui(journal_summary)
    print(trend_summary)
    print(journal_summary)

def main():
    print("🎙️ Voiceify Live Plus: Real-time Emotion Feedback (Wispr Flow-Inspired)")
    setup_files()
    root = tk.Tk()
    app = VoiceifyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
