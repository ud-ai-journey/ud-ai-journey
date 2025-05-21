# 🎙️ Voiceify Live – Real-Time Emotion Feedback CLI (Day 36/100 of #100DaysOfPythonAI)

Voiceify Live is a real-time voice emotion feedback CLI tool, inspired by **Wispr Flow**'s seamless speech experience, crafted to bring **empathetic AI** one step closer to reality.

Imagine speaking your thoughts aloud, and an AI softly reflects back how you’re feeling—*happy, neutral, stressed*—and gently responds with affirmations. That’s the magic of Voiceify Live.

> A heartfelt leap toward the **Empathy Engine**, helping us listen, feel, and understand in real-time.

---

## 🔍 What is Voiceify Live?

**Voiceify Live** is a command-line interface that:
- 🎙️ Listens to your voice continuously.
- 💬 Transcribes your speech in real time.
- 🧠 Analyzes your emotional tone using NLP.
- ❤️ Provides instant emotional feedback.

Think of it as a mindful companion—**a mirror for your emotions through voice**.

---

## 🎯 Features

✅ **Continuous Voice Dictation**  
Seamless listening experience like Wispr Flow—speak naturally without pressing buttons.

✅ **Real-time Speech-to-Text**  
Uses Google’s Speech Recognition API to transcribe your words in real time.

✅ **Sentiment Analysis with Hugging Face Transformers**  
Powered by `distilbert-base-uncased-finetuned-sst-2-english` to detect emotional tone.

✅ **Instant Emotional Feedback**  
Gives responses like “You sound happy!” or “Seems like stress. Want to take a breath?”

✅ **Transcription Save File**  
All your sessions are saved in `voiceify_live_transcript.txt` for future reference.

✅ **Colorful CLI UX**  
Sentiments and scores displayed in color-coded messages with live feedback.

---

## 🧠 Concepts Practiced

- 🎧 Real-time audio capture with `speech_recognition` and `pyaudio`
- ⚙️ Custom loop for continuous listening
- 🤖 NLP with Hugging Face's `pipeline()`
- 🧩 Sentence tokenization using `nltk.sent_tokenize()`
- 🌈 Emotional feedback design for mental health
- 🎨 Beautiful CLI output with `colorama`
- 📝 File handling for clean transcript history

---

## 🚀 How to Run

**Install dependencies:**

```bash
pip install speechrecognition pyaudio transformers colorama nltk
````

**Run the tool (Windows example):**

```bash
$env:TF_ENABLE_ONEDNN_OPTS=0; python voiceify_live.py
```

💡 Tip: You can set `TF_ENABLE_ONEDNN_OPTS=0` globally in Windows Environment Variables to avoid the warning.

---

## 🗣️ Using Voiceify Live

* Speak freely—Voiceify listens for \~7 seconds in each cycle.
* After each cycle, it:

  * Transcribes your voice
  * Analyzes emotional tone
  * Gives feedback
  * Saves to `voiceify_live_transcript.txt`
* Press `Enter` anytime to stop listening.
* Press `Ctrl+C` to exit the tool.

---

## 📁 Sample Output

```plaintext
🎙️ Voiceify Live: Real-time Emotion Feedback (Wispr Flow-Inspired)
Adjusting for ambient noise... Please wait.
Speak anytime to get emotional feedback. Press Enter to stop...

🎙️ Listening for up to 7 seconds...
🎙️ Processing...
Transcribed: yeah I am just thinking of joining a meeting short
Saved to voiceify_live_transcript.txt
Sentiment: NEGATIVE (0.98) - Sounds like stress. Want to take a breath?

🎙️ Listening for up to 7 seconds...
🎙️ Processing...
Transcribed: join a meeting in short and I'm excited about
Saved to voiceify_live_transcript.txt
Sentiment: POSITIVE (1.00) - You’re radiating good vibes!

🎙️ Listening for up to 7 seconds...
🎙️ Processing...
Transcribed: excited about the meeting that I am going to
Saved to voiceify_live_transcript.txt
Sentiment: POSITIVE (1.00) - That’s a cheerful tone—nice!

[Press Enter]

Listening stopped. Transcriptions saved to voiceify_live_transcript.txt.
```

---

## 📝 Output File Sample – `voiceify_live_transcript.txt`

```
Voiceify Live Transcriptions

[2025-05-21 14:00:00] yeah I am just thinking of joining a meeting short
[2025-05-21 14:00:07] join a meeting in short and I'm excited about
[2025-05-21 14:00:14] excited about the meeting that I am going to
```

---

## 📉 Known Limitations

* 🎯 **Sentiment accuracy** for short, ambiguous phrases can misfire. Future versions will include sentiment smoothing.
* 🎧 **Speech clarity** issues may occur with noisy environments. Currently tuned for energy threshold = 200 and 3 retries.

---

## 💡 Why This Matters

Voiceify Live blends the power of **voice AI** with **emotional intelligence**—creating tech that listens not just to *what* you say, but *how* you feel.

It's perfect for:

* 🧘‍♀️ Real-time emotional check-ins
* 🧠 Mental health tracking
* 💼 Workplace tone monitoring
* 🔬 Prototyping the Empathy Engine’s core loop

---

## 📆 #100DaysOfPythonAI Journey

* 🗓️ **Day 36 / 100** ✅
* 🧱 Built: Seamless voice input + real-time emotional feedback.
* 🔜 Coming Up (Day 37+):

  * 🔈 Spoken feedback with TTS
  * 📈 Sentiment trends visualization
  * ⏱️ Auto-stop logic
  * 📊 Summary charts for emotion history

---

## 🧠 Inspired by

* 🔄 **Wispr Flow** (for continuous voice UX)
* ❤️ **Empathy Engine** (for emotionally aware AI tools)
* 🤗 **Hugging Face** (for powerful, accessible NLP)

---

## 🔗 Let’s Connect

I’m building everyday.
Join me in this #100DaysOfPythonAI adventure as I create tools with purpose, emotion, and empathy. 🌱

---

> *“Technology that understands you is powerful. Technology that cares is magical.”*
> — Inspired by the **Empathy Engine** Vision 🌟
