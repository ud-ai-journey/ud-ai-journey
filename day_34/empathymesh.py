import sys
from datetime import datetime
import csv
import os
from transformers import pipeline
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

# Load sentiment analysis model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Log file setup
LOG_FILE = "empathy_log.csv"

def setup_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Speaker", "Text", "Sentiment", "Score", "Match"])

def log_conversation(speaker, text, sentiment, score, match):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, speaker, text, sentiment, f"{score:.2f}", match])

def analyze_sentiment(text):
    if not text.strip():
        return "NEUTRAL", 0.5
    result = classifier(text)[0]
    label = result['label']
    score = result['score']
    return label, score

def calculate_alignment(sentiment_a, score_a, sentiment_b, score_b):
    if sentiment_a == sentiment_b:
        alignment_score = (score_a + score_b) / 2
        return "Match", alignment_score
    else:
        alignment_score = abs(score_a - score_b) / 2
        return "Mismatch", alignment_score

def get_feedback(match, alignment_score):
    if match == "Match":
        if alignment_score > 0.7:
            return "Great harmony in this chat!"
        else:
            return "You're aligned, but could connect more deeply."
    else:
        if alignment_score > 0.4:
            return "You seem out of sync—try to listen calmly."
        else:
            return "Emotions are diverging—consider reflecting on their perspective."

def draw_ascii_mood_bar(alignment_score, match):
    bar_length = 20
    filled = int(bar_length * alignment_score)
    empty = bar_length - filled
    color = Fore.GREEN if match == "Match" else Fore.RED
    bar = color + "█" * filled + "░" * empty + Style.RESET_ALL
    return f"[{bar}] {alignment_score:.2f}"

def main():
    print("EmpathyMesh: Start\nSimulated conversation between User A and User B.")
    print("Type for each user when prompted. Press Ctrl+C to exit.\n")
    setup_log_file()

    current_speaker = "A"
    last_sentiment, last_score = None, None
    last_text = None

    try:
        while True:
            speaker_label = f"User {current_speaker}"
            text = input(f"{Fore.CYAN}{speaker_label}> {Style.RESET_ALL}")
            if not text.strip():
                print("Please enter some text.")
                continue

            # Analyze sentiment
            sentiment, score = analyze_sentiment(text)
            print(f"{Fore.YELLOW}Sentiment: {sentiment} ({score:.2f}){Style.RESET_ALL}")

            # Log the input
            match = "N/A"
            alignment_score = 0
            if last_sentiment and current_speaker == "B":
                match, alignment_score = calculate_alignment(last_sentiment, last_score, sentiment, score)
                feedback = get_feedback(match, alignment_score)
                mood_bar = draw_ascii_mood_bar(alignment_score, match)
                print(f"{Fore.MAGENTA}Alignment: {match} | {mood_bar}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Feedback: {feedback}{Style.RESET_ALL}\n")

            log_conversation(speaker_label, text, sentiment, score, match)

            # Store for next iteration
            if current_speaker == "A":
                last_sentiment, last_score, last_text = sentiment, score, text
            else:
                last_sentiment, last_score, last_text = None, None, None

            # Switch speaker
            current_speaker = "B" if current_speaker == "A" else "A"

    except KeyboardInterrupt:
        print("\n\nEmpathyMesh stopped. Logs saved to empathy_log.csv")
        sys.exit(0)

if __name__ == "__main__":
    main()