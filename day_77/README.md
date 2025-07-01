# 🧭 Daily Decision Coach

Hi! This is my own project to help with something I (and a lot of people I know) struggle with: making everyday decisions without overthinking. I wanted a tool that would give me clarity, break down my options, and even let me email myself a summary for future reflection. Here's what I built, how I built it, and what I learned along the way.

---

## Why I Made This

I kept getting stuck on small but stressful choices—should I move, take a gig, buy something, reach out to someone, etc. I wanted a coach, not just a chatbot, to help me see things clearly: pros, cons, gut-check, wisdom, and a nudge toward action. So I built this app, and learned a lot in the process.

---

## What It Does
- Lets you describe any decision you're stuck on
- Uses Gemini AI to break it down (clarity, pros/cons, emotional check, wisdom, recommendation)
- Lets you pick the tone (gentle, direct, or a bit humorous)
- You can email the advice to your future self (I use this a lot!)
- Keeps a log of your recent decisions so you can reflect later
- All your secrets (API keys, emails) are safe in a `.env` file—nothing in the code

---

## How I Built It (and What I Learned)
- Started with Streamlit for the UI—super fast to prototype
- Gemini API for the actual coaching logic (prompt engineering is everything!)
- SendGrid for the email-to-self feature (make sure to verify your sender email, or it won't work)
- Used `python-dotenv` so I never have to worry about leaking keys
- Ran into a bunch of issues with API errors, email deliverability, and linter warnings—fixed them all by making sure every secret is loaded safely and always a string
- The app warns you if you forget to set up your `.env` file (trust me, I did this more than once)
- Everything is logged locally so you can see your last few decisions and recommendations

---

## How to Run It Yourself
1. Clone this repo and `cd` into `day_77`
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
   ```
   - Get your SendGrid API key and verify your sender email (this tripped me up at first)
   - Get your Gemini API key from Google AI Studio
4. Run the app:
   ```sh
   streamlit run daily_decision_coach.py
   ```

---

## Security Stuff I Learned
- Never, ever commit your `.env` file (it's in `.gitignore`)
- All secrets are loaded with `python-dotenv`—no hardcoded keys
- If you forget a key, the app will warn you and skip the feature

---

## Troubleshooting (Things I Bumped Into)
- **Email not received?**
  - Check your spam folder
  - Make sure your sender email is verified in SendGrid (otherwise, nothing gets delivered)
  - Look at SendGrid's Email Activity dashboard for bounces/drops
  - Try a different recipient email
- **Gemini API issues?**
  - Double-check your API key and model name
  - If you get a 404 or auth error, check your Google Cloud Console or AI Studio

---

## What's Next / What I'd Add
- More wisdom frameworks or "coach personalities"
- Reflection tracker (log outcomes, not just decisions)
- Maybe deploy it online for friends to use

---

## Thanks for Checking This Out!
If you have questions, ideas, or want to build on this, let me know. This was a real learning journey for me, and I hope it helps you too. 