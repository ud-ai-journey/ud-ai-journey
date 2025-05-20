import sys
import csv
import os
import logging
from datetime import datetime
from transformers import pipeline
from colorama import init, Fore, Style
from nltk.tokenize import sent_tokenize
import nltk
import re

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Download NLTK data for sentence tokenization
nltk.download('punkt_tab', quiet=True)

# Initialize colorama for colored terminal output
init()

# Load sentiment analysis model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Log file and draft file setup
LOG_FILE = "empathy_draft_log.csv"
DRAFT_FILE = "empathy_draft.txt"

# Rewrite templates for negative or robotic sentences
REWRITE_TEMPLATES = {
    "NEGATIVE": [
        ("disappoint", "concern", "Let’s address our concerns together to improve outcomes."),
        ("not happy", "concerned", "I’m concerned about this—can we collaborate on a solution?"),
        ("angry", "upset", "I’m feeling upset—can we work together to resolve this?"),
        ("frustrated", "challenged", "I’m feeling challenged by this—let’s find a way forward as a team."),
        ("mad", "frustrated", "I’m frustrated—can we discuss how to move forward constructively?"),
        ("serious", "concerned", "I’m concerned about our progress—can we review updates together?"),
        ("where is", "awaiting", "I’m eager for immediate updates—can we discuss our team’s progress urgently?"),
        ("man", "urgent", "I’m eager for updates—can we discuss our team’s progress soon?"),
        ("failure", "challenge", "We can tackle this challenge as a team to achieve better results."),
        ("bad", "room for improvement", "There’s room for improvement—let’s explore solutions together."),
        (None, None, "Could we discuss this further to find a constructive path forward?")  # Default
    ],
    "POSITIVE_LOW": [
        (None, None, "Let’s add some warmth: consider emphasizing collaboration or appreciation.")
    ]
}

# Formality settings
FORMALITY_TONES = {
    "casual": {
        "greeting": "Hey team,",
        "rewrite_prefix": "Let’s sort this out: "
    },
    "professional": {
        "greeting": "Dear team,",
        "rewrite_prefix": "I propose we address this: "
    },
    "empathetic": {
        "greeting": "Hello team,",
        "rewrite_prefix": "I’d like us to work together on this: "
    }
}

def setup_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Original Sentence", "Sentiment", "Score", "Suggested Rewrite", "Accepted"])

def log_draft(original, sentiment, score, suggestion, accepted):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, original, sentiment, f"{score:.2f}", suggestion, accepted])

def save_draft(final_draft):
    with open(DRAFT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_draft)

def analyze_sentiment(sentence):
    if not sentence.strip():
        return "NEUTRAL", 0.5
    # Force greetings to NEUTRAL
    if re.match(r'^(Dear|Hello|Hey)\s+team[,.\s]*$', sentence, re.IGNORECASE):
        return "NEUTRAL", 0.5
    result = classifier(sentence)[0]
    label = result['label']
    score = result['score']
    if label == "POSITIVE" and score < 0.7:
        return "POSITIVE_LOW", score
    return label, score

def polish_sentence(sentence):
    # Fix grammar and style
    sentence = re.sub(r'\bon the team\'s\b', r'the team’s', sentence, flags=re.IGNORECASE)  # Fix "on the team's"
    sentence = re.sub(r'\.\s*([a-z])', lambda m: '. ' + m.group(1).upper(), sentence)  # Capitalize after period
    sentence = sentence.lower().capitalize()  # Normalize capitalization
    sentence = re.sub(r'\s+', ' ', sentence).strip()  # Normalize spaces
    sentence = re.sub(r'\.\s*\.', '.', sentence)  # Fix multiple periods
    return sentence

def suggest_rewrite(sentence, sentiment, score, formality):
    if sentiment == "NEGATIVE":
        has_team = "team" in sentence.lower()
        for trigger, replacement, template in REWRITE_TEMPLATES["NEGATIVE"]:
            if trigger and trigger in sentence.lower():
                suggestion = f"{FORMALITY_TONES[formality]['rewrite_prefix']}{template}"
                if has_team:
                    suggestion = suggestion.replace("this", "our team’s progress")
                return suggestion
        default_suggestion = f"{FORMALITY_TONES[formality]['rewrite_prefix']}{REWRITE_TEMPLATES['NEGATIVE'][-1][2]}"
        if has_team:
            default_suggestion = default_suggestion.replace("this", "our team’s progress")
        return default_suggestion
    elif sentiment == "POSITIVE_LOW":
        return f"{FORMALITY_TONES[formality]['rewrite_prefix']}{REWRITE_TEMPLATES['POSITIVE_LOW'][0][2]}"
    return sentence

def print_analysis(sentence, sentiment, score, suggestion):
    color = Fore.RED if sentiment == "NEGATIVE" else Fore.YELLOW if sentiment == "POSITIVE_LOW" else Fore.GREEN
    print(f"{color}Original: {sentence}{Style.RESET_ALL}")
    print(f"{color}Sentiment: {sentiment} ({score:.2f}){Style.RESET_ALL}")
    if sentiment in ("NEGATIVE", "POSITIVE_LOW"):
        print(f"{Fore.MAGENTA}Suggestion: {suggestion}{Style.RESET_ALL}")

def main():
    print("EmpathyMail: Start")
    print("Select tone: 1. Casual, 2. Professional, 3. Empathetic")
    tone_choice = input("Enter 1, 2, or 3: ").strip()
    formality = { "1": "casual", "2": "professional", "3": "empathetic" }.get(tone_choice, "empathetic")
    print(f"\nSelected tone: {formality.capitalize()}")
    print(f"Enter your email draft (type ---END--- to finish):\n{FORMALITY_TONES[formality]['greeting']}")

    setup_log_file()

    draft_lines = []
    draft_lines.append(FORMALITY_TONES[formality]['greeting'])
    try:
        while True:
            line = input()
            if line.strip() == "---END---":
                break
            draft_lines.append(line)
    except KeyboardInterrupt:
        print("\nDraft input interrupted. Processing what was entered...")
    
    if len(draft_lines) <= 1:
        print("No draft content entered. Exiting.")
        sys.exit(0)

    # Preprocess to improve sentence splitting
    draft_text = "\n".join(draft_lines)
    draft_text = re.sub(r'^(Dear|Hello|Hey)\s+team[,;]?\s*', r'\1 team.\n', draft_text, flags=re.IGNORECASE)
    draft_text = re.sub(r',([^.\n])', r'.\n\1', draft_text)  # Split on commas not followed by periods
    sentences = sent_tokenize(draft_text)
    final_draft_sentences = []
    
    print("\n🧠 Analyzing Draft...\n")
    
    for sentence in sentences:
        sentiment, score = analyze_sentiment(sentence)
        suggestion = suggest_rewrite(sentence, sentiment, score, formality)
        print_analysis(sentence, sentiment, score, suggestion)
        
        if sentiment in ("NEGATIVE", "POSITIVE_LOW"):
            while True:
                print("Choose an option:")
                print("1. Accept suggestion")
                print("2. Modify suggestion")
                print("3. Keep original")
                choice = input("Enter 1, 2, or 3: ").strip()
                
                if choice == "1":
                    final_draft_sentences.append(suggestion)
                    log_draft(sentence, sentiment, score, suggestion, "Accepted")
                    break
                elif choice == "2":
                    modified = input("Enter your modified sentence: ").strip()
                    mod_sentiment, mod_score = analyze_sentiment(modified)
                    if mod_sentiment == "NEGATIVE" and mod_score > 0.7:
                        print(f"{Fore.RED}Warning: Modified sentence is still NEGATIVE ({mod_score:.2f}). Please try a more constructive tone.{Style.RESET_ALL}")
                        continue
                    polished = polish_sentence(modified)
                    final_draft_sentences.append(polished)
                    log_draft(sentence, sentiment, score, suggestion, f"Modified (Sentiment: {mod_sentiment}, Score: {mod_score:.2f})")
                    print(f"{Fore.GREEN}Modified Sentiment: {mod_sentiment} ({mod_score:.2f}){Style.RESET_ALL}")
                    if polished != modified:
                        print(f"{Fore.YELLOW}Polished Version: {polished}{Style.RESET_ALL}")
                    break
                elif choice == "3":
                    if sentiment == "NEGATIVE" and score > 0.7:
                        print(f"{Fore.RED}Warning: Keeping this NEGATIVE sentence ({score:.2f}) may sound confrontational. Consider modifying it.{Style.RESET_ALL}")
                        continue
                    final_draft_sentences.append(sentence)
                    log_draft(sentence, sentiment, score, suggestion, "Kept Original")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
        else:
            final_draft_sentences.append(sentence)
            log_draft(sentence, sentiment, score, suggestion, "N/A")
    
    final_draft = ". ".join(s.strip(".") for s in final_draft_sentences if s.strip()) + "."
    save_draft(final_draft)
    
    print(f"\n{Fore.GREEN}✅ Final Draft:{Style.RESET_ALL}")
    print(final_draft)
    print(f"\nSaved to {DRAFT_FILE}. Draft history logged in {LOG_FILE}.")

if __name__ == "__main__":
    main()