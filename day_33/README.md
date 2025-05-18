# 🎯 EmotionLens – Real-time Sentiment Feedback for Live Journaling

A lightweight, real-time CLI tool that detects emotions as you type and gives instant feedback using AI sentiment analysis, emojis, and color-coded cues. Each entry is logged with timestamps for emotional journaling.

---

## 🚀 Features

- ⌨️ **Type-based Live Journaling** – Analyze what you type in real time  
- 🧠 **AI-Powered Sentiment Analysis** – Using DistilBERT (via Hugging Face Transformers)  
- 😄 **Emoji Feedback** – Visual emotional feedback with sentiment-based emojis  
- 🌈 **Color-coded Terminal** – Positive (Green), Negative (Red), Neutral (Yellow)  
- 📘 **CSV Logging** – Timestamped logs of your emotional states  
- 🔐 **Private & Offline** – No data is sent anywhere

---

## 🧪 Example

```

EmotionLens: Start
Type and press Enter to analyze sentiment. Press Ctrl+C to exit.

> I feel confident and ready today!
> 💪 \[Positive – 0.98]

> Everything feels pointless...
> 😞 \[Negative – 0.91]

````

Each entry is saved in `emotion_log.csv` for future analysis.

---

## 🧠 Tech Stack

| Module            | Purpose                              |
|-------------------|--------------------------------------|
| `keyboard`        | Read typed keys in real time         |
| `transformers`    | DistilBERT model for sentiment       |
| `colorama`        | Styled, colored CLI output           |
| `csv`, `datetime` | Logging with timestamps              |

---

## ⚙️ Setup

### 📦 Installation

Make sure you have Python 3.8+ installed.

```bash
pip install transformers keyboard colorama
````

---

## ▶️ How to Run

```bash
python emotionlens.py
```

* Start typing your thoughts
* Press `Enter` to analyze each line
* Press `Ctrl + C` to exit safely

---

## 📁 Output

All entries are logged to:

```
emotion_log.csv
```

With fields:

* Timestamp
* Text
* Sentiment
* Confidence Score

---

## 🔒 Disclaimer

This tool is for **personal insight and journaling**. It’s not intended for clinical diagnosis or emotional therapy. Please seek professional help when needed.

---

## 🙌 Credits

* 🤗 Hugging Face Transformers – for DistilBERT
* 👨‍💻 You – for making it magical on Day 33!

---
