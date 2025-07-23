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
from visualizations import create_energy_chart, create_pattern_insights, create_weekly_summary, create_productivity_chart
import time

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
def ensure_user_in_db(user):
    res = supabase.table("users").select("id").eq("id", user.id).execute()
    if not res.data:
        supabase.table("users").insert({
            "id": user.id,
            "email": user.email,
            # Add other fields as needed (e.g., role)
        }).execute()

def register_user(email, password):
    result = supabase.auth.sign_up({"email": email, "password": password})
    if result.user:
        ensure_user_in_db(result.user)
    return bool(result.user)

def login_user(email, password):
    result = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if result.user:
        st.session_state["user"] = result.user
        ensure_user_in_db(result.user)
        return True
    return False

def save_energy_record(user_id, energy_level, confidence):
    try:
        # Fetch user's team_id
        user_row = supabase.table("users").select("team_id").eq("id", user_id).execute()
        team_id = user_row.data[0]["team_id"] if user_row.data else None
        result = supabase.table("energy_data").insert({
            "user_id": user_id,
            "energy_level": energy_level,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat(),
            "team_id": team_id
        }).execute()
        if hasattr(result, 'status_code') and result.status_code >= 400:
            st.error(f"Supabase insert failed: {result}")
        else:
            st.info(f"Supabase insert result: {result}")
        return True
    except Exception as e:
        st.error(f"Supabase insert error: {e}")
        return False

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

# --- Team Management Functions ---
def get_user_team(user):
    res = supabase.table("users").select("team_id").eq("id", user.id).execute()
    if res.data and res.data[0].get("team_id"):
        team_id = res.data[0]["team_id"]
        team = supabase.table("teams").select("*").eq("id", team_id).execute()
        if team.data:
            return team.data[0]
    return None

def get_team_members(team_id):
    res = supabase.table("users").select("id", "email").eq("team_id", team_id).execute()
    return res.data if res.data else []

def get_team_energy_data(team_id):
    res = supabase.table("energy_data").select("*").eq("team_id", team_id).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

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
    if '👥 Team' not in tabs:
        tabs.insert(-1 if role == "admin" else len(tabs), "👥 Team")
    # Manual tab switching using session state
    if 'selected_tab' not in st.session_state:
        st.session_state['selected_tab'] = 0
    selected_tab_idx = st.session_state['selected_tab']
    selected_tab = st.radio("Navigation", tabs, index=selected_tab_idx, horizontal=True)

    # --- Energy Check Tab ---
    if selected_tab == "📸 Energy Check":
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
                st.session_state['selected_tab'] = 1  # Switch to 'Your Data' tab
                time.sleep(1)  # Wait for Supabase to commit
                st.rerun()
            else:
                st.error("Please provide an energy level and confidence.")

    # --- Your Data Tab ---
    elif selected_tab == "📊 Your Data":
        st.header("📊 Your Energy Data")
        user_df = get_user_energy_data(user.id)
        if user_df.empty:
            show_onboarding()
            st.info("No energy data yet. Add your first record!")
        else:
            st.dataframe(user_df)
            # Advanced charts
            st.subheader("📊 Pattern Analysis")
            fig = create_energy_chart(user_df)
            st.plotly_chart(fig, use_container_width=True)
            insights_fig = create_pattern_insights(user_df)
            if insights_fig:
                st.plotly_chart(insights_fig, use_container_width=True)
            weekly_fig = create_weekly_summary(user_df)
            if weekly_fig:
                st.plotly_chart(weekly_fig, use_container_width=True)
            prod_fig = create_productivity_chart(user_df)
            if prod_fig:
                st.plotly_chart(prod_fig, use_container_width=True)
            # AI Insights & Recommendations
            st.subheader("🤖 AI Insights & Recommendations")
            insights_generator = InsightsGenerator()
            weekly_insights = insights_generator.generate_weekly_report(user_df)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🏆 Peak Performance**")
                for insight in weekly_insights['peak_performance']:
                    st.info(insight)
                st.markdown("**🔍 Pattern Discoveries**")
                discoveries = weekly_insights['pattern_discoveries']
                if not discoveries:
                    discoveries = ["Keep tracking! Patterns will emerge as you add more data."]
                for insight in discoveries:
                    st.success(insight)
            with col2:
                st.markdown("**📉 Energy Dips**")
                for insight in weekly_insights['energy_dips']:
                    st.warning(insight)
                st.markdown("**💡 Productivity Tips**")
                for tip in weekly_insights['productivity_tips']:
                    st.write(f"• {tip}")
                st.markdown("**🎯 Next Week Goals**")
                for goal in weekly_insights['next_week_goals']:
                    st.write(f"• {goal}")
            # Download buttons
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
            # PDF export
            from fpdf import FPDF
            import tempfile
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Energy Lens - Your Energy Data", ln=True, align='C')
            pdf.ln(10)
            for col in user_df.columns:
                pdf.cell(40, 10, col, border=1)
            pdf.ln()
            for i, row in user_df.iterrows():
                for col in user_df.columns:
                    val = str(row[col])[:18]
                    pdf.cell(40, 10, val, border=1)
                pdf.ln()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile.flush()
                with open(tmpfile.name, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f.read(),
                        file_name="my_energy_data.pdf",
                        mime="application/pdf",
                        help="Download your energy data as a PDF file."
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
    elif selected_tab == "👤 Profile":
        st.header("👤 Profile")
        st.info("Profile features coming soon! Track your progress and manage your account here.")
        st.write(f"**Email:** {user.email}")
        st.write(f"**Role:** {role}")

    # --- Admin Tab (if admin) ---
    elif role == "admin" and selected_tab == "🛠️ Admin":
        st.header("🛠️ Admin Dashboard")
        st.info("Welcome, Admin! You have access to admin features.")
        st.write("This is an admin-only section. You can add admin dashboards, user management, etc.")
        st.subheader("👥 All Users")
        users_df = get_all_users()
        # Map team_id to team name for display
        if not users_df.empty and 'team_id' in users_df.columns:
            team_map = {}
            team_ids = users_df['team_id'].dropna().unique().tolist()
            if team_ids:
                teams = supabase.table("teams").select("id", "name").in_("id", team_ids).execute()
                if teams.data:
                    team_map = {t['id']: t['name'] for t in teams.data}
            users_df['team'] = users_df['team_id'].map(lambda tid: team_map.get(tid, tid) if tid else None)
        st.dataframe(users_df.drop(columns=["team_id"]) if 'team_id' in users_df.columns else users_df)
        # User role management
        if not users_df.empty:
            st.subheader("🔧 Manage User Roles")
            for idx, row in users_df.iterrows():
                if row['role'] == 'admin':
                    if row['id'] != user.id and st.button(f"Demote {row['email']} to user", key=f"demote_{row['id']}"):
                        supabase.table("users").update({"role": "user"}).eq("id", row['id']).execute()
                        st.success(f"Demoted {row['email']} to user.")
                        st.rerun()
                else:
                    if st.button(f"Promote {row['email']} to admin", key=f"promote_{row['id']}"):
                        supabase.table("users").update({"role": "admin"}).eq("id", row['id']).execute()
                        st.success(f"Promoted {row['email']} to admin.")
                        st.rerun()
        st.subheader("⚡ All Energy Data")
        all_energy_df = get_all_energy_data()
        # Map team_id to team name for display
        if not all_energy_df.empty and 'team_id' in all_energy_df.columns:
            all_energy_df['team'] = all_energy_df['team_id'].map(lambda tid: team_map.get(tid, tid) if tid else None)
        st.dataframe(all_energy_df.drop(columns=["team_id"]) if 'team_id' in all_energy_df.columns else all_energy_df)
    # --- Team Tab ---
    elif selected_tab == "👥 Team":
        st.header("👥 Your Team")
        team = get_user_team(user)
        if not team:
            if role == "admin":
                st.info("You are not part of a team. Create a new team to get a code for your users.")
                new_team_name = st.text_input("Team Name")
                if st.button("Create Team") and new_team_name:
                    import secrets
                    team_code = secrets.token_hex(4).lower()
                    new_team = supabase.table("teams").insert({"code": team_code, "name": new_team_name}).execute()
                    team_id = new_team.data[0]["id"] if new_team.data else None
                    if team_id:
                        supabase.table("users").update({"team_id": team_id}).eq("id", user.id).execute()
                        st.success(f"Team '{new_team_name}' created! Share this code with your users: {team_code}")
                        st.rerun()
            else:
                st.info("You are not part of a team. Enter a team code to join an existing team.")
                team_code = st.text_input("Team Code")
                if st.button("Join Team") and team_code:
                    team_code = team_code.strip().lower()
                    st.write(f"[DEBUG] Your user.id: {user.id}")
                    team_res = supabase.table("teams").select("*").ilike("code", team_code).execute()
                    if team_res.data:
                        team_id = team_res.data[0]["id"]
                        update_result = supabase.table("users").update({"team_id": team_id}).eq("id", user.id).execute()
                        st.write(f"[DEBUG] Update result: {update_result}")
                        st.success(f"Joined team with code {team_code}!")
                        st.rerun()
                    else:
                        st.error("No team found with that code. Please check with your admin.")
        else:
            st.success(f"Team: {team['name']}")
            st.markdown(f"**Team Code:** `{team['code']}`")
            # Role check for admin dashboard features
            is_admin = (role == "admin")
            if is_admin:
                members = get_team_members(team['id'])
                st.write(f"[DEBUG] get_team_members({team['id']}): {members}")
                st.markdown("**Team Members:**")
                for m in members:
                    st.write(m['email'])
                # Team energy data
                team_energy = get_team_energy_data(team['id'])
                if not team_energy.empty:
                    st.markdown("**Team Energy Trends (Anonymized):**")
                    if 'hour' in team_energy.columns:
                        avg_by_hour = team_energy.groupby('hour')['energy_level'].apply(lambda x: (x == 'High').mean() * 100)
                        st.bar_chart(avg_by_hour)
                    leaderboard = team_energy.groupby('user_id')['energy_level'].apply(lambda x: (x == 'High').mean() * 100).sort_values(ascending=False)
                    st.markdown("**Team Leaderboard (High Energy %):**")
                    st.dataframe(leaderboard)
                    st.markdown("**All Team Data:**")
                    st.dataframe(team_energy)
                    # Export team data as CSV
                    if not team_energy.empty:
                        import io
                        csv = team_energy.to_csv(index=False)
                        st.download_button(
                            label="Download Team Data as CSV",
                            data=csv,
                            file_name="team_energy_data.csv",
                            mime="text/csv",
                            help="Download all team energy data as CSV."
                        )
                    # More analytics: show average confidence and energy distribution
                    if not team_energy.empty:
                        st.markdown("**Team Analytics:**")
                        avg_conf = team_energy['confidence'].mean()
                        st.write(f"Average Confidence: {avg_conf:.2f}%")
                        dist = team_energy['energy_level'].value_counts(normalize=True) * 100
                        st.write("Energy Level Distribution (%):")
                        st.write(dist)
                else:
                    st.info("No team energy data yet. Encourage your team to track their energy!")
            else:
                # Regular user: show only their own data and anonymized team stats
                team_energy = get_team_energy_data(team['id'])
                if not team_energy.empty:
                    st.markdown("**Team Energy Trends (Anonymized):**")
                    if 'hour' in team_energy.columns:
                        avg_by_hour = team_energy.groupby('hour')['energy_level'].apply(lambda x: (x == 'High').mean() * 100)
                        st.bar_chart(avg_by_hour)
                    leaderboard = team_energy.groupby('user_id')['energy_level'].apply(lambda x: (x == 'High').mean() * 100).sort_values(ascending=False)
                    st.markdown("**Team Leaderboard (High Energy %):**")
                    st.dataframe(leaderboard)
                    # Show only the logged-in user's data
                    user_data = team_energy[team_energy['user_id'] == user.id]
                    st.markdown("**Your Data in Team:**")
                    st.dataframe(user_data)
                else:
                    st.info("No team energy data yet. Encourage your team to track their energy!") 