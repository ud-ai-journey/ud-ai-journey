# 🎨 EmotiGram – AI Mood-to-Art Generator

**Day 90 of the 100 Days Python & AI Challenge**

> *"Upload a selfie or speak a few words, and get a beautiful artwork that matches your mood!"*

## 🚀 What is EmotiGram?

EmotiGram is a fun, offline AI app that detects your emotion from a selfie or your voice, then generates a unique piece of art or sticker that reflects your vibe. Perfect for sharing, journaling, or just making your day brighter!

## ✨ Features

- 🧠 **Emotion Detection** (face or voice)
- 🎨 **Mood Art Generator** (Stable Diffusion, local)
- 🖼️ **AI Image Creation** (no API, no cloud)
- 🧵 **Emoti-Sticker Generator** (caption with your name & mood)
- 🎁 **Export & Share** (downloadable images)
- 🔄 **Mood Timeline** (optional, track your moods)

## 🛠️ Tech Stack

| Purpose           | Tools                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Interface         | Streamlit                                                             |
| Emotion Detection | FER (Facial Emotion Recognition), transformers sentiment analysis     |
| Text-to-Image     | Local SD with diffusers (free) or InvokeAI                            |
| Voice             | Whisper (optional, for speech)                                        |
| File Handling     | PIL, base64, tempfile                                                 |
| No Cloud, No Cost | Everything offline and lightweight                                    |

## 📦 Folder Structure

- `app.py` – Main Streamlit app
- `requirements.txt` – Dependencies
- `art_styles.json` – Mapping of emotions to art prompts/styles
- `emotion_model.joblib` – Pretrained emotion model (optional)
- `generated/` – Generated images

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   streamlit run app.py
   ```
3. **Open your browser:**
   Go to [http://localhost:8501](http://localhost:8501)

## 📱 How to Use

1. Upload a selfie or record your voice
2. Let the app detect your emotion
3. See a beautiful artwork generated for your mood
4. Download or share your EmotiGram!

---

**Built with ❤️ for Day 90 of the 100 Days Python & AI Challenge** 

## ⚠️ Hardware Requirements & Alternatives

**Stable Diffusion (AI art generation) is resource-intensive!**

- For best results, use a computer with an NVIDIA GPU (4GB+ VRAM recommended).
- On laptops with only integrated graphics (no dedicated GPU), it will work but be **very slow** (5–15+ minutes per image).
- At least 8GB RAM is recommended. Low RAM or old CPUs may cause crashes or freezing.

### 🚀 Alternatives for Low-Power Laptops

- **Google Colab**: Run the app in the cloud for free with GPU. ([Colab link template](https://colab.research.google.com/))
- **Hugging Face Spaces**: Deploy your app for free (with some limitations).
- **Use pre-generated images** for demo if you can't run locally.

### 🛠️ Troubleshooting

- If you see `ModuleNotFoundError: No module named 'diffusers'`, run:
  ```bash
  pip install diffusers torch
  ```
- The first time you generate art, the model will download (~4GB). Make sure you have enough disk space and a stable internet connection. 