# 🤖 Day 55: AI-Powered Excuse Generator (Python Console App)

## 📖 Overview

Welcome to **Day 55** of my **100 Days of Python + AI** journey! 🎉 This project, the **AI-Powered Excuse Generator**, is a simple Python console app that generates creative excuses using the Gemini API. After building polished web apps like the YouTube Title Optimizer Pro on Day 54, I wanted to shift gears back to a raw, powerful Python console app for Day 55. This tool takes a user’s scenario and desired tone, crafts a prompt, and generates a natural-sounding excuse in seconds.

On June 09, 2025, I built this app to generate excuses like, “My assignment was late because my cat decided it was the perfect spot for her nap!”—perfect for a quick laugh or a professional alibi. This project showcases my ability to integrate AI with simple Python scripts, aligning with my goals as an **AI Applications Researcher/Vibe Coder**.

## 🎯 Goals

- Build a Python console app to generate excuses using the Gemini API.
- Take user input for context and tone to customize excuses.
- Keep the app simple, raw, and powerful with minimal dependencies.
- Document the project for my GitHub portfolio.

## 🛠️ Features

- **User Input**:
  - Enter a scenario (e.g., “late assignment”) and tone (e.g., “funny”).
- **AI-Powered Excuses**:
  - Uses the Gemini 1.5 Flash model to generate short, creative excuses.
- **Simple Console Interface**:
  - Runs entirely in the terminal for a lightweight experience.

## 📋 Project Structure

```
day_55/
├── excuse_generator.py     # Main Python script for the console app
├── requirements.txt        # Dependencies for the project
├── .gitignore              # Ignores .env file with API key
└── README.md               # Project documentation (this file)
```

## ⚙️ How It Works

1. **User Input**:
   - The app prompts for a scenario (e.g., “late assignment”) and a tone (e.g., “funny”).
2. **Prompt Crafting**:
   - Constructs a prompt for the Gemini API based on the input.
3. **Excuse Generation**:
   - Sends the prompt to Gemini 1.5 Flash and retrieves a creative excuse.
4. **Output**:
   - Displays the generated excuse in the console.

## 🏆 Achievements

- **Gemini API Integration**:
  - Successfully integrated the Gemini API into a console app.
- **Creative Output**:
  - Generated natural, tone-appropriate excuses like “My assignment was late because my cat decided it was the perfect spot for her nap!”
- **Simplicity**:
  - Kept the app lightweight with a raw Python console interface.
- **Portfolio Addition**:
  - Documented the project for my GitHub portfolio on June 09, 2025.

## 🚀 How to Run

### Prerequisites
- **Python**: Version 3.6 or higher (tested with Python 3.12).
- **Gemini API Key**:
  - Sign up at [Google AI Studio](https://aistudio.google.com/) and get your API key.
  - Create a `.env` file in the `day_55/` directory with:
    ```
    GEMINI_API_KEY=your-api-key-here
    ```
- **Dependencies**:
  - Install required libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Steps
1. **Clone or Download**:
   - Save `excuse_generator.py` and `requirements.txt` in a `day_55/` directory.
   - Create a `.env` file with your Gemini API key.
2. **Run the App**:
   - Navigate to the project directory:
     ```bash
     cd path/to/day_55
     ```
   - Launch the app:
     ```bash
     python excuse_generator.py
     ```
3. **Usage**:
   - Enter a scenario and tone when prompted.
   - View the generated excuse in the console.

## 📈 Sample Output

### Input
- **Context**: late assignment
- **Tone**: funny

### Output
```
🤖 AI-Powered Excuse Generator 🤖
Generate creative excuses in seconds!
----------------------------------------
Why do you need an excuse for? (e.g., late assignment, missing gym): late assignment
What kind of excuse do you want? (funny, emotional, serious, professional): funny

Generating your excuse... 🤔

Here's your excuse: 🤖
My assignment was late because my cat decided it was the perfect spot for her nap!
```

## 🔮 Future Improvements

- **Save Excuses**:
  - Save generated excuses to a `.txt` file for later use.
- **Retry Option**:
  - Add a “generate again” feature to get multiple excuses.
- **CLI Interface**:
  - Use `argparse` or `typer` for a command-line interface.
- **GUI Version**:
  - Create a Tkinter GUI version for a graphical interface.
- **Web App**:
  - Build a Streamlit web app version for broader accessibility.

## 📚 What I Learned

- Integrating the Gemini API into a Python console app.
- Crafting effective prompts for tone-specific, creative responses.
- Keeping a project simple and lightweight with a console interface.
- Documenting a raw Python project for my portfolio.

## 💡 Why This Matters

The AI-Powered Excuse Generator is a fun, practical tool that demonstrates my ability to combine AI with simple Python scripts. It’s a great example of how I can build lightweight, functional apps with real-world applications, adding value to my portfolio as an AI Applications Researcher.

## 📞 Contact

- **Email**: 20udaykumar02@gmail.com
- **Website**: https://ud-ai-kumar.vercel.app/

Feel free to reach out if you’d like to collaborate or learn more about my journey!

---

**Part of Boya Uday Kumar’s 100 Days of Python + AI Journey**  
**June 09, 2025**