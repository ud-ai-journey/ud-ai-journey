import streamlit as st
import pandas as pd
import time
import json
import io
import base64
import requests
from datetime import datetime

# Local imports
from app.utils.session_state import initialize_session_state
from app.utils.ui_helpers import load_css

def show():
    """Render the batch optimizer page"""
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.title("🔄 Batch Title Optimizer")
    st.markdown(
        """
        Optimize multiple YouTube titles at once. Perfect for content creators with lots of videos.
        Upload a CSV file or paste your titles below.
        """
    )
    
    # Input methods tabs
    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])
    
    with tab1:
        # Text area for manual input
        st.subheader("Enter Titles")
        st.caption("Enter one title per line")
        titles_text = st.text_area(
            "Titles",
            height=200,
            placeholder="My First Tutorial\nHow to Code in Python\nBest Gaming Setup 2024",
            label_visibility="collapsed"
        )
    
    with tab2:
        # File upload
        st.subheader("Upload CSV or TXT File")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["csv", "txt"],
            help="CSV should have a column named 'title' or the first column will be used"
        )
        
        if uploaded_file is not None:
            try:
                # Try to read as CSV
                df = pd.read_csv(uploaded_file)
                
                # Check if 'title' column exists
                if 'title' in df.columns:
                    titles = df['title'].tolist()
                else:
                    # Use the first column
                    titles = df.iloc[:, 0].tolist()
                
                # Display preview
                st.success(f"✅ Loaded {len(titles)} titles from file")
                st.dataframe(pd.DataFrame({"Title": titles}).head(5), use_container_width=True)
                
                # Store in session state
                st.session_state.batch_titles = titles
                
            except Exception as e:
                # Try to read as text file
                try:
                    uploaded_file.seek(0)
                    titles = uploaded_file.read().decode("utf-8").splitlines()
                    titles = [t.strip() for t in titles if t.strip()]
                    
                    st.success(f"✅ Loaded {len(titles)} titles from file")
                    st.dataframe(pd.DataFrame({"Title": titles}).head(5), use_container_width=True)
                    
                    # Store in session state
                    st.session_state.batch_titles = titles
                    
                except Exception as e2:
                    st.error(f"❌ Error reading file: {str(e2)}")
    
    # Common settings
    st.subheader("Optimization Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category = st.selectbox(
            "Content Category",
            options=[
                "Tech & Programming",
                "Gaming",
                "Education & Tutorial",
                "Lifestyle & Vlog",
                "Entertainment",
                "Business & Finance",
                "Health & Fitness",
                "Travel",
                "Food & Cooking",
                "Other"
            ]
        )
    
    with col2:
        target_emotion = st.selectbox(
            "Target Emotion",
            options=[
                "Curiosity",
                "Urgency",
                "Excitement",
                "Surprise",
                "FOMO",
                "Achievement",
                "Transformation"
            ]
        )
    
    with col3:
        content_type = st.selectbox(
            "Content Type",
            options=[
                "Tutorial",
                "Review",
                "Vlog",
                "Reaction",
                "Challenge",
                "Tips & Tricks",
                "Behind the Scenes"
            ]
        )
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            ai_model = st.selectbox(
                "AI Model",
                options=[
                    "Gemini Pro (Recommended)",
                    "Gemini Flash (Faster)",
                    "OpenAI GPT-4o",
                    "Claude 3 Opus"
                ]
            )
        
        with col2:
            optimization_strength = st.slider(
                "Optimization Strength",
                min_value=1,
                max_value=10,
                value=7,
                help="Higher values produce more aggressive optimization"
            )
    
    # Process button
    if st.button("🚀 Optimize All Titles", type="primary", use_container_width=True):
        # Get titles from text area if not from file upload
        if not st.session_state.get("batch_titles"):
            if titles_text:
                titles = [t.strip() for t in titles_text.splitlines() if t.strip()]
            else:
                st.error("⚠️ Please enter at least one title or upload a file")
                return
        else:
            titles = st.session_state.batch_titles
        
        # Check if we have titles
        if not titles:
            st.error("⚠️ No titles found to optimize")
            return
        
        # Check if too many titles
        if len(titles) > 50:
            st.warning(f"⚠️ You've entered {len(titles)} titles. Processing may take a while and could be rate limited.")
        
        # Process the titles
        process_batch(titles, category, target_emotion, content_type, ai_model, optimization_strength)

def process_batch(titles, category, target_emotion, content_type, ai_model, optimization_strength):
    """Process a batch of titles"""
    # Create progress indicators
    progress_text = st.empty()
    progress_bar = st.progress(0)
    results_container = st.container()
    
    # Initialize results list
    results = []
    
    # Process each title
    for i, title in enumerate(titles):
        # Update progress
        progress_text.text(f"Processing title {i+1} of {len(titles)}: {title[:30]}...")
        progress_bar.progress((i) / len(titles))
        
        # In a real app, this would call the API
        # For demo purposes, simulate API call with a delay
        time.sleep(0.5)
        
        # Generate mock result
        result = {
            "original": title,
            "optimized": generate_mock_optimized_title(title, category, target_emotion),
            "seo_score": 70 + (hash(title) % 25)  # Random score between 70-95
        }
        
        results.append(result)
    
    # Complete the progress
    progress_text.text("✅ Processing complete!")
    progress_bar.progress(1.0)
    
    # Store results in session state
    st.session_state.batch_results = results
    
    # Display results
    display_batch_results(results)

def generate_mock_optimized_title(title, category, emotion):
    """Generate a mock optimized title for demonstration"""
    emotion_prefixes = {
        "Curiosity": ["Discover Why", "The Secret to", "How to Actually"],
        "Urgency": ["Do This Now:", "Last Chance:", "Don't Miss:"],
        "Excitement": ["Mind-Blowing", "Incredible", "Amazing"],
        "Surprise": ["You Won't Believe", "Shocking Truth About", "Unexpected"],
        "FOMO": ["Everyone Is Talking About", "Don't Miss Out On", "What You're Missing:"],
        "Achievement": ["
