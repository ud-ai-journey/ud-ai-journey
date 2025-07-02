import streamlit as st
import requests
import json
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from collections import Counter
import matplotlib.pyplot as plt

try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
# Define Gemini API URL immediately after loading model
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Add Groq API support
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = "llama-3-70b-8192"
GROQ_API_URL = "https://api.x.ai/v1/chat/completions"

# Tone options
TONE_OPTIONS = {
    "Gentle": "Keep your language warm, gentle, and supportive.",
    "Direct": "Be concise, clear, and direct in your advice.",
    "Humorous": "Add a light, humorous touch to your advice, but keep it respectful."
}

# Supported languages for multilingual mode
LANGUAGES = [
    ("English", "en"),
    ("Hindi", "hi"),
    ("Telugu", "te"),
    ("Spanish", "es"),
    ("French", "fr"),
    ("German", "de"),
    ("Chinese", "zh"),
    ("Japanese", "ja"),
    ("Tamil", "ta"),
    ("Kannada", "kn"),
]

# Helper: Translate text using Gemini
TRANSLATE_PROMPT = """
Translate the following text to {target_language} (use natural, conversational style):

{text}
"""
def gemini_translate(text, target_language_code):
    if target_language_code == "en":
        return text
    prompt = TRANSLATE_PROMPT.format(target_language=target_language_code, text=text)
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY}
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        translated = result["candidates"][0]["content"]["parts"][0]["text"]
        return translated.strip()
    except Exception as e:
        return text + f" (Translation error: {e})"

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
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        try:
            parsed = json.loads(text)
            return parsed
        except Exception:
            import re
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                return {"error": "Could not parse Gemini response."}
    except Exception as e:
        return {"error": str(e)}

# Helper: Query Groq API (OpenAI-compatible)
def query_groq(messages, model=GROQ_MODEL, temperature=0.7):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI Error: {e}"

# Unified AI query function
def query_ai(dilemma, tone, provider, translate_to=None):
    if provider == "Gemini":
        return query_gemini(dilemma, tone)
    elif provider == "Groq":
        # Compose system prompt
        system_prompt = (
            "You are a compassionate decision coach. The user is stuck on a small but stressful choice. "
            "Help them decide using these steps: 1. Clarify the decision 2. Analyze pros & cons 3. Check emotional alignment "
            "4. Offer a wisdom-based reflection 5. Suggest a next step (with a confidence score). "
            f"Tone: {TONE_OPTIONS[tone]}\n"
            "Respond ONLY with a valid JSON object, and nothing else. "
            "Format your response as JSON with these keys: clarified_decision, pros, cons, emotional_read, wisdom, recommendation, confidence_percent.\n"
        )
        user_prompt = f"User's dilemma: {dilemma}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = query_groq(messages)
        try:
            parsed = json.loads(response)
            return parsed
        except Exception:
            import re
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                return {"error": f"Could not parse Groq response. Raw output: {response}"}
    else:
        return {"error": "Unknown AI provider."}

# Helper: Translate text using selected provider
def ai_translate(text, target_language_code, provider):
    if target_language_code == "en":
        return text
    if provider == "Gemini":
        return gemini_translate(text, target_language_code)
    elif provider == "Groq":
        prompt = f"Translate the following text to {target_language_code} (use natural, conversational style):\n\n{text}"
        messages = [
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ]
        response = query_groq(messages, temperature=0)
        return response.strip()
    else:
        return text

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

# Helper: Safely convert result fields to string for logging/email
def field_to_str(val):
    if isinstance(val, list):
        return '\n'.join(str(v) for v in val)
    return str(val)

st.set_page_config(page_title="Decision Coach v2", page_icon="🧭")

# --- Tabs for Coach and Dashboard ---
tabs = st.tabs(["🧭 Decision Coach", "📊 Dashboard"])

with tabs[0]:
    st.title("🧭 Decision Coach v2 – Day 78")
    st.write("Describe your decision below. After you get your recommendation, you can add a calendar reminder to revisit your choice in 24 hours.")

    # AI provider selector
    provider = st.selectbox("Choose AI provider:", ["Gemini", "Groq"], index=0)
    # Language selector
    lang_names = [name for name, code in LANGUAGES]
    lang_choice = st.selectbox("Choose your language:", lang_names, index=0)
    lang_code = dict(LANGUAGES)[lang_choice]

    dilemma = st.text_area("What's your decision dilemma?", placeholder="Should I move to a new city for work?")
    tone = st.selectbox("Choose the tone of advice:", list(TONE_OPTIONS.keys()), index=0)
    email = st.text_input("(Optional) Email this to my future self:", placeholder="you@email.com")
    private_mode = st.checkbox("🔒 Private Session (don't log or email this decision)")

    if st.button("Coach Me!") and dilemma.strip():
        with st.spinner("Thinking deeply about your decision..."):
            # Translate dilemma to English if needed
            if lang_code != "en":
                dilemma_en = ai_translate(dilemma, "en", provider)
            else:
                dilemma_en = dilemma
            result = query_ai(dilemma_en, tone, provider)
        if "error" in result:
            st.error(f"AI Error: {result['error']}")
        else:
            if private_mode:
                st.info("Private Session: This decision will NOT be logged or emailed.")
            # Translate each field back to selected language if needed
            if lang_code != "en":
                for key in ["clarified_decision", "pros", "cons", "emotional_read", "wisdom", "recommendation"]:
                    val = result.get(key, "")
                    if isinstance(val, list):
                        result[key] = [ai_translate(v, lang_code, provider) for v in val]
                    else:
                        result[key] = ai_translate(val, lang_code, provider)
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

            # Feedback slider
            feedback = st.slider("Was this helpful?", 1, 5, 3, format="%d", help="1 = Not at all, 5 = Extremely helpful")
            if st.button("Submit Feedback"):
                st.success("Thank you for your feedback!")
                if not private_mode:
                    # Store feedback in the log as a separate entry
                    feedback_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "dilemma": dilemma,
                        "feedback": feedback,
                        "result": {k: field_to_str(v) for k, v in result.items()},
                        "language": lang_code,
                        "provider": provider
                    }
                    # Append feedback to log
                    try:
                        if os.path.exists(LOG_PATH):
                            with open(LOG_PATH, "r", encoding="utf-8") as f:
                                logs = json.load(f)
                        else:
                            logs = []
                        logs.append(feedback_entry)
                        with open(LOG_PATH, "w", encoding="utf-8") as f:
                            json.dump(logs, f, indent=2)
                    except Exception as e:
                        st.warning(f"Could not log feedback: {e}")

            # Log and email only if not private mode
            if not private_mode:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "dilemma": dilemma,
                    "tone": tone,
                    "result": {k: field_to_str(v) for k, v in result.items()},
                    "email": email,
                    "language": lang_code,
                    "provider": provider
                }
                log_decision(log_entry)
                if email and SENDGRID_API_KEY and SENDGRID_FROM_EMAIL:
                    subject = f"Your Daily Decision Coach Result: {dilemma[:40]}..."
                    body = (
                        f"Decision: {dilemma}\n\n"
                        f"Tone: {tone}\n"
                        f"Language: {lang_choice}\n"
                        f"Provider: {provider}\n\n"
                        f"Decision Clarity: {field_to_str(result.get('clarified_decision', '-'))}\n"
                        f"Pros: {field_to_str(result.get('pros', '-'))}\n"
                        f"Cons: {field_to_str(result.get('cons', '-'))}\n"
                        f"Emotional Gut-Check: {field_to_str(result.get('emotional_read', '-'))}\n"
                        f"Wisdom Lens: {field_to_str(result.get('wisdom', '-'))}\n"
                        f"Recommendation: {field_to_str(result.get('recommendation', '-'))}\n"
                        f"Confidence: {result.get('confidence_percent', '-')}%\n"
                    )
                    sent, err = send_email(email, subject, body)
                    if sent:
                        st.success("✅ Emailed your decision summary!")
                    else:
                        st.error(f"Email failed: {err}. Please check your SendGrid API key and sender email.")
            # Calendar reminder section
            if st.button("Add Reminder to Calendar"):
                event_title = "Revisit Your Decision"
                event_description = f"Reflect on your decision: {dilemma}"
                start_time = datetime.now() + timedelta(days=1)
                end_time = start_time + timedelta(hours=1)
                dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
                dtstart = start_time.strftime('%Y%m%dT%H%M%SZ')
                dtend = end_time.strftime('%Y%m%dT%H%M%SZ')
                ics_content = f"""BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTAMP:{dtstamp}\nDTSTART:{dtstart}\nDTEND:{dtend}\nSUMMARY:{event_title}\nDESCRIPTION:{event_description}\nEND:VEVENT\nEND:VCALENDAR"""
                st.download_button(
                    label="Download .ics Reminder",
                    data=ics_content,
                    file_name="revisit_decision.ics",
                    mime="text/calendar"
                )

    st.markdown("---")
    st.caption("Your choices matter. This tool is for reflection, not medical or legal advice.")
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

with tabs[1]:
    st.title("📊 Self-Insight Dashboard")
    st.write("See patterns and trends in your decision-making journey.")
    if not os.path.exists(LOG_PATH):
        st.info("No decisions logged yet.")
    else:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
        if not logs:
            st.info("No decisions logged yet.")
        else:
            # --- Memory Mode: User Patterns & Values ---
            with st.expander("🧠 Memory Mode: Your Decision Patterns", expanded=True):
                # Most common tone
                tones = [entry.get("tone", "-") for entry in logs]
                if tones:
                    most_common_tone = Counter(tones).most_common(1)[0][0]
                    st.write(f"**Your most used tone:** {most_common_tone}")
                # Top 3 dilemma themes (keywords)
                all_dilemmas = " ".join([entry.get("dilemma", "") for entry in logs])
                words = [w.lower() for w in all_dilemmas.split() if len(w) > 3]
                word_counts = Counter(words)
                top_themes = [w for w, _ in word_counts.most_common(3)]
                if top_themes:
                    st.write(f"**Your top themes:** {', '.join(top_themes)}")
                # Most frequent wisdom/reflection phrases
                wisdoms = [entry["result"].get("wisdom", "") for entry in logs if "result" in entry]
                wisdom_counts = Counter(wisdoms)
                top_wisdoms = [w for w, _ in wisdom_counts.most_common(3) if w.strip()]
                if top_wisdoms:
                    st.write("**Your most common wisdom reflections:**")
                    for w in top_wisdoms:
                        st.markdown(f"> {w}")
                # Confidence pattern
                confidences = [float(entry["result"].get("confidence_percent", 0)) for entry in logs if "result" in entry]
                if confidences:
                    avg_conf = sum(confidences) / len(confidences)
                    st.write(f"**Your average confidence in decisions:** {avg_conf:.1f}%")
                st.caption("Memory Mode helps you reflect on your own patterns and values over time.")

            # Most common tones
            tones = [entry.get("tone", "-") for entry in logs]
            tone_counts = Counter(tones)
            st.subheader("Most Common Tones")
            fig, ax = plt.subplots()
            ax.bar(list(tone_counts.keys()), list(tone_counts.values()), color=["#8ecae6", "#ffb703", "#219ebc"])
            ax.set_ylabel("Count")
            ax.set_xlabel("Tone")
            st.pyplot(fig)

            # Confidence level trends
            confidences = []
            timestamps = []
            for entry in logs:
                try:
                    conf = float(entry["result"].get("confidence_percent", 0))
                except Exception:
                    conf = 0
                confidences.append(conf)
                timestamps.append(entry.get("timestamp", ""))
            st.subheader("Confidence Level Trend")
            if confidences:
                fig2, ax2 = plt.subplots()
                ax2.plot(timestamps, confidences, marker="o")
                ax2.set_ylabel("Confidence (%)")
                ax2.set_xlabel("Decision # / Time")
                plt.xticks(rotation=45, ha='right', fontsize=8)
                st.pyplot(fig2)

            # Wordcloud of dilemma keywords
            st.subheader("Common Themes (Wordcloud)")
            all_dilemmas = " ".join([entry.get("dilemma", "") for entry in logs])
            if WORDCLOUD_AVAILABLE and all_dilemmas.strip():
                wc = WordCloud(width=600, height=300, background_color="white").generate(all_dilemmas)
                fig3, ax3 = plt.subplots()
                ax3.imshow(wc, interpolation="bilinear")
                ax3.axis("off")
                st.pyplot(fig3)
            else:
                st.write(">> Install `wordcloud` with `pip install wordcloud` for a visual wordcloud, or see keywords below:")
                words = all_dilemmas.lower().split()
                word_counts = Counter(words)
                st.write(dict(word_counts.most_common(10)))

            # Top 5 decisions with highest confidence
            st.subheader("Top 5 Most Confident Decisions")
            sorted_logs = sorted(logs, key=lambda x: float(x["result"].get("confidence_percent", 0)), reverse=True)
            for entry in sorted_logs[:5]:
                st.write(f"**{entry['dilemma']}**")
                st.write(f"Confidence: {entry['result'].get('confidence_percent', '-')}%")
                st.write(f"Recommendation: {entry['result'].get('recommendation', '-')}")
                st.markdown("---")

            # Show average feedback
            feedbacks = [entry.get("feedback") for entry in logs if "feedback" in entry]
            if feedbacks:
                avg_feedback = sum(feedbacks) / len(feedbacks)
                st.subheader(f"Average user feedback: {avg_feedback:.2f} / 5") 