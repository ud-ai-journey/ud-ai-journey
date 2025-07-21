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

def ordinal(n):
    """Return the ordinal string of a number (e.g., 1st, 2nd, 3rd, 4th)"""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

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
    
    # Onboarding: Show a prominent Start Here button if user hasn't started energy check or data view
    if not st.session_state.get('show_energy_check') and not st.session_state.get('show_data'):
        st.markdown("""
        <div style='background: #e3f2fd; padding: 1.5rem; border-radius: 1rem; margin-bottom: 1.5rem;'>
            <h2 style='color: #1976d2;'>👋 Welcome to Energy Lens!</h2>
            <p style='font-size: 1.1rem;'>
                Discover your energy patterns and optimize your productivity.<br>
                <b>To get started, click the button below and take your first energy reading!</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Start Here", key="start_here_btn", help="Begin your energy journey. We'll guide you step by step!"):
            st.session_state['show_energy_check'] = True
            st.experimental_rerun()

    # Use tabs for main navigation
    tab1, tab2, tab3 = st.tabs(["📸 Energy Check", "📊 Your Data", "👤 Profile"])

    with tab1:
        st.header("📸 Energy Check")
        st.info("👋 New here? Start by taking a photo or uploading an image. We'll analyze your energy level and help you discover your best productivity patterns!\n\n**Tips:**\n- Make sure your face is clearly visible\n- Good lighting helps with accurate detection\n- You can always enter your energy manually if needed")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Take Photo")
            st.info("Use your webcam to take a live photo. For best results, face the camera directly and smile!")
            photo = st.camera_input("Take a photo for energy analysis", help="Click to open your webcam and snap a photo.")
            if photo and st.button("🔍 Analyze Energy", help="Analyze the photo and get your energy reading."):
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
                                st.info(f"📊 This is your {ordinal(today_count)} energy reading today")
                            
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
            st.info("Upload a recent photo of yourself. Clear, well-lit images work best.")
            uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'], help="Choose a photo file to analyze your energy.")
            if uploaded_file and st.button("🔍 Analyze Uploaded Image", help="Analyze the uploaded image and get your energy reading."):
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
                                st.info(f"📊 This is your {ordinal(today_count)} energy reading today")
                            
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
                        st.info(f"📊 This is your {ordinal(today_count)} energy reading today")
                    
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

        # After manual entry and insights, add CSV download option
        st.divider()
        st.subheader("⬇️ Download Your Data")
        energy_data = auth.get_user_energy_data()
        if not energy_data.empty:
            csv = energy_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="energy_lens_data.csv",
                mime="text/csv",
                help="Download all your tracked energy/emotion data as a CSV file."
            )
        else:
            st.info("No data available to download yet. Start tracking your energy!")
    
    # Data Visualization Section
    with tab2:
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
    with tab3:
        st.header("👤 Profile")
        st.info("Profile features coming soon! Track your progress and manage your account here.")
        # Add content for profile management here
        # Example: st.write(f"Welcome, {current_user['name']}! This section is under construction.")

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