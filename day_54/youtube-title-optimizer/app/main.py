import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import requests
import json
from PIL import Image
import io
import base64
import uuid
import logging
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stateful_button import button
from streamlit_extras.stoggle import stoggle
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

# Local imports
from app.utils.session_state import initialize_session_state
from app.utils.ui_helpers import load_lottie, load_css, render_svg
from app.components.title_card import TitleCard
from app.components.metrics_dashboard import MetricsDashboard
from app.components.youtube_preview import YouTubePreview

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
VERSION = "2.0.0"

def main():
    # Initialize session state
    initialize_session_state()
    
    # Load custom CSS
    load_css("app/static/css/style.css")
    
    # Page configuration
    st.set_page_config(
        page_title="YouTube Title Optimizer Pro",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.image("app/static/img/logo.png", width=200)
        st.title("YouTube Title Optimizer")
        st.caption(f"Enterprise Edition v{VERSION}")
        
        # User profile section if logged in
        if st.session_state.get("user_authenticated", False):
            with stylable_container(
                key="profile_container",
                css_styles="""
                    {
                        background-color: rgba(255, 255, 255, 0.1);
                        border-radius: 0.5rem;
                        padding: 1rem;
                        margin-bottom: 1rem;
                    }
                """
            ):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("app/static/img/avatar.png", width=50)
                with col2:
                    st.write(f"**{st.session_state.user_name}**")
                    st.caption(f"Plan: {st.session_state.user_plan}")
                    
                # Usage metrics
                st.progress(st.session_state.usage_percentage / 100, 
                           f"API Usage: {st.session_state.usage_percentage}%")
        
        # Navigation menu
        selected = option_menu(
            menu_title=None,
            options=[
                "Home", 
                "Batch Optimizer", 
                "Analytics", 
                "Competitor Analysis",
                "Settings",
                "Account"
            ],
            icons=[
                "house", 
                "list-task", 
                "graph-up", 
                "binoculars",
                "gear",
                "person"
            ],
            default_index=0,
        )
        
        # Load appropriate page based on selection
        if selected == "Home":
            st.session_state.current_page = "home"
        elif selected == "Batch Optimizer":
            switch_page("batch_optimizer")
        elif selected == "Analytics":
            switch_page("analytics")
        elif selected == "Competitor Analysis":
            switch_page("competitor_analysis")
        elif selected == "Settings":
            switch_page("settings")
        elif selected == "Account":
            switch_page("account")
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.caption("© 2025 Uday Kumar")
        st.sidebar.caption("100 Days of Python + AI Challenge")
    
    # Main content area - Home page
    if st.session_state.current_page == "home":
        render_home_page()

def render_home_page():
    # Header with animation
    col1, col2 = st.columns([3, 2])
    
    with col1:
        colored_header(
            label="YouTube Title Optimizer Pro",
            description="AI-Powered Title Optimization for Maximum Engagement",
            color_name="red-70",
        )
        st.markdown(
            """
            Transform your YouTube titles with advanced AI technology. Get data-driven, 
            SEO-optimized titles that increase clicks, engagement, and channel growth.
            """
        )
    
    with col2:
        lottie_animation = load_lottie("app/static/animations/youtube.json")
        st_lottie(lottie_animation, height=200, key="youtube_animation")
    
    # Quick stats dashboard
    if st.session_state.get("user_authenticated", False):
        metrics_dashboard = MetricsDashboard()
        metrics_dashboard.render()
    
    # Main optimization form
    with st.form(key="optimization_form"):
        st.subheader("🚀 Optimize Your YouTube Title")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            original_title = st.text_input(
                "Current Video Title",
                placeholder="e.g., My First Coding Tutorial",
                help="Enter your current or draft video title"
            )
            
            description = st.text_area(
                "Video Description",
                placeholder="Describe what your video is about...",
                help="A good description helps the AI understand your content better",
                height=100
            )
        
        with col2:
            # Advanced options in an expander
            with st.expander("Advanced Options", expanded=True):
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
                        "Music",
                        "Sports",
                        "News & Politics",
                        "Science & Technology",
                        "Arts & Crafts",
                        "Other"
                    ]
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    target_emotion = st.selectbox(
                        "Target Emotion",
                        options=[
                            "Curiosity",
                            "Urgency",
                            "Excitement",
                            "Surprise",
                            "FOMO",
                            "Achievement",
                            "Transformation",
                            "Relief",
                            "Amusement",
                            "Trust"
                        ]
                    )
                
                with col2:
                    content_type = st.selectbox(
                        "Content Type",
                        options=[
                            "Tutorial",
                            "Review",
                            "Vlog",
                            "Reaction",
                            "Challenge",
                            "Tips & Tricks",
                            "Behind the Scenes",
                            "Unboxing",
                            "Interview",
                            "Documentary",
                            "Case Study",
                            "News",
                            "Entertainment"
                        ]
                    )
                
                # AI model selection
                ai_model = st.selectbox(
                    "AI Model",
                    options=[
                        "Gemini Pro (Recommended)",
                        "Gemini Flash (Faster)",
                        "OpenAI GPT-4o",
                        "Claude 3 Opus",
                        "Ensemble (Multi-model)"
                    ]
                )
                
                # Optimization strength
                optimization_strength = st.slider(
                    "Optimization Strength",
                    min_value=1,
                    max_value=10,
                    value=7,
                    help="Higher values produce more aggressive optimization"
                )
        
        # Submit button
        submit_col1, submit_col2 = st.columns([3, 1])
        with submit_col1:
            submit_button = st.form_submit_button(
                "🚀 Optimize Title",
                use_container_width=True,
                type="primary"
            )
        with submit_col2:
            advanced_analysis = st.checkbox(
                "Include advanced analysis",
                value=True,
                help="Provides detailed metrics and competitor analysis"
            )
    
    # Process form submission
    if submit_button:
        if not original_title or not description:
            st.error("⚠️ Please provide both a title and description!")
        else:
            with st.spinner("Optimizing your title with AI..."):
                # Simulate API call with progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    # Simulate processing steps
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                # Call optimization API
                try:
                    # In a real app, this would be an actual API call
                    # response = requests.post(
                    #     f"{API_URL}/api/v1/optimize",
                    #     json={
                    #         "original_title": original_title,
                    #         "description": description,
                    #         "category": category,
                    #         "target_emotion": target_emotion,
                    #         "content_type": content_type,
                    #         "model": ai_model,
                    #         "strength": optimization_strength,
                    #         "advanced_analysis": advanced_analysis
                    #     }
                    # )
                    # result = response.json()
                    
                    # For demo, generate mock results
                    result = generate_mock_results(
                        original_title, 
                        description, 
                        category, 
                        target_emotion,
                        content_type
                    )
                    
                    # Store results in session state
                    st.session_state.last_result = result
                    
                    # Display results
                    display_optimization_results(result)
                    
                except Exception as e:
                    logger.error(f"Optimization error: {str(e)}")
                    st.error(f"❌ An error occurred: {str(e)}")

def generate_mock_results(original_title, description, category, emotion, content_type):
    """Generate sophisticated mock results for demonstration"""
    
    # Base structure for results
    results = {
        "improved_title": f"🔥 Ultimate Guide: {original_title} That Will Transform Your {category} Skills",
        "alternates": [
            f"How I {original_title} (Shocking {category} Results!)",
            f"The {emotion} Truth About {original_title} | {content_type} 2025",
            f"10 {category} Secrets: {original_title} Experts Don't Tell You"
        ],
        "reason": f"The optimized title leverages emotional triggers ({emotion}), uses power words, and includes SEO-friendly keywords for the {category} niche. The structure follows proven high-CTR patterns for {content_type} content.",
        "seo_score": 87,
        "emotional_hooks": ["curiosity", "achievement", "expertise"],
        "metrics": {
            "predicted_ctr": 8.7,
            "keyword_density": 4.2,
            "readability_score": 82,
            "emotional_impact": 76,
            "trend_alignment": 92
        },
        "keyword_analysis": {
            "primary_keywords": ["guide", category.lower(), content_type.lower()],
            "secondary_keywords": ["transform", "skills", "ultimate"],
            "missing_opportunities": ["how to", "tutorial", "beginner"]
        },
        "competitor_analysis": {
            "similar_videos": [
                {"title": f"How To Master {original_title} in 2025", "views": "1.2M", "ctr": "6.8%"},
                {"title": f"I Tried {original_title} For 30 Days", "views": "892K", "ctr": "7.2%"},
                {"title": f"{category} Masterclass: {original_title}", "views": "504K", "ctr": "5.9%"}
            ],
            "trending_patterns": ["numbered lists", "year in title", "emotional adjectives"]
        },
        "thumbnail_suggestions": [
            "Show before/after results with shocked expression",
            "Use bold text overlay with key benefit",
            "Include progress chart or graph for data-driven content"
        ],
        "a_b_test_recommendation": {
            "test_a": f"🔥 Ultimate Guide: {original_title} That Will Transform Your {category} Skills",
            "test_b": f"I Tried {original_title} For 30 Days (Shocking Results!)",
            "estimated_difference": "12% CTR improvement potential"
        }
    }
    
    return results

def display_optimization_results(result):
    """Display sophisticated optimization results"""
    
    # Success message
    st.success("✅ Title optimization complete!")
    
    # Main results in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Optimized Titles", 
        "🔍 Advanced Analysis", 
        "📈 Performance Metrics",
        "👁️ Visual Preview"
    ])
    
    with tab1:
        # Main optimized title
        st.subheader("🏆 Primary Recommendation")
        title_card = TitleCard(
            title=result["improved_title"],
            seo_score=result["seo_score"],
            emotional_hooks=result["emotional_hooks"]
        )
        title_card.render()
        
        # Alternative titles
        st.subheader("🔄 Alternative Suggestions")
        for i, alt_title in enumerate(result["alternates"], 1):
            with st.container():
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(f"**Option {i}:** {alt_title}")
                with cols[1]:
                    if st.button(f"Copy #{i}", key=f"copy_alt_{i}"):
                        st.session_state[f"copied_{i}"] = True
                        st.info(f"Copied option {i} to clipboard!")
        
        # Reasoning
        st.subheader("💡 Why This Works")
        st.markdown(result["reason"])
        
        # A/B Testing recommendation
        st.subheader("🧪 A/B Testing Recommendation")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Test A:** {result['a_b_test_recommendation']['test_a']}")
        with col2:
            st.info(f"**Test B:** {result['a_b_test_recommendation']['test_b']}")
        st.caption(f"Potential impact: {result['a_b_test_recommendation']['estimated_difference']}")
    
    with tab2:
        # Keyword analysis
        st.subheader("🔑 Keyword Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Primary Keywords**")
            for keyword in result["keyword_analysis"]["primary_keywords"]:
                st.markdown(f"- {keyword}")
        
        with col2:
            st.write("**Secondary Keywords**")
            for keyword in result["keyword_analysis"]["secondary_keywords"]:
                st.markdown(f"- {keyword}")
        
        with col3:
            st.write("**Opportunities**")
            for keyword in result["keyword_analysis"]["missing_opportunities"]:
                st.markdown(f"- {keyword}")
        
        # Competitor analysis
        st.subheader("🥇 Competitor Analysis")
        competitor_df = pd.DataFrame(result["competitor_analysis"]["similar_videos"])
        st.dataframe(competitor_df, use_container_width=True)
        
        st.write("**Trending Patterns**")
        for pattern in result["competitor_analysis"]["trending_patterns"]:
            st.markdown(f"- {pattern}")
        
        # Thumbnail suggestions
        st.subheader("🖼️ Thumbnail Suggestions")
        for suggestion in result["thumbnail_suggestions"]:
            st.markdown(f"- {suggestion}")
    
    with tab3:
        # Performance metrics
        st.subheader("📊 Predicted Performance")
        
        # Metrics in cards
        metrics_cols = st.columns(5)
        with metrics_cols[0]:
            st.metric("Predicted CTR", f"{result['metrics']['predicted_ctr']}%", "+2.3%")
        with metrics_cols[1]:
            st.metric("Keyword Density", f"{result['metrics']['keyword_density']}", "+1.5")
        with metrics_cols[2]:
            st.metric("Readability", f"{result['metrics']['readability_score']}/100", "+12")
        with metrics_cols[3]:
            st.metric("Emotional Impact", f"{result['metrics']['emotional_impact']}/100", "+18")
        with metrics_cols[4]:
            st.metric("Trend Alignment", f"{result['metrics']['trend_alignment']}%", "+5%")
        
        style_metric_cards()
        
        # Performance visualization
        with chart_container(["Radar Chart", "Bar Chart"]):
            # Create radar chart
            categories = list(result["metrics"].keys())
            values = list(result["metrics"].values())
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Optimized Title',
                line_color='rgba(255, 65, 54, 0.8)',
                fillcolor='rgba(255, 65, 54, 0.2)'
            ))
            
            # Add a baseline for comparison
            baseline_values = [5.5, 2.8, 65, 58, 70]
            fig.add_trace(go.Scatterpolar(
                r=baseline_values,
                theta=categories,
                fill='toself',
                name='Average Title',
                line_color='rgba(44, 160, 44, 0.8)',
                fillcolor='rgba(44, 160, 44, 0.2)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Visual preview
        st.subheader("👁️ YouTube Preview")
        youtube_preview = YouTubePreview(
            title=result["improved_title"],
            thumbnail_url="app/static/img/thumbnail_preview.jpg"
        )
        youtube_preview.render()
        
        # Mobile preview
        st.subheader("📱 Mobile Preview")
        st.image("app/static/img/mobile_preview.png", use_column_width=True)
        
        # Generate thumbnail button
        if st.button("🖼️ Generate AI Thumbnail", type="primary"):
            with st.spinner("Generating thumbnail..."):
                time.sleep(2)
                st.image("app/static/img/ai_thumbnail.jpg", use_column_width=True)
                st.download_button(
                    label="Download Thumbnail",
                    data=open("app/static/img/ai_thumbnail.jpg", "rb").read(),
                    file_name="optimized_thumbnail.jpg",
                    mime="image/jpeg"
                )

if __name__ == "__main__":
    main()
