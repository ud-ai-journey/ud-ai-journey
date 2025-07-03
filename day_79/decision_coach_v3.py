import streamlit as st
import requests
import json
import os
from datetime import datetime, timedelta, date
from collections import Counter
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import io
import csv

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = "llama-3-70b-8192"
GROQ_API_URL = "https://api.x.ai/v1/chat/completions"

# --- CONFIG ---
LOG_PATH = os.path.join(os.path.dirname(__file__), "decision_log.json")

# --- Value Meter Options ---
VALUE_OPTIONS = [
    "Freedom", "Growth", "Security", "Relationships", "Health", "Stability", "Creativity", "Impact"
]

# --- Emotion Tone Options ---
EMOTION_OPTIONS = [
    "Confident", "Anxious", "Excited", "Confused", "Overwhelmed"
]

# --- Tone options ---
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

def query_gemini(dilemma, tone, user_values, user_feeling):
    prompt = f'''
You are a compassionate decision coach. The user is stuck on a small but stressful choice. Help them decide using these steps:
1. Clarify the decision
2. Analyze pros & cons
3. Check emotional alignment
4. Offer a wisdom-based reflection
5. Suggest a next step (with a confidence score)

Tone: {TONE_OPTIONS[tone]}
User values involved: {', '.join(user_values) if user_values else 'None'}
Based on the user's language, infer their emotional tone (e.g., anxious, hopeful, overwhelmed, confident). User self-reports feeling: {user_feeling}.

Format your response as JSON with these keys: clarified_decision, pros, cons, emotional_read, wisdom, recommendation, confidence_percent, emotional_tone.

User's dilemma: {dilemma}
'''
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY}
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

def query_ai(dilemma, tone, provider, user_values, user_feeling):
    if provider == "Gemini":
        return query_gemini(dilemma, tone, user_values, user_feeling)
    elif provider == "Groq":
        system_prompt = (
            "You are a compassionate decision coach. The user is stuck on a small but stressful choice. "
            "Help them decide using these steps: 1. Clarify the decision 2. Analyze pros & cons 3. Check emotional alignment "
            "4. Offer a wisdom-based reflection 5. Suggest a next step (with a confidence score). "
            f"Tone: {TONE_OPTIONS[tone]}\n"
            f"User values involved: {', '.join(user_values) if user_values else 'None'}\n"
            "Based on the user's language, infer their emotional tone (e.g., anxious, hopeful, overwhelmed, confident). "
            f"User self-reports feeling: {user_feeling}.\n"
            "Respond ONLY with a valid JSON object, and nothing else. "
            "Format your response as JSON with these keys: clarified_decision, pros, cons, emotional_read, wisdom, recommendation, confidence_percent, emotional_tone.\n"
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

def field_to_str(val):
    if isinstance(val, list):
        return '\n'.join(str(v) for v in val)
    return str(val)

st.set_page_config(page_title="Decision Coach v3", page_icon="🧠")

st.markdown(f"**Streamlit version:** {st.__version__}")

tabs = st.tabs(["🧠 Decision Coach V3", "📊 Dashboard"])

with tabs[0]:
    st.title("🧠 Decision Coach V3 – Day 79")
    st.write("Describe your decision below. Now with Value Meter, Emotion Tone, and 7-Day Follow-up!")

    provider = st.selectbox("Choose AI provider:", ["Gemini", "Groq"], index=0)
    lang_names = [name for name, code in LANGUAGES]
    lang_choice = st.selectbox("Choose your language:", lang_names, index=0)
    lang_code = dict(LANGUAGES)[lang_choice]

    dilemma = st.text_area("What's your decision dilemma?", placeholder="Should I move to a new team?")
    tone = st.selectbox("Choose the tone of advice:", list(TONE_OPTIONS.keys()), index=0)
    user_values = st.multiselect(
        "What values does this decision affect?",
        VALUE_OPTIONS,
        key="values"
    )
    user_feeling = st.selectbox(
        "How are you feeling about this decision?",
        EMOTION_OPTIONS,
        key="user_feeling"
    )
    email = st.text_input("(Optional) Email this to my future self:", placeholder="you@email.com")
    private_mode = st.checkbox("🔒 Private Session (don't log or email this decision)")

    if st.button("Coach Me!") and dilemma.strip():
        with st.spinner("Thinking deeply about your decision..."):
            # Translate dilemma to English if needed
            if lang_code != "en":
                dilemma_en = ai_translate(dilemma, "en", provider)
            else:
                dilemma_en = dilemma
            result = query_ai(dilemma_en, tone, provider, user_values, user_feeling)
        if "error" in result:
            st.error(f"AI Error: {result['error']}")
        else:
            if private_mode:
                st.info("Private Session: This decision will NOT be logged or emailed.")
            # Translate each field back to selected language if needed
            if lang_code != "en":
                # pros and cons are lists, others are strings
                for key in ["pros", "cons"]:
                    val = result.get(key, "")
                    if isinstance(val, list):
                        result[key] = [ai_translate(str(v), lang_code, provider) for v in val]
                for key in ["clarified_decision", "emotional_read", "wisdom", "recommendation"]:
                    val = result.get(key, "")
                    if isinstance(val, str):
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

        # Log and email only if not private mode
        followup_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        if not private_mode:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "dilemma": dilemma,
                "tone": tone,
                "values": user_values,
                "emotional_tone": user_feeling,
                "result": {k: field_to_str(v) for k, v in result.items()},
                "followup_date": followup_date,
                "email": email,
                "language": lang_code,
                "provider": provider
            }
            log_decision(log_entry)
        # 7-day calendar reminder
        if st.button("Add 7-Day Reflection Reminder to Calendar"):
            event_title = f"Reflect on: {dilemma[:40]}..."
            event_description = (
                f"How do you feel now about this decision?\nWould you still make it today?\n\n"
                f"What has changed since you made this decision? Do you feel aligned with your values?"
            )
            start_time = datetime.now() + timedelta(days=7)
            end_time = start_time + timedelta(hours=1)
            dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
            dtstart = start_time.strftime('%Y%m%dT%H%M%SZ')
            dtend = end_time.strftime('%Y%m%dT%H%M%SZ')
            ics_content = f"""BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTAMP:{dtstamp}\nDTSTART:{dtstart}\nDTEND:{dtend}\nSUMMARY:{event_title}\nDESCRIPTION:{event_description}\nEND:VEVENT\nEND:VCALENDAR"""
            st.download_button(
                label="Download 7-Day .ics Reminder",
                data=ics_content,
                file_name="reflect_decision_7days.ics",
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
                st.write(f"→ {entry.get('result', {}).get('recommendation', '-')}")
                st.write(f"_{entry['timestamp']}_")
                st.markdown("---")

with tabs[1]:
    # Two-stage rerun: if force_rerun is set, clear and rerun again
    if st.session_state.get('force_rerun'):
        st.session_state['force_rerun'] = False
        st.rerun()
    st.title("📊 Self-Insight Dashboard")
    st.write("See patterns and trends in your decision-making journey.")
    # Always reload the log from disk at the start of the dashboard
    if not os.path.exists(LOG_PATH):
        st.info("No decisions logged yet.")
        logs = []
    else:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    if not logs:
        st.info("No decisions logged yet.")
    else:
        # --- Value Trends Table ---
        all_values = [v for entry in logs for v in entry.get("values", [])]
        value_counts = Counter(all_values)
        if value_counts:
            st.markdown("#### Value Trends (Top 5)")
            st.table({"Value": list(value_counts.keys())[:5], "Frequency": list(value_counts.values())[:5]})

        # --- Decision Reflection Journal ---
        st.markdown("### 📝 Decision Reflection Journal")
        for idx, entry in enumerate(logs[::-1]):
            with st.expander(f"{entry.get('dilemma', 'No dilemma')} ({entry.get('timestamp', '')[:10]})", expanded=False):
                st.write(f"**Values:** {', '.join(entry.get('values', []))}")
                st.write(f"**Recommendation:** {entry.get('result', {}).get('recommendation', '-')}")
                st.write(f"**Original Feeling:** {entry.get('emotional_tone', '-')}")
                st.write(f"**Follow-up Date:** {entry.get('followup_date', '-')}")
                reflection_key = f"reflection_{idx}"
                current_reflection = entry.get('reflection', '')
                reflection = st.text_area("How do you feel about this decision now? Did the outcome align with your values? What would you do differently?", value=current_reflection, key=reflection_key)
                ai_feedback = entry.get('ai_feedback', '')
                if st.button("Save Reflection", key=f"save_{idx}"):
                    # Update the log entry and save
                    logs_index = len(logs) - 1 - idx  # Because we reversed
                    logs[logs_index]['reflection'] = reflection
                    with open(LOG_PATH, "w", encoding="utf-8") as f:
                        json.dump(logs, f, indent=2)
                    st.success("Reflection saved!")
                # --- AI Feedback on Reflection ---
                if reflection.strip():
                    if st.button("Get AI Feedback on My Reflection", key=f"ai_feedback_{idx}"):
                        dilemma = entry.get('dilemma', '')
                        values = entry.get('values', [])
                        recommendation = entry.get('result', {}).get('recommendation', '-')
                        user_feeling = entry.get('emotional_tone', '-')
                        prompt = f"""
You are a supportive self-growth coach. Here is the user's original dilemma, their values, the decision made, and their reflection. Give a supportive, growth-oriented response. If possible, suggest one thing to consider for next time.\n\nDilemma: {dilemma}\nValues: {', '.join(values)}\nRecommendation: {recommendation}\nOriginal Feeling: {user_feeling}\nReflection: {reflection}\n"""
                        # Use Gemini by default for feedback
                        data = {"contents": [{"parts": [{"text": prompt}]}]}
                        headers = {"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY}
                        try:
                            response = requests.post(GEMINI_API_URL, headers=headers, json=data)
                            response.raise_for_status()
                            result = response.json()
                            feedback_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                        except Exception as e:
                            feedback_text = f"AI Error: {e}"
                        logs_index = len(logs) - 1 - idx
                        logs[logs_index]['ai_feedback'] = feedback_text
                        with open(LOG_PATH, "w", encoding="utf-8") as f:
                            json.dump(logs, f, indent=2)
                        st.success("AI feedback saved!")
                        ai_feedback = feedback_text
                    if ai_feedback:
                        st.markdown(f"**AI Feedback:**\n> {ai_feedback}")
                # --- Reflection Reminder ---
                if not entry.get('reflection_reminder_set'):
                    if st.button("Set Reflection Reminder", key=f"reminder_{idx}"):
                        dilemma = entry.get('dilemma', '')
                        followup_date = entry.get('followup_date')
                        if followup_date:
                            try:
                                start_time = datetime.strptime(followup_date, "%Y-%m-%d") + timedelta(days=7)
                            except Exception:
                                start_time = datetime.now() + timedelta(days=7)
                        else:
                            start_time = datetime.now() + timedelta(days=7)
                        end_time = start_time + timedelta(hours=1)
                        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
                        dtstart = start_time.strftime('%Y%m%dT%H%M%SZ')
                        dtend = end_time.strftime('%Y%m%dT%H%M%SZ')
                        event_title = f"Reflect on: {dilemma[:40]}..."
                        event_description = f"Take a moment to reflect on your decision: {dilemma}"
                        ics_content = f"""BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTAMP:{dtstamp}\nDTSTART:{dtstart}\nDTEND:{dtend}\nSUMMARY:{event_title}\nDESCRIPTION:{event_description}\nEND:VEVENT\nEND:VCALENDAR"""
                        st.download_button(
                            label="Download Reflection .ics Reminder",
                            data=ics_content,
                            file_name="reflection_reminder.ics",
                            mime="text/calendar",
                            key=f"ics_{idx}"
                        )
                        logs_index = len(logs) - 1 - idx
                        logs[logs_index]['reflection_reminder_set'] = True
                        with open(LOG_PATH, "w", encoding="utf-8") as f:
                            json.dump(logs, f, indent=2)
                        st.success("Reflection reminder set!")

        # --- Reflection Analytics ---
        st.markdown("### 📈 Reflection Analytics")
        num_with_reflection = sum(1 for entry in logs if entry.get('reflection'))
        st.write(f"**Decisions with reflections:** {num_with_reflection} / {len(logs)}")
        num_with_ai_feedback = sum(1 for entry in logs if entry.get('ai_feedback'))
        st.write(f"**Reflections with AI feedback:** {num_with_ai_feedback} / {num_with_reflection if num_with_reflection else 1}")
        # Helper to safely check for non-empty strings
        def is_nonempty_str(val):
            return isinstance(val, str) and val.strip() != ''
        all_reflections = " ".join([entry.get('reflection', '') for entry in logs if is_nonempty_str(entry.get('reflection', ''))])
        all_ai_feedback = " ".join([entry.get('ai_feedback', '') for entry in logs if is_nonempty_str(entry.get('ai_feedback', ''))])
        if all_reflections:
            try:
                from wordcloud import WordCloud
                wc = WordCloud(width=600, height=300, background_color="white").generate(all_reflections)
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            except ImportError:
                st.write(">> Install `wordcloud` for a visual wordcloud of your reflections.")
            words = all_reflections.lower().split()
            word_counts = Counter(words)
            st.write("**Most common words in reflections:**")
            st.write(dict(word_counts.most_common(10)))
        if all_ai_feedback:
            st.markdown("#### AI Feedback Wordcloud")
            try:
                from wordcloud import WordCloud
                wc = WordCloud(width=600, height=300, background_color="white").generate(all_ai_feedback)
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            except ImportError:
                st.write(">> Install `wordcloud` for a visual wordcloud of your AI feedback.")
            words = all_ai_feedback.lower().split()
            word_counts = Counter(words)
            st.write("**Most common words in AI feedback:**")
            st.write(dict(word_counts.most_common(10)))

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
        try:
            from wordcloud import WordCloud
            WORDCLOUD_AVAILABLE = True
        except ImportError:
            WORDCLOUD_AVAILABLE = False
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

        # --- Streaks & Consistency Tracker ---
        st.markdown("### 🔥 Streaks & Consistency Tracker")
        # Gather all unique dates with a decision or reflection
        activity_dates = set()
        for entry in logs:
            ts = entry.get('timestamp', '')
            if ts:
                try:
                    d = datetime.fromisoformat(ts).date()
                    activity_dates.add(d)
                except Exception:
                    pass
            # If reflection exists, also count its save date (if different)
            if entry.get('reflection') and entry.get('reflection') != '':
                # For simplicity, use timestamp as reflection date
                if ts:
                    try:
                        d = datetime.fromisoformat(ts).date()
                        activity_dates.add(d)
                    except Exception:
                        pass
        if activity_dates:
            all_dates = sorted(activity_dates)
            # Calculate streaks
            streak = 0
            longest_streak = 0
            prev_day = None
            current_streak = 0
            today = date.today()
            for d in all_dates:
                if prev_day is None:
                    current_streak = 1
                elif (d - prev_day).days == 1:
                    current_streak += 1
                else:
                    current_streak = 1
                if current_streak > longest_streak:
                    longest_streak = current_streak
                prev_day = d
            # Check if streak is current (ends today)
            if all_dates and (today - all_dates[-1]).days == 0:
                streak = current_streak
            else:
                streak = 0
            st.write(f"**Current Streak:** {streak} day{'s' if streak != 1 else ''}")
            st.write(f"**Longest Streak:** {longest_streak} day{'s' if longest_streak != 1 else ''}")
            # Motivational message
            if streak >= 3:
                st.success(f"🔥 You're on a {streak}-day streak! Keep it up!")
            elif streak == 2:
                st.info("Nice! Two days in a row. Can you make it three?")
            elif streak == 1:
                st.info("You started a new streak today! 🎉")
            else:
                st.warning("No current streak. Start today to build your self-growth habit!")
            # Calendar heatmap (simple matplotlib grid)
            st.markdown("#### Activity Calendar")
            # Build a month grid for the current month
            first_day = today.replace(day=1)
            last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)) if first_day.month != 12 else date(today.year, 12, 31)
            days_in_month = (last_day - first_day).days + 1
            month_days = [first_day + timedelta(days=i) for i in range(days_in_month)]
            activity_map = np.array([1 if d in activity_dates else 0 for d in month_days])
            fig, ax = plt.subplots(figsize=(8, 1))
            ax.imshow(activity_map[np.newaxis, :], cmap="Greens", aspect="auto")
            ax.set_yticks([])
            ax.set_xticks(range(days_in_month))
            ax.set_xticklabels([str(d.day) for d in month_days], fontsize=8)
            for spine in ax.spines.values():
                spine.set_visible(False)
            st.pyplot(fig)
        else:
            st.info("No activity yet. Log a decision or reflection to start your streak!")

        # --- Action Plan & Progress Tracker ---
        st.markdown("### 🏁 Action Plan & Progress Tracker")
        for idx, entry in enumerate(logs[::-1]):
            with st.expander(f"Action Plan: {entry.get('dilemma', 'No dilemma')} ({entry.get('timestamp', '')[:10]})", expanded=False):
                # Load or initialize action steps
                logs_index = len(logs) - 1 - idx
                action_plan = entry.get('action_plan', [])
                if not action_plan:
                    action_plan = []
                # Add new step
                new_step = st.text_input("Add a new action step:", key=f"new_step_{idx}")
                new_date = st.date_input("Target date (optional):", value=None, key=f"new_date_{idx}")
                if st.button("Add Step", key=f"add_step_{idx}"):
                    if new_step.strip():
                        action_plan.append({
                            'description': new_step.strip(),
                            'done': False,
                            'target_date': str(new_date) if new_date else ''
                        })
                        logs[logs_index]['action_plan'] = action_plan
                        with open(LOG_PATH, "w", encoding="utf-8") as f:
                            json.dump(logs, f, indent=2)
                        st.success("Step added!")
                # Show checklist
                completed = 0
                all_done = all(step['done'] for step in action_plan) if action_plan else False
                prev_all_done_key = f"prev_all_done_{idx}"
                if prev_all_done_key not in st.session_state:
                    st.session_state[prev_all_done_key] = all_done
                for step_idx, step in enumerate(action_plan):
                    col1, col2 = st.columns([0.08, 0.92])
                    with col1:
                        checked = st.checkbox("Mark step as done", value=step['done'], key=f"step_done_{idx}_{step_idx}", label_visibility="collapsed")
                    with col2:
                        st.write(f"{step['description']}" + (f" _(by {step['target_date']})_" if step['target_date'] else ""))
                    if checked != step['done']:
                        action_plan[step_idx]['done'] = checked
                        logs[logs_index]['action_plan'] = action_plan
                        with open(LOG_PATH, "w", encoding="utf-8") as f:
                            json.dump(logs, f, indent=2)
                completed = sum(step['done'] for step in action_plan)
                all_done = all(step['done'] for step in action_plan) if action_plan else False
                if action_plan:
                    st.progress(completed / len(action_plan))
                    st.write(f"**{completed}/{len(action_plan)} steps completed!**")
                    # Only trigger balloons on transition from not all done to all done
                    if not st.session_state[prev_all_done_key] and all_done:
                        st.balloons()
                        st.success("Congratulations! You completed all your action steps for this decision.")
                        st.session_state['force_rerun'] = True
                        st.rerun()
                    st.session_state[prev_all_done_key] = all_done
                else:
                    st.info("No action steps yet. Add one above!")

        # --- Action Plan Analytics ---
        st.markdown("### 📊 Action Plan Analytics")
        total_decisions = len(logs)
        with_action = sum(1 for entry in logs if entry.get('action_plan'))
        all_steps = [step for entry in logs for step in entry.get('action_plan', [])]
        completed_steps = [step for step in all_steps if step.get('done')]
        st.write(f"**Decisions with action plans:** {with_action} / {total_decisions}")
        st.write(f"**Total action steps:** {len(all_steps)}")
        st.write(f"**Completed steps:** {len(completed_steps)}")
        if all_steps:
            st.write(f"**Average steps per decision:** {len(all_steps)/total_decisions:.2f}")
            st.write(f"**% of steps completed:** {100*len(completed_steps)/len(all_steps):.1f}%")

        # --- Personalized Insights & AI Trends Coach ---
        st.markdown("### 🤖 Personalized Insights & AI Trends Coach")
        if st.button("Get My Insights", key="get_insights"):
            # Summarize the log for AI
            log_summary = []
            for entry in logs:
                log_summary.append({
                    'timestamp': entry.get('timestamp', ''),
                    'dilemma': entry.get('dilemma', ''),
                    'values': entry.get('values', []),
                    'emotional_tone': entry.get('emotional_tone', ''),
                    'reflection': entry.get('reflection', ''),
                    'action_plan': entry.get('action_plan', []),
                    'result': entry.get('result', {}),
                })
            prompt = f"""
You are a personal growth coach. Here is a summary of the user's decision log, including dilemmas, values, emotions, reflections, and action plans. Analyze the data and provide:
- 3-5 personalized insights about their decision patterns, values, and emotional trends
- 1-3 growth suggestions or new habits to try
- Highlight any positive changes or areas for improvement

User Log Summary (JSON):
{json.dumps(log_summary, indent=2)}
"""
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            headers = {"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY}
            try:
                response = requests.post(GEMINI_API_URL, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                insights_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception as e:
                insights_text = f"AI Error: {e}"
            # Save insights in a separate insights log
            insights_log_path = os.path.join(os.path.dirname(__file__), "insights_log.json")
            if os.path.exists(insights_log_path):
                with open(insights_log_path, "r", encoding="utf-8") as f:
                    insights_log = json.load(f)
            else:
                insights_log = []
            insights_entry = {
                "timestamp": datetime.now().isoformat(),
                "insights": insights_text
            }
            insights_log.append(insights_entry)
            with open(insights_log_path, "w", encoding="utf-8") as f:
                json.dump(insights_log, f, indent=2)
            st.success("AI insights generated and saved!")
            st.markdown(f"**Your Personalized Insights:**\n\n{insights_text}")
        # Show timeline of past insights
        insights_log_path = os.path.join(os.path.dirname(__file__), "insights_log.json")
        if os.path.exists(insights_log_path):
            with open(insights_log_path, "r", encoding="utf-8") as f:
                insights_log = json.load(f)
            if insights_log:
                st.markdown("#### 🕒 Insights Timeline")
                for entry in insights_log[::-1]:
                    st.write(f"_{entry['timestamp']}_")
                    st.markdown(entry['insights'])
                    st.markdown("---")

        # --- Accountability Partner & Sharing ---
        st.markdown("### 🤝 Accountability Partner & Sharing")
        # Set or update accountability partner email
        partner_email_path = os.path.join(os.path.dirname(__file__), "partner_email.json")
        if os.path.exists(partner_email_path):
            with open(partner_email_path, "r", encoding="utf-8") as f:
                partner_email_data = json.load(f)
            default_partner_email = partner_email_data.get("email", "")
        else:
            default_partner_email = ""
        partner_email = st.text_input("Accountability Partner Email:", value=default_partner_email, key="partner_email")
        if st.button("Save Partner Email"):
            with open(partner_email_path, "w", encoding="utf-8") as f:
                json.dump({"email": partner_email}, f)
            st.success("Partner email saved!")
        # Share each decision
        shared_count = 0
        for idx, entry in enumerate(logs[::-1]):
            with st.expander(f"Share: {entry.get('dilemma', 'No dilemma')} ({entry.get('timestamp', '')[:10]})", expanded=False):
                share_options = st.multiselect(
                    "What would you like to share?",
                    ["Dilemma", "Action Plan", "Reflection"],
                    default=["Dilemma"],
                    key=f"share_opts_{idx}"
                )
                if st.button("Share with Partner", key=f"share_btn_{idx}"):
                    if not partner_email:
                        st.error("Please set your partner's email first.")
                    elif not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
                        st.error("SendGrid API key or sender email not set in environment.")
                    else:
                        subject = f"Decision Coach Update: {entry.get('dilemma', '')[:40]}..."
                        body = ""
                        if "Dilemma" in share_options:
                            body += f"Dilemma: {entry.get('dilemma', '')}\nValues: {', '.join(entry.get('values', []))}\nRecommendation: {entry.get('result', {}).get('recommendation', '-')}\n\n"
                        if "Action Plan" in share_options and entry.get('action_plan'):
                            body += "Action Plan:\n"
                            for step in entry['action_plan']:
                                status = "[x]" if step.get('done') else "[ ]"
                                body += f"{status} {step.get('description', '')} (by {step.get('target_date', '')})\n"
                            body += "\n"
                        if "Reflection" in share_options and entry.get('reflection'):
                            body += f"Reflection: {entry.get('reflection', '')}\n\n"
                        # Send email
                        import smtplib
                        from email.mime.text import MIMEText
                        from email.mime.multipart import MIMEMultipart
                        msg = MIMEMultipart()
                        msg["From"] = SENDGRID_FROM_EMAIL or ""
                        msg["To"] = partner_email
                        msg["Subject"] = subject
                        msg.attach(MIMEText(body, "plain"))
                        try:
                            smtp_server = "smtp.sendgrid.net"
                            smtp_port = 587
                            username = "apikey"
                            password = SENDGRID_API_KEY or ""
                            with smtplib.SMTP(smtp_server, smtp_port) as server:
                                server.starttls()
                                server.login(username, password)
                                server.sendmail(SENDGRID_FROM_EMAIL or "", partner_email, msg.as_string())
                            st.success("Shared with your accountability partner!")
                            # Mark as shared
                            logs_index = len(logs) - 1 - idx
                            logs[logs_index]['shared_with_partner'] = True
                            with open(LOG_PATH, "w", encoding="utf-8") as f:
                                json.dump(logs, f, indent=2)
                            shared_count += 1
                        except Exception as e:
                            st.error(f"Email failed: {e}")
                # Log/display partner feedback
                partner_feedback = entry.get('partner_feedback', '')
                feedback = st.text_area("Log partner's feedback (if received):", value=partner_feedback, key=f"partner_feedback_{idx}")
                if st.button("Save Partner Feedback", key=f"save_feedback_{idx}"):
                    logs_index = len(logs) - 1 - idx
                    logs[logs_index]['partner_feedback'] = feedback
                    with open(LOG_PATH, "w", encoding="utf-8") as f:
                        json.dump(logs, f, indent=2)
                    st.success("Partner feedback saved!")
                if partner_feedback:
                    st.markdown(f"**Partner Feedback:**\n> {partner_feedback}")
        # Analytics
        st.markdown("### 📊 Accountability Analytics")
        total_shared = sum(1 for entry in logs if entry.get('shared_with_partner'))
        total_feedback = sum(1 for entry in logs if entry.get('partner_feedback'))
        st.write(f"**Decisions shared with partner:** {total_shared} / {len(logs)}")
        st.write(f"**Decisions with partner feedback:** {total_feedback} / {len(logs)}")

        # --- Smart Reminders & Nudges ---
        st.markdown("### ⏰ Smart Reminders & Nudges")
        # Opt-in and frequency
        reminders_path = os.path.join(os.path.dirname(__file__), "reminders.json")
        if os.path.exists(reminders_path):
            with open(reminders_path, "r", encoding="utf-8") as f:
                reminders_data = json.load(f)
        else:
            reminders_data = {"opt_in": False, "frequency": "Weekly", "reminders": []}
        opt_in = st.checkbox("Opt-in to email reminders for action steps and reflections", value=reminders_data.get("opt_in", False), key="reminder_optin")
        frequency = st.selectbox("Reminder frequency:", ["Daily", "Weekly", "Custom"], index=["Daily", "Weekly", "Custom"].index(reminders_data.get("frequency", "Weekly")), key="reminder_freq")
        if st.button("Save Reminder Settings"):
            reminders_data["opt_in"] = opt_in
            reminders_data["frequency"] = frequency
            with open(reminders_path, "w", encoding="utf-8") as f:
                json.dump(reminders_data, f, indent=2)
            st.success("Reminder settings saved!")
        # Schedule reminders for action steps
        if opt_in and SENDGRID_API_KEY and SENDGRID_FROM_EMAIL:
            for idx, entry in enumerate(logs[::-1]):
                logs_index = len(logs) - 1 - idx
                action_plan = entry.get('action_plan', [])
                for step_idx, step in enumerate(action_plan):
                    if step.get('target_date') and not step.get('reminder_sent'):
                        if st.button(f"Schedule Reminder for Step: {step['description']} (Due {step['target_date']})", key=f"reminder_step_{idx}_{step_idx}"):
                            # Send email reminder
                            user_email = entry.get('email', '')
                            if not user_email:
                                st.error("No user email set for this decision. Add your email to receive reminders.")
                            else:
                                subject = f"Action Step Reminder: {step['description']}"
                                body = f"This is a reminder to complete your action step: {step['description']} (Due {step['target_date']}) for your decision: {entry.get('dilemma', '')}"
                                import smtplib
                                from email.mime.text import MIMEText
                                from email.mime.multipart import MIMEMultipart
                                msg = MIMEMultipart()
                                msg["From"] = SENDGRID_FROM_EMAIL or ""
                                msg["To"] = user_email
                                msg["Subject"] = subject
                                msg.attach(MIMEText(body, "plain"))
                                try:
                                    smtp_server = "smtp.sendgrid.net"
                                    smtp_port = 587
                                    username = "apikey"
                                    password = SENDGRID_API_KEY or ""
                                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                                        server.starttls()
                                        server.login(username, password)
                                        server.sendmail(SENDGRID_FROM_EMAIL or "", user_email, msg.as_string())
                                    st.success("Reminder email sent!")
                                    # Mark as sent
                                    logs[logs_index]['action_plan'][step_idx]['reminder_sent'] = True
                                    with open(LOG_PATH, "w", encoding="utf-8") as f:
                                        json.dump(logs, f, indent=2)
                                    # Save to reminders log
                                    reminders_data.setdefault("reminders", []).append({
                                        "type": "action_step",
                                        "description": step['description'],
                                        "date": step['target_date'],
                                        "decision": entry.get('dilemma', ''),
                                        "sent": True
                                    })
                                    with open(reminders_path, "w", encoding="utf-8") as f:
                                        json.dump(reminders_data, f, indent=2)
                                    # Reload reminders_data after saving
                                    with open(reminders_path, "r", encoding="utf-8") as f:
                                        reminders_data = json.load(f)
                                except Exception as e:
                                    st.error(f"Email failed: {e}")
        # Schedule reflection reminders
        if opt_in and SENDGRID_API_KEY and SENDGRID_FROM_EMAIL:
            for idx, entry in enumerate(logs[::-1]):
                logs_index = len(logs) - 1 - idx
                if not entry.get('reflection_reminder_sent'):
                    if st.button(f"Schedule Reflection Reminder for: {entry.get('dilemma', '')}", key=f"reminder_reflect_{idx}"):
                        user_email = entry.get('email', '')
                        if not user_email:
                            st.error("No user email set for this decision. Add your email to receive reminders.")
                        else:
                            subject = f"Reflection Reminder: {entry.get('dilemma', '')[:40]}..."
                            body = f"This is a reminder to reflect on your decision: {entry.get('dilemma', '')}"
                            import smtplib
                            from email.mime.text import MIMEText
                            from email.mime.multipart import MIMEMultipart
                            msg = MIMEMultipart()
                            msg["From"] = SENDGRID_FROM_EMAIL or ""
                            msg["To"] = user_email
                            msg["Subject"] = subject
                            msg.attach(MIMEText(body, "plain"))
                            try:
                                smtp_server = "smtp.sendgrid.net"
                                smtp_port = 587
                                username = "apikey"
                                password = SENDGRID_API_KEY or ""
                                with smtplib.SMTP(smtp_server, smtp_port) as server:
                                    server.starttls()
                                    server.login(username, password)
                                    server.sendmail(SENDGRID_FROM_EMAIL or "", user_email, msg.as_string())
                                st.success("Reflection reminder email sent!")
                                logs[logs_index]['reflection_reminder_sent'] = True
                                with open(LOG_PATH, "w", encoding="utf-8") as f:
                                    json.dump(logs, f, indent=2)
                                reminders_data.setdefault("reminders", []).append({
                                    "type": "reflection",
                                    "description": entry.get('dilemma', ''),
                                    "date": entry.get('followup_date', ''),
                                    "decision": entry.get('dilemma', ''),
                                    "sent": True
                                })
                                with open(reminders_path, "w", encoding="utf-8") as f:
                                    json.dump(reminders_data, f, indent=2)
                                # Reload reminders_data after saving
                                with open(reminders_path, "r", encoding="utf-8") as f:
                                    reminders_data = json.load(f)
                            except Exception as e:
                                st.error(f"Email failed: {e}")
        # Show upcoming/past reminders
        st.markdown("#### 📅 Reminder Dashboard")
        reminders = reminders_data.get("reminders", [])
        if reminders:
            for rem in reminders[::-1]:
                st.write(f"**Type:** {rem['type']} | **Description:** {rem['description']} | **Date:** {rem['date']} | **Decision:** {rem['decision']} | **Sent:** {'✅' if rem.get('sent') else '❌'}")
        else:
            st.info("No reminders scheduled yet.")
        # Motivational nudge if inactive for 3+ days
        if logs:
            last_activity = max(datetime.fromisoformat(entry.get('timestamp', '1970-01-01')).date() for entry in logs if entry.get('timestamp'))
            days_since = (date.today() - last_activity).days
            if days_since >= 3:
                st.warning(f"It's been {days_since} days since your last check-in. Remember, small steps matter! 🌱")

        # --- Edit Email for Past Decisions ---
        st.markdown("### ✉️ Edit Email for Past Decisions")
        for idx, entry in enumerate(logs[::-1]):
            with st.expander(f"Edit Email: {entry.get('dilemma', 'No dilemma')} ({entry.get('timestamp', '')[:10]})", expanded=False):
                logs_index = len(logs) - 1 - idx
                current_email = entry.get('email', '')
                new_email = st.text_input("User email for reminders:", value=current_email, key=f"edit_email_{idx}")
                if st.button("Save Email", key=f"save_email_{idx}"):
                    logs[logs_index]['email'] = new_email
                    with open(LOG_PATH, "w", encoding="utf-8") as f:
                        json.dump(logs, f, indent=2)
                    st.success("Email updated for this decision!")

        # --- Export & Download Your Journey ---
        st.markdown("### 📤 Export & Download Your Journey")
        export_format = st.selectbox("Choose export format:", ["JSON", "CSV", "PDF"], key="export_format")
        if export_format == "JSON":
            json_data = json.dumps(logs, indent=2, ensure_ascii=False)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"decision_journey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        elif export_format == "CSV":
            output = io.StringIO()
            fieldnames = ["timestamp", "dilemma", "values", "emotional_tone", "reflection", "action_plan", "result", "partner_feedback"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for entry in logs:
                writer.writerow({
                    "timestamp": entry.get("timestamp", ""),
                    "dilemma": entry.get("dilemma", ""),
                    "values": ", ".join(entry.get("values", [])),
                    "emotional_tone": entry.get("emotional_tone", ""),
                    "reflection": entry.get("reflection", ""),
                    "action_plan": "; ".join([step.get("description", "") for step in entry.get("action_plan", [])]),
                    "result": str(entry.get("result", {})),
                    "partner_feedback": entry.get("partner_feedback", "")
                })
            st.download_button(
                label="Download CSV",
                data=output.getvalue(),
                file_name=f"decision_journey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        elif export_format == "PDF":
            try:
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Decision Coach Journey Export", ln=True, align="C")
                for entry in logs:
                    pdf.ln(5)
                    pdf.set_font("Arial", style="B", size=11)
                    pdf.cell(0, 10, txt=f"Dilemma: {entry.get('dilemma', '')}", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(0, 8, txt=f"Date: {entry.get('timestamp', '')}", ln=True)
                    pdf.cell(0, 8, txt=f"Values: {', '.join(entry.get('values', []))}", ln=True)
                    pdf.cell(0, 8, txt=f"Feeling: {entry.get('emotional_tone', '')}", ln=True)
                    if entry.get('reflection'):
                        pdf.multi_cell(0, 8, txt=f"Reflection: {entry.get('reflection', '')}")
                    if entry.get('action_plan'):
                        pdf.multi_cell(0, 8, txt=f"Action Plan: {'; '.join([step.get('description', '') for step in entry.get('action_plan', [])])}")
                    if entry.get('partner_feedback'):
                        pdf.multi_cell(0, 8, txt=f"Partner Feedback: {entry.get('partner_feedback', '')}")
                    pdf.ln(2)
                pdf_output = io.BytesIO()
                pdf.output(pdf_output)
                st.download_button(
                    label="Download PDF",
                    data=pdf_output.getvalue(),
                    file_name=f"decision_journey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            except ImportError:
                st.warning("PDF export requires the 'fpdf' package. Install with 'pip install fpdf'.")
            st.info("Your exported data is private and for your use only. Keep it safe!")

        # --- Milestones & Achievements ---
        # st.markdown("### 🏅 Milestones & Achievements")
        # achievements_path = os.path.join(os.path.dirname(__file__), "achievements.json")
        # if os.path.exists(achievements_path):
        #     with open(achievements_path, "r", encoding="utf-8") as f:
        #         achievements = json.load(f)
        # else:
        #     achievements = {}
        # # Define milestone conditions
        # now = datetime.now().isoformat()
        # unlocked = []
        # # 1. First decision logged
        # if len(logs) >= 1 and "first_decision" not in achievements:
        #     achievements["first_decision"] = {"name": "First Decision!", "desc": "Logged your first decision.", "date": now, "emoji": "🎉"}
        #     unlocked.append("first_decision")
        # # 2. 7-day streak
        # streak = 0
        # prev_day = None
        # all_dates = sorted({datetime.fromisoformat(entry.get('timestamp', '1970-01-01')).date() for entry in logs if entry.get('timestamp')})
        # current_streak = 0
        # for d in all_dates:
        #     if prev_day is None:
        #         current_streak = 1
        #     elif (d - prev_day).days == 1:
        #         current_streak += 1
        #     else:
        #         current_streak = 1
        #     if current_streak >= 7 and "7_day_streak" not in achievements:
        #         achievements["7_day_streak"] = {"name": "7-Day Streak!", "desc": "Logged decisions 7 days in a row.", "date": now, "emoji": "🔥"}
        #         unlocked.append("7_day_streak")
        #     prev_day = d
        # # 3. 10 reflections
        # num_reflections = sum(1 for entry in logs if entry.get('reflection'))
        # if num_reflections >= 10 and "10_reflections" not in achievements:
        #     achievements["10_reflections"] = {"name": "Reflective Master", "desc": "Wrote 10 reflections.", "date": now, "emoji": "📝"}
        #     unlocked.append("10_reflections")
        # # 4. 5 action plans completed
        # num_completed_plans = sum(1 for entry in logs if entry.get('action_plan') and all(step.get('done') for step in entry.get('action_plan', [])))
        # if num_completed_plans >= 5 and "5_action_plans" not in achievements:
        #     achievements["5_action_plans"] = {"name": "Action Hero", "desc": "Completed 5 action plans.", "date": now, "emoji": "✅"}
        #     unlocked.append("5_action_plans")
        # # 5. First partner feedback
        # if any(entry.get('partner_feedback') for entry in logs) and "first_partner_feedback" not in achievements:
        #     achievements["first_partner_feedback"] = {"name": "Feedback Loop", "desc": "Received your first partner feedback.", "date": now, "emoji": "🤝"}
        #     unlocked.append("first_partner_feedback")
        # # 6. 10 reminders scheduled
        # reminders_path = os.path.join(os.path.dirname(__file__), "reminders.json")
        # if os.path.exists(reminders_path):
        #     with open(reminders_path, "r", encoding="utf-8") as f:
        #         reminders_data = json.load(f)
        #     num_reminders = len(reminders_data.get("reminders", []))
        #     if num_reminders >= 10 and "10_reminders" not in achievements:
        #         achievements["10_reminders"] = {"name": "Reminder Pro", "desc": "Scheduled 10 reminders.", "date": now, "emoji": "⏰"}
        #         unlocked.append("10_reminders")
        # # 7. 100% completion of an action plan
        # if any(entry.get('action_plan') and all(step.get('done') for step in entry.get('action_plan', [])) for entry in logs) and "perfect_plan" not in achievements:
        #     achievements["perfect_plan"] = {"name": "Perfect Plan", "desc": "Completed 100% of an action plan.", "date": now, "emoji": "🏆"}
        #     unlocked.append("perfect_plan")
        # # Save achievements
        # if unlocked:
        #     with open(achievements_path, "w", encoding="utf-8") as f:
        #         json.dump(achievements, f, indent=2)
        #     st.balloons()
        #     st.success(f"New achievement{'s' if len(unlocked) > 1 else ''} unlocked: " + ", ".join(achievements[k]['name'] for k in unlocked))
        # # Show all unlocked achievements
        # if achievements:
        #     for key, ach in achievements.items():
        #         st.markdown(f"{ach['emoji']} **{ach['name']}** — {ach['desc']} _(Unlocked: {ach['date'][:10]})_")
        # else:
        #     st.info("No achievements unlocked yet. Start logging decisions and taking action!") 