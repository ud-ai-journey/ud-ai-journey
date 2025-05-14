# 🎙️ Lie Detector Lite

A fun CLI tool that analyzes speech for tone, tempo, and fillers to guess if you're truthful or not.  
*Not a real lie detector! Just a playful AI project.*

---

## 🔧 Features

- 🎤 Start/stop voice recording with Enter key  
- 🧠 Sentiment analysis (using `distilbert`)  
- 🌀 Tempo detection (`pydub`)  
- 🛑 Filler word spotting (e.g., “uh,” “um”)  
- 🤔 Verdict: **Truthful** ✅ or **Suspicious** 🧢  
- 🎨 Colorful CLI with `colorama`  

---

## 🚀 Setup

### Prerequisites
- Python 3.8+  
- Microphone  
- Internet connection  
- `ffmpeg`  

### Installing Dependencies
```bash
pip install speechrecognition transformers colorama pydub
```
---

## ▶️ Usage

```bash
python lie_detector.py
```

### How to Use
- Press **Enter** to start/stop recording  
- Speak your sentence (e.g., “I didn’t eat the cookie!”)  
- The tool provides tone analysis and a verdict  
- Choose to retry or exit  

---

## 📎 Example

```
🎙️ Press Enter to start...
🔊 Recording...
🛑 Stopped.
🧠 Analyzing: 'I swear I didn’t, uh, do it'
🧪 Tone: Negative (0.65)
🌀 Tempo: Fast
🛑 Fillers: Yes
🤔 Verdict: Suspicious 🧢
Want to try again? (y/n):
```

---

## 🧠 Tech

- **Speech recognition:** `speech_recognition` (Voice-to-text)  
- **Sentiment analysis:** `transformers` (DistilBERT)  
- **Tempo detection:** `pydub`  
- **CLI styling:** `colorama`  

---

## ⚠️ Disclaimer

*For fun and learning only — this is not a real lie detector!*

---

## 🙌 Thanks

- Hugging Face  
- speech_recognition  
- pydub  
- colorama
