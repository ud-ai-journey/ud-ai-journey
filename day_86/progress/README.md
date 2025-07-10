# 🚀 GURU SAHAYAM (ClassGenie Hackathon Edition)

Empowering Teachers in Multi-Grade Classrooms  


---

## 🏆 Project Overview
GURU SAHAYAM (formerly ClassGenie) is an AI-powered assistant designed to help teachers in India's multi-grade, multi-lingual, and culturally diverse classrooms. Built for the Agentic AI Day Hackathon, it leverages cutting-edge AI to generate lesson plans, quizzes, feedback, and more—tailored to local language and community context.

---

## 💡 Problem Statement
**Empowering Teachers in Multi-Grade Classrooms**  
Teachers in India often manage classrooms with students of different ages, languages, and cultural backgrounds. GURU SAHAYAM provides instant, context-aware educational content, saving time and making learning more inclusive.

---

## ✨ Key Features
- **Local Language Support:** Generate content in English or 12+ Indian languages.
- **Cultural/Regional/Community Context:** Tailor lessons to your students' backgrounds (e.g., "Andhra Chenchus").
- **Visual Aids Suggestions:** Get ideas for diagrams and images to support your teaching.
- **Speech-to-Text Input:** Dictate lesson topics and feedback (works best in Chrome).
- **User-Friendly UI:** Designed for quick adoption by teachers and hackathon judges.

---

## 🚦 Quick Start
1. **Install dependencies:** See below.
2. **Get a Google Gemini API key:** [Sign up here](https://aistudio.google.com/app/apikey) (free tier available).
3. **Add your API key:**
   - Create a `.streamlit/secrets.toml` file:
     ```toml
     GOOGLE_API_KEY = "your-gemini-api-key"
     ```
   - Or edit `main.py` to paste your key directly (not recommended for production).
4. **Run the app:**
   ```sh
   streamlit run day_84/main.py
   ```
5. **Use the sidebar:** Select language, enter cultural context, and choose a tool.
6. **Fill in details:** Use text or speech input, generate content, and download results.

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```sh
git clone <your-repo-url>
cd ud-ai-journey
```

### 2. Install dependencies
```sh
pip install streamlit google-generativeai pillow
```

### 3. Add your Gemini API key
- [Get your key here](https://aistudio.google.com/app/apikey)
- Add to `.streamlit/secrets.toml` or directly in `main.py`

### 4. Run the app
```sh
streamlit run day_84/main.py
```

---

## 🖥️ Usage Guide
- **Select Output Language:** Choose from English or Indian languages.
- **Cultural/Regional/Community Context:** Enter details like "Rural Karnataka" or "Andhra Chenchus" for tailored content.
- **Choose a Tool:** Lesson Plan Generator, Quiz Maker, Feedback Writer, etc.
- **Speech-to-Text:** Click the mic icon to dictate inputs (Chrome recommended).
- **Visual Aids:** Enable for suggestions; image generation requires paid Gemini API.
- **Download:** Save generated content for classroom use.

---

## ⚠️ Known Limitations
- **Image Generation:** Only available with paid Gemini API tier.
- **Best in Chrome:** Speech-to-text works best in Chromium browsers.
- **Google API Quotas:** Free tier may have usage limits.
- **Linter Warnings:** Some IDEs may show import warnings; ignore if the app runs.

---

## 👥 Credits
- **Project Lead:** Uday Kumar
- **Brand Name:** GURU SAHAYAM
- **Built for:** Agentic AI Day Hackathon 2024
- **Inspired by:** My Dad

---

## 💬 Contact

Reach out on GitHub or connect via [Portfolio](https://ud-ai-kumar.vercel.app/) to collaborate on educational AI projects.

*Built with ❤️ for educators | Powered by GEMINI AI & Prompt Engineering*
