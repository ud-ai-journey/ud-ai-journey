# 🎤 PronounceIt - Picture to Pronunciation App

**Day 89 of the 100 Days Python & AI Challenge**

> *"Learn how to pronounce anything by just taking a picture!"*

## 🚀 What is PronounceIt?

**PronounceIt** is an offline AI app that helps you learn pronunciation and build vocabulary from real-world images. Just upload or snap a photo, and the app will:

- 🔍 Detect objects in your image using YOLOv8
- 🔊 Generate IPA transcription and audio pronunciation (6 languages)
- 📚 Build your vocabulary journal automatically
- 📊 Track your learning with analytics
- 🎮 Play learning games (flashcards, guessing)
- 📷 Use live camera for instant learning

## ✨ Key Features

- **Offline, zero API costs** – all processing is local
- **YOLOv8 object detection** (COCO classes)
- **IPA transcription** and **audio generation** (gTTS)
- **Vocabulary journal** with audio playback
- **Learning analytics** (Plotly)
- **Gamified learning** (flashcards, guessing)
- **Multi-language support** (English, Spanish, French, German, Italian, Portuguese)
- **Beautiful Streamlit UI** with dark mode

## 🛠️ Tech Stack

| Component         | Technology         |
|-------------------|-------------------|
| Frontend          | Streamlit         |
| Object Detection  | YOLOv8 (Ultralytics) |
| TTS               | gTTS              |
| Phonetics         | eng-to-ipa        |
| Analytics         | Plotly            |
| Image Processing  | OpenCV, Pillow    |
| Data Storage      | JSON              |

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run saythat_app.py
   ```

3. **Open your browser:**  
   Go to [http://localhost:8501](http://localhost:8501)

## 📱 How to Use

1. **Choose input method:** Upload an image or use your camera.
2. **Select language:** Pick from 6 languages in the sidebar.
3. **View detections:** See objects with bounding boxes and confidence.
4. **Learn pronunciation:** Get IPA, audio, and add to your vocabulary.
5. **Play games:** Flashcards and guessing game to reinforce learning.
6. **Track progress:** View analytics and vocabulary stats.

## 🎯 Use Cases

- Language learners
- Kids and education
- Tourists and travelers
- Memory training
- Classroom teaching

## 📊 Analytics & Gamification

- Daily detection charts
- Most common objects
- Vocabulary stats
- Flashcard review
- Guess the object

## 📝 Notes

- **Detection is limited to common objects (COCO classes) supported by YOLOv8.**
- **No logo/brand detection** (custom models required for that).
- **All processing is local and offline.**

## 📦 Folder Structure

- `saythat_app.py` – Main Streamlit app
- `requirements.txt` – Dependencies
- `vocabulary.json` – Your saved vocabulary
- `yolov8n.pt` – YOLOv8 model weights
- `audio_*.mp3` – Generated pronunciation audio
- `sample_image.jpg` – Example image for testing
- `demo.py` – Demo script for core features

**Built with ❤️ for Day 89 of the 100 Days Python & AI Challenge**

*"The best AI products are the ones that work offline and scale to infinity!"* 🚀 