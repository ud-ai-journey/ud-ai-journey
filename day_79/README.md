# Decision Coach V3 – Self-Therapy Toolkit (Day 79)

## Overview
Decision Coach V3 is your all-in-one self-therapy and decision support toolkit. It helps you reflect, plan, and grow with features like value tracking, emotion logging, action plans, reminders, partner sharing, and more—all in a beautiful Streamlit dashboard.

---

## Features

- **Value Meter:** Select which personal values each decision touches (e.g., Growth, Security, Freedom).
- **Emotion Tone:** Log how you feel about each decision (Confident, Anxious, etc.).
- **Action Plan & Progress Tracker:** Break decisions into actionable steps, set target dates, and check off progress.
- **Reflection Journal:** Write and save reflections for each decision, and get AI feedback on your thoughts.
- **Reminders & Nudges:** Schedule email reminders for action steps and reflections. Get nudges if you're inactive.
- **Partner Sharing:** Share decisions, action plans, or reflections with an accountability partner via email.
- **Edit Email for Past Decisions:** Update your email for any decision to enable reminders.
- **Export & Download:** Download your entire journey as JSON, CSV, or PDF for backup, sharing, or review.

---

## How to Run

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   # For PDF export:
   pip install fpdf
   ```
2. **Set up environment variables:**
   - `SENDGRID_API_KEY` and `SENDGRID_FROM_EMAIL` for email features.
   - `GEMINI_API_KEY` for AI feedback (optional).
3. **Start the app:**
   ```bash
   streamlit run decision_coach_v3.py
   ```
4. **Open in your browser** (usually at http://localhost:8501)

---

## How to Use

- **Log a Decision:** Fill out the form in the Decision Coach tab. Add your email to enable reminders.
- **Track Progress:** Use the Action Plan & Progress Tracker to break down and complete steps.
- **Reflect:** Write and save reflections for each decision. Get AI feedback if desired.
- **Reminders:** Opt-in and schedule reminders for action steps and reflections. Edit your email for past decisions if needed.
- **Share:** Use the Partner Sharing section to email updates to an accountability partner.
- **Export:** Go to the Export & Download section in the dashboard, choose your format, and download your journey.

---

## Privacy
Your data is stored locally and is private to you. Exported files are for your use only—keep them safe!

---

## Credits
Built as part of the 100 Days of AI Journey. Powered by Streamlit, Gemini, and SendGrid. 