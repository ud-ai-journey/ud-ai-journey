# ✨ Day 53: Real-Time Language Translator with AI + Streamlit + Voice Input 🌐

## 📖 Overview

Welcome to **Day 53** of my **100 Days of Python + AI** journey! 🎉 This project, the **Real-Time Language Translator**, is a Streamlit web app that breaks language barriers by allowing users to speak into a microphone, select source and target languages, and get instant translations powered by the Gemini API (with a fallback to Google Translate). The app also features text-to-speech (TTS) to read translations aloud, making it a practical tool for travelers, learners, and global teams.

Building on my recent work with Streamlit and the Gemini API (e.g., the YouTube Title Optimizer on Day 52), this project introduced me to voice input using `speechrecognition`, translation APIs, and TTS with `gTTS`. On June 07, 2025, I successfully ran the app, translating "A part of 100 is Python code" from English to Spanish: "Una parte de 100 es código Python." This project aligns with my roadmap goals of creating AI-driven tools for real-world use cases, enhancing my skills as an **AI Applications Researcher/Vibe Coder**.

## 🎯 Goals

- Learn to capture voice input using `speechrecognition` in Python.
- Integrate translation APIs (Gemini and Google Translate) for real-time language conversion.
- Build a responsive, user-friendly UI with `Streamlit`.
- Add text-to-speech functionality to read translations aloud using `gTTS`.
- Create a practical tool for breaking language barriers.

## 🛠️ Features

- **Voice Input** 🎙️:
  - Users can speak into their microphone, and the app converts speech to text.
- **Language Selection** 🌐:
  - Dropdowns to select source and target languages (e.g., English to Spanish).
- **AI-Powered Translation** 🤖:
  - Uses the Gemini API for natural, contextually accurate translations.
  - Falls back to Google Translate if Gemini fails.
- **Text-to-Speech** 🔊:
  - Plays the translated text aloud using `gTTS`.
- **Streamlit UI** 🌐:
  - Clean, centered interface with dynamic updates.

## 📋 Project Structure

```
day_53/
├── app.py                  # Streamlit app for the user interface
├── requirements.txt        # Dependencies for the project
├── .gitignore              # Ignores .env file with API key
└── README.md               # Project documentation (this file)
```

- **`app.py`**: The Streamlit app that handles voice input, translation, and TTS playback.
- **`requirements.txt`**: Lists dependencies like `streamlit`, `speechrecognition`, `googletrans`, and `gTTS`.
- **`.gitignore`**: Ensures the `.env` file (with the API key) is not uploaded to GitHub.
- **`README.md`**: This documentation file.

## ⚙️ How It Works

1. **Voice Input**:
   - Users click "Speak Now" to record audio via their microphone.
   - The app uses `speechrecognition` to convert speech to text.
2. **Translation**:
   - The app sends the recognized text to the Gemini API for translation.
   - If Gemini fails, it falls back to Google Translate.
3. **Output Display**:
   - The translated text is displayed in the Streamlit app.
   - Users can click "Play Translation" to hear the translated text aloud.

## 🏆 Achievements

- **Voice Input**:
  - Successfully captured and converted speech to text using `speechrecognition`.
- **Translation**:
  - Integrated the Gemini API for natural translations, with a fallback to Google Translate.
- **Text-to-Speech**:
  - Added TTS functionality using `gTTS` to read translations aloud.
- **Streamlit UI**:
  - Built a clean, centered UI with dynamic updates for real-time translation.
- **Successful Run**:
  - Translated "A part of 100 is Python code" from English to Spanish on June 07, 2025.

## 🚀 How to Run

### Prerequisites
- **Python**: Version 3.6 or higher (tested with Python 3.12).
- **Gemini API Key**:
  - Sign up at [Google AI Studio](https://aistudio.google.com/) and get your API key.
  - Create a `.env` file in the `day_53/` directory with:
    ```
    GEMINI_API_KEY=your-api-key-here
    ```
- **Dependencies**:
  - Install required libraries:
    ```bash
    pip install -r requirements.txt
    ```
  - Ensure `PyAudio` is installed for `speechrecognition`:
    ```bash
    pip install PyAudio
    ```

### Steps
1. **Clone or Download**:
   - Save `app.py` and `requirements.txt` in a `day_53/` directory.
   - Create a `.env` file with your Gemini API key.

2. **Run the App**:
   - Navigate to the project directory:
     ```bash
     cd path/to/day_53
     ```
   - Launch the Streamlit app:
     ```bash
     streamlit run app.py
     ```
   - Open the provided URL (e.g., `http://localhost:8501`) in your browser.

3. **Usage**:
   - Select source and target languages (e.g., English to Spanish).
   - Click "Speak Now" and say something (e.g., "A part of 100 is Python code").
   - View the translated text and click "Play Translation" to hear it aloud.

## 📈 Sample Output

### Input
- **Source Language**: English
- **Target Language**: Spanish
- **Spoken Text**: A part of 100 is Python code.

### Output
- **Translated English → Spanish**: Una parte de 100 es código Python.

## 🔮 Future Improvements

- **Emoji Flag Selector**: Add flag emojis to the language dropdown for a visual touch.
- **Auto-Detect Language**: Use `speechrecognition` to auto-detect the source language.
- **Custom Translation Context**: Allow users to specify tone (e.g., polite, casual) via the Gemini prompt.
- **Error Handling**: Improve robustness for noisy environments or poor internet.
- **Deployment**: Host the app on Streamlit Community Cloud for public access.

## 📚 What I Learned

- Capturing voice input with `speechrecognition` and handling microphone audio.
- Using the Gemini API for natural language translation.
- Implementing a fallback mechanism with Google Translate.
- Adding text-to-speech functionality with `gTTS`.
- Building a real-time, interactive UI with Streamlit.
- Troubleshooting Python package installation issues (e.g., `speechrecognition` vs. `speech_recognition`).

## 💡 Why This Matters

The Real-Time Language Translator is a practical tool that can help travelers, language learners, and global teams communicate effortlessly. It combines voice input, AI translation, and TTS, showcasing my ability to build end-to-end AI applications with a focus on user experience.

## 📞 Contact

- **Email**: 20udaykumar02@gmail.com
- **Website**: https://ud-ai-kumar.vercel.app/

Feel free to reach out if you’d like to collaborate or learn more about my journey!

---

**Part of Boya Uday Kumar’s 100 Days of Python + AI Journey**  
**June 07, 2025**