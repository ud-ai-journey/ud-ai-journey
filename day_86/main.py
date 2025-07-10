"""
🎓 Guru Sahayam - Enhanced AI Teaching Assistant
Enhanced with refined prompt engineering and improved UI
Day 86 of the 100 Days Python & AI Challenge
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os
import time
from typing import Dict, Any, List

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBuhkDZVZhXKtui6ElYYg5rhFrazshJUrk"
genai.configure(api_key=GEMINI_API_KEY)

# Enhanced model configuration
MODEL_NAME = "gemini-2.5-flash"

# Enhanced token limits
MAX_TOKENS_LESSON_PLAN = 4000
MAX_TOKENS_QUIZ = 3500
MAX_TOKENS_FEEDBACK = 2000
MAX_TOKENS_STORY = 3000
MAX_TOKENS_EMAIL = 2500

# Page configuration with enhanced styling
st.set_page_config(
    page_title="🎓 Guru Sahayam - Enhanced AI Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .success-card {
        border-left-color: #28a745;
    }
    
    .warning-card {
        border-left-color: #ffc107;
    }
    
    .info-card {
        border-left-color: #17a2b8;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .metric-display {
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        color: #28a745;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.5s ease;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stSelectbox > div > div > div {
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'teacher_name': 'Uday Kumar',
        'school': 'Rural Primary School',
        'grades': ['Grade 3', 'Grade 4', 'Grade 5'],
        'subjects': ['Mathematics', 'Science', 'English'],
        'languages': ['English', 'Hindi', 'Marathi'],
        'cultural_context': 'Rural farming community with traditional values',
        'teaching_style': 'Interactive and hands-on learning',
        'class_size': '25-30 students'
    }

if 'recent_activities' not in st.session_state:
    st.session_state.recent_activities = []

def generate_enhanced_ai_response(prompt: str, max_tokens: int, temperature: float = 0.7) -> str:
    """
    Enhanced AI response generator with better error handling and response formatting
    """
    try:
        # Use the correct API for the current version
        model = genai.GenerativeModel(MODEL_NAME)
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "❌ **Unexpected Error:** Please try again."
            
    except Exception as e:
        return f"❌ **Connection Error:** {str(e)}"

def create_enhanced_lesson_prompt(subject: str, topic: str, grade_level: str, duration: str, 
                                learning_style: str, special_requirements: str, 
                                cultural_context: str, teaching_style: str) -> str:
    """
    Enhanced prompt engineering for lesson plan generation
    """
    return f"""
You are Guru Sahayam, an expert Indian educator with 20+ years of experience in rural and urban schools across India. You specialize in creating culturally relevant, engaging lesson plans that work in real Indian classrooms.

**CONTEXT:**
- Teacher: {st.session_state.user_data['teacher_name']}
- School: {st.session_state.user_data['school']}
- Cultural Context: {cultural_context}
- Teaching Style: {teaching_style}
- Class Size: {st.session_state.user_data['class_size']}

**LESSON SPECIFICATIONS:**
- Subject: {subject}
- Topic: {topic}
- Grade Level: {grade_level}
- Duration: {duration}
- Learning Style Focus: {learning_style}
{f"- Special Requirements: {special_requirements}" if special_requirements else ""}

**CREATION GUIDELINES:**
1. **Cultural Relevance**: Use local examples, stories, and contexts that students can relate to
2. **Practical Approach**: Focus on hands-on activities and real-world applications
3. **Language Sensitivity**: Consider multilingual classroom needs
4. **Resource Constraints**: Design for limited resources (minimal technology, basic materials)
5. **Assessment**: Include both formative and summative assessment strategies
6. **Differentiation**: Address varying learning levels within the same class

**STRUCTURE YOUR RESPONSE AS:**

## 🎯 LEARNING OBJECTIVES
- 3-4 specific, measurable objectives
- Grade-appropriate language and complexity

## 📚 PREREQUISITES & PRIOR KNOWLEDGE
- What students should already know
- How to assess prior knowledge

## 🛠️ MATERIALS & RESOURCES
- List all required materials (keep it minimal)
- Technology requirements (if any)
- Handouts or worksheets needed

## 📖 LESSON STRUCTURE

### 🌅 Opening (5-10 minutes)
- Engaging hook using local context
- Connection to students' daily lives
- Clear learning goals presentation

### 🎯 Main Content (majority of time)
- Step-by-step teaching sequence
- Interactive student activities
- Regular checks for understanding
- Cultural integration points

### 🏁 Closure (5-10 minutes)
- Summary activity
- Connection to next lesson
- Homework preview

## 📊 ASSESSMENT STRATEGIES
- Formative assessment during lesson
- Summative assessment options
- Success criteria for each objective

## 🎨 DIFFERENTIATION STRATEGIES
- Support for struggling learners
- Extensions for advanced students
- Accommodations for special needs
- Multilingual support options

## 🏠 HOMEWORK & EXTENSION
- Meaningful homework assignment
- Additional resources for interested students
- Parent involvement suggestions

## 💡 TEACHING TIPS
- Classroom management strategies
- Common challenges and solutions
- Time management tips

Make this lesson plan practical, culturally relevant, and ready for immediate use in an Indian classroom setting.
"""

def create_enhanced_quiz_prompt(subject: str, topic: str, grade_level: str, 
                              question_types: List[str], difficulty: str, 
                              cultural_context: str) -> str:
    """
    Enhanced prompt engineering for quiz generation
    """
    return f"""
You are an expert Indian educator creating culturally relevant assessments for {grade_level} students.

**CONTEXT:**
- Subject: {subject}
- Topic: {topic}
- Grade Level: {grade_level}
- Difficulty: {difficulty}
- Cultural Context: {cultural_context}

**QUIZ REQUIREMENTS:**
- Question Types: {', '.join(question_types)}
- Include local examples and contexts
- Use age-appropriate language
- Mix of difficulty levels
- Clear, unambiguous questions

**STRUCTURE YOUR RESPONSE AS:**

## 📝 QUIZ QUESTIONS

### Multiple Choice Questions (if selected)
- 4 options per question
- Only one correct answer
- Include local context where possible

### True/False Questions (if selected)
- Clear, unambiguous statements
- Mix of true and false statements

### Short Answer Questions (if selected)
- 2-3 sentence responses expected
- Include local examples

### Essay Questions (if selected)
- Clear rubric expectations
- Cultural relevance

## 📊 ANSWER KEY
- Correct answers with explanations
- Partial credit guidelines
- Common misconceptions to watch for

## 🎯 ASSESSMENT RUBRIC
- Point distribution
- Grading criteria
- Time allocation suggestions

Make questions engaging, culturally relevant, and appropriate for Indian students at this grade level.
"""

def create_enhanced_feedback_prompt(student_name: str, subject: str, performance: str, 
                                  strengths: str, areas_improvement: str, 
                                  cultural_context: str) -> str:
    """
    Enhanced prompt engineering for feedback generation
    """
    return f"""
You are a caring Indian teacher writing personalized feedback for a student's parent.

**STUDENT CONTEXT:**
- Name: {student_name}
- Subject: {subject}
- Performance: {performance}
- Strengths: {strengths}
- Areas for Improvement: {areas_improvement}
- Cultural Context: {cultural_context}

**FEEDBACK GUIDELINES:**
1. **Tone**: Warm, encouraging, and culturally sensitive
2. **Language**: Clear and accessible to parents
3. **Structure**: Organized and easy to read
4. **Actionable**: Include specific suggestions for improvement
5. **Positive**: Focus on growth and potential

**STRUCTURE YOUR RESPONSE AS:**

## 📝 STUDENT FEEDBACK REPORT

### 🎯 Overall Performance
- Brief summary of current performance
- Progress made this term

### 🌟 Strengths & Achievements
- Specific examples of what the student does well
- Positive reinforcement

### 📈 Areas for Growth
- Specific areas needing improvement
- Constructive suggestions
- Resources or support needed

### 🏠 How Parents Can Help
- Specific suggestions for home support
- Activities parents can do with the child
- Communication strategies

### 📚 Next Steps
- Goals for the coming weeks
- Teacher's commitment to support
- Timeline for follow-up

Make this feedback encouraging, practical, and culturally appropriate for Indian families.
"""

def main():
    """Main application function"""
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Guru Sahayam - Enhanced AI Teaching Assistant</h1>
        <p>Empowering Indian Teachers with Culturally Relevant AI Tools</p>
        <p><strong>Teacher:</strong> {teacher_name} | <strong>School:</strong> {school}</p>
    </div>
    """.format(
        teacher_name=st.session_state.user_data['teacher_name'],
        school=st.session_state.user_data['school']
    ), unsafe_allow_html=True)
    
    # Enhanced sidebar
    st.sidebar.title("🛠️ Guru Sahayam Tools")
    st.sidebar.markdown("---")
    
    feature = st.sidebar.selectbox(
        "Choose your tool:",
        [
            "📚 Enhanced Lesson Plan Generator",
            "❓ Smart Quiz Maker",
            "📝 Personalized Feedback Writer",
            "📖 Homework Helper",
            "✍️ Creative Writing Assistant",
            "📚 Cultural Story Generator",
            "📧 Parent Communication Helper",
            "🌍 Multilingual Learning Buddy",
            "📊 Student Progress Tracker",
            "⚙️ Settings & Preferences"
        ]
    )
    
    # Display selected feature
    if feature == "📚 Enhanced Lesson Plan Generator":
        show_enhanced_lesson_generator()
    elif feature == "❓ Smart Quiz Maker":
        show_smart_quiz_maker()
    elif feature == "📝 Personalized Feedback Writer":
        show_feedback_writer()
    elif feature == "📖 Homework Helper":
        show_homework_helper()
    elif feature == "✍️ Creative Writing Assistant":
        show_creative_writing_assistant()
    elif feature == "📚 Cultural Story Generator":
        show_cultural_story_generator()
    elif feature == "📧 Parent Communication Helper":
        show_parent_communication_helper()
    elif feature == "🌍 Multilingual Learning Buddy":
        show_multilingual_buddy()
    elif feature == "📊 Student Progress Tracker":
        show_progress_tracker()
    elif feature == "⚙️ Settings & Preferences":
        show_settings()

def show_enhanced_lesson_generator():
    """Enhanced lesson plan generator with refined prompts"""
    st.header("📚 Enhanced Lesson Plan Generator")
    st.markdown("Create culturally relevant, engaging lesson plans in minutes!")
    
    # User input section
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox(
            "Subject:",
            ["Mathematics", "Science", "English", "Hindi", "Social Studies", 
             "Environmental Studies", "Art & Craft", "Physical Education", "Other"]
        )
        if subject == "Other":
            subject = st.text_input("Enter subject:")
            
        topic = st.text_input("Topic/Theme:", placeholder="e.g., Fractions, Photosynthesis, Story Writing")
        
        grade_level = st.selectbox(
            "Grade Level:",
            ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", 
             "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"]
        )
    
    with col2:
        duration = st.selectbox(
            "Lesson Duration:",
            ["30 minutes", "45 minutes", "60 minutes", "90 minutes", "120 minutes", "Custom"]
        )
        if duration == "Custom":
            duration = st.text_input("Enter duration:")
            
        learning_style = st.selectbox(
            "Learning Style Focus:",
            ["Mixed (Visual, Auditory, Kinesthetic)", "Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
        )
        
        special_requirements = st.text_area(
            "Special Requirements:",
            placeholder="Any specific requirements, accommodations, or focus areas..."
        )
    
    # Generate button with enhanced styling
    if st.button("🚀 Generate Enhanced Lesson Plan", type="primary", use_container_width=True):
        if topic and subject:
            with st.spinner("🎓 Guru Sahayam is creating your lesson plan..."):
                # Create enhanced prompt
                prompt = create_enhanced_lesson_prompt(
                    subject, topic, str(grade_level or ""), str(duration or ""), str(learning_style or ""), 
                    special_requirements, st.session_state.user_data['cultural_context'],
                    st.session_state.user_data['teaching_style']
                )
                
                # Generate response
                response = generate_enhanced_ai_response(prompt, MAX_TOKENS_LESSON_PLAN)
                
                # Display result
                st.markdown("### 📋 Generated Lesson Plan")
                st.markdown(response)
                
                # Add to recent activities
                st.session_state.recent_activities.append({
                    'timestamp': datetime.now().isoformat(),
                    'activity': f'Generated lesson plan for {subject} - {topic}',
                    'type': 'lesson_plan'
                })
                
                # Success message
                st.success("✅ Lesson plan generated successfully!")
        else:
            st.error("Please fill in all required fields.")

def show_smart_quiz_maker():
    """Smart quiz maker with enhanced prompts"""
    st.header("❓ Smart Quiz Maker")
    st.markdown("Create culturally relevant assessments in minutes!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox("Subject:", ["Mathematics", "Science", "English", "Hindi", "Social Studies"])
        topic = st.text_input("Topic:", placeholder="e.g., Fractions, Photosynthesis")
        grade_level = st.selectbox("Grade Level:", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
        
    with col2:
        difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard", "Mixed"])
        question_types = st.multiselect(
            "Question Types:",
            ["Multiple Choice", "True/False", "Short Answer", "Essay"],
            default=["Multiple Choice"]
        )
    
    if st.button("🎯 Generate Smart Quiz", type="primary", use_container_width=True):
        if topic and subject and question_types:
            with st.spinner("Creating your quiz..."):
                prompt = create_enhanced_quiz_prompt(
                    subject, topic, str(grade_level or ""), question_types, str(difficulty or ""),
                    st.session_state.user_data['cultural_context']
                )
                
                response = generate_enhanced_ai_response(prompt, MAX_TOKENS_QUIZ)
                
                st.markdown("### 📝 Generated Quiz")
                st.markdown(response)
                
                st.success("✅ Quiz generated successfully!")

def show_feedback_writer():
    """Personalized feedback writer"""
    st.header("📝 Personalized Feedback Writer")
    st.markdown("Create warm, encouraging feedback for parents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("Student Name:")
        subject = st.selectbox("Subject:", ["Mathematics", "Science", "English", "Hindi", "Social Studies"])
        performance = st.selectbox("Overall Performance:", ["Excellent", "Good", "Satisfactory", "Needs Improvement"])
        
    with col2:
        strengths = st.text_area("Student Strengths:", placeholder="What does the student do well?")
        areas_improvement = st.text_area("Areas for Improvement:", placeholder="What can the student work on?")
    
    if st.button("💌 Generate Feedback", type="primary", use_container_width=True):
        if student_name and subject:
            with st.spinner("Writing personalized feedback..."):
                prompt = create_enhanced_feedback_prompt(
                    student_name, subject, str(performance or ""), strengths, areas_improvement,
                    st.session_state.user_data['cultural_context']
                )
                
                response = generate_enhanced_ai_response(prompt, MAX_TOKENS_FEEDBACK)
                
                st.markdown("### 📝 Student Feedback")
                st.markdown(response)
                
                st.success("✅ Feedback generated successfully!")

def show_homework_helper():
    """Homework helper feature"""
    st.header("📖 Homework Helper")
    st.markdown("Get help with homework assignments and explanations")
    
    homework_topic = st.text_input("Homework Topic:", placeholder="e.g., Math problem, Science concept")
    grade_level = st.selectbox("Grade Level:", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
    specific_question = st.text_area("Specific Question or Problem:", placeholder="Describe what you need help with...")
    
    if st.button("🤔 Get Homework Help", type="primary", use_container_width=True):
        if homework_topic and specific_question:
            with st.spinner("Analyzing your homework..."):
                prompt = f"""
You are a helpful Indian teacher assisting a {grade_level} student with homework.

Topic: {homework_topic}
Question: {specific_question}
Cultural Context: {st.session_state.user_data['cultural_context']}

Provide:
1. Clear, step-by-step explanation
2. Relevant examples from daily life
3. Additional practice problems
4. Tips for understanding the concept

Make it engaging and appropriate for the student's age level.
"""
                
                response = generate_enhanced_ai_response(prompt, 2000)
                
                st.markdown("### 📚 Homework Help")
                st.markdown(response)
                
                st.success("✅ Homework help provided!")

def show_creative_writing_assistant():
    """Creative writing assistant"""
    st.header("✍️ Creative Writing Assistant")
    st.markdown("Get help with creative writing assignments")
    
    writing_type = st.selectbox("Writing Type:", ["Story", "Essay", "Poem", "Letter", "Report"])
    topic = st.text_input("Topic or Theme:", placeholder="e.g., My Family, A Rainy Day, My Village")
    grade_level = st.selectbox("Grade Level:", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
    
    if st.button("✍️ Get Writing Help", type="primary", use_container_width=True):
        if topic:
            with st.spinner("Helping with creative writing..."):
                prompt = f"""
You are an expert Indian teacher helping a {grade_level} student with creative writing.

Writing Type: {writing_type}
Topic: {topic}
Cultural Context: {st.session_state.user_data['cultural_context']}

Provide:
1. Writing prompts and ideas
2. Vocabulary suggestions
3. Structure guidelines
4. Cultural elements to include
5. Example sentences or paragraphs

Make it engaging and culturally relevant.
"""
                
                response = generate_enhanced_ai_response(prompt, MAX_TOKENS_STORY)
                
                st.markdown("### ✍️ Writing Assistance")
                st.markdown(response)
                
                st.success("✅ Writing help provided!")

def show_cultural_story_generator():
    """Cultural story generator"""
    st.header("📚 Cultural Story Generator")
    st.markdown("Create culturally relevant stories for your students")
    
    story_type = st.selectbox("Story Type:", ["Moral Story", "Educational Story", "Cultural Story", "Adventure Story"])
    theme = st.text_input("Theme or Topic:", placeholder="e.g., Honesty, Friendship, Village Life")
    grade_level = st.selectbox("Grade Level:", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
    
    if st.button("📖 Generate Story", type="primary", use_container_width=True):
        if theme:
            with st.spinner("Creating a cultural story..."):
                prompt = f"""
You are an expert Indian storyteller creating a {str(story_type or "").lower()} for {str(grade_level or "")} students.

Theme: {theme}
Cultural Context: {st.session_state.user_data['cultural_context']}

Create:
1. An engaging story with local characters
2. Cultural elements and values
3. Age-appropriate language
4. Discussion questions
5. Moral or learning point

Make it culturally relevant and educational.
"""
                
                response = generate_enhanced_ai_response(prompt, MAX_TOKENS_STORY)
                
                st.markdown("### 📚 Cultural Story")
                st.markdown(response)
                
                st.success("✅ Story generated successfully!")

def show_parent_communication_helper():
    """Parent communication helper"""
    st.header("📧 Parent Communication Helper")
    st.markdown("Create effective communication with parents")
    
    communication_type = st.selectbox("Communication Type:", ["Progress Report", "Behavior Notice", "Achievement Celebration", "General Update"])
    student_name = st.text_input("Student Name:")
    key_points = st.text_area("Key Points to Include:", placeholder="What do you want to communicate?")
    
    if st.button("📧 Generate Communication", type="primary", use_container_width=True):
        if student_name and key_points:
            with st.spinner("Creating parent communication..."):
                prompt = f"""
You are a caring Indian teacher writing to a parent about their child.

Communication Type: {communication_type}
Student: {student_name}
Key Points: {key_points}
Cultural Context: {st.session_state.user_data['cultural_context']}

Write:
1. Warm, respectful tone
2. Clear, actionable information
3. Cultural sensitivity
4. Specific examples
5. Next steps or follow-up

Make it professional yet personal.
"""
                
                response = generate_enhanced_ai_response(prompt, MAX_TOKENS_EMAIL)
                
                st.markdown("### 📧 Parent Communication")
                st.markdown(response)
                
                st.success("✅ Communication created successfully!")

def show_multilingual_buddy():
    """Multilingual learning buddy"""
    st.header("🌍 Multilingual Learning Buddy")
    st.markdown("Get help with multiple languages")
    
    source_language = st.selectbox("From Language:", ["English", "Hindi", "Marathi", "Other"])
    target_language = st.selectbox("To Language:", ["English", "Hindi", "Marathi", "Other"])
    content = st.text_area("Content to Translate/Explain:", placeholder="Enter text or concept to work with")
    
    if st.button("🌍 Get Language Help", type="primary", use_container_width=True):
        if content:
            with st.spinner("Processing language request..."):
                prompt = f"""
You are a multilingual Indian teacher helping with language learning.

From: {source_language}
To: {target_language}
Content: {content}
Cultural Context: {st.session_state.user_data['cultural_context']}

Provide:
1. Translation if needed
2. Cultural context and explanations
3. Usage examples
4. Related vocabulary
5. Learning tips

Make it educational and culturally relevant.
"""
                
                response = generate_enhanced_ai_response(prompt, 2000)
                
                st.markdown("### 🌍 Language Assistance")
                st.markdown(response)
                
                st.success("✅ Language help provided!")

def show_progress_tracker():
    """Student progress tracker"""
    st.header("📊 Student Progress Tracker")
    st.markdown("Track and visualize student progress")
    
    # Simulated progress data
    st.markdown("### 📈 Progress Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card success-card">
            <h3>📚 Mathematics</h3>
            <div class="progress-container">
                <div class="progress-fill" style="width: 85%;"></div>
            </div>
            <p>85% - Excellent Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card info-card">
            <h3>🔬 Science</h3>
            <div class="progress-container">
                <div class="progress-fill" style="width: 78%;"></div>
            </div>
            <p>78% - Good Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card warning-card">
            <h3>📖 English</h3>
            <div class="progress-container">
                <div class="progress-fill" style="width: 65%;"></div>
            </div>
            <p>65% - Needs Attention</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("📊 Progress tracking features coming soon!")

def show_settings():
    """Settings and preferences"""
    st.header("⚙️ Settings & Preferences")
    st.markdown("Customize your Guru Sahayam experience")
    
    st.subheader("👤 Teacher Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Teacher Name", value=st.session_state.user_data['teacher_name'])
        st.text_input("School Name", value=st.session_state.user_data['school'])
        st.text_input("Class Size", value=st.session_state.user_data['class_size'])
        
    with col2:
        st.multiselect("Teaching Grades", 
                      ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"],
                      default=st.session_state.user_data['grades'])
        st.multiselect("Subjects Taught",
                      ["Mathematics", "Science", "English", "Hindi", "Social Studies"],
                      default=st.session_state.user_data['subjects'])
    
    st.subheader("🌍 Cultural Context")
    cultural_context = st.text_area("Cultural Context", 
                                   value=st.session_state.user_data['cultural_context'],
                                   placeholder="Describe your school's cultural context...")
    
    st.subheader("🎯 Teaching Preferences")
    teaching_style = st.selectbox("Teaching Style", 
                                 ["Interactive and hands-on", "Traditional lecture-based", 
                                  "Technology-focused", "Mixed approach"],
                                 index=0)
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")

if __name__ == "__main__":
    main() 