# 🪄 WhisprWand – Voice-Powered Wish Journal

**A magical CLI journal that records your spoken wishes, analyzes their emotional tone, and responds with enchanting affirmations. Not just a journal — a spark of belief!**

---

## 🔧 Features

- 🎙️ **Voice-activated wish recording**  
- 🧠 **Sentiment analysis using DistilBERT**  
- 💌 **Magical affirmations tailored to your mood**  
- 📝 **Securely logs each wish into a JSON journal**  
- 🎨 **Colorful CLI output with Colorama**  
- 🔔 **Optional chime sound using pygame (add your own chime.wav)**  

---

## 🚀 Setup

### ✅ Prerequisites
- Python 3.8+
- Microphone
- Internet connection

### 📦 Installation

```bash
pip install speechrecognition transformers colorama pygame
```

> 🔔 Optional: Add a `chime.wav` file to the root directory if you want magical sound effects when wishes are logged!

---

## ▶️ How to Use

```bash
python whisprwand.py
```

1. Speak your wish aloud (e.g., _“I want to inspire millions!”_)  
2. Your wish is transcribed and emotionally analyzed  
3. You'll receive a magical affirmation based on your mood  
4. The wish and analysis are saved to `whispers.json`  
5. Choose to whisper another dream or exit

---

## 📎 Example Output

```
🪄 Welcome to WhisprWand! ✨
🎙️ Speak your wish...
🧠 Analyzing emotion...
😊 Mood: Positive (0.92)
🌈 Whisper Logged!
✨ Magic Note: "Your dreams are blooming like stars!"
📘 Saved to Journal!
Would you like to speak another dream? (y/n):
```

---

## 🧠 Tech Behind the Magic

- `speech_recognition` – Voice-to-text conversion  
- `transformers` – DistilBERT for emotional tone detection  
- `colorama` – Styled CLI feedback  
- `pygame` – Optional chime sound after logging a wish  

---

## ⚠️ Disclaimer

This project is for **learning and creative inspiration only**.  
Your dreams are magical—but this isn’t therapy. 💖

---

## 🙌 Credits & Thanks

- 🤗 Hugging Face (for sentiment models)  
- 🎤 SpeechRecognition library  
- 🌈 Colorama for CLI aesthetics  
- 🔔 pygame for audio magic  

---

✨ *Keep whispering your dreams. The universe is listening.*  
🧙‍♀️ Built with belief on **Day 30** of the **100-Day Python + AI Challenge**
```

