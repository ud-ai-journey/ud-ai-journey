import speech_recognition as sr
from transformers import pipeline
from datetime import datetime

# Initialize recognizer and sentiment analysis pipeline
recognizer = sr.Recognizer()
sentiment_pipeline = pipeline("sentiment-analysis")

def listen_and_transcribe():
    with sr.Microphone() as source:
        print("Listening... Please speak your thoughts.")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing your input...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return None

def detect_mood(text):
    if not text:
        return "Unknown"
    result = sentiment_pipeline(text)[0]
    label = result['label']
    score = result['score']
    # Map sentiment to mood emojis
    if label == 'POSITIVE':
        emoji = '😊'
        mood = 'Happy'
    elif label == 'NEGATIVE':
        emoji = '😢'
        mood = 'Sad'
    else:
        emoji = '😐'
        mood = 'Neutral'
    return f"{mood} {emoji}"

def save_entry(text, mood):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] Mood: {mood}\nThoughts: {text}\n\n"
    with open("mood_journal.txt", "a", encoding="utf-8") as file:
        file.write(entry)
    print(f"Entry saved at {timestamp}\n")

def main():
    print("Welcome to your AI Mood Journal!")
    while True:
        text = listen_and_transcribe()
        if text:
            mood = detect_mood(text)
            print(f"Detected mood: {mood}")
            save_entry(text, mood)
        else:
            print("No input detected. Please try again.")
        cont = input("Would you like to add another entry? (y/n): ").strip().lower()
        if cont != 'y':
            print("Goodbye! Keep your mood journal updated.")
            break

if __name__ == "__main__":
    main()