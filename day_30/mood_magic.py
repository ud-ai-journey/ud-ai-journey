from transformers import pipeline
import random

# Initialize sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

# Affirmations for different moods
AFFIRMATIONS = {
    "positive": [
        "The universe is already listening – your voice carries power! 🌟",
        "Your dreams are blooming like stars in the night sky. ✨",
        "Keep shining, your positivity lights the way! ☀️"
    ],
    "negative": [
        "Even in shadows, your wishes hold strength. You’re enough. 🕯️",
        "Every step forward counts, even the small ones. Keep going! 🌱",
        "The stars see your courage, even when you doubt. 💪"
    ],
    "neutral": [
        "Your whispers are seeds planted in the cosmos. They’ll grow! 🌿",
        "The universe hears your calm heart. Trust the journey! 🌀",
        "Your voice is a gentle ripple, creating waves of change. 🌊"
    ]
}

def analyze_mood(text):
    """Analyze sentiment of the spoken wish."""
    if not text:
        return "neutral", 0.0
    result = sentiment_analyzer(text)[0]
    label = result['label'].lower()
    score = result['score']
    return label, score

def get_affirmation(mood):
    """Return a magical affirmation based on mood."""
    return random.choice(AFFIRMATIONS.get(mood, AFFIRMATIONS["neutral"]))