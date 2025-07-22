import streamlit as st
import pandas as pd
import plotly.express as px
from auth_system import AuthSystem

def show_new_landing_page():
    """Show landing page with Gmail authentication"""
    
    # Initialize auth system
    auth = AuthSystem()
    
    # Check if user is already logged in
    current_user = auth.get_current_user()
    
    if current_user:
        # User is logged in - show personalized dashboard
        show_user_dashboard(auth, current_user)
    else:
        # Show login page
        show_login_page(auth)

def show_login_page(auth):
    """Show Gmail login page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 4rem; color: #1f77b4; margin-bottom: 1rem;">⚡ Energy Lens</h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 2rem;">Discover your energy patterns to optimize productivity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 Track Your Energy, Optimize Your Life
        
        **Energy Lens** uses AI to analyze your facial expressions and detect your energy levels throughout the day. 
        
        ### ✨ What you'll discover:
        - **Peak Performance Times** - When you're most productive
        - **Energy Patterns** - Daily and weekly trends
        - **Productivity Insights** - Personalized optimization tips
        - **LinkedIn-Ready Reports** - Share your progress
        
        ### 🔒 Privacy First
        - All data stored locally on your device
        - No data sent to external servers
        - Your energy readings are completely private
        """)
    
    with col2:
        st.markdown("""
        ## 📊 See Your Patterns
        
        Track your energy levels and discover when you're most productive. 
        Our AI analyzes your facial expressions to give you real-time insights.
        """)
        
        # Demo chart
        demo_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01 09:00', periods=8, freq='2H'),
            'energy': [2, 3, 3, 2, 1, 2, 3, 2]
        })
        
        fig = px.line(demo_data, x='time', y='energy', 
                     title="Your Energy Throughout the Day",
                     labels={'energy': 'Energy Level (1=Low, 2=Medium, 3=High)'})
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Login section
    st.markdown("## 🔐 Get Started")
    
    with st.container():
        st.markdown("""
        ### Sign in with your Gmail to start tracking your energy patterns
        """)
        
        # Gmail login form
        with st.form("gmail_login"):
            email = st.text_input("📧 Gmail Address", placeholder="your.email@gmail.com")
            name = st.text_input("👤 Your Name (Optional)", placeholder="Your name")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.form_submit_button("🚀 Start Tracking", type="primary", use_container_width=True):
                    if email and '@gmail.com' in email:
                        # Login user
                        user_id = auth.login_user(email, name)
                        st.success(f"Welcome back, {auth.get_current_user()['name']}! 🎉")
                        st.rerun()
                    else:
                        st.error("Please enter a valid Gmail address")
            
            with col2:
                if st.form_submit_button("👀 Take a Tour", use_container_width=True):
                    st.info("🎯 Tour coming soon! Sign in to start tracking your energy.")
    
    # Social proof
    st.divider()
    st.markdown("## 👥 What Users Are Saying")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        > *"Finally understand when I'm most productive! This app changed my work routine completely."*
        > 
        > **- Sarah M., Product Manager**
        """)
    
    with col2:
        st.markdown("""
        > *"The LinkedIn reports are gold! My network loves seeing my energy optimization journey."*
        > 
        > **- Mike R., Consultant**
        """)
    
    with col3:
        st.markdown("""
        > *"Privacy-first approach is exactly what I needed. My data stays on my device."*
        > 
        > **- Lisa K., Developer**
        """)

def show_user_dashboard(auth, user):
    """Show personalized dashboard for logged-in user"""
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; color: #1f77b4; margin-bottom: 1rem;">Welcome back, {user['name']}! 👋</h1>
        <p style="font-size: 1.2rem; color: #666;">Ready to optimize your energy today?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User stats
    stats = auth.get_user_stats()
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Readings", stats['total_readings'])
        
        with col2:
            st.metric("High Energy %", f"{stats['high_energy_percentage']:.1f}%")
        
        with col3:
            st.metric("Avg Confidence", f"{stats['avg_confidence']:.1f}%")
        
        with col4:
            st.metric("Days Tracking", "7+")  # Placeholder
        
        # Quick actions
        st.markdown("## 🎯 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📸 Check Energy Now", type="primary", use_container_width=True):
                st.success("🎯 Energy tracking ready! Use the navigation menu above to access the tracker.")
        
        with col2:
            if st.button("📊 View Profile", use_container_width=True):
                st.info("👤 Profile view coming soon!")
        
        with col3:
            if st.button("📤 Generate Report", use_container_width=True):
                st.info("📊 Report generation coming soon!")
        
        # Recent activity
        energy_data = auth.get_user_energy_data()
        if not energy_data.empty:
            st.markdown("## 📈 Recent Activity")
            
            recent_data = energy_data.head(5)
            for _, row in recent_data.iterrows():
                energy_class = f"energy-{str(row['energy_level']).lower()}"
                st.markdown(f"""
                <div style="padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa; border-radius: 0.5rem;">
                    <span class="{energy_class}">{row['energy_level']}</span> energy 
                    ({row['confidence']:.1f}% confidence) - {row['timestamp'].strftime('%I:%M %p')}
                </div>
                """, unsafe_allow_html=True)
    
    # Logout option
    st.divider()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Ready to track your energy patterns?")
    
    with col2:
        if st.button("🚪 Logout"):
            auth.logout_user()
            st.success("Logged out successfully!")
            st.rerun()

if __name__ == "__main__":
    show_new_landing_page() 