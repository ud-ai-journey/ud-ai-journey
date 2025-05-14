import speech_recognition as sr
from transformers import pipeline
from pydub import AudioSegment
import numpy as np

# Initialize sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def record_audio():
    """Record audio and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak your sentence...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def analyze_sentiment(text):
    """Analyze sentiment of the text."""
    if not text:
        return "neutral", 0.0
    result = sentiment_analyzer(text)[0]
    label = result['label'].lower()
    score = result['score']
    return label, score

def analyze_tempo(audio_file="temp.wav"):
    """Analyze speech tempo using pydub."""
    try:
        audio = AudioSegment.from_wav(audio_file)
        # Calculate average amplitude to detect pauses
        samples = np.array(audio.get_array_of_samples())
        avg_amplitude = np.mean(np.abs(samples))
        # Simple heuristic: high amplitude variation = fast tempo
        tempo = "fast" if np.std(samples) > avg_amplitude * 0.5 else "normal"
        return tempo
    except:
        return "normal"

def detect_filler_words(text):
    """Detect filler words like 'uh', 'um', 'I swear'."""
    fillers = ["uh", "um", "i swear", "like", "you know"]
    text = text.lower()
    filler_count = sum(text.count(f) for f in fillers)
    return filler_count > 0