import sys
import time
from datetime import datetime
import keyboard
from transformers import pipeline
from colorama import init, Fore, Style
import csv
import os

# Initialize colorama for colored terminal output
init()

# Load sentiment analysis model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Emoji mapping for sentiments
SENTIMENT_EMOJIS = {
    "POSITIVE": "💪",
    "NEGATIVE": "😞",
    "NEUTRAL": "😐"
}

# Color mapping for sentiments
SENTIMENT_COLORS = {
    "POSITIVE": Fore.GREEN,
    "NEGATIVE": Fore.RED,
    "NEUTRAL": Fore.YELLOW
}

# Character mapping for special keys
KEY_MAP = {
    'space': ' ',
    'dot': '.',
    'comma': ',',
    'exclamation': '!',
    'question': '?',
    'semicolon': ';',
    'colon': ':',
    'quote': "'",
    'double quote': '"',
    'slash': '/',
    'backslash': '\\',
    'dash': '-',
    'underscore': '_',
    'plus': '+',
    'equals': '=',
    'left paren': '(',
    'right paren': ')',
    'left brace': '{',
    'right brace': '}',
    'left bracket': '[',
    'right bracket': ']',
    'at': '@',
    'hash': '#',
    'dollar': '$',
    'percent': '%',
    'caret': '^',
    'ampersand': '&',
    'asterisk': '*',
    'less': '<',
    'greater': '>',
    'pipe': '|',
    'tilde': '~',
    'grave': '`'
}

# Log file setup
LOG_FILE = "emotion_log.csv"

def setup_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Text", "Sentiment", "Score"])

def log_emotion(text, sentiment, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, text, sentiment, f"{score:.2f}"])

def analyze_sentiment(text):
    if not text.strip():
        return "NEUTRAL", 0.5
    result = classifier(text)[0]
    label = result['label']
    score = result['score']
    return label, score

def print_sentiment(text, sentiment, score):
    emoji = SENTIMENT_EMOJIS.get(sentiment, "😐")
    color = SENTIMENT_COLORS.get(sentiment, Fore.WHITE)
    print(f"{color}> {text}{Style.RESET_ALL}")
    print(f"{color}{emoji} [{sentiment.capitalize()} – {score:.2f}]{Style.RESET_ALL}\n")

def get_char_from_key(key_name):
    # Return mapped character if in KEY_MAP, else use key_name if it's a single character
    return KEY_MAP.get(key_name.lower(), key_name if len(key_name) == 1 else '')

def main():
    print("EmotionLens: Start\nType and press Enter to analyze sentiment. Press Ctrl+C to exit.\n")
    setup_log_file()
    
    current_line = []
    
    try:
        while True:
            char = keyboard.read_event(suppress=True)
            
            if char.name == 'enter' and char.event_type == keyboard.KEY_DOWN:
                text = ''.join(current_line).strip()
                if text:
                    sentiment, score = analyze_sentiment(text)
                    print_sentiment(text, sentiment, score)
                    log_emotion(text, sentiment, score)
                current_line = []
            elif char.name == 'backspace' and char.event_type == keyboard.KEY_DOWN:
                if current_line:
                    current_line.pop()
            elif char.event_type == keyboard.KEY_DOWN and char.name not in ('ctrl', 'alt', 'shift'):
                mapped_char = get_char_from_key(char.name)
                if mapped_char:  # Only append if we have a valid character
                    current_line.append(mapped_char)
                
    except KeyboardInterrupt:
        print("\n\nEmotionLens stopped. Logs saved to emotion_log.csv")
        sys.exit(0)

if __name__ == "__main__":
    main()