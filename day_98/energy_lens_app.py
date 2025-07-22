import streamlit as st
from supabase import create_client, Client
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
import cv2
from deepface import DeepFace
from PIL import Image
import numpy as np
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

# --- Supabase Setup ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Helper: Get User Role ---
def get_user_role(user):
    return user.user_metadata.get("role", "user")

# --- Auth Functions ---
def register_user(email, password):
    result = supabase.auth.sign_up({"email": email, "password": password})
    return bool(result.user)

def login_user(email, password):
    result = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if result.user:
        st.session_state["user"] = result.user
        return True
    return False

def save_energy_record(user_id, energy_level, confidence):
    supabase.table("energy_data").insert({
        "user_id": user_id,
        "energy_level": energy_level,
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
    return True

def get_user_energy_data(user_id):
    res = supabase.table("energy_data").select("*").eq("user_id", user_id).order("timestamp", desc=True).execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

def get_all_users():
    res = supabase.table("users").select("*").execute()
    return pd.DataFrame(res.data)

def get_all_energy_data():
    res = supabase.table("energy_data").select("*").order("timestamp", desc=True).execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

def analyze_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        result = DeepFace.analyze(opencv_image, actions=['emotion'], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]
        emotions = result['emotion']
        dominant_emotion = max(emotions, key=emotions.get)
        confidence = emotions[dominant_emotion]
        # Map emotion to energy level
        energy_mapping = {
            'happy': 'High',
            'surprise': 'High',
            'neutral': 'Medium',
            'sad': 'Low',
            'angry': 'Low',
            'fear': 'Low',
            'disgust': 'Low'
        }
        energy_level = energy_mapping.get(dominant_emotion, 'Medium')
        return energy_level, float(confidence)
    except Exception as e:
        st.warning(f"Energy detection failed: {e}")
        return None, None

# --- Onboarding ---
def show_onboarding():
    st.markdown("""
    <div style='background: #e3f2fd; padding: 1.5rem; border-radius: 1rem; margin-bottom: 1.5rem;'>
        <h2 style='color: #1976d2;'>👋 Welcome to Energy Lens!</h2>
        <p style='font-size: 1.1rem;'>
            Discover your energy patterns and optimize your productivity.<br>
            <b>To get started, record your first energy reading below!</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Main App ---
st.title("Energy Lens AI (Supabase Edition)")

if "user" not in st.session_state:
    st.subheader("Register")
    reg_email = st.text_input("Email (register)")
    reg_password = st.text_input("Password (register)", type="password")
    if st.button("Register"):
        if len(reg_password) < 6:
            st.error("Password must be at least 6 characters.")
        elif register_user(reg_email, reg_password):
            st.success("Registration successful! Please confirm your email and log in.")
        else:
            st.error("Registration failed.")

    st.subheader("Login")
    login_email = st.text_input("Email (login)")
    login_password = st.text_input("Password (login)", type="password")
    if st.button("Login"):
        if login_user(login_email, login_password):
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Login failed.")
else:
    user = st.session_state["user"]
    role = get_user_role(user)
    st.success(f"Logged in as: {user.email} (Role: {role})")
    st.button("Logout", on_click=lambda: st.session_state.pop("user"))

    # --- Tabbed Layout ---
    tabs = ["📸 Energy Check", "📊 Your Data", "👤 Profile"]
    if role == "admin":
        tabs.append("🛠️ Admin")
    selected_tab = st.tabs(tabs)

    # --- Energy Check Tab ---
    with selected_tab[0]:
        st.header("📸 Energy Check")
        st.info("Choose how you'd like to record your energy:")
        energy_input_method = st.radio(
            "Input Method",
            ["📷 Take Photo", "📁 Upload Image", "✏️ Manual Entry"],
            horizontal=True
        )
        energy_level = None
        confidence = None
        photo = None
        uploaded_file = None
        if energy_input_method == "📷 Take Photo":
            photo = st.camera_input("Take a photo for energy analysis")
            if photo:
                energy_level, confidence = analyze_image(photo.getvalue())
                if energy_level is not None and confidence is not None:
                    st.success(f"Detected: {energy_level} ({confidence:.1f}% confidence)")
                else:
                    st.warning("Could not detect energy level. Please select manually.")
                    energy_level = st.selectbox("Select Energy Level", ["High", "Medium", "Low"])
                    confidence = st.slider("Confidence (%)", 0, 100, 80)
        elif energy_input_method == "📁 Upload Image":
            uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                energy_level, confidence = analyze_image(uploaded_file.read())
                if energy_level is not None and confidence is not None:
                    st.success(f"Detected: {energy_level} ({confidence:.1f}% confidence)")
                else:
                    st.warning("Could not detect energy level. Please select manually.")
                    energy_level = st.selectbox("Select Energy Level", ["High", "Medium", "Low"])
                    confidence = st.slider("Confidence (%)", 0, 100, 80)
        else:
            energy_level = st.selectbox("Your Energy Level", ["High", "Medium", "Low"])
            confidence = st.slider("Confidence (%)", 0, 100, 80)
        if st.button("Save Energy Record"):
            if energy_level is not None and confidence is not None:
                save_energy_record(user.id, energy_level, confidence)
                st.success("Energy record saved!")
                st.rerun()
            else:
                st.error("Please provide an energy level and confidence.")

    # --- Your Data Tab ---
    with selected_tab[1]:
        st.header("📊 Your Energy Data")
        user_df = get_user_energy_data(user.id)
        if user_df.empty:
            show_onboarding()
            st.info("No energy data yet. Add your first record!")
        else:
            st.dataframe(user_df)
            st.subheader("📈 Energy Trend")
            fig = px.line(user_df.sort_values("timestamp"), x="timestamp", y="energy_level", title="Your Energy Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)
            csv = user_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="my_energy_data.csv",
                mime="text/csv",
                help="Download your energy data as a CSV file."
            )
            st.subheader("💡 Insights & Tips")
            high_count = (user_df["energy_level"] == "High").sum()
            total = len(user_df)
            if total > 0:
                pct_high = 100 * high_count / total
                st.info(f"You reported 'High' energy {pct_high:.1f}% of the time.")
                if pct_high > 60:
                    st.success("Great job! Try to schedule important tasks during your high-energy periods.")
                elif pct_high > 30:
                    st.info("You have a balanced energy pattern. Consider tracking for a full week for deeper insights.")
                else:
                    st.warning("Consider what factors might be lowering your energy and try to optimize your routine.")

    # --- Profile Tab ---
    with selected_tab[2]:
        st.header("👤 Profile")
        st.info("Profile features coming soon! Track your progress and manage your account here.")
        st.write(f"**Email:** {user.email}")
        st.write(f"**Role:** {role}")

    # --- Admin Tab (if admin) ---
    if role == "admin" and len(selected_tab) > 3:
        with selected_tab[3]:
            st.header("🛠️ Admin Dashboard")
            st.info("Welcome, Admin! You have access to admin features.")
            st.write("This is an admin-only section. You can add admin dashboards, user management, etc.")
            st.subheader("👥 All Users")
            users_df = get_all_users()
            if not users_df.empty:
                st.dataframe(users_df)
            else:
                st.info("No users found in the users table.")
            st.subheader("⚡ All Energy Data")
            all_energy_df = get_all_energy_data()
            if not all_energy_df.empty:
                st.dataframe(all_energy_df)
            else:
                st.info("No energy data found.") 