import streamlit as st
import re
from datetime import datetime

def summarize_email(email_text):
    # Simple summary: first 2-3 non-empty lines after the first greeting or announcement
    lines = [line.strip() for line in email_text.split('\n') if line.strip()]
    # Remove common header/footer and marketing lines
    skip_words = ["logo", "unsubscribe", "inbox", "team", "best", "turn ideas", "unsub", "cheers", "regards", "waiting on", "hear from our users", "questions?", "start building now", "start building", "learn more", "content challenge", "build challenge", "prize", "waitlist"]
    filtered = [line for line in lines if not any(x in line.lower() for x in skip_words)]
    # Find the first line that looks like a real announcement or greeting
    for i, line in enumerate(filtered):
        if any(greet in line.lower() for greet in ["hi", "hello", "dear", "hey", "news", "exciting", "we have", "is free", "good news", "update"]):
            summary_lines = filtered[i:i+3]
            break
    else:
        summary_lines = filtered[:3]
    return ' '.join(summary_lines) if summary_lines else 'No summary found.'

# Function to extract action items
def extract_actions(email_text):
    actions = re.findall(r'(?:action|task|need to|should|must)\s+(.+?)(?:\n|\.|$)', email_text, re.IGNORECASE)
    deadlines = re.findall(r'(?:by|due)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+)', email_text, re.IGNORECASE)
    return [f"- {a.strip()} {'(due ' + d + ')' if d else ''}" for a, d in zip(actions, deadlines[:len(actions)])] or ["- No action items found"]

# Function to analyze tone (basic heuristic)
def analyze_tone(email_text):
    if re.search(r'\b(sorry|apologize|regret)\b', email_text, re.IGNORECASE):
        return "Apologetic"
    elif re.search(r'\b(urgent|immediately|now)\b', email_text, re.IGNORECASE):
        return "Assertive"
    elif re.search(r'\b(hi|hey|thanks)\b', email_text, re.IGNORECASE):
        return "Polite"
    return "Neutral"

# Streamlit UI
st.title("MailMind - Email Summarizer & Action Extractor")
st.write("Upload an email thread or paste the text below to get a smart summary, action items, and tone analysis.")

# Default email sample
default_email = """
Subject: Project Update

Hi Team,
I apologize for the delay in the project timeline. We need to finalize the report by 6/22/2025. Please review the draft and provide feedback. Thanks!
Best,
John
"""
email_text = st.text_area("Paste your email here:", value=default_email, height=200)

if st.button("Analyze Email"):
    if email_text.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        summary = summarize_email(email_text)
        actions = extract_actions(email_text)
        tone = analyze_tone(email_text)

        st.subheader("Summary")
        st.write(summary)
        st.subheader("Action Items")
        for action in actions:
            st.write(action)
        st.subheader("Tone")
        st.write(tone)
        st.write(f"Analyzed on: {timestamp}")
    else:
        st.warning("Please enter or paste an email to analyze.")

st.write("Made with ❤️ by Uday Kumar - Day 67 Project")