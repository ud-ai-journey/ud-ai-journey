"""
Guru Sahayam - Main Streamlit Application
AI-Powered Multi-Grade Classroom Assistant
"""

import streamlit as st
import json
import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List

# Import our core modules
from core.agents import get_orchestrator
from core.config import get_config

# Page configuration
st.set_page_config(
    page_title="Guru Sahayam - AI Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }
    
    .success-metric {
        border-left-color: #28a745;
    }
    
    .warning-metric {
        border-left-color: #ffc107;
    }
    
    .info-metric {
        border-left-color: #17a2b8;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .sparkline {
        font-family: monospace;
        font-size: 1.2rem;
        color: #28a745;
    }
    
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = get_orchestrator()

if 'config' not in st.session_state:
    st.session_state.config = get_config()

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'teacher_name': 'Uday Kumar',
        'school': 'Rural Primary School',
        'grades': ['Grade 3', 'Grade 4', 'Grade 5'],
        'subjects': ['Mathematics', 'Science', 'English'],
        'languages': ['English', 'Hindi', 'Marathi'],
        'cultural_context': 'Rural farming community'
    }

if 'recent_activities' not in st.session_state:
    st.session_state.recent_activities = []

def main():
    """Main application function"""
    
    # Sidebar navigation
    st.sidebar.title("🎓 Guru Sahayam")
    st.sidebar.markdown("AI-Powered Teaching Assistant")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose your workspace:",
        ["📊 Teacher Dashboard", "📝 Lesson Creator", "📚 Content Library", 
         "📈 Student Progress", "⚙️ Settings", "📱 Mobile View"]
    )
    
    if page == "📊 Teacher Dashboard":
        show_teacher_dashboard()
    elif page == "📝 Lesson Creator":
        show_lesson_creator()
    elif page == "📚 Content Library":
        show_content_library()
    elif page == "📈 Student Progress":
        show_student_progress()
    elif page == "⚙️ Settings":
        show_settings()
    elif page == "📱 Mobile View":
        show_mobile_view()

def show_teacher_dashboard():
    """Display the main teacher dashboard"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👨‍🏫 Teacher Dashboard</h1>
        <p>Welcome back, {teacher_name}! Here's your teaching overview.</p>
    </div>
    """.format(teacher_name=st.session_state.user_data['teacher_name']), unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card success-metric">
            <h3>⏰ Time Saved Today</h3>
            <h2>3.5h</h2>
            <p>vs 8h manual prep</p>
            <div class="sparkline">▁▂▃▄▅▆▇█</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card info-metric">
            <h3>📊 Student Engagement</h3>
            <h2>92%</h2>
            <p>Average engagement</p>
            <div class="sparkline">▁▂▃▄▅▆▇█</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card warning-metric">
            <h3>✅ Content Quality</h3>
            <h2>4.8/5</h2>
            <p>Safety checks passed</p>
            <div class="sparkline">▁▂▃▄▅▆▇█</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card info-metric">
            <h3>📧 Parent Communication</h3>
            <h2>95%</h2>
            <p>Satisfaction rate</p>
            <div class="sparkline">▁▂▃▄▅▆▇█</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚 Create Lesson Plan", use_container_width=True):
            st.success("Opening Lesson Creator...")
            st.session_state.page = "lesson_creator"
    
    with col2:
        if st.button("❓ Generate Quiz", use_container_width=True):
            st.success("Generating quiz...")
            # Simulate quiz generation
            time.sleep(1)
            st.info("Quiz generated successfully!")
    
    with col3:
        if st.button("📝 Write Feedback", use_container_width=True):
            st.success("Opening feedback tool...")
            # Simulate feedback generation
            time.sleep(1)
            st.info("Feedback generated!")
    
    with col4:
        if st.button("📊 View Progress", use_container_width=True):
            st.success("Loading progress data...")
            st.session_state.page = "student_progress"
    
    # Recent Activities
    st.subheader("📋 Recent Activities")
    
    # Simulate recent activities
    activities = [
        {"time": "2 hours ago", "action": "Created Math lesson for Grade 3-5", "status": "✅"},
        {"time": "4 hours ago", "action": "Generated Science quiz", "status": "✅"},
        {"time": "1 day ago", "action": "Updated parent communication", "status": "✅"},
        {"time": "2 days ago", "action": "Created English story", "status": "✅"}
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.write(activity["status"])
        with col2:
            st.write(activity["action"])
        with col3:
            st.write(activity["time"])
    
    # System Status
    st.subheader("🔧 System Status")
    
    # Agent status
    agent_status = st.session_state.orchestrator.get_agent_status()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🤖 AI Agents: All Active")
        st.write("• Content Creation Agent ✅")
        st.write("• Differentiation Agent ✅")
        st.write("• Localization Agent ✅")
    
    with col2:
        st.info("🌐 Language Support: 12 Languages")
        st.write("• English, Hindi, Marathi")
        st.write("• Telugu, Tamil, Bengali")
        st.write("• And 6 more languages")
    
    with col3:
        st.info("📱 Mobile Ready")
        st.write("• Responsive design ✅")
        st.write("• Offline capability ✅")
        st.write("• Voice input ready ✅")

def show_lesson_creator():
    """Display the lesson plan creation interface"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📝 Lesson Plan Creator</h1>
        <p>Create personalized, culturally relevant lesson plans for multiple grades</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lesson creation form
    with st.form("lesson_creation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Subject",
                ["Mathematics", "Science", "English", "Social Studies", "Hindi", "Computer Science"]
            )
            
            topic = st.text_input("Topic", placeholder="e.g., Fractions, Photosynthesis, Story Writing")
            
            grades = st.multiselect(
                "Grade Levels",
                ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8"],
                default=["Grade 3", "Grade 4", "Grade 5"]
            )
        
        with col2:
            languages = st.multiselect(
                "Languages",
                ["English", "Hindi", "Marathi", "Telugu", "Tamil", "Bengali", "Gujarati"],
                default=["English", "Hindi"]
            )
            
            cultural_context = st.selectbox(
                "Cultural Context",
                ["Rural farming community", "Urban middle class", "Tribal community", 
                 "Coastal fishing village", "Mountain region", "Desert region"]
            )
            
            duration = st.slider("Lesson Duration (minutes)", 30, 120, 45, 15)
        
        # Advanced options
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                include_visual_aids = st.checkbox("Include Visual Aids", value=True)
                include_assessment = st.checkbox("Include Assessment", value=True)
                include_homework = st.checkbox("Include Homework", value=True)
            
            with col2:
                learning_style = st.selectbox(
                    "Primary Learning Style",
                    ["Mixed", "Visual", "Auditory", "Kinesthetic"]
                )
                
                difficulty_level = st.selectbox(
                    "Difficulty Level",
                    ["Basic", "Intermediate", "Advanced"]
                )
        
        # Generate button
        if st.form_submit_button("🚀 Generate Lesson Plan", use_container_width=True):
            if topic and grades:
                generate_lesson_plan(subject, topic, grades, languages, cultural_context, duration)
            else:
                st.error("Please fill in all required fields!")

def generate_lesson_plan(subject, topic, grades, languages, cultural_context, duration):
    """Generate lesson plan using AI agents"""
    
    with st.spinner("🤖 AI agents are creating your lesson plan..."):
        # Simulate AI processing
        time.sleep(2)
        
        # Prepare input for AI agents
        input_data = {
            "task_type": "lesson_creation",
            "subject": subject,
            "topic": topic,
            "grades": grades,
            "languages": languages,
            "cultural_context": cultural_context,
            "duration": duration
        }
        
        # Process through orchestrator
        result = st.session_state.orchestrator.process_request(input_data)
        
        if "error" not in result:
            display_lesson_plan(result)
        else:
            st.error(f"Error generating lesson plan: {result['error']}")

def display_lesson_plan(result):
    """Display the generated lesson plan"""
    
    st.success("✅ Lesson plan generated successfully!")
    
    # Display lesson plan in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📚 Content", "🎯 Activities", "📊 Assessment"])
    
    with tab1:
        st.subheader("Lesson Plan Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Subject:** Mathematics")
            st.write("**Topic:** Fractions")
            st.write("**Grades:** Grade 3-5")
            st.write("**Duration:** 45 minutes")
        
        with col2:
            st.write("**Languages:** English, Hindi")
            st.write("**Cultural Context:** Rural farming community")
            st.write("**Learning Style:** Mixed")
            st.write("**Difficulty:** Intermediate")
    
    with tab2:
        st.subheader("Learning Objectives")
        
        objectives = [
            "Understand basic fraction concepts",
            "Compare fractions using visual aids",
            "Solve simple fraction problems",
            "Apply fractions to real-world scenarios"
        ]
        
        for i, objective in enumerate(objectives, 1):
            st.write(f"{i}. {objective}")
        
        st.subheader("Main Content")
        st.write("""
        Today we'll explore fractions through examples from our farming community. 
        We'll use local examples like dividing harvests, measuring land, and sharing resources.
        
        **Key Concepts:**
        - What are fractions?
        - How to read and write fractions
        - Comparing fractions
        - Adding and subtracting fractions
        """)
    
    with tab3:
        st.subheader("Interactive Activities")
        
        activities = [
            "**Group Discussion:** Share examples of fractions in daily life",
            "**Hands-on:** Use fraction circles to visualize concepts",
            "**Problem Solving:** Solve fraction problems with local examples",
            "**Assessment:** Quick quiz to check understanding"
        ]
        
        for activity in activities:
            st.write(f"• {activity}")
    
    with tab4:
        st.subheader("Assessment Questions")
        
        questions = [
            "What fraction represents half of a harvest?",
            "Compare 1/3 and 1/4 using visual aids",
            "Add 1/4 + 1/4 and explain your answer",
            "Apply fractions to a real farming scenario"
        ]
        
        for i, question in enumerate(questions, 1):
            st.write(f"**Q{i}:** {question}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save as Template"):
            st.success("Lesson plan saved as template!")
    
    with col2:
        if st.button("📤 Export PDF"):
            st.success("PDF exported successfully!")
    
    with col3:
        if st.button("📱 Share with Parents"):
            st.success("Shared with parents!")

def show_content_library():
    """Display the content library"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📚 Content Library</h1>
        <p>Access and manage your teaching resources</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search = st.text_input("🔍 Search content", placeholder="Search by topic, subject, or grade")
    
    with col2:
        subject_filter = st.selectbox("Subject", ["All", "Mathematics", "Science", "English", "Social Studies"])
    
    with col3:
        grade_filter = st.selectbox("Grade", ["All", "Grade 3", "Grade 4", "Grade 5", "Grade 6"])
    
    # Content grid
    st.subheader("📋 Your Content")
    
    # Simulate content library
    content_items = [
        {"title": "Fractions for Grade 3-5", "subject": "Mathematics", "grade": "Grade 3-5", "type": "Lesson Plan", "date": "2024-01-15"},
        {"title": "Photosynthesis Basics", "subject": "Science", "grade": "Grade 4-6", "type": "Lesson Plan", "date": "2024-01-14"},
        {"title": "Story Writing Workshop", "subject": "English", "grade": "Grade 3-5", "type": "Activity", "date": "2024-01-13"},
        {"title": "Math Quiz - Fractions", "subject": "Mathematics", "grade": "Grade 3-5", "type": "Assessment", "date": "2024-01-12"},
        {"title": "Science Experiment Guide", "subject": "Science", "grade": "Grade 4-6", "type": "Activity", "date": "2024-01-11"},
        {"title": "English Grammar Rules", "subject": "English", "grade": "Grade 3-5", "type": "Reference", "date": "2024-01-10"}
    ]
    
    # Filter content
    filtered_content = content_items
    if search:
        filtered_content = [item for item in content_items if search.lower() in item["title"].lower()]
    if subject_filter != "All":
        filtered_content = [item for item in filtered_content if item["subject"] == subject_filter]
    if grade_filter != "All":
        filtered_content = [item for item in filtered_content if item["grade"] == grade_filter]
    
    # Display content
    for item in filtered_content:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{item['title']}**")
                st.write(f"*{item['subject']} • {item['grade']} • {item['type']}*")
            
            with col2:
                st.write(item["date"])
            
            with col3:
                if st.button("👁️ View", key=f"view_{item['title']}"):
                    st.info(f"Opening {item['title']}")
            
            with col4:
                if st.button("✏️ Edit", key=f"edit_{item['title']}"):
                    st.info(f"Editing {item['title']}")
            
            with col5:
                if st.button("📤 Export", key=f"export_{item['title']}"):
                    st.success(f"Exported {item['title']}")
            
            st.divider()

def show_student_progress():
    """Display student progress tracking"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📈 Student Progress</h1>
        <p>Track and analyze student performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Student selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_student = st.selectbox(
            "Select Student",
            ["All Students", "Priya Sharma", "Rahul Patel", "Anjali Singh", "Vikram Kumar"]
        )
    
    with col2:
        selected_subject = st.selectbox(
            "Select Subject",
            ["All Subjects", "Mathematics", "Science", "English", "Social Studies"]
        )
    
    # Progress overview
    st.subheader("📊 Progress Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Score", "78%", "+5%")
    
    with col2:
        st.metric("Engagement Rate", "92%", "+3%")
    
    with col3:
        st.metric("Time Spent", "45 min/day", "+10 min")
    
    with col4:
        st.metric("Assignments", "15/20", "75%")
    
    # Progress chart
    st.subheader("📈 Progress Trends")
    
    # Simulate progress data
    dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
    progress_data = pd.DataFrame({
        'Date': dates,
        'Mathematics': [65, 68, 72, 70, 75, 78, 80, 82, 85, 88, 90, 92, 95, 98, 100],
        'Science': [70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 98, 100, 100, 100],
        'English': [60, 65, 70, 75, 80, 85, 90, 92, 95, 98, 100, 100, 100, 100, 100]
    })
    
    fig = px.line(progress_data, x='Date', y=['Mathematics', 'Science', 'English'],
                  title='Student Progress Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
    # Individual student details
    if selected_student != "All Students":
        st.subheader(f"👤 {selected_student} - Detailed Progress")
        
        # Student metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Grade", "A-", "+2 grades")
            st.metric("Attendance", "95%", "+5%")
        
        with col2:
            st.metric("Homework Completion", "90%", "+10%")
            st.metric("Class Participation", "88%", "+3%")
        
        with col3:
            st.metric("Test Scores", "85%", "+8%")
            st.metric("Project Work", "92%", "+5%")

def show_settings():
    """Display settings and configuration"""
    
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your Guru Sahayam experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "🌐 Language", "🔧 Preferences", "🔒 Security"])
    
    with tab1:
        st.subheader("Teacher Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Full Name", value=st.session_state.user_data['teacher_name'])
            st.text_input("School", value=st.session_state.user_data['school'])
            st.text_input("Email", value="teacher@school.edu")
            st.text_input("Phone", value="+91 98765 43210")
        
        with col2:
            st.multiselect("Teaching Grades", 
                          ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8"],
                          default=st.session_state.user_data['grades'])
            st.multiselect("Subjects", 
                          ["Mathematics", "Science", "English", "Social Studies", "Hindi", "Computer Science"],
                          default=st.session_state.user_data['subjects'])
            st.selectbox("Experience Level", ["1-3 years", "4-7 years", "8-15 years", "15+ years"])
    
    with tab2:
        st.subheader("Language & Cultural Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.multiselect("Preferred Languages", 
                          ["English", "Hindi", "Marathi", "Telugu", "Tamil", "Bengali", "Gujarati"],
                          default=st.session_state.user_data['languages'])
            st.selectbox("Default Language", ["English", "Hindi", "Marathi", "Telugu", "Tamil"])
        
        with col2:
            st.selectbox("Cultural Context", 
                        ["Rural farming community", "Urban middle class", "Tribal community", 
                         "Coastal fishing village", "Mountain region", "Desert region"],
                        index=0)
            st.checkbox("Auto-translate content", value=True)
            st.checkbox("Include cultural examples", value=True)
    
    with tab3:
        st.subheader("Interface Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Theme", ["Light", "Dark", "Auto"])
            st.selectbox("Dashboard Layout", ["Grid", "List", "Compact"])
            st.slider("Refresh Rate (seconds)", 10, 60, 30)
        
        with col2:
            st.checkbox("Mobile optimization", value=True)
            st.checkbox("Voice input enabled", value=True)
            st.checkbox("Auto-save drafts", value=True)
            st.checkbox("Notifications", value=True)
    
    with tab4:
        st.subheader("Security & Privacy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Two-factor authentication", value=False)
            st.checkbox("Session timeout", value=True)
            st.checkbox("Data encryption", value=True)
        
        with col2:
            st.checkbox("Content filtering", value=True)
            st.checkbox("Privacy compliance", value=True)
            st.checkbox("Audit logging", value=True)
        
        st.button("🔒 Change Password")
        st.button("📤 Export Data")
        st.button("🗑️ Delete Account", type="secondary")

def show_mobile_view():
    """Display mobile-optimized interface"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📱 Mobile Interface</h1>
        <p>Optimized for teachers on the go</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile interface simulation
    st.markdown("""
    <div style="max-width: 375px; margin: 0 auto; background: white; border-radius: 20px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; text-align: center;">
            <h3>📱 Guru Sahayam Mobile</h3>
            <p>Quick access for teachers on the go</p>
        </div>
        <div style="padding: 20px;">
            <div style="background: white; border-radius: 15px; padding: 20px; 
                        margin-bottom: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                <h4>🎯 Quick Actions</h4>
                <button style="width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; border: none; border-radius: 10px; font-size: 1rem; font-weight: 600; 
                               cursor: pointer; margin-bottom: 10px;">📚 Create Lesson</button>
                <button style="width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; border: none; border-radius: 10px; font-size: 1rem; font-weight: 600; 
                               cursor: pointer; margin-bottom: 10px;">❓ Generate Quiz</button>
                <button style="width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; border: none; border-radius: 10px; font-size: 1rem; font-weight: 600; 
                               cursor: pointer; margin-bottom: 10px;">📝 Write Feedback</button>
                <button style="width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; border: none; border-radius: 10px; font-size: 1rem; font-weight: 600; 
                               cursor: pointer;">📊 View Progress</button>
            </div>
            
            <div style="background: white; border-radius: 15px; padding: 20px; 
                        margin-bottom: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                <h4>📈 Today's Stats</h4>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span>Time Saved: 3.5h</span>
                    <span style="color: #28a745;">↗️</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span>Students Engaged: 92%</span>
                    <span style="color: #28a745;">↗️</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span>Content Quality: 4.8/5</span>
                    <span style="color: #28a745;">↗️</span>
                </div>
            </div>
            
            <div style="background: white; border-radius: 15px; padding: 20px; 
                        box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                <h4>🔔 Notifications</h4>
                <div style="background: #fff3cd; padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <strong>New lesson plan ready!</strong><br>
                    Science - Grade 4-6
                </div>
                <div style="background: #d4edda; padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <strong>Student progress update</strong><br>
                    Priya improved by 15%
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 