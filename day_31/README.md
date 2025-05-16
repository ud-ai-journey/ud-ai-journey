# 🎵 MoodMuse – Emotion-to-Music Generator | Day 31

Welcome to **Day 31** of the 100-Day Python + AI Challenge!  
Today’s project is **MoodMuse** – a soulful CLI tool that listens to your emotions and plays a matching track to reflect or uplift your mood.  
Because sometimes, the right tune can heal what words cannot. 🌌🎶

---

## 🔧 Features

✨ 🎙️ Voice input to capture your current emotion  
✨ 🧠 Sentiment detection using Hugging Face's DistilBERT  
✨ 🎧 Auto-plays a royalty-free music track matching your vibe (Positive / Neutral / Negative)  
✨ 🎨 Beautifully colored CLI with heart  
✨ 🔔 Optional music playback via `pygame`  

---

## 🚀 Setup

**Prerequisites:**  
- Python 3.8+  
- Microphone  
- Internet connection  

**Install the dependencies:**
```bash
pip install speechrecognition transformers pygame colorama
````

**Add Music Files:**
Place 3 royalty-free tracks inside a folder named `audio/` in the root directory:

* `positive.mp3`
* `neutral.mp3`
* `negative.mp3`

You can grab free background tracks from [Pixabay Music](https://pixabay.com/music/).

---

## ▶️ How to Use

```bash
python moodmuse.py
```

1. Speak your heart out – how you’re feeling right now.
2. The app understands your tone and decodes the emotion.
3. It plays a music track that resonates with your current mood.
4. Feel seen. Feel heard. Feel better. ✨

---

## 📎 Example Output

```
🎵 Welcome to MoodMuse! 🎧
🎙️ Say how you feel today...
📜 You said: "I feel so drained today..."
🧠 Analyzing emotion...
😞 Mood Detected: Negative (0.85)
🎧 Now playing: “Calm Restore” for your mood
✨ Tip: “It’s okay to rest. Your energy will bloom again.”
Would you like to express another mood? (y/n):
```

---

## 🧠 Tech Stack

* `speech_recognition` – Voice to text conversion
* `transformers` – DistilBERT for emotion detection
* `pygame` – Background music player
* `colorama` – Colored terminal output

---

## ⚠️ Disclaimer

This is a learning project for emotional exploration.
MoodMuse is not a replacement for professional mental health support. But it is a small magical friend that listens and plays you a tune when you need it the most. 💛

---

## 🙌 Acknowledgements

* [Hugging Face Transformers](https://huggingface.co/)
* [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
* [Pygame](https://www.pygame.org/)
* [Colorama](https://pypi.org/project/colorama/)
* [Pixabay Music](https://pixabay.com/music/)

---

Keep vibing, keep coding.
Let your emotions be the melody, and your code be the harmony. 🎼💻
**– You, the Muse of MoodMuse**
