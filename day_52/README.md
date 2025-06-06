# 🎥 YouTube Title Optimizer with AI (Day 52)

This is a simple yet powerful AI-based YouTube Title Optimizer built using **Gemini API** and **Streamlit** as part of the [100 Days of Python + AI Challenge].

It helps creators optimize their video titles for **SEO**, **clickability**, and **emotional engagement**, based on the video’s current title, description, and category.

---

## 🚀 Features

✅ Gemini API integration for AI-powered optimization  
✅ Clean and responsive Streamlit interface  
✅ SEO-friendly improved title (under 70 characters)  
✅ 3 alternate title suggestions  
✅ Reasoning behind why the optimized title works  
✅ Content category selector (Tech, Vlog, Gaming, etc.)  
✅ “Copy to clipboard” buttons for easy usage  
✅ Error handling and fallback logic for smooth UX

---

## 📸 Demo Screenshot

![YouTube Title Optimizer Screenshot](C:\Users\uday kumar\Python-AI\ud-ai-journey\day_52\Screenshot 2025-06-06 214658.png) 

---

## 🧠 How It Works

The app takes 3 inputs from the user:
- Current YouTube Video Title
- Description of the Video
- Content Category

It then sends this data to the **Gemini 1.5 Flash model** with a carefully crafted prompt to generate:
- A main optimized title
- 3 alternate suggestions
- A short explanation of why the title is effective

---

## 🛠️ Tech Stack

- `Python 3.10+`
- `Streamlit`
- `Google Generative AI (Gemini)`
- `python-dotenv` for managing API keys

---

## 📂 Project Structure

```

day\_52\_youtube\_title\_optimizer/
├── app.py                  # Streamlit front-end
├── title\_optimizer.py      # Gemini prompt & response logic
├── .env                    # Contains your GEMINI\_API\_KEY
└── README.md               # This file

```

---

## 🔐 .env Format

```

GEMINI\_API\_KEY=your\_gemini\_api\_key\_here

```

---

## ▶️ How to Run

1. Clone this repo or navigate to your project folder:
   ```bash
   git clone https://github.com/ud-ai-journey/ud-ai-journey.git
   cd day_52_youtube_title_optimizer
   ```

2. Install dependencies:

   ```bash
   pip install streamlit python-dotenv google-generativeai
   ```

3. Create your `.env` file and add your `GEMINI_API_KEY`.

4. Run the app:

   ```bash
   streamlit run app.py
   ```

---

## 📌 Example Output

**Input:**

* Title: `My Empathy Engine in Two Days`
* Description: `build empathy engine in 2 days`
* Category: `Tech`

**Output:**

> **Optimized Title:**
> `Build an Empathy Engine in 48 Hours!`

> **Alternate Suggestions:**
>
> * Empathy Engine: 2-Day Build Challenge!
> * Hack Your Empathy: 48-Hour Project
> * I Built an Empathy Engine in 2 Days!

> **Why This Works:**
> *The improved titles use stronger action verbs ("Build," "Hack"), create a sense of urgency ("48 Hours!"), and incorporate keywords like "Empathy Engine" for better SEO.*

---

## 👨‍💻 Author

**Boya Uday Kumar**
Part of the 100 Days of Python + AI Challenge
\[June 2025]

---

## 📅 Day Tracker

✅ **Day 52 Completed** | 🔥 Challenge: \[YouTube Title Optimizer]

```

