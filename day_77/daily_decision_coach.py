import streamlit as st
import requests
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

# --- WARN IF SECRETS MISSING ---
if not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
    st.warning("SendGrid API key or sender email not set. Please add them to your .env file.")
if not GEMINI_API_KEY:
    st.warning("Gemini API key not set. Please add it to your .env file.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Tone options
TONE_OPTIONS = {
    "Gentle": "Keep your language warm, gentle, and supportive.",
    "Direct": "Be concise, clear, and direct in your advice.",
    "Humorous": "Add a light, humorous touch to your advice, but keep it respectful."
}

def send_email(to_email, subject, body):
    smtp_server = "smtp.sendgrid.net"
    smtp_port = 587
    username = "apikey"
    password = SENDGRID_API_KEY or ""
    msg = MIMEMultipart()
    msg["From"] = SENDGRID_FROM_EMAIL or ""
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(SENDGRID_FROM_EMAIL or "", to_email, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)

# Prompt template for Gemini
PROMPT_TEMPLATE = '''
You are a compassionate decision coach. The user is stuck on a small but stressful choice. Help them decide using these steps:
1. Clarify the decision
2. Analyze pros & cons
3. Check emotional alignment
4. Offer a wisdom-based reflection
5. Suggest a next step (with a confidence score)

Tone: {tone}

Format your response as JSON with these keys: clarified_decision, pros, cons, emotional_read, wisdom, recommendation, confidence_percent.

User's dilemma: {dilemma}
'''

def query_gemini(dilemma, tone):
    prompt = PROMPT_TEMPLATE.format(dilemma=dilemma, tone=TONE_OPTIONS[tone])
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Extract the model's text response
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        # Try to parse as JSON
        try:
            parsed = json.loads(text)
            return parsed
        except Exception:
            # Fallback: try to extract JSON from text
            import re
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                return {"error": "Could not parse Gemini response."}
    except Exception as e:
        return {"error": str(e)}

# Log each session
LOG_PATH = os.path.join(os.path.dirname(__file__), "decision_log.json")
def log_decision(entry):
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        st.warning(f"Could not log decision: {e}")

# Streamlit UI
st.set_page_config(page_title="Daily Decision Coach", page_icon="🧭")
st.title("🧭 Daily Decision Coach")
st.write("Struggling with a small but stressful choice? Let your AI coach help you reflect and decide.")

dilemma = st.text_area("Describe your decision dilemma:", placeholder="Should I move to a new team at work?")
tone = st.selectbox("Choose the tone of advice:", list(TONE_OPTIONS.keys()), index=0)
email = st.text_input("(Optional) Email this to my future self:", placeholder="you@email.com")

if st.button("Coach Me!") and dilemma.strip():
    with st.spinner("Thinking deeply about your decision..."):
        result = query_gemini(dilemma, tone)
    if "error" in result:
        st.error(f"AI Error: {result['error']}")
    else:
        with st.expander("🧩 Decision Clarity", expanded=True):
            st.write(result.get("clarified_decision", "-"))
        with st.expander("✅ Pros", expanded=False):
            pros = result.get("pros", [])
            if isinstance(pros, list):
                for p in pros:
                    st.markdown(f"- {p}")
            else:
                st.write(pros)
        with st.expander("⚠️ Cons", expanded=False):
            cons = result.get("cons", [])
            if isinstance(cons, list):
                for c in cons:
                    st.markdown(f"- {c}")
            else:
                st.write(cons)
        with st.expander("💓 Emotional Gut-Check", expanded=False):
            st.write(result.get("emotional_read", "-"))
        with st.expander("🦉 Wisdom Lens", expanded=False):
            st.write(result.get("wisdom", "-"))
        with st.expander("🎯 Recommendation", expanded=True):
            st.write(f"{result.get('recommendation', '-')}")
            st.write(f"**Confidence:** {result.get('confidence_percent', '-')}%")
        # Log the session
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "dilemma": dilemma,
            "tone": tone,
            "result": result,
            "email": email
        }
        log_decision(log_entry)
        # Email feature
        if email and SENDGRID_API_KEY and SENDGRID_FROM_EMAIL:
            subject = f"Your Daily Decision Coach Result: {dilemma[:40]}..."
            body = f"Decision: {dilemma}\n\nTone: {tone}\n\n" \
                f"Decision Clarity: {result.get('clarified_decision', '-')}\n" \
                f"Pros: {result.get('pros', '-')}\n" \
                f"Cons: {result.get('cons', '-')}\n" \
                f"Emotional Gut-Check: {result.get('emotional_read', '-')}\n" \
                f"Wisdom Lens: {result.get('wisdom', '-')}\n" \
                f"Recommendation: {result.get('recommendation', '-')}\n" \
                f"Confidence: {result.get('confidence_percent', '-')}%\n"
            sent, err = send_email(email, subject, body)
            if sent:
                st.success("✅ Emailed your decision summary!")
            else:
                st.error(f"Email failed: {err}. Please check your SendGrid API key and sender email.")

st.markdown("---")
st.caption("Your choices matter. This tool is for reflection, not medical or legal advice.")
# Optionally: show last 3 decisions
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        logs = json.load(f)
    if logs:
        st.markdown("#### Recent Decisions")
        for entry in logs[-3:][::-1]:
            st.write(f"**{entry['dilemma']}**")
            st.write(f"→ {entry['result'].get('recommendation', '-')}")
            st.write(f"_{entry['timestamp']}_")
            st.markdown("---") 