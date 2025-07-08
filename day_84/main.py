import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os
import base64
from google.generativeai import types
from PIL import Image
from io import BytesIO
import streamlit.components.v1 as components

# --- API Configuration ---
# Best practice: Use Streamlit secrets for your API key.
# Create a .streamlit/secrets.toml file with:
# GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
# Then use: genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# For this example, we'll use the provided key, but remember to secure it.
GEMINI_API_KEY = "AIzaSyBuhkDZVZhXKtui6ElYYg5rhFrazshJUrk"
# Remove genai.configure(api_key=GEMINI_API_KEY) as it's not needed for google-genai
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
# except Exception as e:
#     st.error(f"API Key configuration failed: {e}")
#     st.stop() # Stop the app if API key is invalid or not configured

MODEL_NAME = "gemini-2.5-flash"

# --- Token Limits ---
# Adjusted for potentially longer outputs from the new tools
MAX_TOKENS_LESSON_PLAN = 3000
MAX_TOKENS_QUIZ = 3000
MAX_TOKENS_FEEDBACK = 2000
MAX_TOKENS_HOMEWORK_SUMMARY = 1500
MAX_TOKENS_CREATIVE_WRITING = 1500
MAX_TOKENS_MORAL_STORY = 1500
MAX_TOKENS_PARENT_EMAIL = 1500
MAX_TOKENS_LANGUAGE_BUDDY = 500

# --- Safety Settings ---
# Default safety settings - can be overridden by the Test Safety Feature
DEFAULT_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# --- Page Configuration ---
st.set_page_config(
    page_title="GURU SAHAYAM - Hackathon Edition",
    page_icon="🎓",
    layout="wide"
)

# --- Hackathon Banner ---
st.markdown("""
<div style='background: linear-gradient(90deg, #4f8cff 0%, #38e8ff 100%); padding: 1rem 0; border-radius: 8px; text-align: center; margin-bottom: 1rem;'>
    <span style='font-size: 2rem; font-weight: bold; color: white;'>🚀 GURU SAHAYAM <span style='font-size:1.2rem;'>(ClassGenie Hackathon Edition)</span></span><br/>
    <span style='color: #fff; font-size: 1.1rem;'>Empowering Teachers in Multi-Grade Classrooms &mdash; Agentic AI Day Hackathon 2024</span>
</div>
""", unsafe_allow_html=True)

# --- Title and Description ---
st.title("🎓 GURU SAHAYAM - AI Assistant for Schools")
st.markdown("*Empowering Teachers & Students with Smart AI Tools for India's Diverse Classrooms*")

# --- Hackathon Context ---
st.info("""
**About this Project:**  
This is a special hackathon edition of ClassGenie, rebranded as **GURU SAHAYAM** for the Agentic AI Day 2024. It is designed to empower teachers in multi-grade, multi-lingual, and culturally diverse classrooms across India.  

**Key Features:**  
- Local language support  
- Cultural/Regional/Community context awareness  
- Visual aids suggestions  
- Speech-to-text input  
- User-friendly, hackathon-ready UI
""")

# --- Quick Start / How to Use Expander ---
with st.expander("🚦 Quick Start / How to Use"):
    st.markdown("""
    1. **Select Output Language:** Choose your preferred language for all AI-generated content.
    2. **(Optional) Enter Cultural/Regional/Community Context:** E.g., 'Rural Karnataka', 'Andhra Chenchus', 'Urban Delhi', etc. This will tailor lesson plans, quizzes, and feedback to your classroom's needs.
    3. **Choose a Tool:** Pick from Lesson Plan Generator, Quiz Maker, Feedback Writer, and more.
    4. **Fill in the Details:** Enter subject, topic, grade, and other options as prompted.
    5. **Use Speech-to-Text:** Click the mic icon to dictate inputs (works best in Chrome).
    6. **Generate & Download:** Click the generate button, review the output, and download as needed.
    7. **Visual Aids:** If enabled, get suggestions for diagrams/images to support your lesson.
    """)

# --- Sidebar for Feature Selection ---
st.sidebar.title("🛠️ ClassGenie Tools")
# Add language selection dropdown
supported_languages = [
    "English",
    "Hindi",
    "Kannada",
    "Tamil",
    "Telugu",
    "Marathi",
    "Bengali",
    "Gujarati",
    "Punjabi",
    "Malayalam",
    "Odia",
    "Assamese",
    "Urdu"
]
language = st.sidebar.selectbox("Select Output Language:", supported_languages, index=0)

# Add cultural context input
global_cultural_context = st.sidebar.text_input(
    "Cultural/Regional/Community Context (optional):",
    placeholder="e.g., Rural Karnataka, Tribal community, Urban Delhi, Marathi-medium, etc."
)

feature = st.sidebar.selectbox(
    "Choose a tool:",
    [
        "📚 Lesson Plan Generator",
        "❓ Quiz Maker",
        "📝 Feedback Writer",
        "📖 Homework Summarizer",
        "✍️ Creative Writing Starter",
        "📚 Moral Story Generator",
        "📧 Parent Email Generator",
        "🌍 Language Buddy",
        "🧪 Test Safety Feature"
    ]
)

# --- AI Response Generation Function ---
def generate_ai_response(prompt, max_tokens, safety_settings_override=None):
    """
    Generates AI response using Gemini API with robust error handling.
    For google-genai v1.24.0: uses genai.configure and genai.GenerativeModel.
    """
    try:
        current_safety_settings = safety_settings_override if safety_settings_override is not None else DEFAULT_SAFETY_SETTINGS

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.7,
            },
            safety_settings=current_safety_settings
        )

        if response and hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                text_response = "".join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
                return text_response
            else:
                finish_reason = candidate.finish_reason.name if hasattr(candidate, 'finish_reason') and candidate.finish_reason else "UNKNOWN"
                if finish_reason == "SAFETY":
                    return "❌ **AI Safety Filter Activated:** The generated content was blocked due to safety guidelines. Please try a different prompt or topic."
                elif finish_reason == "MAX_TOKENS":
                    return f"⚠️ **Max tokens reached ({max_tokens}):** The response was truncated. Consider a longer response by increasing the `max_tokens` parameter or by making the prompt more focused."
                elif finish_reason == "STOP_SEQUENCE":
                     return "⚠️ **Stop sequence reached:** The response was truncated. Consider refining your prompt."
                else:
                    return f"❌ **AI returned no usable content.** Reason: {finish_reason}"
        else:
            return "❌ **An unexpected error occurred with the AI response.** Please try again."

    except Exception as e:
        return f"❌ **An error occurred:** {str(e)}"

# Add this function to generate an image from a prompt using Gemini/Imagen

def generate_gemini_image(prompt, api_key):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )
    images = []
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            images.append(image)
    return images

# Helper function to parse visual aids from text

def parse_visual_aids(text):
    lines = text.split('\n')
    visual_aids = []
    capture = False
    for line in lines:
        if 'visual aid' in line.lower() or 'visual:' in line.lower() or 'diagram' in line.lower() or 'chart' in line.lower():
            capture = True
        if capture and (line.strip() != '' and not line.strip().startswith('#')):
            visual_aids.append(line.strip())
        if capture and (line.strip() == '' or line.strip().startswith('##')):
            capture = False
    return visual_aids

# Custom speech-to-text component using Web Speech API

def speech_to_text(label, key, language='en-IN'):
    st.write(label)
    # Add a container for error messages
    error_placeholder = st.empty()
    html_string = f'''
    <div style="display: flex; align-items: center; gap: 8px;">
        <input id="stt_input_{key}" type="text" style="width: 300px; padding: 6px; font-size: 16px;" placeholder="Click mic and speak..." />
        <button id="stt_btn_{key}" style="background: #f44336; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; font-size: 20px; cursor: pointer; position: relative; overflow: hidden;">
            <span id="stt_mic_icon_{key}" style="display: inline-block; transition: transform 0.2s;">🎤</span>
            <span id="stt_wave_{key}" style="display: none; position: absolute; left: 0; top: 0; width: 40px; height: 40px; border-radius: 50%; background: rgba(76,175,80,0.2); animation: stt_pulse_{key} 1s infinite;"></span>
        </button>
        <span id="stt_status_{key}" style="font-weight: bold; color: green; display: none; margin-left: 8px;">Listening...</span>
    </div>
    <div id="stt_error_{key}" style="color: red; font-weight: bold; margin-top: 4px;"></div>
    <style>
    @keyframes stt_pulse_{key} {{
        0% {{ transform: scale(1); opacity: 0.7; }}
        50% {{ transform: scale(1.3); opacity: 0.3; }}
        100% {{ transform: scale(1); opacity: 0.7; }}
    }}
    </style>
    <script>
    const btn = document.getElementById('stt_btn_{key}');
    const input = document.getElementById('stt_input_{key}');
    const status = document.getElementById('stt_status_{key}');
    const wave = document.getElementById('stt_wave_{key}');
    const errorDiv = document.getElementById('stt_error_{key}');
    let recognition = null;
    if (btn && input && status && wave && errorDiv) {{
        btn.onclick = function() {{
            if (!('webkitSpeechRecognition' in window)) {{
                errorDiv.textContent = 'Speech recognition not supported in this browser.';
                return;
            }}
            errorDiv.textContent = '';
            recognition = new webkitSpeechRecognition();
            recognition.lang = '{language}';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            // Show listening indicator and pulse
            status.style.display = 'inline';
            wave.style.display = 'block';
            btn.style.background = '#4CAF50'; // green
            recognition.onresult = function(event) {{
                input.value = event.results[0][0].transcript;
                const streamlitEvent = new CustomEvent('streamlit:setComponentValue', {{ detail: {{ value: input.value }} }});
                window.parent.document.dispatchEvent(streamlitEvent);
                // Hide listening indicator and pulse
                status.style.display = 'none';
                wave.style.display = 'none';
                btn.style.background = '#f44336'; // red
            }};
            recognition.onerror = function(event) {{
                let msg = 'Speech recognition error: ' + event.error;
                if (event.error === 'no-speech') {{
                    msg = 'No speech detected. Please try again and speak clearly into your microphone.';
                }} else if (event.error === 'audio-capture') {{
                    msg = 'No microphone detected. Please check your mic connection and permissions.';
                }} else if (event.error === 'not-allowed') {{
                    msg = 'Microphone access denied. Please allow mic access in your browser.';
                }}
                errorDiv.textContent = msg;
                // Hide listening indicator and pulse
                status.style.display = 'none';
                wave.style.display = 'none';
                btn.style.background = '#f44336'; // red
            }};
            recognition.onend = function() {{
                // Hide listening indicator and pulse
                status.style.display = 'none';
                wave.style.display = 'none';
                btn.style.background = '#f44336'; // red
            }};
            recognition.start();
        }};
    }}
    </script>
    '''
    recognized = components.html(html_string, height=80)
    return recognized

# --- Feature Implementations ---

# FEATURE 1: LESSON PLAN GENERATOR (Existing)
if feature == "📚 Lesson Plan Generator":
    st.header("📚 Lesson Plan Generator")
    st.markdown("Create comprehensive lesson plans in minutes!")
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject:", ["Science", "Mathematics", "English", "History", "Geography", "Art", "Physical Education", "Music", "Other"])
        if subject == "Other": subject = st.text_input("Enter subject:")
        # Use speech-to-text for topic input
        topic = st.text_input("Topic/Theme:", placeholder="e.g., Photosynthesis, Fractions, World War II", key="topic_text")
        stt_result = speech_to_text("Or use your voice for Topic/Theme:", key="topic_stt", language="en-IN")
        if stt_result and stt_result != "":
            topic = stt_result
    with col2:
        grade_level = st.selectbox("Grade Level:", ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"])
        duration = st.selectbox("Lesson Duration:", ["30 minutes", "45 minutes", "60 minutes", "90 minutes", "Custom"])
        if duration == "Custom": duration = st.text_input("Enter duration:")
    with st.expander("🔧 Advanced Options"):
        learning_style = st.selectbox("Learning Style Focus:", ["Mixed (Visual, Auditory, Kinesthetic)", "Visual", "Auditory", "Kinesthetic", "Reading/Writing"])
        special_requirements = st.text_area("Special Requirements:", placeholder="Any specific requirements, accommodations, or focus areas...")
    # Add visual aids checkbox
    include_visual_aids = st.checkbox("Include Visual Aids (images/diagrams)?", value=False)
    if st.button("🚀 Generate Lesson Plan", type="primary"):
        if topic and subject:
            visual_aids_instruction = "\n\nAdditionally, suggest 2-3 relevant visual aids (images, diagrams, or charts) that would help teach this lesson. For each, provide a title and a detailed description in {language}. If possible, describe what the image should depict so a teacher or student could draw or create it." if include_visual_aids else ""
            lesson_prompt = f"""
You are an experienced curriculum specialist and master teacher with 15+ years of classroom experience. 
Create a comprehensive, engaging lesson plan with the following specifications:
- Subject: {subject}
- Topic: {topic}
- Grade Level: {grade_level}
- Duration: {duration}
- Learning Style: {learning_style}
{f"- Special Requirements: {special_requirements}" if special_requirements else ""}
{f"- Cultural/Regional/Community Context: {global_cultural_context}" if global_cultural_context else ""}

Structure your lesson plan with these sections:
## LESSON OVERVIEW
- Clear learning objectives (3-4 specific, measurable goals)
- Key concepts students will master
- Prerequisites/prior knowledge needed
## MATERIALS & RESOURCES
- List all materials needed
- Technology requirements
- Handouts or worksheets needed
## LESSON STRUCTURE
### Opening (5-10 minutes)
- Hook/engagement activity
- Connection to prior learning
### Main Content (majority of time)
- Step-by-step teaching sequence
- Student activities and interactions
- Checks for understanding
### Closure (5-10 minutes)
- Summary activity
- Preview of next lesson
## ASSESSMENT
- Formative assessment strategies
- Summative assessment options
- Success criteria
## DIFFERENTIATION
- Support for struggling learners
- Extensions for advanced students
- Accommodations for special needs
## HOMEWORK/EXTENSION
- Optional homework assignment
- Additional resources for interested students
Make it practical, engaging, and age-appropriate. Use active learning strategies and include specific examples.

IMPORTANT: Write the entire lesson plan in {language}. If the language is not English, translate all content and section headings to {language}.{visual_aids_instruction}"
"""
            with st.spinner("🎯 Generating your lesson plan..."):
                lesson_plan = generate_ai_response(lesson_prompt, max_tokens=MAX_TOKENS_LESSON_PLAN)
            
            if not lesson_plan.startswith("❌") and not lesson_plan.startswith("⚠️"):
                st.session_state['lesson_plan'] = lesson_plan
                st.session_state['visual_aids'] = parse_visual_aids(lesson_plan) if include_visual_aids else []
            else:
                st.error(lesson_plan)
        else:
            st.error("Please fill in the subject and topic fields.")

    # Always display the lesson plan and visual aids if present
    if 'lesson_plan' in st.session_state:
        st.success("✅ Lesson Plan Generated!")
        st.markdown(st.session_state['lesson_plan'])
        if include_visual_aids and 'visual_aids' in st.session_state:
            st.subheader("Visual Aids")
            for idx, va in enumerate(st.session_state['visual_aids']):
                # Improve the prompt for image generation
                improved_prompt = f"Create an educational, colorful, labeled diagram: {va}. Make it clear and suitable for students."
                st.markdown(f"**{va}**")
                if st.button(f"Generate Image for Visual Aid {idx+1}", key=f"lesson_visual_{idx}"):
                    with st.spinner("Generating image..."):
                        try:
                            images = generate_gemini_image(improved_prompt, api_key=GEMINI_API_KEY)
                            if images:
                                st.session_state[f"lesson_image_{idx}"] = images[0]
                            else:
                                st.session_state[f"lesson_image_{idx}"] = None
                        except Exception as e:
                            st.error(f"Image generation failed: {e}")
                            st.session_state[f"lesson_image_{idx}"] = None
                if f"lesson_image_{idx}" in st.session_state and st.session_state[f"lesson_image_{idx}"]:
                    st.image(st.session_state[f"lesson_image_{idx}"])
                elif f"lesson_image_{idx}" in st.session_state and st.session_state[f"lesson_image_{idx}"] is None:
                    st.error("No image generated. Try a different prompt or check your API key.")
        st.download_button(label="📥 Download Lesson Plan", data=st.session_state['lesson_plan'], file_name=f"{subject}_{topic}_{grade_level}_lesson_plan.txt", mime="text/plain")

# FEATURE 2: QUIZ MAKER (Existing)
elif feature == "❓ Quiz Maker":
    st.header("❓ Quiz Maker")
    st.markdown("Generate quizzes and assessments instantly!")
    
    col1, col2 = st.columns(2)
    with col1:
        # Add speech-to-text for quiz subject/topic
        quiz_subject = st.text_input("Subject/Topic:", placeholder="e.g., Ancient Rome, Algebra, Cell Biology", key="quiz_subject_text")
        quiz_subject_stt = speech_to_text("Or use your voice for Subject/Topic:", key="quiz_subject_stt", language="en-IN")
        if quiz_subject_stt and quiz_subject_stt != "":
            quiz_subject = quiz_subject_stt
        quiz_type = st.selectbox("Quiz Type:", ["Multiple Choice", "True/False", "Short Answer", "Mixed Format"])
    with col2:
        num_questions = st.slider("Number of Questions:", 5, 20, 10)
        difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard", "Mixed"])
        grade_level_quiz = st.selectbox("Grade Level:", ["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/Adult"])
    
    include_visual_aids_quiz = st.checkbox("Include Visual Aids (images/diagrams)?", value=False)
    if st.button("🎯 Generate Quiz", type="primary"):
        if quiz_subject:
            visual_aids_instruction_quiz = "\n\nAdditionally, suggest 2-3 relevant visual aids (images, diagrams, or charts) that would help students answer or understand the quiz questions. For each, provide a title and a detailed description in {language}. If possible, describe what the image should depict so a teacher or student could draw or create it." if include_visual_aids_quiz else ""
            quiz_type_str = quiz_type.lower() if quiz_type else ""
            difficulty_str = difficulty.lower() if difficulty else ""
            quiz_prompt = f"""
You are an expert assessment designer and educator.
Create a {difficulty_str} level {quiz_type_str} quiz about {quiz_subject} for {grade_level_quiz} students.
Requirements:
- {num_questions} questions total
- Age-appropriate language and content
- Clear, unambiguous questions
- Correct answers provided
- Brief explanations for answers
{f'- Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}
Format:
- Number each question
- For multiple choice: provide 4 options (A, B, C, D)
- For true/false: state the statement clearly
- Include an answer key at the end
- Add brief explanations for learning
Make questions that test understanding, not just memorization. Include a variety of cognitive levels (recall, comprehension, application, analysis).

IMPORTANT: Write the entire quiz, questions, options, and answer key in {language}. If the language is not English, translate all content and section headings to {language}.{visual_aids_instruction_quiz}"
"""
            with st.spinner("🎯 Creating your quiz..."):
                quiz_content = generate_ai_response(quiz_prompt, max_tokens=MAX_TOKENS_QUIZ)
            
            if not quiz_content.startswith("❌") and not quiz_content.startswith("⚠️"):
                st.session_state['quiz_content'] = quiz_content
                st.session_state['quiz_visual_aids'] = parse_visual_aids(quiz_content) if include_visual_aids_quiz else []
            else:
                st.error(quiz_content)
        else:
            st.error("Please enter a subject or topic for the quiz.")

    # Always display the quiz and visual aids if present
    if 'quiz_content' in st.session_state:
        st.success("✅ Quiz Generated!")
        st.markdown(st.session_state['quiz_content'])
        if include_visual_aids_quiz and 'quiz_visual_aids' in st.session_state:
            st.subheader("Visual Aids")
            for idx, va in enumerate(st.session_state['quiz_visual_aids']):
                improved_prompt = f"Create an educational, colorful, labeled diagram: {va}. Make it clear and suitable for students."
                st.markdown(f"**{va}**")
                if st.button(f"Generate Image for Visual Aid {idx+1}", key=f"quiz_visual_{idx}"):
                    with st.spinner("Generating image..."):
                        try:
                            images = generate_gemini_image(improved_prompt, api_key=GEMINI_API_KEY)
                            if images:
                                st.session_state[f"quiz_image_{idx}"] = images[0]
                            else:
                                st.session_state[f"quiz_image_{idx}"] = None
                        except Exception as e:
                            st.error(f"Image generation failed: {e}")
                            st.session_state[f"quiz_image_{idx}"] = None
                if f"quiz_image_{idx}" in st.session_state and st.session_state[f"quiz_image_{idx}"]:
                    st.image(st.session_state[f"quiz_image_{idx}"])
                elif f"quiz_image_{idx}" in st.session_state and st.session_state[f"quiz_image_{idx}"] is None:
                    st.error("No image generated. Try a different prompt or check your API key.")
        st.download_button(label="📥 Download Quiz", data=st.session_state['quiz_content'], file_name=f"{quiz_subject}_quiz_{num_questions}q.txt", mime="text/plain")

# FEATURE 3: FEEDBACK WRITER (Existing)
elif feature == "📝 Feedback Writer":
    st.header("📝 Feedback Writer")
    st.markdown("Generate personalized student feedback and report comments!")
    # Add speech-to-text for all main fields
    student_name = st.text_input("Student Name:", placeholder="Enter student's first name", key="feedback_student_name_text")
    student_name_stt = speech_to_text("Or use your voice for Student Name:", key="feedback_student_name_stt", language="en-IN")
    if student_name_stt and student_name_stt != "":
        student_name = student_name_stt
    subject_area = st.text_input("Subject Area:", placeholder="e.g., Mathematics, Reading, Science", key="feedback_subject_area_text")
    subject_area_stt = speech_to_text("Or use your voice for Subject Area:", key="feedback_subject_area_stt", language="en-IN")
    if subject_area_stt and subject_area_stt != "":
        subject_area = subject_area_stt
    col1, col2 = st.columns(2)
    with col1: performance_level = st.selectbox("Overall Performance:", ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsatisfactory"])
    with col2: feedback_type = st.selectbox("Feedback Type:", ["Report Card Comment", "Progress Report", "Parent Conference Notes", "Improvement Plan"])
    strengths = st.text_area("Strengths Observed:", placeholder="What is the student doing well?", key="feedback_strengths_text")
    strengths_stt = speech_to_text("Or use your voice for Strengths Observed:", key="feedback_strengths_stt", language="en-IN")
    if strengths_stt and strengths_stt != "":
        strengths = strengths_stt
    areas_for_growth = st.text_area("Areas for Growth:", placeholder="What needs improvement?", key="feedback_areas_text")
    areas_for_growth_stt = speech_to_text("Or use your voice for Areas for Growth:", key="feedback_areas_stt", language="en-IN")
    if areas_for_growth_stt and areas_for_growth_stt != "":
        areas_for_growth = areas_for_growth_stt
    specific_examples = st.text_area("Specific Examples:", placeholder="Concrete examples of work or behavior", key="feedback_examples_text")
    specific_examples_stt = speech_to_text("Or use your voice for Specific Examples:", key="feedback_examples_stt", language="en-IN")
    if specific_examples_stt and specific_examples_stt != "":
        specific_examples = specific_examples_stt
    
    if st.button("✍️ Generate Feedback", type="primary"):
        if student_name and subject_area:
            feedback_type_str = feedback_type.lower() if feedback_type else ""
            feedback_prompt = f"""
You are a caring, professional teacher writing {feedback_type_str} for a student.
Student: {student_name}
Subject: {subject_area}
Performance Level: {performance_level}
Strengths: {strengths if strengths else "General positive attributes"}
Areas for Growth: {areas_for_growth if areas_for_growth else "General improvement areas"}
Specific Examples: {specific_examples if specific_examples else "Classroom observations"}
{f'Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}
Write professional, constructive feedback that:
- Uses positive, encouraging language
- Is specific and actionable
- Balances strengths with growth areas
- Provides concrete next steps
- Is appropriate for parents/guardians to read
- Shows genuine care for the student's development
Tone: Professional but warm, constructive, future-focused
Length: 2-3 paragraphs for report cards, longer for progress reports

IMPORTANT: Write the entire feedback in {language}. If the language is not English, translate all content and section headings to {language}."
"""
            with st.spinner("✍️ Writing personalized feedback..."):
                feedback_content = generate_ai_response(feedback_prompt, max_tokens=MAX_TOKENS_FEEDBACK)
            
            if not feedback_content.startswith("❌") and not feedback_content.startswith("⚠️"):
                st.success("✅ Feedback Generated!")
                st.markdown(feedback_content)
                st.download_button(label="📥 Download Feedback", data=feedback_content, file_name=f"{student_name}_{subject_area}_feedback.txt", mime="text/plain")
            else:
                st.error(feedback_content)
        else:
            st.error("Please enter student name and subject area.")

# FEATURE 4: HOMEWORK SUMMARIZER
elif feature == "📖 Homework Summarizer":
    st.header("📖 Homework Summarizer")
    st.markdown("Get concise summaries of lengthy homework assignments.")
    
    homework_text = st.text_area("Paste Homework Text Here:", placeholder="Enter the full text of the homework assignment...", height=300)
    
    if st.button("🎯 Summarize Homework", type="primary"):
        if homework_text:
            homework_prompt = f"""
You are an expert educator tasked with creating clear and concise summaries of homework assignments.
Please summarize the following homework text into 2-3 bullet points or a short paragraph (max 3 lines) that clearly convey the main tasks and objectives.
{f'Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}

Homework Text:
---
{homework_text}
---

Summary:
"""
            with st.spinner("📚 Summarizing homework..."):
                summary = generate_ai_response(homework_prompt, max_tokens=MAX_TOKENS_HOMEWORK_SUMMARY)
            
            if not summary.startswith("❌") and not summary.startswith("⚠️"):
                st.success("✅ Summary Generated!")
                st.markdown(summary)
                st.download_button(label="📥 Download Summary", data=summary, file_name="homework_summary.txt", mime="text/plain")
            else:
                st.error(summary)
        else:
            st.error("Please paste the homework text to summarize.")

# FEATURE 5: CREATIVE WRITING STARTER
elif feature == "✍️ Creative Writing Starter":
    st.header("✍️ Creative Writing Starter")
    st.markdown("Kickstart your imagination with an AI-generated story opening.")
    
    genre_or_theme = st.text_input("Story Genre or Theme:", placeholder="e.g., Sci-Fi adventure, Mystery in a haunted house, Fantasy quest")
    
    if st.button("🚀 Generate Story Starter", type="primary"):
        if genre_or_theme:
            writing_prompt = f"""
You are a creative writing coach and a master storyteller.
Generate an engaging opening paragraph (3-5 sentences) for a story based on the following genre or theme:
{f'Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}

Genre/Theme: {genre_or_theme}

Story Starter:
"""
            with st.spinner("✍️ Crafting your story starter..."):
                starter = generate_ai_response(writing_prompt, max_tokens=MAX_TOKENS_CREATIVE_WRITING)
            
            if not starter.startswith("❌") and not starter.startswith("⚠️"):
                st.success("✅ Story Starter Generated!")
                st.markdown(starter)
                st.download_button(label="📥 Download Starter", data=starter, file_name="creative_writing_starter.txt", mime="text/plain")
            else:
                st.error(starter)
        else:
            st.error("Please enter a genre or theme for the story.")

# FEATURE 6: MORAL STORY GENERATOR
elif feature == "📚 Moral Story Generator":
    st.header("📚 Moral Story Generator")
    st.markdown("Create delightful stories that teach valuable lessons.")
    
    col1, col2 = st.columns(2)
    with col1:
        age_group = st.selectbox("Target Age Group:", ["Young Children (3-6)", "Children (7-10)", "Pre-teens (11-13)", "Teens (14-17)"])
    with col2:
        moral = st.text_input("Moral of the Story:", placeholder="e.g., Honesty is the best policy, The importance of kindness, Never give up")
    
    if st.button("📖 Generate Moral Story", type="primary"):
        if moral:
            story_prompt = f"""
You are a talented storyteller who crafts engaging and educational tales.
Write a 3-5 paragraph story suitable for {age_group} that clearly illustrates the moral: "{moral}".
{f'Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}
Ensure the story has a clear beginning, middle, and end, and that the moral is naturally integrated into the narrative.

Story:
"""
            with st.spinner("📚 Weaving your story..."):
                story = generate_ai_response(story_prompt, max_tokens=MAX_TOKENS_MORAL_STORY)
            
            if not story.startswith("❌") and not story.startswith("⚠️"):
                st.success("✅ Moral Story Generated!")
                st.markdown(story)
                st.download_button(label="📥 Download Story", data=story, file_name="moral_story.txt", mime="text/plain")
            else:
                st.error(story)
        else:
            st.error("Please specify the moral of the story.")

# FEATURE 7: PARENT EMAIL GENERATOR
elif feature == "📧 Parent Email Generator":
    st.header("📧 Parent Email Generator")
    st.markdown("Draft polite and professional emails to parents efficiently.")
    
    student_name_email = st.text_input("Student's Name:", placeholder="Enter student's full name")
    email_context = st.selectbox(
        "Email Context:",
        [
            "Praise for excellent work/behavior",
            "Concern about academic performance",
            "Concern about behavior/classroom conduct",
            "General update on progress",
            "Invitation to a parent-teacher conference",
            "Request for specific information",
            "Follow-up on a previous discussion"
        ]
    )
    additional_details = st.text_area("Add Specific Details (Optional):", placeholder="e.g., Mention a specific assignment, date of conference, specific behavior observed...", height=150)
    
    if st.button("📧 Generate Parent Email", type="primary"):
        if student_name_email and email_context:
            email_prompt = f"""
You are a professional educator composing an email to a parent or guardian.
Student Name: {student_name_email}
Email Context: {email_context}
Additional Details: {additional_details if additional_details else "No specific additional details provided."}
{f'Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}
Compose a polite, professional, and concise email. Tailor the tone based on the context (praise should be warm, concerns should be constructive and empathetic).

Email:
"""
            with st.spinner("📧 Composing email..."):
                email_content = generate_ai_response(email_prompt, max_tokens=MAX_TOKENS_PARENT_EMAIL)
            
            if not email_content.startswith("❌") and not email_content.startswith("⚠️"):
                st.success("✅ Parent Email Drafted!")
                st.markdown(email_content)
                st.download_button(label="📥 Download Email Draft", data=email_content, file_name=f"parent_email_{student_name_email.replace(' ', '_')}.txt", mime="text/plain")
            else:
                st.error(email_content)
        else:
            st.error("Please provide the student's name and select an email context.")

# FEATURE 8: LANGUAGE BUDDY
elif feature == "🌍 Language Buddy":
    st.header("🌍 Language Buddy")
    st.markdown("Translate words or sentences and get usage tips.")
    
    text_to_translate = st.text_area("Enter Word or Sentence:", placeholder="e.g., Hello, How are you? / Bonjour, Comment ça va?")
    target_language = st.text_input("Target Language:", placeholder="e.g., Spanish, French, German, Japanese")
    
    if st.button("🌍 Translate & Explain", type="primary"):
        if text_to_translate and target_language:
            language_prompt = f"""
You are a helpful language assistant.
Translate the following text to {target_language}.
Additionally, provide a brief usage tip or cultural note if relevant.
{f'Cultural/Regional/Community Context: {global_cultural_context}' if global_cultural_context else ''}

Text: "{text_to_translate}"
Target Language: {target_language}

Output Format:
Translation: [Translated text]
Usage Tip: [Relevant tip]
"""
            with st.spinner("🌍 Translating..."):
                language_response = generate_ai_response(language_prompt, max_tokens=MAX_TOKENS_LANGUAGE_BUDDY)
            
            if not language_response.startswith("❌") and not language_response.startswith("⚠️"):
                st.success("✅ Translation & Tip Generated!")
                st.markdown(language_response)
                st.download_button(label="📥 Download Translation", data=language_response, file_name=f"translation_{target_language}.txt", mime="text/plain")
            else:
                st.error(language_response)
        else:
            st.error("Please enter text to translate and the target language.")

# FEATURE 9: TEST SAFETY FEATURE (Existing)
elif feature == "🧪 Test Safety Feature":
    st.header("🧪 Test Safety Feature")
    st.markdown("This feature allows you to test how the AI responds to different safety settings.")

    test_prompt = st.text_area("Enter a test prompt:", "Tell me about the historical context of World War 2, focusing on the causes and major events. Be detailed.")

    st.subheader("Safety Settings Options:")
    safety_option = st.radio(
        "Choose safety settings:",
        ("Default (Block Medium and Above)", "More Permissive (Block Low and Above)", "Most Permissive (Block None)"),
        index=0
    )

    safety_settings_to_apply = None
    if safety_option == "Default (Block Medium and Above)":
        safety_settings_to_apply = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    elif safety_option == "More Permissive (Block Low and Above)":
        safety_settings_to_apply = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
        ]
    elif safety_option == "Most Permissive (Block None)":
        safety_settings_to_apply = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

    if st.button("Run Test"):
        with st.spinner("Testing AI response..."):
            test_result = generate_ai_response(test_prompt, max_tokens=3000, safety_settings_override=safety_settings_to_apply)
        
        st.subheader("Test Result:")
        st.markdown(test_result)


# --- Other Features (Coming Soon) ---
else:
    st.header(f"{feature}")
    st.info("🚧 This feature is coming soon! We're building it with advanced prompt engineering.")
    st.markdown("""
    **Coming Soon:**
    - 📖 Homework Summarizer
    - ✍️ Creative Writing Starter  
    - 📚 Moral Story Generator
    - 📧 Parent Email Generator
    - 🌍 Language Buddy
    
    Each feature will demonstrate different prompt engineering techniques!
    """)

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ for educators | Powered by AI & Prompt Engineering")

# --- Prompt Engineering Learning Section ---
with st.expander("🧠 Learn: Prompt Engineering Tips"):
    st.markdown("""
    ## 🎯 Prompt Engineering Lessons from ClassGenie
    
    **1. Role Definition**: "You are an experienced curriculum specialist..."
    - Gives the AI context and expertise level
    - Creates consistent, professional output
    
    **2. Specific Structure**: Clear sections and formatting requirements
    - Ensures consistent, usable output
    - Makes results actionable for teachers
    
    **3. Context Variables**: Grade level, duration, subject, etc.
    - Personalizes output for specific needs
    - Increases relevance and usability
    
    **4. Output Format**: Detailed formatting instructions
    - Creates scannable, professional documents
    - Ensures practical usability
    
    **5. Tone & Style**: "Professional but warm, constructive..."
    - Matches the audience and use case
    - Builds trust and usability
    
    **6. Handling AI Responses**: Check `finish_reason` and `content.parts` for robustness.
    - Prevents errors when AI is blocked or truncates.
    - Provides user-friendly feedback.
    - Use adequate `max_tokens` to prevent truncation warnings.
    
    **7. Safety Settings**: Be aware of `SAFETY` finish reasons (code 2).
    - If prompts trigger safety filters, consider:
        - Rephrasing the prompt to be less sensitive.
        - Carefully adjusting `safety_settings` if absolutely necessary (use with caution!).
    """)