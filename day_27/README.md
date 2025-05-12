# 🌈 MindMate – AI Affirmation Generator | Day 27

Welcome to Day 27 of the 100-Day Python + AI Challenge!  
Today’s project is **MindMate** – a voice-powered AI tool that listens to your thoughts, detects your emotional state, and offers uplifting affirmations to brighten your mood.

---

## ✨ Features

✅ Voice input using your microphone  
✅ Sentiment analysis using Hugging Face transformers  
✅ Personalized affirmations based on detected mood  
✅ Emoji-based responses to match your feelings  
✅ Encouraging messages for self-care and growth  
✅ Clean CLI interface and mood-boosting experience  

---

## 🧠 How It Works

1. You speak your thoughts out loud.
2. The app transcribes your words using Google Speech Recognition.
3. It detects your emotional tone (Positive / Negative / Neutral).
4. Based on the tone, it shows a relevant affirmation and emoji to lift you up.

---

## 🔧 Tech Stack

- Python 3  
- `speech_recognition` – for capturing voice input  
- `transformers` – for mood analysis  
- `colorama` – for colored terminal output (optional bonus)  

---

## 📂 Folder Structure

```

day\_27\_mindmate\_affirmation\_generator/
├── mindmate.py           # Main CLI app
├── affirmations.py       # Mood-wise affirmation database
├── mood\_utils.py         # Sentiment analysis logic
├── README.md             # You are here!

````

---

## 🚀 How to Run

1. Open terminal and navigate to project folder.

2. Install the required packages:

```bash
pip install speechrecognition transformers colorama
````

3. Run the app:

```bash
python mindmate.py
```

---

## 🗣️ Example Output

```
🎙️ Speak your thoughts: "I feel like I'm not doing enough."

🧠 Analyzing mood...
😢 Mood Detected: Negative

🌟 Affirmation: "You are doing your best, and that is always enough." 💖

Would you like another affirmation? (y/n):
```

---

## ❤️ Why This Matters

Daily affirmations and mood check-ins can improve self-awareness, emotional regulation, and confidence. **MindMate** helps you cultivate that habit with a little help from AI.

---

Happy affirming! 🌻
Keep building your best self, one line of code at a time 💪


