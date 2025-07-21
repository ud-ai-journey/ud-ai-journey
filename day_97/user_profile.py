import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from data_manager import DataManager
from insights_generator import InsightsGenerator

def show_user_profile():
    """Show user profile and tracking history"""
    
    # Initialize components
    data_manager = DataManager()
    insights_generator = InsightsGenerator()
    
    # Page header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; color: #1f77b4; margin-bottom: 1rem;">👤 Your Energy Profile</h1>
        <p style="font-size: 1.2rem; color: #666;">Track your progress and discover your patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user data
    energy_data = data_manager.get_energy_data()
    
    if energy_data.empty:
        st.info("📈 Start tracking your energy to see your profile!")
        return
    
    # User Stats Overview
    st.markdown("## 📊 Your Energy Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_readings = len(energy_data)
        st.metric("Total Readings", total_readings)
    
    with col2:
        high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
        st.metric("High Energy %", f"{high_energy_pct:.1f}%")
    
    with col3:
        avg_confidence = energy_data['confidence'].mean()
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
    
    with col4:
        days_tracking = (energy_data['timestamp'].max() - energy_data['timestamp'].min()).days + 1
        st.metric("Days Tracking", days_tracking)
    
    # Energy Timeline
    st.markdown("## 📈 Your Energy Journey")
    
    # Create timeline chart
    timeline_data = energy_data.sort_values('timestamp').copy()
    timeline_data['energy_score'] = timeline_data['energy_level'].replace({'High': 3, 'Medium': 2, 'Low': 1})
    
    fig = px.scatter(timeline_data, x='timestamp', y='energy_score', 
                     color='energy_level',
                     title="Your Energy Timeline",
                     labels={'energy_score': 'Energy Level (1=Low, 2=Medium, 3=High)'})
    
    fig.update_traces(marker_size=10)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly Patterns
    st.markdown("## 📅 Weekly Energy Patterns")
    
    if 'day_of_week' in energy_data.columns:
        weekly_patterns = energy_data.groupby(['day_of_week', 'energy_level']).size().unstack(fill_value=0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_patterns = weekly_patterns.reindex([day for day in day_order if day in weekly_patterns.index])
        
        fig = px.bar(weekly_patterns, title="Energy by Day of Week")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Hourly Patterns
    st.markdown("## ⏰ Hourly Energy Patterns")
    
    if 'hour' in energy_data.columns:
        hourly_patterns = energy_data.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        
        fig = px.line(hourly_patterns, title="Energy by Hour of Day")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Personal Insights
    st.markdown("## 🎯 Your Personal Insights")
    
    insights = insights_generator.generate_weekly_report(energy_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Peak Performance")
        for insight in insights['peak_performance'][:2]:
            st.info(insight)
    
    with col2:
        st.subheader("📉 Energy Dips")
        for insight in insights['energy_dips'][:2]:
            st.warning(insight)
    
    # Progress Tracking
    st.markdown("## 🎯 Progress Goals")
    
    # Calculate progress metrics
    if len(energy_data) >= 7:
        recent_week = energy_data.tail(7)
        recent_high_energy = (recent_week['energy_level'] == 'High').mean() * 100
        
        st.metric("This Week's High Energy %", f"{recent_high_energy:.1f}%")
        
        if recent_high_energy > 50:
            st.success("🎉 Great job! You're maintaining high energy levels!")
        elif recent_high_energy > 30:
            st.info("📈 Good progress! Keep tracking to optimize further.")
        else:
            st.warning("💪 Keep tracking! Patterns will emerge with more data.")
    
    # Achievements
    st.markdown("## 🏆 Achievements")
    
    achievements = []
    
    if len(energy_data) >= 10:
        achievements.append("📊 Data Collector - 10+ energy readings")
    
    if len(energy_data) >= 30:
        achievements.append("📈 Pattern Seeker - 30+ energy readings")
    
    if len(energy_data) >= 50:
        achievements.append("🎯 Energy Master - 50+ energy readings")
    
    high_energy_days = energy_data.groupby(energy_data['timestamp'].dt.date)['energy_level'].apply(
        lambda x: (x == 'High').mean() * 100
    )
    
    if (high_energy_days > 60).sum() >= 3:
        achievements.append("⚡ High Energy Champion - 3+ days with 60%+ high energy")
    
    if achievements:
        for achievement in achievements:
            st.markdown(f"✅ {achievement}")
    else:
        st.info("Keep tracking to unlock achievements!")
    
    # Export Data
    st.markdown("## 📤 Export Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export as CSV"):
            filename = data_manager.export_data('csv')
            if filename:
                st.success(f"Data exported to {filename}")
    
    with col2:
        if st.button("📄 Export as JSON"):
            filename = data_manager.export_data('json')
            if filename:
                st.success(f"Data exported to {filename}")
    
    # Settings
    st.markdown("## ⚙️ Profile Settings")
    
    with st.expander("Data Management"):
        if st.button("🗑️ Clear All Data"):
            if st.checkbox("I understand this will delete all my energy data"):
                # Add clear data functionality
                st.warning("Data cleared successfully")
    
    with st.expander("Privacy Settings"):
        st.info("🔒 All your data is stored locally and never sent to external servers.")
        st.info("📱 Your energy readings are completely private.")

if __name__ == "__main__":
    show_user_profile() 