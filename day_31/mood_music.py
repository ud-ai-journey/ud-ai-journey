from transformers import pipeline
import os

# Initialize sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

# Music tracks and tips for each mood
MOOD_CONFIG = {
    "positive": {
        "track": "audio/positive.mp3",
        "title": "Bright Horizon",
        "tip": "Keep shining, your joy is contagious!"
    },
    "neutral": {
        "track": "audio/neutral.mp3",
        "title": "Gentle Flow",
        "tip": "Embrace the calm, new ideas are brewing."
    },
    "negative": {
        "track": "audio/negative.mp3",
        "title": "Calm Restore",
        "tip": "It’s okay to rest. Your energy will bloom again."
    }
}

def analyze_mood(text):
    """Analyze sentiment of spoken text."""
    if not text:
        return "neutral", 0.0
    result = sentiment_analyzer(text)[0]
    label = result['label'].lower()
    score = result['score']
    return label, score

def get_music_for_mood(mood):
    """Return music track and metadata for the mood."""
    return MOOD_CONFIG.get(mood, MOOD_CONFIG["neutral"])