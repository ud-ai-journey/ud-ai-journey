import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import hashlib
import os
import cv2
import numpy as np
from PIL import Image
import io

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

class SimpleEnergyDetector:
    """Simple energy detector using OpenCV face detection"""
    
    def __init__(self):
        # Load OpenCV face cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    def detect_energy(self, image_input):
        """Detect energy level using simple face/eye detection"""
        try:
            # Convert to PIL Image if needed
            if hasattr(image_input, 'read'):
                image = Image.open(image_input)
            else:
                image = image_input
            
            # Convert to OpenCV format
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return "Low", 60.0  # No face detected = low energy
            
            # Count eyes for each face
            total_eyes = 0
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                total_eyes += len(eyes)
            
            # Simple energy classification based on face/eye detection
            if len(faces) >= 1 and total_eyes >= 2:
                # Good face detection with eyes = high energy
                return "High", 85.0
            elif len(faces) >= 1:
                # Face detected but no eyes = medium energy
                return "Medium", 70.0
            else:
                # No face = low energy
                return "Low", 60.0
                
        except Exception as e:
            # Fallback to manual classification
            return "Medium", 65.0

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
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
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
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("quick_start"):
                name = st.text_input("Your Name (Optional)", placeholder="Enter your name or leave blank")
                
                if st.form_submit_button("🎯 Start Tracking Now", type="primary", use_container_width=True):
                    auth = AuthSystem()
                    if name and name.strip():
                        user_name = name.strip()
                    else:
                        user_name = "You"
                    
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
    
    energy_detector = SimpleEnergyDetector()
    
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
            st.session_state['show_energy_check'] = False
            st.rerun()
    
    with col4:
        if st.button("🚪 Logout"):
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
                    
                    if auth.save_energy_record(energy_level, confidence):
                        st.balloons()
                        st.success(f"🎯 Energy Level: {energy_level} ({confidence:.1f}% confidence)")
                        
                        energy_data = auth.get_user_energy_data()
                        
                        if not energy_data.empty:
                            st.markdown("### 💡 What This Means For You Today:")
                            
                            today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
                            today_count = len(today_data)
                            
                            if today_count == 1:
                                st.info("🌟 This is your first energy reading today - great start!")
                            else:
                                st.info(f"📊 This is your {today_count}rd energy reading today")
                            
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
                    
                    if auth.save_energy_record(energy_level, confidence):
                        st.balloons()
                        st.success(f"🎯 Energy Level: {energy_level} ({confidence:.1f}% confidence)")
                        
                        energy_data = auth.get_user_energy_data()
                        
                        if not energy_data.empty:
                            st.markdown("### 💡 What This Means For You Today:")
                            
                            today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
                            today_count = len(today_data)
                            
                            if today_count == 1:
                                st.info("🌟 This is your first energy reading today - great start!")
                            else:
                                st.info(f"📊 This is your {today_count}rd energy reading today")
                            
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
                
                energy_data = auth.get_user_energy_data()
                
                if not energy_data.empty:
                    st.markdown("### 💡 What This Means For You Today:")
                    
                    today_data = energy_data[energy_data['timestamp'].dt.date == datetime.now().date()]
                    today_count = len(today_data)
                    
                    if today_count == 1:
                        st.info("🌟 This is your first energy reading today - great start!")
                    else:
                        st.info(f"📊 This is your {today_count}rd energy reading today")
                    
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
                
                st.subheader("📋 Your Energy Records")
                st.dataframe(energy_data.head(10))
                
                # Simple energy chart
                try:
                    timeline_data = energy_data.sort_values('timestamp').copy()
                    timeline_data['energy_score'] = timeline_data['energy_level'].replace({'High': 3, 'Medium': 2, 'Low': 1})
                    
                    fig = px.scatter(timeline_data, x='timestamp', y='energy_score', 
                                   color='energy_level', title="Your Energy Timeline")
                    fig.update_traces(marker_size=10)
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Chart creation failed: {e}")
                
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
            
            # Simple energy chart
            try:
                timeline_data = energy_data.sort_values('timestamp').copy()
                timeline_data['energy_score'] = timeline_data['energy_level'].replace({'High': 3, 'Medium': 2, 'Low': 1})
                
                fig = px.scatter(timeline_data, x='timestamp', y='energy_score', 
                               color='energy_level', title="Your Energy Journey")
                fig.update_traces(marker_size=10)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart creation failed: {e}")
            
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