### 📘 `README.md` — Day 34: EmpathyMesh 🧠💬

---

# EmpathyMesh – Day 34 of 100 Days of Python + AI

**Simulated Empathy-Aware Conversations with Sentiment Alignment**

---

## 🔍 Overview

**EmpathyMesh** is a Command Line Interface (CLI) tool that simulates an emotionally intelligent conversation between two users – **User A** and **User B**. It analyzes the sentiment behind each message, checks emotional alignment between users, and provides real-time visual and textual feedback to help build better emotional understanding.

> A step toward building emotionally-aware agents and systems – inspired by the *Empathy Engine* vision.

---

## 🎯 Features

* 🔠 **Two-user alternating conversation interface**
* 💬 **Sentiment analysis** using Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`)
* ✅ **Emotional alignment check** between two turns
* 📊 **ASCII mood bar** to visualize harmony
* 💡 **Empathy feedback** to encourage deeper listening and understanding
* 📝 **CSV logging** of timestamp, speaker, sentiment, alignment, and scores

---

## 🧠 Concepts Practiced

* Transformers & NLP with Hugging Face `pipeline`
* Real-time sentiment analysis
* ASCII-based CLI visualizations
* File handling and structured CSV logging
* Emotional design and user feedback loop

---

## 🚀 How to Run

1. **Install dependencies** (make sure you're in a virtual environment or project folder):

   ```bash
   pip install transformers colorama
   ```

2. **Run the script**:

   ```bash
   python empathymesh.py
   ```

3. **Start the conversation**:

   * The script prompts `User A` and `User B` alternately to enter text.
   * Press `Ctrl + C` to exit and save the conversation log.

---

## 📁 Sample Log Output

```csv
Timestamp,Speaker,Text,Sentiment,Score,Match
2025-05-19 12:00:00,User A,I feel so excited about this project!,POSITIVE,0.98,N/A
2025-05-19 12:00:20,User B,Same here! It's inspiring to build this.,POSITIVE,0.91,Match
```

---

## 📈 Mood Bar Visualization

```
Alignment: Match | [████████████░░░░░░░░░░░] 0.65
Feedback: You’re aligned, but could connect more deeply.
```

---

## 🧩 Potential Improvements

* Voice input/output integration
* GUI version using Tkinter or web-based React UI
* Emotion trend graphs from the log file
* Add sarcasm/empathy detection module

---

## 🙌 Why It Matters

EmpathyMesh goes beyond code – it's a digital tool that promotes **emotional awareness** and **alignment**, making machines a little more **human**.

Perfect for exploring:

* Human-AI interaction
* Digital mental health tools
* Building blocks for your larger **Empathy Engine** project

---

## 📆 Progress

🗓️ **Day 34 / 100** of my #100DaysOfPythonAI
🔗 Follow my journey and daily builds!

---
