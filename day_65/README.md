# 🎤 Day 65 – VibeCheck: Real-Time Speech Emotion Recognition 🧠🎶

Welcome to **Day 65** of my Python + AI journey!  
Today’s project is all about understanding the vibes in your voice using machine learning and audio processing.  
**VibeCheck** listens to your speech, analyzes it, and predicts your emotion in real time!

---

## 🛠️ What It Does

VibeCheck is a console-based tool that:
- Records 5 seconds of your voice from the microphone
- Extracts MFCC features from the audio
- Predicts your emotion (neutral, happy, sad, angry) using a trained model
- Shows the detected emotion with a timestamp in the terminal
- Handles missing models gracefully and guides you to train your own

---

## 💡 Features

- **Real-time audio recording**
- **MFCC feature extraction**
- **Emotion prediction with a scikit-learn model**
- **Console feedback with timestamps**
- **Easy model training script included**
- **Expandable emotion set**

---

## 🚀 How to Run

1. **Install requirements**
   ```powershell
   pip install numpy librosa sounddevice scikit-learn joblib
   ```

2. **Train the model (if you don’t have one)**
   - Download the RAVDESS dataset and set the path in `train_emotion_model.py`
   - Run:
     ```powershell
     python train_emotion_model.py
     ```
   - This will create `emotion_model.joblib` in your folder

3. **Run VibeCheck**
   ```powershell
   python vibecheck.py
   ```

---

## 🎬 Usage

- Speak into your microphone when prompted
- See your detected emotion and timestamp in the console
- Press `Ctrl+C` to exit

---

## 🗂️ Tech Stack

* Python 3.x
* numpy, librosa, sounddevice, scikit-learn, joblib

---

## 📁 Files

| File                    | Description                        |
|-------------------------|------------------------------------|
| `vibecheck.py`          | Main script for emotion detection  |
| `train_emotion_model.py`| Script to train the model          |
| `emotion_model.joblib`  | Trained model file                 |

---

## 🌟 Why This Matters

This project combines audio processing, machine learning, and real-time feedback.  
It’s a step towards building smarter, more empathetic AI tools that can understand human emotions.

> “The voice is the window to the soul — and now, to the AI as well.” – Me on Day 65

---

## 🙌 Acknowledgments

Thanks to the open-source community, RAVDESS dataset creators, and every coder who keeps learning.

---

**#Day65Complete ✅**
