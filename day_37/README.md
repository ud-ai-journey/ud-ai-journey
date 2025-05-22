# Voiceify Live Plus 🎙️  
*A Real-Time Voice Sentiment Feedback System*

---

## 🔍 Description  
**Voiceify Live Plus** is a Command Line Interface (CLI) tool that listens to your voice, transcribes it in real-time, and provides instant emotional feedback using sentiment analysis. Inspired by Wispr Flow’s seamless dictation experience, it detects your emotional tone (happy, stressed, neutral), speaks personalized feedback, tracks sentiment trends, and stores your transcriptions for daily journaling.  

This project was built as part of my **#100DaysOfPythonAI** journey and is a step toward creating the **Empathy Engine**—an AI that understands and responds to human emotions in real-time.

Perfect for emotional awareness, mental well-being, and workplace communication!

---

## 🎯 Features  

- 🎙️ **Continuous Voice Dictation** – Seamlessly listens to your voice (Wispr Flow-inspired).  
- 💬 **Real-Time Speech-to-Text** – Uses Google Speech Recognition to transcribe speech.  
- 🧠 **Sentiment Analysis** – Detects emotional tone using Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`).  
- 🗣️ **Spoken Emotional Feedback** – Uses `pyttsx3` for real-time vocal response.  
- 📊 **Sentiment Trends** – Tracks and displays last 5 emotions using emojis.  
- 📈 **Mini Trend Summary** – Shows percentage breakdown (e.g., Positive: 60% | Neutral: 20% | Negative: 20%).  
- ⏹️ **Auto-Stop** – Halts after 2 minutes of silence.  
- 📝 **Daily Journal Summary** – Summarizes all utterances and emotional stats.  
- 💾 **Transcription Saving** – Stores logs in `voiceify_live_transcript.txt`.  
- 🌈 **Colored CLI Output** – Beautiful, vibrant terminal visuals using `colorama`.

---

## 🚀 How to Run

### ✅ Prerequisites
- Python 3.12+
- A working microphone
- Internet connection (for speech recognition)

### 🛠️ Setup

```bash
git clone https://github.com/your-username/voiceify-live-plus.git
cd voiceify-live-plus
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tool:

```bash
python voiceify_live_plus.py
```

💡 *Windows users: To avoid TensorFlow oneDNN warnings, use:*

```powershell
$env:TF_ENABLE_ONEDNN_OPTS=0; python voiceify_live_plus.py
```

---

## 🧑‍💻 Usage

* Speak naturally to get real-time emotional feedback (spoken + text).
* Press `Enter` to manually stop, or wait 2 minutes for auto-stop.
* View the **sentiment trend** with emojis and percentage summary.
* Check your **journal summary** at the end.
* Transcriptions are stored in `voiceify_live_transcript.txt`.
* Use `Ctrl+C` to exit at any point.

---

## 📁 Sample Interaction

```plaintext
🎙️ Voiceify Live Plus: Real-time Emotion Feedback (Wispr Flow-Inspired)
Adjusting for ambient noise... Please wait.
Speak anytime to get emotional feedback. Press Enter to stop...

🎙️ Listening for up to 7 seconds...
🎙️ Processing...
Transcribed: how are you
Sentiment: NEUTRAL (0.50) - You sound neutral. Maybe a bit tired?
🎧 Feedback Spoken Aloud: “You sound neutral. Maybe a bit tired?”

🎙️ Listening for up to 7 seconds...
🎙️ Processing...
Transcribed: I am doing good how you
Sentiment: NEUTRAL (0.83) - Feeling balanced—any big plans?
🎧 Feedback Spoken Aloud: “Feeling balanced—any big plans?”

[Press Enter]

🧠 Sentiment Trend: 😐😐  
📊 Positive: 0% | Neutral: 100% | Negative: 0%

📝 Daily Journal Summary:
- Total Utterances: 2  
- Average Sentiment Score: 0.67  
- Most Common Mood: NEUTRAL  
- Top Feedbacks:
  - "You sound neutral. Maybe a bit tired?" (x1)
  - "Feeling balanced—any big plans?" (x1)

🗂️ Transcription Saved To: `voiceify_live_transcript.txt`
```

---

## 📸 Demo

🎥 *Coming soon:* A 15-second screen recording of Voiceify Live Plus in action!

---

## 🧩 Potential Improvements

* 🌐 **Multilingual Support** – Add translation using `googletrans`.
* 📊 **Emotion Meter** – Visual ASCII emotion bar.
* 😄 **Advanced Emotions** – Use `bhadresh-savani/distilbert-base-uncased-emotion`.
* 📋 **Clipboard Integration** – Auto-copy text with `pyperclip`.
* 🧬 **Tone Analysis** – Use `librosa` for vocal pitch/emotion tracking.
* 💻 **GUI Interface** – Build in Tkinter or Streamlit.
* 🧘 **Mental Health Prompts** – Add mindfulness tips for negative moods.

---

## 🙌 Why It Matters

Voiceify Live Plus is more than a tool—it's a **real-time empathetic AI companion**. Whether you're a creator, professional, or someone seeking emotional self-awareness, this project supports **mental wellness**, **emotional intelligence**, and **AI voice innovation**.

This is a core part of my long-term vision for the **Empathy Engine**.

---

## 📢 Share the Project

* Try it out and send your feedback!
* Star ⭐ the repo if you find it useful.
* Follow my journey: [GitHub Profile](https://github.com/ud-ai-journey/ud-ai-journey)

