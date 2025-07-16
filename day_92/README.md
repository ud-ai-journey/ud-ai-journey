# 🌟 KidDiary.ai – Magical Journaling for Kids

A daily voice or text journal powered by Python + AI that helps kids express their feelings, build reflection habits, and receive kind feedback from a friendly AI companion.

---

## ✅ What’s Implemented (Day 92)

- 📁 **Project structure**: Modular folders for models, utils, data, audio, and templates
- 🎨 **Streamlit UI**: Kid-friendly, with text input and playful layout
- 🧠 **Emotion classifier**: Offline-friendly (keyword-based, easy to upgrade)
- ✍️ **AI diary story generator**: Rephrases input into a magical story
- 🧙‍♂️ **Doodle the Diary Dragon**: Gives kind, wise feedback
- 💾 **Local JSON storage**: Entries are saved and shown in a timeline with mood emoji
- 📅 **Timeline view**: Recent entries displayed with date and mood emoji

---

## 🚀 How to Run

```bash
cd day_92
streamlit run app.py
```

---

## 🛠️ Next Steps
- Add voice input (speech recognition)
- Upgrade emotion detection to use transformers
- Add PDF export for weekly scrapbook
- Enhance timeline/calendar visualization
- Add audio feedback (gTTS/pyttsx3)

---

## ✨ Key Features (Vision)
- 🧒 Kid-friendly voice/text input
- 🎭 Emotion detection
- 📝 Diary entry generation
- 🌈 Mood color or emoji
- 📅 Calendar or timeline view
- 🧙‍♂️ AI Companion: Doodle the Diary Dragon
- 📥 Optional export: Weekly memory scrapbook PDF

---

## Tech Stack
- Streamlit for UI
- speech_recognition (optional voice input)
- transformers (emotion analysis)
- ollama/llama2 or GPT4All (diary story generation)
- matplotlib/emoji charts (visualization)
- gTTS/pyttsx3 (audio feedback)
- JSON/SQLite (storage) 