from transformers import pipeline
import random

# Initialize sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

# Deities and their wisdom quotes for different moods
DEITIES = [
    {"name": "Athena", "title": "The Goddess of Wisdom", "mythology": "Greek", "emoji": "🦉"},
    {"name": "Odin", "title": "The Allfather", "mythology": "Norse", "emoji": "🐺"},
    {"name": "Kali", "title": "The Goddess of Transformation", "mythology": "Indian", "emoji": "🔥"},
    {"name": "Ra", "title": "The Sun God", "mythology": "Egyptian", "emoji": "☀️"}
]

WISDOM_QUOTES = {
    "positive": {
        "Athena": "Your joy is a beacon; let it guide others to wisdom.",
        "Odin": "The winds of victory carry your laughter—ride them boldly!",
        "Kali": "Your light burns bright; let it dance through the cosmos.",
        "Ra": "The sun within you shines eternal—bask in its warmth."
    },
    "negative": {
        "Athena": "In moments of chaos, the mind seeks the clarity of silence. Trust the stillness.",
        "Odin": "Even the mightiest storms pass—endure, for wisdom lies in scars.",
        "Kali": "Destruction precedes creation. Embrace the void, for it births renewal.",
        "Ra": "Even in darkness, the sun rises again. Hold fast, dawn approaches."
    },
    "neutral": {
        "Athena": "Balance is the root of wisdom—seek it in your thoughts.",
        "Odin": "The raven watches, silent. Observe, and the path will reveal itself.",
        "Kali": "Stillness is power—let the universe move while you stand firm.",
        "Ra": "The sun neither hurries nor lingers—find peace in its steady rhythm."
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

def select_deity():
    """Randomly select a deity for the session."""
    return random.choice(DEITIES)

def get_wisdom(mood, deity_name):
    """Get wisdom quote based on mood and deity."""
    mood_quotes = WISDOM_QUOTES.get(mood, WISDOM_QUOTES["neutral"])
    return mood_quotes.get(deity_name, "The universe speaks through silence—listen.")