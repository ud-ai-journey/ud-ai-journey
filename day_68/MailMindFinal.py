import streamlit as st

# --- LOGO AND PAGE CONFIG ---
st.set_page_config(
    page_title="MailMind - Smart Email Analyzer",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded",
)

import re
from datetime import datetime
from transformers import pipeline

# --- INITIALIZE PIPELINES ---
@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")
@st.cache_resource
def get_sentiment():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

summarizer = get_summarizer()
sentiment_analyzer = get_sentiment()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/streamlit/brand/main/logos/mark/streamlit-mark-color.png", width=64)
    st.title("📬 MailMind")
    st.markdown("#### ✨ Summarize, extract actions, & analyze tone from any email thread.")
    st.markdown("""
    **How to use:**
    1. Paste or upload your email/thread.
    2. Click **Analyze Email**.
    3. Copy/share the results!
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ for busy professionals.\n\nBy [Uday Kumar](https://github.com/ud-ai-journey)")
    st.markdown("[GitHub Repo](https://github.com/ud-ai-journey/ud-ai-journey/tree/main/day_67)")

# --- HELPERS ---
def summarize_email(email_text):
    cleaned = re.sub(r'^\s*(Subject|From|To|Date):.*$', '', email_text, flags=re.MULTILINE)
    cleaned = re.sub(r'(Sent from|Best regards|Thanks|Sincerely|--|__)\s*.*$', '', cleaned, flags=re.MULTILINE)
    words = cleaned.split()
    if len(words) > 30:
        # HuggingFace models have a max token limit (e.g., 1024 for BART). We'll chunk and summarize each part, then summarize the summaries.
        chunk_size = 900  # tokens/words per chunk (safe for BART)
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        summaries = []
        for chunk in chunks:
            try:
                s = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            except Exception as e:
                s = f"[Summary error: {str(e)}]"
            summaries.append(s)
        # If more than one chunk, summarize the summaries
        if len(summaries) > 1:
            try:
                final_summary = summarizer(' '.join(summaries), max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            except Exception as e:
                final_summary = ' '.join(summaries)
            summary = final_summary
        else:
            summary = summaries[0]
    elif len(words) > 0:
        lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
        summary = ' '.join(lines[:2])
    else:
        summary = "No content to summarize."
    return summary

def extract_actions(email_text):
    patterns = [
        r'(?:action|task|need to|should|must|please|could you|can you)\s+([^\.!?]+[\.!?])',
        r'(?:by|due|deadline)\s+([^\.!?]+[\.!?])'
    ]
    actions = []
    for pat in patterns:
        found = re.findall(pat, email_text, re.IGNORECASE)
        actions.extend([f"- {a.strip()}" for a in found])
    return actions if actions else ["- No action items found"]

def analyze_tone(email_text):
    words = email_text.split()
    if not words:
        return "No content to analyze."
    chunk_size = 400  # safe for DistilBERT
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    sentiments = []
    for chunk in chunks:
        try:
            s = sentiment_analyzer(chunk)[0]['label']
        except Exception as e:
            s = f"ERROR: {str(e)}"
        sentiments.append(s)
    # Aggregate: majority vote, fallback to first if tie or error
    from collections import Counter
    valid_sentiments = [s for s in sentiments if s in ('POSITIVE', 'NEGATIVE')]
    if valid_sentiments:
        base_tone = Counter(valid_sentiments).most_common(1)[0][0].capitalize()
    else:
        base_tone = "Unknown"
    tone_patterns = {
        "Apologetic": r'\\b(sorry|apologize|regret)\\b',
        "Urgent": r'\\b(urgent|asap|immediately|now)\\b',
        "Formal": r'\\b(dear|respectfully|sincerely|regards)\\b',
        "Friendly": r'\\b(thanks|appreciate|great|awesome)\\b'
    }
    detected = [tone for tone, pat in tone_patterns.items() if re.search(pat, email_text, re.IGNORECASE)]
    return f"{base_tone}" + (f" ({', '.join(detected)})" if detected else "")

def get_icon_for_tone(tone):
    if "Apologetic" in tone:
        return "🙏"
    elif "Urgent" in tone:
        return "⏰"
    elif "Friendly" in tone:
        return "😊"
    elif "Positive" in tone:
        return "👍"
    elif "Negative" in tone:
        return "⚠️"
    return "✉️"

# --- MAIN LAYOUT ---
st.markdown(
    "<h1 style='text-align: center;'>📬 MailMind &mdash; Smart Email Analyzer</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>Paste or upload your email to get an instant, AI-powered summary, action items, and tone analysis!</p>", unsafe_allow_html=True)
st.markdown("---")

# --- INPUTS: File uploader OR text area ---
col_upload, col_paste = st.columns([1, 3], gap="large")
with col_upload:
    uploaded_file = st.file_uploader("Upload .txt/.eml", type=["txt", "eml"])
with col_paste:
    default_email = """
Subject: Project Update Meeting & Next Steps

Hi Team,

I hope this email finds you well. Following our discussion yesterday, we need to finalize the report by Friday. Please review the draft I shared and provide your feedback as soon as possible.

Key points that require immediate attention:
1. Update the project timeline
2. Add missing metrics
3. Review the budget section

Let's schedule a follow-up meeting next Tuesday at 2 PM to discuss the changes.

Best regards,
John
"""
    email_text = st.text_area("📝 Paste your email here:", value=default_email, height=200)

# --- INGEST EMAIL CONTENT ---
if uploaded_file:
    raw_bytes = uploaded_file.read()
    try:
        email_text = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        email_text = raw_bytes.decode('latin1')

# --- HISTORY STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- ANALYZE BUTTON ---
analyze = st.button("🔍 Analyze Email", use_container_width=True)

if analyze and email_text.strip():
    with st.spinner("Analyzing... please wait"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = summarize_email(email_text)
        actions = extract_actions(email_text)
        tone = analyze_tone(email_text)
        icon = get_icon_for_tone(tone)

        # --- BEAUTIFUL OUTPUT LAYOUT ---
        st.success("✅ Analysis Complete!", icon="✅")
        st.markdown("### Results")
        out1, out2, out3 = st.columns(3, gap="large")
        with out1:
            st.markdown("#### 📋 Summary")
            st.code(summary, language="markdown")
            if st.button("📋 Copy Summary", key="copy_summary"):
                st.session_state["summary_clip"] = summary
                st.toast("Summary copied!")
        with out2:
            st.markdown("#### ✅ Action Items")
            st.code('\n'.join(actions), language="markdown")
            if st.button("📋 Copy Actions", key="copy_actions"):
                st.session_state["actions_clip"] = '\n'.join(actions)
                st.toast("Actions copied!")
        with out3:
            st.markdown(f"#### 🎭 Tone {icon}")
            st.code(tone, language="markdown")
            if st.button("📋 Copy Tone", key="copy_tone"):
                st.session_state["tone_clip"] = tone
                st.toast("Tone copied!")

        st.markdown(f"<div style='text-align:right; color: gray;'>Analyzed on: {timestamp}</div>", unsafe_allow_html=True)
        st.info("Tip: You can paste these results into your notes, project tools, or email replies.", icon="💡")

        # --- HISTORY ---
        st.session_state.history.append({
            "summary": summary,
            "actions": actions,
            "tone": tone,
            "timestamp": timestamp
        })

        # --- FEEDBACK ---
        st.markdown("---")
        st.markdown("#### 💬 Was this summary helpful?")
        feedback = st.radio("", ["👍 Yes", "👎 No"], horizontal=True, key="feedback")
        if feedback == "👍 Yes":
            st.success("Thanks for your feedback! 🚀")
        elif feedback == "👎 No":
            st.warning("Sorry! Please suggest improvements [here](https://github.com/ud-ai-journey/ud-ai-journey/issues).")

elif analyze:
    st.warning("Please enter or upload an email to analyze.")

# --- HISTORY DISPLAY ---
if st.checkbox("📜 Show Analysis History"):
    for entry in reversed(st.session_state.history):
        st.markdown(f"**⏱ {entry['timestamp']}**")
        st.markdown(f"**Summary:** {entry['summary']}")
        st.markdown(f"**Actions:** {'; '.join(entry['actions'])}")
        st.markdown(f"**Tone:** {entry['tone']}")
        st.markdown("---")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color: gray;'>MailMind &copy; 2025 &mdash; Open Source AI Email Assistant</p>",
    unsafe_allow_html=True
)