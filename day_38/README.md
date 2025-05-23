
# 🎙️ Voiceify Live Plus - Day 38

**Voiceify Live Plus** is a real-time emotion-aware speech transcription and feedback application built with Python. It listens to user speech, transcribes it, detects emotional tone using advanced NLP models, and provides live sentiment feedback, mindfulness tips, and mood reflections—all through a beautiful GUI.

---

## 🚀 Features

- ✅ **Live Speech Recognition** (via `speech_recognition`)
- ✅ **Emotion Detection** (via HuggingFace `distilbert-base-uncased-emotion`)
- ✅ **Real-Time Sentiment Trend Analysis**
- ✅ **GUI Interface** (via `Tkinter`)
- ✅ **Live Feedback & Quotes** based on emotional tone
- ✅ **Multilingual Translation to English** (via `googletrans`)
- ✅ **Tone Analysis** via pitch detection (`librosa`)
- ✅ **Text-to-Speech Feedback** (`pyttsx3`)
- ✅ **Auto Clipboard Copy of Transcripts**
- ✅ **Session Summary & Mindfulness Tips**
- ✅ **Local Transcript Log with Timestamps**

---

## 🧠 Tech Stack

| Component            | Library/Tool                           |
|---------------------|----------------------------------------|
| Speech Recognition   | `speech_recognition`                   |
| NLP / Emotion Model  | `transformers` (HuggingFace pipeline) |
| Translation          | `googletrans`                          |
| TTS Feedback         | `pyttsx3`                              |
| GUI Framework        | `tkinter`                              |
| Pitch Analysis       | `librosa`                              |
| Text Handling        | `nltk`, `colorama`, `pyperclip`        |
| Backend Processing   | `threading`, `queue`, `deque`          |

---

## 🔧 Setup Instructions

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
````

If `requirements.txt` is missing, install manually:

```bash
pip install speechrecognition transformers googletrans==4.0.0-rc1 pyttsx3 nltk librosa soundfile numpy colorama pyperclip
```

2. **Download NLTK Data**

   Automatically handled in code: `nltk.download('punkt', quiet=True)`

3. **Run the App**

   ```bash
   python voiceify_live_plus.py
   ```

4. **Use the GUI**

   * Click **"Start Listening"** to begin live speech feedback.
   * Click **"Stop Listening"** to end the session.
   * View live feedback, quotes, emotion analysis, and transcription.

---

## 📁 File Structure

```
voiceify_live_plus.py       # Main application script
voiceify_live_transcript.txt # Auto-generated transcript log
README.md                    # You're here!
```

---

## 🌈 Emotional Feedback Themes

* 😄 Joy / Love → Positive reinforcement & quotes
* 😟 Sadness / Anger / Fear → Empathy, mindfulness tips
* 😐 Surprise → Neutral check-in

---

## 📌 TODO (Future Improvements)

* [ ] Add daily session summary save/export
* [ ] Enable cloud-based emotion analytics dashboard
* [ ] Mobile or web-based deployment (Flask or Kivy)
* [ ] Add user voice emotion visualization (graphs)
* [ ] Implement dark mode UI switch
* [ ] Add journaling capability for voice notes

---

## 🧘 Quotes of the Day

> *“Stillness speaks more than noise.”*
> *“The darkest nights produce the brightest stars.”*

---

## 👤 Author

Built with ❤️ for emotional awareness and mental wellness.

