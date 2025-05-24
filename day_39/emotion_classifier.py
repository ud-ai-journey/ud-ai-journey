# Day 39: Emotion Classifier using HuggingFace
from transformers import pipeline
import sys
import re

# Fix Unicode encoding for Windows PowerShell
sys.stdout.reconfigure(encoding='utf-8')

# Initialize the emotion classifier pipeline with the new model
print("Loading emotion classifier model...")
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

# Small pre-labeled dataset for testing
dataset = [
    {"text": "I feel so tired and alone.", "label": "sad"},
    {"text": "I am so excited for the weekend!", "label": "happy"},
    {"text": "This is so frustrating, I can’t believe it!", "label": "angry"},
    {"text": "I love spending time with my friends.", "label": "happy"},
    {"text": "I’m really upset about what happened.", "label": "sad"},
    {"text": "I can’t stand this nonsense anymore!", "label": "angry"},
    {"text": "What a wonderful day it is today!", "label": "happy"},
    {"text": "I feel so down after that news.", "label": "sad"}
]

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation (keep basic spaces and words)
    text = re.sub(r'[^\w\s]', '', text)
    # Optional: Remove extra words (e.g., "man" in "i am happy man")
    words = text.split()
    if len(words) > 5:  # Arbitrary threshold for "extra" words
        text = " ".join(words[:5])
    return text

def is_valid_input(text):
    # Check for empty or whitespace-only input
    if not text.strip():
        return False, "Input cannot be empty. Please enter a sentence."
    # Check for minimum length (at least 2 words)
    words = text.split()
    if len(words) < 2:
        return False, "Input is too short. Please enter a sentence with at least 2 words."
    # Improved gibberish check: ensure at least one word has a vowel and looks "English-like"
    valid_words = 0
    for word in words:
        if re.search(r'[aeiou]', word.lower()) and len(word) > 2:  # Word must have a vowel and be longer than 2 chars
            valid_words += 1
    if valid_words < 1:
        return False, "Input appears to be gibberish. Please enter a meaningful sentence."
    return True, None

def classify_emotion(text):
    try:
        # Preprocess the text
        processed_text = preprocess_text(text)
        result = classifier(processed_text)[0]
        emotion = result['label']
        score = result['score']
        return emotion, score
    except Exception as e:
        return "Error", f"Classification error: {e}"

def evaluate_on_dataset():
    print("\n📊 Evaluating classifier on dataset...")
    correct = 0
    total = len(dataset)
    
    for item in dataset:
        text = item['text']
        true_label = item['label']
        predicted_label, score = classify_emotion(text)
        
        # Map model labels to dataset labels (model uses 'sadness' for 'sad', 'joy' for 'happy', etc.)
        predicted_label_mapped = predicted_label
        if predicted_label == "sadness":
            predicted_label_mapped = "sad"
        elif predicted_label == "joy" or predicted_label == "love":
            predicted_label_mapped = "happy"
        elif predicted_label == "anger":
            predicted_label_mapped = "angry"
        elif predicted_label == "fear":
            predicted_label_mapped = "sad"  # Fear often aligns with sadness in this context
        elif predicted_label == "surprise":
            predicted_label_mapped = "happy"  # Surprise often aligns with happiness in positive contexts
        
        is_correct = predicted_label_mapped == true_label
        if is_correct:
            correct += 1
        print(f"Text: {text}")
        print(f"True Label: {true_label}, Predicted: {predicted_label_mapped} (Score: {score:.2f}) {'✅' if is_correct else '❌'}")
    
    accuracy = (correct / total) * 100
    print(f"\nAccuracy: {accuracy:.2f}% ({correct}/{total})")

def main():
    print("🎭 Day 39: Emotion Classifier")
    print("Enter a sentence to classify its emotion (or type 'exit' to quit).")
    
    # Evaluate the classifier on the dataset first
    evaluate_on_dataset()
    
    # Interactive loop for user input
    while True:
        try:
            user_input = input("\nEnter a sentence (or 'exit'): ")
            if user_input.lower() == 'exit':
                print("Exiting Emotion Classifier. Goodbye!")
                break
            
            # Validate the input
            is_valid, error_message = is_valid_input(user_input)
            if not is_valid:
                print(error_message)
                continue
            
            emotion, score = classify_emotion(user_input)
            if emotion == "Error":
                print(f"Error: {score}")
            else:
                print(f"Emotion: {emotion.upper()} (Confidence: {score:.2f})")
        except Exception as e:
            print(f"Error in input loop: {e}. Please try again.")

if __name__ == "__main__":
    main()