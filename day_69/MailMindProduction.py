import streamlit as st
import streamlit as st
from streamlit import query_params
import os
import inspect
import textwrap
import pyperclip  # For reliable clipboard operations
import re
from datetime import datetime
from transformers import pipeline
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import pandas as pd
import urllib.parse as urlparse
import streamlit.components.v1 as components



# --- LOGO AND PAGE CONFIG ---
st.set_page_config(
    page_title="MailMind - Smart Email Analyzer",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR SOPHISTICATED UI ---
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main > div {
        padding-top: 2rem;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Card styling */
    .analysis-card {
        background: linear-gradient(145deg, #f8fafc, #e2e8f0);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-card p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Success/warning styling */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 10px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        border-radius: 10px;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE PIPELINES ---
@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

@st.cache_resource
def get_sentiment():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

summarizer = get_summarizer()
sentiment_analyzer = get_sentiment()

# --- INITIALIZE SESSION STATES ---
if "email_text" not in st.session_state:
    st.session_state.email_text = ""
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "analysis_id" not in st.session_state:
    st.session_state.analysis_id = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}
if "settings" not in st.session_state:
    st.session_state.settings = {
        "summary_length": "Medium",
        "auto_copy": False,
        "include_sentiment": True,
        "include_actions": True,
        "dark_mode": False
    }

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h1>📬 MailMind</h1>
        <p>Smart Email Analyzer</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- ANALYTICS DASHBOARD ---
    st.markdown("### 📊 Analytics Dashboard")
    
    total_analyses = len(st.session_state.history)
    positive_feedback = sum(1 for i in range(1, total_analyses + 1) 
                          if st.session_state.get("feedback_given", {}).get(i) == "positive")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_analyses}</h3>
            <p>Analyses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
            <h3>{positive_feedback}</h3>
            <p>👍 Feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- TONE DISTRIBUTION CHART ---
    if st.session_state.history:
        tone_data = [entry.get('tone', 'Unknown') for entry in st.session_state.history]
        tone_counts = Counter([tone.split()[0] for tone in tone_data if tone != 'Unknown'])
        
        if tone_counts:
            st.markdown("### 🎭 Tone Distribution")
            fig = px.pie(
                values=list(tone_counts.values()),
                names=list(tone_counts.keys()),
                color_discrete_sequence=['#667eea', '#764ba2', '#48bb78', '#ed8936', '#e53e3e']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                height=300,
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # --- SETTINGS ---
    st.markdown("### ⚙️ Settings")
    
    st.session_state.settings["summary_length"] = st.selectbox(
        "📝 Summary Length",
        ["Short", "Medium", "Detailed"],
        index=["Short", "Medium", "Detailed"].index(st.session_state.settings["summary_length"]),
        help="Choose your preferred summary length"
    )
    
    st.session_state.settings["auto_copy"] = st.checkbox(
        "📋 Auto-copy summary",
        value=st.session_state.settings["auto_copy"],
        help="Automatically copy summary to clipboard after analysis"
    )
    
    st.markdown("#### 🎯 Analysis Preferences")
    st.session_state.settings["include_sentiment"] = st.checkbox(
        "🎭 Include tone analysis", 
        value=st.session_state.settings["include_sentiment"]
    )
    st.session_state.settings["include_actions"] = st.checkbox(
        "✅ Extract action items", 
        value=st.session_state.settings["include_actions"]
    )
    
    st.markdown("---")
    
    # --- QUICK ACTIONS ---
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.feedback_given = {}
        st.session_state.current_analysis = None
        st.success("History cleared!")
    
    if st.button("📊 Export Analytics", use_container_width=True):
        if st.session_state.history:
            df = pd.DataFrame([
                {
                    'Timestamp': entry['timestamp'],
                    'Tone': entry.get('tone', 'Unknown'),
                    'Actions_Count': len(entry.get('actions', [])),
                    'Summary_Length': len(entry.get('summary', '').split())
                }
                for entry in st.session_state.history
            ])
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                "mailmind_analytics.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.info("No data to export yet!")
    
    st.markdown("---")
    
    # --- RECENT ACTIVITY ---
    if st.session_state.history:
        st.markdown("### 🕐 Recent Activity")
        for entry in st.session_state.history[-3:]:
            tone_icon = entry.get('icon', '✉️')
            st.markdown(f"""
            <div style="padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px; margin-bottom: 0.5rem;">
                <small>{entry['timestamp']}</small><br>
                <strong>{tone_icon} {entry.get('tone', 'Unknown')}</strong>
            </div>
            """, unsafe_allow_html=True)

# --- NAVIGATION HANDLER ---
# If the user selects Documentation, render docs and stop further execution
if 'page' in locals() and page == "📄 Documentation":
    st.header("📄 Documentation")
    # Load README.md from repository root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    readme_path = os.path.join(repo_root, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_md = f.read()
        st.markdown(readme_md)
    else:
        st.warning("README.md not found in project root.")

    st.markdown("---")
    st.subheader("Function Reference")

    def doc_md(func):
        doc = inspect.getdoc(func) or "No description provided."
        sig = str(inspect.signature(func))
        return f"### `{func.__name__}{sig}`\n\n{doc}"

    for fn in [summarize_email, extract_actions, analyze_tone]:
        st.markdown(doc_md(fn))

    st.stop()

# --- HELPER FUNCTIONS ---
# --- CLIENT-SIDE COPY & SHARE HELPERS ---

def clipboard_js_button(text: str, label: str, key: str):
    """Render an HTML button that copies `text` to the user's clipboard via JS."""
    safe_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n")
    html = f"""
    <button id='{key}' onclick="navigator.clipboard.writeText(`{safe_text}`).then(()=>{{let btn=document.getElementById('{key}');let init=btn.innerHTML;btn.innerHTML='✅ Copied';setTimeout(()=>btn.innerHTML=init,2000);}})" 
            style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:0.5rem 1.5rem;color:#fff;border:none;border-radius:8px;cursor:pointer;width:100%;">
        📋 {label}
    </button>"""
    components.html(html, height=45)


def mailto_share_button(text: str, label: str, key: str):
    """Render a button that opens the default mail client with `text` in body."""
    mailto = f"mailto:?subject=MailMind%20Analysis&body={urlparse.quote(text)}"
    html = f"""
    <a id='{key}' href='{mailto}' style="text-decoration:none;" target="_blank">
        <button style="background:linear-gradient(135deg,#d946ef 0%,#7c3aed 100%);padding:0.5rem 1.5rem;color:#fff;border:none;border-radius:8px;cursor:pointer;width:100%;">
            📤 {label}
        </button>
    </a>"""
    components.html(html, height=45)


def copy_to_clipboard(text):
    """Helper function to copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        st.error(f"Could not copy to clipboard: {str(e)}")
        return False

def summarize_email(email_text, length_preference="Medium"):
    cleaned = re.sub(r'^\s*(Subject|From|To|Date):.*$', '', email_text, flags=re.MULTILINE)
    cleaned = re.sub(r'(Sent from|Best regards|Thanks|Sincerely|--|__)\s*.*$', '', cleaned, flags=re.MULTILINE)
    words = cleaned.split()
    
    # Adjust summary length based on preference
    length_map = {
        "Short": {"max_length": 80, "min_length": 20},
        "Medium": {"max_length": 130, "min_length": 30},
        "Detailed": {"max_length": 200, "min_length": 50}
    }
    
    length_params = length_map.get(length_preference, length_map["Medium"])
    
    if len(words) > 30:
        chunk_size = 900
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        summaries = []
        for chunk in chunks:
            try:
                s = summarizer(chunk, **length_params, do_sample=False)[0]['summary_text']
            except Exception as e:
                s = f"[Summary error: {str(e)}]"
            summaries.append(s)
        
        if len(summaries) > 1:
            try:
                final_summary = summarizer(' '.join(summaries), **length_params, do_sample=False)[0]['summary_text']
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
        r'(?:by|due|deadline)\s+([^\.!?]+[\.!?])',
        r'(?:follow up|follow-up|remind|schedule)\s+([^\.!?]+[\.!?])'
    ]
    actions = set()
    for pat in patterns:
        found = re.findall(pat, email_text, re.IGNORECASE)
        actions.update([f"• {a.strip()}" for a in found if a.strip()])
    
    unique_actions = list(set(actions))
    return unique_actions if unique_actions else ["• No action items found"]

def analyze_tone(email_text):
    words = email_text.split()
    if not words:
        return "No content to analyze."
    chunk_size = 400
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    sentiments = []
    for chunk in chunks:
        try:
            s = sentiment_analyzer(chunk)[0]['label']
        except Exception as e:
            s = f"ERROR: {str(e)}"
        sentiments.append(s)
    
    valid_sentiments = [s for s in sentiments if s in ('POSITIVE', 'NEGATIVE')]
    if valid_sentiments:
        base_tone = Counter(valid_sentiments).most_common(1)[0][0].capitalize()
    else:
        base_tone = "Unknown"
    
    tone_patterns = {
        "Apologetic": r'\b(sorry|apologize|regret)\b',
        "Urgent": r'\b(urgent|asap|immediately|now)\b',
        "Formal": r'\b(dear|respectfully|sincerely|regards)\b',
        "Friendly": r'\b(thanks|appreciate|great|awesome)\b',
        "Professional": r'\b(meeting|schedule|project|report)\b'
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
    elif "Professional" in tone:
        return "💼"
    elif "Positive" in tone:
        return "👍"
    elif "Negative" in tone:
        return "⚠️"
    return "✉️"

# --- MAIN LAYOUT ---
st.markdown("""
<div class="main-header fade-in">
    <h1>📬 MailMind</h1>
    <p>Advanced AI-Powered Email Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown("### 📥 Email Input")

col_upload, col_paste = st.columns([1, 2], gap="large")

with col_upload:
    st.markdown("""
    <div class="analysis-card">
        <h4>📤 Upload Email File</h4>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["txt", "eml", "msg"],
        help="Upload your email file (.txt, .eml, .msg)"
    )
    
    if uploaded_file:
        try:
            raw_bytes = uploaded_file.read()
            try:
                email_text = raw_bytes.decode('utf-8')
            except UnicodeDecodeError:
                email_text = raw_bytes.decode('latin1')
            st.session_state.email_text = email_text
            st.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

with col_paste:
    st.markdown("""
    <div class="analysis-card">
        <h4>✍️ Paste Email Content</h4>
    </div>
    """, unsafe_allow_html=True)
    
    default_email = """Subject: Quarterly Review Meeting & Strategic Planning

Dear Team,

I hope this message finds you well. As we approach the end of Q3, I wanted to schedule our quarterly review meeting to discuss our progress and plan for Q4.

Please review the attached performance metrics and come prepared to discuss:
1. Current project status and deliverables
2. Resource allocation for upcoming initiatives  
3. Budget considerations for next quarter
4. Strategic priorities moving forward

Could everyone please confirm their availability for next Wednesday at 2:30 PM? We'll need approximately 2 hours for this session.

Looking forward to our productive discussion.

Best regards,
Sarah Johnson
Director of Operations""" if not st.session_state.email_text else st.session_state.email_text

    email_text = st.text_area(
        "Paste your email content here:",
        value=default_email,
        height=400,
        help="Paste the full email content including headers if available"
    )
    
    if email_text != st.session_state.email_text:
        st.session_state.email_text = email_text

# --- ANALYZE BUTTON ---
st.markdown("---")
analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])

with analyze_col2:
    analyze = st.button("🚀 Analyze Email", use_container_width=True, type="primary")

# --- ANALYSIS LOGIC ---
if analyze and st.session_state.email_text.strip():
    with st.spinner("🧠 AI is analyzing your email... Please wait"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Perform analysis based on settings
            summary = summarize_email(
                st.session_state.email_text, 
                st.session_state.settings["summary_length"]
            )
            
            actions = extract_actions(st.session_state.email_text) if st.session_state.settings["include_actions"] else []
            tone = analyze_tone(st.session_state.email_text) if st.session_state.settings["include_sentiment"] else "Analysis disabled"
            icon = get_icon_for_tone(tone)

            st.session_state.analysis_id += 1
            current_id = st.session_state.analysis_id
            
            st.session_state.current_analysis = {
                "id": current_id,
                "summary": summary,
                "actions": actions,
                "tone": tone,
                "timestamp": timestamp,
                "icon": icon,
                "email_length": len(st.session_state.email_text.split())
            }

            st.session_state.history.append(st.session_state.current_analysis.copy())
            
            # Auto-copy if enabled
            if st.session_state.settings["auto_copy"]:
                copy_to_clipboard(summary)
                st.toast("📋 Summary auto-copied to clipboard!")

        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")

elif analyze:
    st.warning("⚠️ Please enter or upload an email to analyze.")

# --- DISPLAY RESULTS ---
if st.session_state.current_analysis:
    analysis = st.session_state.current_analysis
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Stats row
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("📝 Email Length", f"{analysis['email_length']} words")
    with stats_col2:
        st.metric("📋 Summary Length", f"{len(analysis['summary'].split())} words")
    with stats_col3:
        st.metric("✅ Action Items", len(analysis['actions']))
    with stats_col4:
        st.metric("🕐 Analysis Time", "< 1 sec")
    
    st.markdown("---")
    
    # Results display
    result_col1, result_col2, result_col3 = st.columns(3, gap="large")
    
    with result_col1:
        st.markdown("""
        <div class="analysis-card fade-in">
            <h4>📋 Smart Summary</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area(
            "",
            value=analysis["summary"],
            height=300,
            key=f"summary_display_{analysis['id']}",
            disabled=True
        )
        
        col_copy, col_share = st.columns(2)
        with col_copy:
            clipboard_js_button(analysis["summary"], "Copy", key=f"summary_copy_btn_{analysis['id']}" )
        with col_share:
            mailto_share_button(analysis["summary"], "Share", key=f"summary_share_btn_{analysis['id']}" )

    with result_col2:
        st.markdown("""
        <div class="analysis-card fade-in">
            <h4>✅ Action Items</h4>
        </div>
        """, unsafe_allow_html=True)
        
        actions_text = '\n'.join(analysis["actions"])
        st.text_area(
            "",
            value=actions_text,
            height=300,
            key=f"actions_display_{analysis['id']}",
            disabled=True
        )
        
        col_copy, col_export = st.columns(2)
        with col_copy:
            clipboard_js_button(actions_text, "Copy", key=f"actions_copy_btn_{analysis['id']}" )
        with col_export:
            st.download_button("📝 To-Do", actions_text, file_name="todo.txt", mime="text/plain", key=f"todo_download_{analysis['id']}", use_container_width=True)

    with result_col3:
        st.markdown(f"""
        <div class="analysis-card fade-in">
            <h4>🎭 Tone Analysis {analysis['icon']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area(
            "",
            value=analysis["tone"],
            height=300,
            key=f"tone_display_{analysis['id']}",
            disabled=True
        )
        
        col_copy, col_insight = st.columns(2)
        with col_copy:
            clipboard_js_button(analysis["tone"], "Copy", key=f"tone_copy_btn_{analysis['id']}" )
        with col_insight:
            if st.button("🧠 Insights", key=f"insights_tone_{analysis['id']}", use_container_width=True):
                st.info("Detailed insights coming soon!")

    # Timestamp and feedback
    st.markdown(f"<div style='text-align: right; color: #64748b; font-style: italic; margin-top: 1rem;'>⏰ Analyzed on: {analysis['timestamp']}</div>", unsafe_allow_html=True)
    
    # Enhanced feedback section
    current_id = analysis['id']
    if current_id not in st.session_state.feedback_given:
        st.markdown("---")
        st.markdown("### 💬 How was this analysis?")
        
        feedback_col1, feedback_col2, feedback_col3, feedback_col4 = st.columns(4)
        
        with feedback_col1:
            if st.button("🎯 Excellent", key=f"feedback_excellent_{current_id}", use_container_width=True):
                st.session_state.feedback_given[current_id] = "excellent"
                st.success("🚀 Thank you for the excellent rating!")
        
        with feedback_col2:
            if st.button("👍 Good", key=f"feedback_good_{current_id}", use_container_width=True):
                st.session_state.feedback_given[current_id] = "good"
                st.success("✅ Thanks for the positive feedback!")
        
        with feedback_col3:
            if st.button("👎 Poor", key=f"feedback_poor_{current_id}", use_container_width=True):
                st.session_state.feedback_given[current_id] = "poor"
                st.warning("😔 We'll work on improving!")
        
        with feedback_col4:
            if st.button("🐛 Bug Report", key=f"feedback_bug_{current_id}", use_container_width=True):
                st.session_state.feedback_given[current_id] = "bug"
                st.info("🔧 Please report issues on our GitHub!")

# --- HISTORY SECTION ---
if len(st.session_state.history) > 1:
    st.markdown("---")
    show_history = st.checkbox("📜 View Analysis History", value=False)
    
    if show_history:
        st.markdown("### 📜 Previous Analyses")
        
        # History controls
        history_col1, history_col2 = st.columns([3, 1])
        with history_col1:
            st.markdown(f"Showing {len(st.session_state.history)-1} previous analyses")
        with history_col2:
            if st.button("🗑️ Clear All", key="clear_history_main"):
                st.session_state.history = [st.session_state.history[-1]]  # Keep only current
                st.success("History cleared!")
                st.rerun()
        
        # Display history
        history_to_show = st.session_state.history[:-1] if st.session_state.current_analysis else st.session_state.history
        
        for i, entry in enumerate(reversed(history_to_show)):
            with st.expander(f"📧 Analysis #{len(history_to_show)-i} - {entry['timestamp']}", expanded=False):
                hist_col1, hist_col2, hist_col3 = st.columns(3)
                
                with hist_col1:
                    st.markdown("**📋 Summary:**")
                    st.text_area("", value=entry['summary'], height=120, key=f"history_summary_{entry['id']}", disabled=True)
                
                with hist_col2:
                    st.markdown("**✅ Actions:**")
                    st.text_area("", value='\n'.join(entry['actions']), height=120, key=f"history_actions_{entry['id']}", disabled=True)
                
                with hist_col3:
                    st.markdown(f"**🎭 Tone {entry.get('icon', '✉️')}:**")
                    st.text_area("", value=entry['tone'], height=120, key=f"history_tone_{entry['id']}", disabled=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-top: 2rem;'>
    <h3>🚀 MailMind Pro</h3>
    <p>Advanced AI Email Intelligence • Built with ❤️ for busy professionals</p>
    <p><strong>By Uday Kumar</strong> | <a href="https://github.com/ud-ai-journey/ud-ai-journey)" style="color: #ffd700;">GitHub</a> | <a href="javascript:void(0)" onclick="window.open('docs.html','_blank')" style="color: #ffd700;">Documentation</a></p>
</div>
""", unsafe_allow_html=True)


# Redirect to standalone documentation page when requested
params = st.query_params
if params.get("page", ["analyze"])[0].lower().startswith("doc"):
    doc_path = os.path.join(os.path.dirname(__file__), "docs.html")
    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            doc_html = f.read()
        components.html("<script>window.location.replace('docs.html');</script>", height=0)
    else:
        st.error("Documentation file not found.")
    st.stop()


