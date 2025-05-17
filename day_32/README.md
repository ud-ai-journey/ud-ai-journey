# 🧙‍♂️ MythosMind | Day 32

Welcome to **Day 32** of the 100-Day Python + AI Challenge!  
Today's project is A mystical voice-powered CLI oracle that listens to your spoken questions, detects your emotional state, and responds with divine wisdom from ancient mythologies. Whether you seek clarity, comfort, or insight — the Oracle hears you.

---

## 🔧 Features

- 🎙️ **Voice-activated Q&A** — Speak your heart, be heard
- 🧠 **Emotion analysis** using DistilBERT
- 🕊️ **Ancient wisdom** from Athena, Odin, Ra, Kali
- 🎨 **Cinematic terminal UI** using `colorama`
- 🔔 Optional **ambient chanting** with `pygame`
- 📝 **Journaled entries** in `mythos_journal.json`

---

## 🚀 Setup

**Prerequisites**  
- Python 3.8+  
- Microphone  
- Internet connection  

**Install dependencies:**

```bash
pip install speechrecognition transformers colorama pygame
````

**Optional:**

* Add an `oracle_chant.wav` file inside an `audio/` folder for ambiance.

---

## ▶️ Usage

```bash
python mythosmind.py
```

You’ll meet a randomly chosen deity from a mythological pantheon.
Ask your question aloud. The system analyzes your emotional tone and returns a unique piece of wisdom.

---

## 📎 Example

```
🧙‍♀️ You are now speaking to Athena – The Goddess of Wisdom 🦉
🎙️ Ask your question, seeker...
📜 You asked: "Why do I feel so lost?"
🧠 Analyzing emotion...
😞 Mood Detected: Negative (0.89)
💬 Oracle Speaks:
"In moments of chaos, the mind seeks the clarity of silence. Trust the stillness."
📘 Entry saved to mythos_journal.json

Would you like to consult the Oracle again? (y/n):
```

---

## 🛠️ Tech Stack

* `speech_recognition` → Convert spoken words into text
* `transformers` (DistilBERT) → Emotion detection
* `colorama` → Colorful, immersive terminal UI
* `pygame` → Optional sound playback

---

## ⚠️ Disclaimer

This project is meant for fun, reflection, and creative learning.
The Oracle offers comfort — not clinical advice. Seek real help if needed ❤️

---

## 🙌 Thanks To

* [Hugging Face](https://huggingface.co)
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [Colorama](https://pypi.org/project/colorama/)
* [Pygame](https://www.pygame.org/)

---

🧘‍♂️ Ask. Feel. Reflect.
Let the ancient voices guide you through the modern maze.

```