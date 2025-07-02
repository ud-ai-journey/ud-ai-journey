# 🧭 Decision Coach v2 – Day 78

Hey! This is my Day 78 project, where I took my original Decision Coach and turned it into a much smarter, more personal, and privacy-friendly experience. Here's what I built, how it works, and what I learned along the way.

---

## What's New in v2 (Day 78)

- **Calendar Reminder:** After you get your AI recommendation, you can download a .ics file to remind yourself to revisit your decision in 24 hours. Works with Google, Outlook, Apple Calendar, etc.
- **Self-Insight Dashboard:** There's a whole dashboard tab now! It shows:
  - Most common tones you use
  - Confidence trends
  - Wordcloud of your dilemmas (if you install `wordcloud`)
  - Top 5 most confident decisions
  - "Memory Mode" that summarizes your patterns, values, and wisdoms
  - Average user feedback
- **Multilingual Coach:** You can pick your language (English, Hindi, Telugu, etc.). The app translates your dilemma and the AI's response using Gemini or Groq.
- **Memory Mode:** The dashboard now highlights your most common tones, themes, wisdoms, and average confidence—so you can see your own growth and patterns.
- **Privacy Option:** There's a "Private Session" checkbox. If you use it, your decision is NOT logged or emailed—just shown on screen.
- **Feedback Slider:** After each recommendation, you can rate how helpful it was (1–5). The dashboard shows your average feedback.
- **Groq & Gemini Support:** You can pick which AI backend to use. Groq is super fast, Gemini is great for Google users.

---

## How to Run It Yourself
1. Clone this repo and `cd` into `day_78`
2. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
3. Make a `.env` file (see `.env.example` for what you need):
   ```ini
   SENDGRID_API_KEY=your_sendgrid_api_key
   SENDGRID_FROM_EMAIL=your_verified_sender@email.com
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.0-flash
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=llama-3-70b-8192
   ```
   - Get your SendGrid API key and verify your sender email
   - Get your Gemini API key from Google AI Studio
   - Get your Groq API key from x.ai
4. Run the app:
   ```sh
   streamlit run decision_coach_v2.py
   ```

---

## Security & Privacy
- Never commit your `.env` file (it's in `.gitignore`)
- All secrets are loaded with `python-dotenv`—no hardcoded keys
- "Private Session" mode lets you use the app without logging or emailing anything

---

## Troubleshooting
- **Groq/Gemini errors?**
  - Double-check your API key and model name
  - If you get a 400 or 503 error, try a different model or check your quota
- **Email not received?**
  - Check your spam folder
  - Make sure your sender email is verified in SendGrid
- **Wordcloud not showing?**
  - Install it with `pip install wordcloud`

---

## What I Learned
- How to combine multiple AI backends in one app
- How to make a Streamlit dashboard that's actually useful
- How to handle privacy and feedback in a real-world tool
- Prompt engineering is everything—be explicit with LLMs!
- Building for real users means thinking about language, privacy, and reflection

---

## What's Next
- Even deeper "Memory Mode" (maybe let the coach reference your past values)
- More dashboard analytics
- Deploy online for friends to use

---

## Thanks for Checking This Out!
If you have questions, ideas, or want to build on this, let me know. This was a real learning journey for me, and I hope it helps you too. 