import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import hashlib
import os
from energy_detector import EnergyDetector
from pattern_analyzer import PatternAnalyzer
from insights_generator import InsightsGenerator

# Page config
st.set_page_config(
    page_title="Energy Lens - Your Personal Energy Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 3rem; font-weight: bold; color: #1f77b4; text-align: center; margin-bottom: 2rem; }
    .energy-high { color: #2ecc71; font-weight: bold; }
    .energy-medium { color: #f39c12; font-weight: bold; }
    .energy-low { color: #e74c3c; font-weight: bold; }
    .metric-card { background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4; }
    .user-welcome { background: linear-gradient(90deg, #1f77b4, #ff7f0e); color: white; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

def get_today_count(energy_data):
    """Safely get today's energy reading count"""
    try:
        # Ensure timestamp column is datetime
        energy_data['timestamp'] = pd.to_datetime(energy_data['timestamp'], errors='coerce')
        today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
        return len(today_data)
    except:
        return len(energy_data)  # Fallback to total count

class AuthSystem:
    def __init__(self):
        self.db_path = "user_data.db"
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                energy_level TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hour INTEGER,
                day_of_week TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def login_user(self, email, name=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            user_id, existing_name = user
            cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
            name = existing_name or name
        else:
            cursor.execute("INSERT INTO users (email, name) VALUES (?, ?)", (email, name or email.split('@')[0]))
            user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        st.session_state['user_id'] = user_id
        st.session_state['user_email'] = email
        st.session_state['user_name'] = name
        st.session_state['is_authenticated'] = True
        
        return user_id
    
    def logout_user(self):
        for key in ['user_id', 'user_email', 'user_name', 'is_authenticated']:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self):
        if st.session_state.get('is_authenticated'):
            return {
                'id': st.session_state.get('user_id'),
                'email': st.session_state.get('user_email'),
                'name': st.session_state.get('user_name')
            }
        return None
    
    def save_energy_record(self, energy_level, confidence):
        user = self.get_current_user()
        if not user:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now()
        hour = timestamp.hour
        day_of_week = timestamp.strftime('%A')
        
        cursor.execute('''
            INSERT INTO energy_data (user_id, energy_level, confidence, timestamp, hour, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user['id'], energy_level, confidence, timestamp, hour, day_of_week))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_energy_data(self):
        user = self.get_current_user()
        if not user:
            return pd.DataFrame()
        
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT energy_level, confidence, timestamp, hour, day_of_week
            FROM energy_data 
            WHERE user_id = ?
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=[user['id']])
        conn.close()
        
        if not df.empty:
            # Ensure timestamp is properly converted
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            # Remove any rows with invalid timestamps
            df = df.dropna(subset=['timestamp'])
        
        return df

def show_landing_page():
    """Show landing page with optional Gmail login"""
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 4rem; color: #1f77b4; margin-bottom: 1rem;">⚡ Energy Lens</h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 2rem;">Discover when you do your best work</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 Track Your Energy, Discover Your Rhythm
        
        **Energy Lens** helps you understand your natural energy patterns throughout the day. 
        
        ### ✨ What you'll discover:
        - **Your Peak Hours** - When you're naturally most focused
        - **Energy Patterns** - Daily and weekly trends in your work
        - **Productivity Insights** - When to schedule important vs routine tasks
        - **Shareable Reports** - Document your energy optimization journey
        
        ### 🔒 Privacy First
        - All data stored locally on your device
        - No data sent to external servers
        - Your energy readings are completely private
        """)
    
    with col2:
        st.markdown("## 📊 See Your Patterns")
        
        demo_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01 09:00', periods=8, freq='2H'),
            'energy': [2, 3, 3, 2, 1, 2, 3, 2]
        })
        
        fig = px.line(demo_data, x='time', y='energy', 
                     title="Example: Your Energy Throughout the Day",
                     labels={'energy': 'Energy Level (1=Low, 2=Medium, 3=High)'})
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("## 🚀 Start Your Energy Journey")
    
    with st.container():
        st.markdown("""
        ### Ready to discover your energy patterns?
        
        **Get started in seconds:**
        """)
        
        # Simple start with optional name
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("quick_start"):
                name = st.text_input("Your Name (Optional)", placeholder="Enter your name or leave blank")
                
                if st.form_submit_button("🎯 Start Tracking Now", type="primary", use_container_width=True):
                    # Create user with optional name
                    auth = AuthSystem()
                    if name and name.strip():
                        user_name = name.strip()
                    else:
                        user_name = "You"
                    
                    # Generate consistent user ID based on session
                    if 'persistent_user_id' not in st.session_state:
                        import secrets
                        st.session_state.persistent_user_id = f"user_{secrets.token_hex(8)}"
                    
                    anonymous_email = f"{st.session_state.persistent_user_id}@local.com"
                    user_id = auth.login_user(anonymous_email, user_name)
                    st.success(f"Welcome, {user_name}! Start tracking your energy patterns.")
                    st.rerun()
        
        with col2:
            st.markdown("""
            **✨ What you'll get:**
            - 📊 Beautiful energy visualizations
            - 🎯 Personalized insights
            - 📈 Pattern analysis
            - 💡 Productivity tips
            """)
    
    # Real user experience
    st.divider()
    st.markdown("## 👥 Real User Experience")
    
    st.markdown("""
    > *"Building this app taught me the difference between 'works on my machine' and 'real users can actually use it.' 
    > 
    > I discovered that session management is everything - users need their data to persist across refreshes. 
    > The manual entry option became my favorite feature for tracking energy after meetings and long coding sessions.
    > 
    > Most importantly, I learned that realistic AI expectations beat overpromising every time."*
    > 
    > **- Uday Kumar Boya, Developer & Creator**
    """)
    
    st.markdown("""
    **🎯 Want to share your experience?** 
    Test the app and let me know what you discover about your energy patterns!
    """)

def show_main_app():
    """Show main app for authenticated users"""
    
    auth = AuthSystem()
    current_user = auth.get_current_user()
    
    if not current_user:
        st.error("Please log in to access Energy Lens")
        return
    
    energy_detector = EnergyDetector()
    pattern_analyzer = PatternAnalyzer()
    insights_generator = InsightsGenerator()
    
    # Header
    st.markdown(f"""
    <div class="user-welcome">
        <h1>⚡ Energy Lens</h1>
        <p>Welcome back, {current_user['name']}! Let's optimize your energy today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home"):
            # Clear all session states to return to main dashboard
            for key in ['show_energy_check', 'show_data']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("📸 Energy Check"):
            st.session_state['show_energy_check'] = True
            st.rerun()
    
    with col3:
        if st.button("📊 Your Data"):
            st.session_state['show_data'] = True
            st.session_state['show_energy_check'] = False  # Clear other states
            st.rerun()
    
    with col4:
        if st.button("🚪 Logout"):
            # Clear all session states and logout
            for key in ['show_energy_check', 'show_data', 'persistent_user_id']:
                if key in st.session_state:
                    del st.session_state[key]
            auth.logout_user()
            st.rerun()
    

    
    st.divider()
    
    # Energy Check Section
    if st.session_state.get('show_energy_check'):
        st.header("📸 Energy Check")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Take Photo")
            st.info("💡 Tip: Good lighting and clear face work best")
            photo = st.camera_input("Take a photo for energy analysis")
            if photo and st.button("🔍 Analyze Energy"):
                with st.spinner("Analyzing your energy level..."):
                    energy_level, confidence = energy_detector.detect_energy(photo)
                    
                    # Save the record first
                    if auth.save_energy_record(energy_level, confidence):
                        st.balloons()
                        
                        # Show immediate insights
                        st.success(f"🎯 Energy Level: {energy_level} ({confidence:.1f}% confidence)")
                        
                        # Get user's data for context
                        energy_data = auth.get_user_energy_data()
                        
                        if not energy_data.empty:
                            st.markdown("### 💡 What This Means For You Today:")
                            
                            # Today's context
                            today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
                            today_count = len(today_data)
                            
                            if today_count == 1:
                                st.info("🌟 This is your first energy reading today - great start!")
                            else:
                                st.info(f"📊 This is your {today_count}rd energy reading today")
                            
                            # Energy-specific insights
                            if energy_level == "High":
                                st.success("🚀 You're in your peak zone! Schedule important work now.")
                                st.markdown("- Perfect time for creative tasks")
                                st.markdown("- Great for important decisions")
                                st.markdown("- Consider blocking 2-3 hours for focused work")
                            elif energy_level == "Medium":
                                st.warning("⚖️ You're in a balanced state - good for varied tasks.")
                                st.markdown("- Mix high-focus and routine work")
                                st.markdown("- Good time for meetings and collaboration")
                                st.markdown("- Consider taking short breaks between tasks")
                            else:
                                st.error("😴 You're in a low energy state - time for lighter activities.")
                                st.markdown("- Plan routine or administrative tasks")
                                st.markdown("- Consider taking a short break")
                                st.markdown("- Avoid important decisions right now")
                            
                            # Pattern insights
                            if len(energy_data) >= 3:
                                st.markdown("### 📈 Your Pattern This Week:")
                                high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
                                st.metric("High Energy %", f"{high_energy_pct:.1f}%")
                                
                                if high_energy_pct > 60:
                                    st.success("🔥 You're maintaining high energy levels - keep it up!")
                                elif high_energy_pct > 30:
                                    st.info("📈 Good energy balance - consider optimizing your peak hours")
                                else:
                                    st.warning("💪 Focus on identifying what boosts your energy")
                        else:
                            st.info("🎯 Great first reading! Track a few more to see your patterns emerge.")
                    else:
                        st.error("Failed to save energy record")
        
        with col2:
            st.subheader("📁 Upload Image")
            st.info("💡 Tip: Clear, well-lit photos work best")
            uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
            if uploaded_file and st.button("🔍 Analyze Uploaded Image"):
                with st.spinner("Analyzing your energy level..."):
                    energy_level, confidence = energy_detector.detect_energy(uploaded_file)
                    
                    # Save the record first
                    if auth.save_energy_record(energy_level, confidence):
                        st.balloons()
                        
                        # Show immediate insights
                        st.success(f"🎯 Energy Level: {energy_level} ({confidence:.1f}% confidence)")
                        
                        # Get user's data for context
                        energy_data = auth.get_user_energy_data()
                        
                        if not energy_data.empty:
                            st.markdown("### 💡 What This Means For You Today:")
                            
                            # Today's context
                            today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
                            today_count = len(today_data)
                            
                            if today_count == 1:
                                st.info("🌟 This is your first energy reading today - great start!")
                            else:
                                st.info(f"📊 This is your {today_count}rd energy reading today")
                            
                            # Energy-specific insights
                            if energy_level == "High":
                                st.success("🚀 You're in your peak zone! Schedule important work now.")
                                st.markdown("- Perfect time for creative tasks")
                                st.markdown("- Great for important decisions")
                                st.markdown("- Consider blocking 2-3 hours for focused work")
                            elif energy_level == "Medium":
                                st.warning("⚖️ You're in a balanced state - good for varied tasks.")
                                st.markdown("- Mix high-focus and routine work")
                                st.markdown("- Good time for meetings and collaboration")
                                st.markdown("- Consider taking short breaks between tasks")
                            else:
                                st.error("😴 You're in a low energy state - time for lighter activities.")
                                st.markdown("- Plan routine or administrative tasks")
                                st.markdown("- Consider taking a short break")
                                st.markdown("- Avoid important decisions right now")
                            
                            # Pattern insights
                            if len(energy_data) >= 3:
                                st.markdown("### 📈 Your Pattern This Week:")
                                high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
                                st.metric("High Energy %", f"{high_energy_pct:.1f}%")
                                
                                if high_energy_pct > 60:
                                    st.success("🔥 You're maintaining high energy levels - keep it up!")
                                elif high_energy_pct > 30:
                                    st.info("📈 Good energy balance - consider optimizing your peak hours")
                                else:
                                    st.warning("💪 Focus on identifying what boosts your energy")
                        else:
                            st.info("🎯 Great first reading! Track a few more to see your patterns emerge.")
                    else:
                        st.error("Failed to save energy record")
        
        st.divider()
        
        # Manual Entry
        st.subheader("✏️ Manual Entry")
        manual_energy = st.selectbox("Energy Level:", ["High", "Medium", "Low"])
        if st.button("💾 Save Manual Entry"):
            if auth.save_energy_record(manual_energy, 100.0):
                st.success("✅ Manual entry saved!")
                
                # Show immediate insights for manual entry too
                energy_data = auth.get_user_energy_data()
                
                if not energy_data.empty:
                    st.markdown("### 💡 What This Means For You Today:")
                    
                    # Today's context
                    today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
                    today_count = len(today_data)
                    
                    if today_count == 1:
                        st.info("🌟 This is your first energy reading today - great start!")
                    else:
                        st.info(f"📊 This is your {today_count}rd energy reading today")
                    
                    # Energy-specific insights
                    if manual_energy == "High":
                        st.success("🚀 You're in your peak zone! Schedule important work now.")
                        st.markdown("- Perfect time for creative tasks")
                        st.markdown("- Great for important decisions")
                        st.markdown("- Consider blocking 2-3 hours for focused work")
                    elif manual_energy == "Medium":
                        st.warning("⚖️ You're in a balanced state - good for varied tasks.")
                        st.markdown("- Mix high-focus and routine work")
                        st.markdown("- Good time for meetings and collaboration")
                        st.markdown("- Consider taking short breaks between tasks")
                    else:
                        st.error("😴 You're in a low energy state - time for lighter activities.")
                        st.markdown("- Plan routine or administrative tasks")
                        st.markdown("- Consider taking a short break")
                        st.markdown("- Avoid important decisions right now")
                    
                    # Pattern insights
                    if len(energy_data) >= 3:
                        st.markdown("### 📈 Your Pattern This Week:")
                        high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
                        st.metric("High Energy %", f"{high_energy_pct:.1f}%")
                        
                        if high_energy_pct > 60:
                            st.success("🔥 You're maintaining high energy levels - keep it up!")
                        elif high_energy_pct > 30:
                            st.info("📈 Good energy balance - consider optimizing your peak hours")
                        else:
                            st.warning("💪 Focus on identifying what boosts your energy")
                else:
                    st.info("🎯 Great first reading! Track a few more to see your patterns emerge.")
            else:
                st.error("Failed to save entry")
    
    # Data Visualization Section
    elif st.session_state.get('show_data'):
        st.header("📊 Your Energy Data")
        
        try:
            energy_data = auth.get_user_energy_data()
            
            if not energy_data.empty:
                st.success(f"✅ Found {len(energy_data)} energy readings")
                
                # Show raw data first
                st.subheader("📋 Your Energy Records")
                st.dataframe(energy_data.head(10))
                
                # Beautiful Energy Charts
                try:
                    from visualizations import create_energy_chart, create_pattern_insights, create_weekly_summary
                    
                    # Main energy analysis chart
                    st.subheader("📈 Energy Pattern Analysis")
                    energy_chart = create_energy_chart(energy_data)
                    st.plotly_chart(energy_chart, use_container_width=True)
                    
                    # Pattern insights
                    insights_chart = create_pattern_insights(energy_data)
                    if insights_chart:
                        st.subheader("🎯 Detection Insights")
                        st.plotly_chart(insights_chart, use_container_width=True)
                    
                    # Weekly summary if we have enough data
                    if len(energy_data) >= 3:
                        weekly_chart = create_weekly_summary(energy_data)
                        if weekly_chart:
                            st.subheader("📅 Weekly Energy Summary")
                            st.plotly_chart(weekly_chart, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Advanced charts failed: {e}")
                    # Fallback to simple chart
                    try:
                        timeline_data = energy_data.sort_values('timestamp').copy()
                        timeline_data['energy_score'] = timeline_data['energy_level'].replace({'High': 3, 'Medium': 2, 'Low': 1})
                        
                        fig = px.scatter(timeline_data, x='timestamp', y='energy_score', 
                                       color='energy_level', title="Your Energy Timeline")
                        fig.update_traces(marker_size=10)
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e2:
                        st.error(f"Simple chart also failed: {e2}")
                
                # Pattern insights
                try:
                    insights = pattern_analyzer.analyze_patterns(energy_data)
                    if insights:
                        st.subheader("🎯 Key Insights")
                        for insight in insights:
                            st.info(insight)
                    else:
                        st.info("📈 Track more data to get personalized insights")
                except Exception as e:
                    st.error(f"Insights generation failed: {e}")
                
                # Add actionable tips
                st.subheader("💡 Actionable Tips")
                st.markdown("""
                - **Schedule important tasks** during your peak energy hours
                - **Plan routine work** during your energy dips
                - **Take breaks** when energy is consistently low
                - **Track patterns** for 1-2 weeks for better insights
                """)
                
                # Quick stats
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Readings", len(energy_data))
                
                with col2:
                    high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
                    st.metric("High Energy %", f"{high_energy_pct:.1f}%")
                
                with col3:
                    avg_confidence = energy_data['confidence'].mean()
                    st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
                    
            else:
                st.info("📈 Start tracking your energy to see patterns emerge!")
                st.markdown("""
                **To get started:**
                1. Use the camera to take a photo
                2. Upload an image
                3. Or manually enter your energy level
                
                Track a few readings to see your patterns!
                """)
                
        except Exception as e:
            st.error(f"Data loading failed: {e}")
            st.info("Try refreshing the page or logging in again")
    
    # Default view - show beautiful dashboard
    else:
        st.header("📊 Your Energy Dashboard")
        
        energy_data = auth.get_user_energy_data()
        
        if not energy_data.empty:
            # Quick stats at the top
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Readings", len(energy_data))
            
            with col2:
                high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
                st.metric("High Energy %", f"{high_energy_pct:.1f}%")
            
            with col3:
                avg_confidence = energy_data['confidence'].mean()
                st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
            
            with col4:
                days_tracking = (energy_data['timestamp'].max() - energy_data['timestamp'].min()).days + 1
                st.metric("Days Tracking", days_tracking)
            
            # Beautiful charts
            try:
                from visualizations import create_energy_chart, create_pattern_insights, create_productivity_chart, create_energy_trend, create_weekly_summary
                
                # Main energy chart
                st.subheader("📈 Your Energy Journey")
                energy_chart = create_energy_chart(energy_data)
                st.plotly_chart(energy_chart, use_container_width=True)
                
                # Additional insights in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    # Productivity chart
                    productivity_chart = create_productivity_chart(energy_data)
                    if productivity_chart:
                        st.subheader("🎯 Productivity Score")
                        st.plotly_chart(productivity_chart, use_container_width=True)
                
                with col2:
                    # Pattern insights
                    insights_chart = create_pattern_insights(energy_data)
                    if insights_chart:
                        st.subheader("📊 Detection Insights")
                        st.plotly_chart(insights_chart, use_container_width=True)
                
                # Energy trend if we have enough data
                if len(energy_data) >= 3:
                    trend_chart = create_energy_trend(energy_data)
                    if trend_chart:
                        st.subheader("📈 Energy Trend Analysis")
                        st.plotly_chart(trend_chart, use_container_width=True)
                
                # Weekly summary if we have enough data
                if len(energy_data) >= 5:
                    weekly_chart = create_weekly_summary(energy_data)
                    if weekly_chart:
                        st.subheader("📅 Weekly Energy Heatmap")
                        st.plotly_chart(weekly_chart, use_container_width=True)
                
            except Exception as e:
                st.error(f"Chart creation failed: {e}")
                # Fallback to simple display
                st.subheader("📋 Recent Readings")
                recent_data = energy_data.head(10)
                
                for _, row in recent_data.iterrows():
                    energy_class = f"energy-{str(row['energy_level']).lower()}"
                    timestamp = pd.to_datetime(row['timestamp'], errors='coerce')
                    try:
                        time_str = timestamp.strftime('%I:%M %p')
                    except:
                        time_str = 'Unknown'
                    
                    st.markdown(f"""
                    <div style="padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa; border-radius: 0.5rem;">
                        <span class="{energy_class}">{row['energy_level']}</span> energy 
                        ({row['confidence']:.1f}% confidence) - {time_str}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Recent readings with better styling
                st.subheader("📋 Recent Energy Readings")
                recent_data = energy_data.head(5)
                
                for _, row in recent_data.iterrows():
                    energy_class = f"energy-{str(row['energy_level']).lower()}"
                    timestamp = pd.to_datetime(row['timestamp'], errors='coerce')
                    try:
                        time_str = timestamp.strftime('%I:%M %p')
                        date_str = timestamp.strftime('%b %d')
                    except:
                        time_str = 'Unknown'
                        date_str = 'Unknown'
                    
                    st.markdown(f"""
                    <div style="padding: 1rem; margin: 0.5rem 0; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 0.5rem; border-left: 4px solid #1f77b4;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span class="{energy_class}" style="font-size: 1.2rem; font-weight: bold;">{row['energy_level']}</span>
                                <div style="color: #666; font-size: 0.9rem;">{date_str} at {time_str}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: #1f77b4; font-weight: bold;">{row['confidence']:.1f}%</div>
                                <div style="color: #666; font-size: 0.8rem;">confidence</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Pattern insights
                insights = pattern_analyzer.analyze_patterns(energy_data)
                if insights:
                    st.subheader("🎯 Your Energy Insights")
                    for insight in insights:
                        st.info(insight)
        else:
            st.info("📈 Start tracking your energy to see patterns emerge!")
            st.markdown("""
            **🎯 Ready to discover your energy patterns?**
            
            Track your energy levels to unlock:
            - 📊 Beautiful visualizations of your patterns
            - 🎯 Personalized insights about your peak hours
            - 📈 Weekly summaries and trends
            - 💡 Actionable productivity tips
            
            Use the camera, upload photos, or manually enter your energy levels to get started!
            """)

def main():
    """Main app function"""
    
    # Check if user is authenticated
    auth = AuthSystem()
    current_user = auth.get_current_user()
    
    # Try to recover session if user has persistent ID but no current session
    if not current_user and 'persistent_user_id' in st.session_state:
        try:
            # Attempt to login with persistent ID
            anonymous_email = f"{st.session_state.persistent_user_id}@local.com"
            user_id = auth.login_user(anonymous_email, "You")
            current_user = auth.get_current_user()
            if current_user:
                st.success("Welcome back! Your data is safe.")
        except:
            pass  # If recovery fails, show landing page
    
    if not current_user:
        # Show landing page
        show_landing_page()
    else:
        # Show main app
        show_main_app()

if __name__ == "__main__":
    main() 