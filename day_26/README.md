# 🧠 AI Mood Journal – Day 26

Welcome to Day 26 of the 100-Day Python + AI Challenge!  
Today's project is an **AI-Powered Mood Journal** – a voice-enabled diary that not only transcribes your thoughts but also detects your mood using sentiment analysis. Perfect for self-reflection, emotional tracking, or just talking it out.

---

## 📌 Features

✅ Speak your journal entries – no typing needed  
✅ Transcribes your thoughts using voice recognition  
✅ Analyzes emotional tone with a pre-trained AI sentiment model  
✅ Logs entries with timestamp and mood emoji  
✅ Simple CLI interface with graceful error handling  

---

## 📁 Folder Structure

day\_26\_mood\_journal/
├── mood\_journal.py           # Main script
└── mood\_journal.txt          # Auto-generated journal log

````

---

## 🚀 How to Run

### 1. 📦 Install Dependencies

> Make sure Python 3.7+ is installed.

```bash
pip install SpeechRecognition transformers torch
pip install pipwin && pipwin install pyaudio  # (Windows only)
````

### 2. 🎤 Run the App

```bash
python mood_journal.py
```

> Speak your thoughts when prompted. Your entry and detected mood will be saved to `mood_journal.txt`.

---

## ✨ Sample Output

```
Welcome to your AI Mood Journal!
Listening... Please speak your thoughts.
Processing your input...
You said: I had a great day at work today!
Detected mood: Happy 😊
Entry saved at 2025-05-11 22:19:45

Would you like to add another entry? (y/n): n
Goodbye! Keep your mood journal updated.
```

---

## 🧠 Behind the Scenes

* **SpeechRecognition** is used to convert voice to text
* **Hugging Face Transformers** pipeline detects sentiment
* Entries are auto-timestamped and saved locally

---

🫶 Crafted by **Uday Kumar** with care and curiosity 💙

