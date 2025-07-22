import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import os
from energy_detector import EnergyDetector
from auth_system import AuthSystem
from pattern_analyzer import PatternAnalyzer
from visualizations import create_energy_chart, create_pattern_insights
from insights_generator import InsightsGenerator

# Page config
st.set_page_config(
    page_title="Energy Lens - Your Personal Energy Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .energy-high { color: #2ecc71; font-weight: bold; }
    .energy-medium { color: #f39c12; font-weight: bold; }
    .energy-low { color: #e74c3c; font-weight: bold; }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .user-welcome {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize components
    auth = AuthSystem()
    energy_detector = EnergyDetector()
    pattern_analyzer = PatternAnalyzer()
    insights_generator = InsightsGenerator()
    
    # Check authentication
    current_user = auth.get_current_user()
    
    if not current_user:
        # Redirect to login
        st.error("Please log in to access Energy Lens")
        st.button("🔐 Go to Login", on_click=lambda: st.session_state.update({'page': '🏠 Home'}))
        return
    
    # User is authenticated - show personalized app
    show_authenticated_app(auth, current_user, energy_detector, pattern_analyzer, insights_generator)

def show_authenticated_app(auth, user, energy_detector, pattern_analyzer, insights_generator):
    """Show the main app for authenticated users"""
    
    # Header with user info
    st.markdown(f"""
    <div class="user-welcome">
        <h1>⚡ Energy Lens</h1>
        <p>Welcome back, {user['name']}! Let's optimize your energy today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Home"):
            st.session_state['page'] = "🏠 Home"
            st.rerun()
    
    with col2:
        if st.button("🎯 Energy Tracker"):
            st.session_state['page'] = "🎯 Energy Tracker"
            st.rerun()
    
    with col3:
        if st.button("📊 Weekly Report"):
            st.session_state['page'] = "📊 Weekly Report"
            st.rerun()
    
    with col4:
        if st.button("👤 Profile"):
            st.session_state['page'] = "👤 Profile"
            st.rerun()
    
    with col5:
        if st.button("🚪 Logout"):
            auth.logout_user()
            st.success("Logged out successfully!")
            st.rerun()
    
    st.divider()
    
    # Sidebar for energy tracking
    with st.sidebar:
        st.header("🎯 Quick Energy Check")
        
        # Energy Check
        st.subheader("📸 Energy Check")
        energy_check_method = st.radio(
            "Choose input method:",
            ["📷 Take Photo", "📁 Upload Image"]
        )
        
        if energy_check_method == "📷 Take Photo":
            photo = st.camera_input("Take a photo for energy analysis")
            if photo:
                if st.button("🔍 Analyze Energy"):
                    with st.spinner("Analyzing your energy level..."):
                        energy_level, confidence = energy_detector.detect_energy(photo)
                        st.success(f"Energy Level: {energy_level} ({confidence:.1f}% confidence)")
                        
                        # Save to user's database
                        if auth.save_energy_record(energy_level, confidence):
                            st.balloons()
                        else:
                            st.error("Failed to save energy record")
        
        else:
            uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
            if uploaded_file and st.button("🔍 Analyze Energy"):
                with st.spinner("Analyzing your energy level..."):
                    energy_level, confidence = energy_detector.detect_energy(uploaded_file)
                    st.success(f"Energy Level: {energy_level} ({confidence:.1f}% confidence)")
                    
                    # Save to user's database
                    if auth.save_energy_record(energy_level, confidence):
                        st.balloons()
                    else:
                        st.error("Failed to save energy record")
        
        st.divider()
        
        # Manual Entry
        st.subheader("✏️ Manual Entry")
        manual_energy = st.selectbox("Energy Level:", ["High", "Medium", "Low"])
        if st.button("💾 Save Manual Entry"):
            if auth.save_energy_record(manual_energy, 100.0):
                st.success("Entry saved!")
            else:
                st.error("Failed to save entry")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Your Energy Patterns")
        
        # Get user's energy data
        energy_data = auth.get_user_energy_data()
        
        if not energy_data.empty:
            # Energy trend chart
            fig = create_energy_chart(energy_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Pattern insights
            insights = pattern_analyzer.analyze_patterns(energy_data)
            if insights:
                st.subheader("🎯 Key Insights")
                for insight in insights:
                    st.info(insight)
        else:
            st.info("📈 Start tracking your energy to see patterns emerge!")
    
    with col2:
        st.header("📈 Today's Stats")
        
        # Get today's data for current user
        if not energy_data.empty and 'timestamp' in energy_data.columns:
            # Ensure timestamp is datetime
            energy_data['timestamp'] = pd.to_datetime(energy_data['timestamp'], errors='coerce')
            today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
        else:
            today_data = pd.DataFrame()
        
        if not today_data.empty:
            avg_energy = today_data['energy_level'].mode().iloc[0] if not today_data.empty else 'Medium'
            energy_class = f"energy-{str(avg_energy).lower()}"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>Average Energy</h3>
                <p class="{energy_class}">{avg_energy}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric("Records Today", len(today_data))
            st.metric("Confidence Avg", f"{today_data['confidence'].mean():.1f}%")
        else:
            st.info("No data for today yet!")
    
    # Bottom section
    st.divider()
    
    # Weekly Insights Report
    st.header("📊 Weekly Energy Insights Report")
    
    # Generate insights for current user
    weekly_insights = insights_generator.generate_weekly_report(energy_data)
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        # Summary stats
        summary = weekly_insights['summary']
        st.subheader("📈 This Week's Summary")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Readings", summary['total_readings'])
        with col_b:
            st.metric("High Energy %", f"{summary['high_energy_percentage']:.1f}%")
        with col_c:
            st.metric("Avg Confidence", f"{summary['avg_confidence']:.1f}%")
        
        # Key discoveries
        st.subheader("🎯 Key Discoveries")
        for discovery in weekly_insights['peak_performance'] + weekly_insights['pattern_discoveries']:
            st.info(discovery)
        
        # Productivity tips
        st.subheader("💡 Productivity Tips")
        for tip in weekly_insights['productivity_tips']:
            st.write(f"• {tip}")
    
    with col4:
        # Next week goals
        st.subheader("🎯 Next Week Goals")
        for goal in weekly_insights['next_week_goals']:
            st.write(f"• {goal}")
        
        st.divider()
        
        # Shareable content
        st.subheader("📤 Share Your Insights")
        shareable_quote = weekly_insights['shareable_quote']
        st.text_area("LinkedIn Post", shareable_quote, height=150)
        
        if st.button("📋 Copy LinkedIn Post"):
            st.success("LinkedIn post copied to clipboard!")

if __name__ == "__main__":
    main() 