import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os # Import os to potentially use environment variables for API key

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBuhkDZVZhXKtui6ElYYg5rhFrazshJUrk"
genai.configure(api_key=GEMINI_API_KEY)

# Select Gemini model - using gemini-2.5-flash for free tier availability
MODEL_NAME = "gemini-2.5-flash"

# Define token limits for different features (can be adjusted)
MAX_TOKENS_LESSON_PLAN = 3000  # Increased for more comprehensive lesson plans
MAX_TOKENS_QUIZ = 3000        # Increased for more detailed quizzes
MAX_TOKENS_FEEDBACK = 1500    # Increased for more detailed feedback

# Configure the page
st.set_page_config(
    page_title="ClassGenie - AI Assistant for Schools",
    page_icon="🎓",
    layout="wide"
)

# Title and Description
st.title("🎓 ClassGenie - AI Assistant for Schools")
st.markdown("*Empowering Teachers & Students with Smart AI Tools*")

# Sidebar for feature selection
st.sidebar.title("🛠️ ClassGenie Tools")
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
        "🧪 Test Safety Feature" # Added for easy testing
    ]
)

def generate_ai_response(prompt, max_tokens, safety_settings_override=None):
    """
    Generate AI response using Gemini API.
    Includes robust error handling for safety blocks and other API issues.
    Allows overriding safety settings.
    """
    try:
        # Define default safety settings (can be adjusted if needed)
        default_safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # Use provided override or default safety settings
        current_safety_settings = safety_settings_override if safety_settings_override is not None else default_safety_settings

        model = genai.GenerativeModel(
            MODEL_NAME,
            safety_settings=current_safety_settings # Apply safety settings here
        )
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.7,
            }
        )

        # --- Robust Response Handling ---
        if response and response.candidates:
            candidate = response.candidates[0] # Assuming the first candidate is the most relevant
            if candidate.content and candidate.content.parts:
                # If there are parts, join them to form the text
                text_response = "".join(part.text for part in candidate.content.parts)
                return text_response
            else:
                # If no content or parts, check finish reason
                finish_reason = candidate.finish_reason.name if candidate.finish_reason else "UNKNOWN"
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
        # --- End of Robust Response Handling ---

    except Exception as e:
        # This catches broader exceptions like network errors, invalid API keys, etc.
        return f"❌ **An error occurred:** {str(e)}"

# FEATURE 1: LESSON PLAN GENERATOR
if feature == "📚 Lesson Plan Generator":
    st.header("📚 Lesson Plan Generator")
    st.markdown("Create comprehensive lesson plans in minutes!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox(
            "Subject:",
            ["Science", "Mathematics", "English", "History", "Geography", "Art", "Physical Education", "Music", "Other"]
        )
        if subject == "Other":
            subject = st.text_input("Enter subject:")
            
        topic = st.text_input("Topic/Theme:", placeholder="e.g., Photosynthesis, Fractions, World War II")
    
    with col2:
        grade_level = st.selectbox(
            "Grade Level:",
            ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", 
             "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"]
        )
        
        duration = st.selectbox(
            "Lesson Duration:",
            ["30 minutes", "45 minutes", "60 minutes", "90 minutes", "Custom"]
        )
        if duration == "Custom":
            duration = st.text_input("Enter duration:")
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        learning_style = st.selectbox(
            "Learning Style Focus:",
            ["Mixed (Visual, Auditory, Kinesthetic)", "Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
        )
        
        special_requirements = st.text_area(
            "Special Requirements:",
            placeholder="Any specific requirements, accommodations, or focus areas..."
        )
    
    # Generate button
    if st.button("🚀 Generate Lesson Plan", type="primary"):
        if topic and subject:
            # PROMPT ENGINEERING - This is our core prompt!
            lesson_prompt = f"""
You are an experienced curriculum specialist and master teacher with 15+ years of classroom experience. 

Create a comprehensive, engaging lesson plan with the following specifications:
- Subject: {subject}
- Topic: {topic}
- Grade Level: {grade_level}
- Duration: {duration}
- Learning Style: {learning_style}
{f"- Special Requirements: {special_requirements}" if special_requirements else ""}

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
"""
            
            with st.spinner("🎯 Generating your lesson plan..."):
                # Use the defined token limit for lesson plans
                lesson_plan = generate_ai_response(lesson_prompt, max_tokens=MAX_TOKENS_LESSON_PLAN)
            
            # Display the result or error message
            if not lesson_plan.startswith("❌") and not lesson_plan.startswith("⚠️"):
                st.success("✅ Lesson Plan Generated!")
                st.markdown(lesson_plan)
                
                # Download option
                st.download_button(
                    label="📥 Download Lesson Plan",
                    data=lesson_plan,
                    file_name=f"{subject}_{topic}_{grade_level}_lesson_plan.txt",
                    mime="text/plain"
                )
            else:
                st.error(lesson_plan) # Display the error/warning message from generate_ai_response
        else:
            st.error("Please fill in the subject and topic fields.")

# FEATURE 2: QUIZ MAKER
elif feature == "❓ Quiz Maker":
    st.header("❓ Quiz Maker")
    st.markdown("Generate quizzes and assessments instantly!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        quiz_subject = st.text_input("Subject/Topic:", placeholder="e.g., Ancient Rome, Algebra, Cell Biology")
        quiz_type = st.selectbox(
            "Quiz Type:",
            ["Multiple Choice", "True/False", "Short Answer", "Mixed Format"]
        )
    
    with col2:
        num_questions = st.slider("Number of Questions:", 5, 20, 10)
        difficulty = st.selectbox(
            "Difficulty Level:",
            ["Easy", "Medium", "Hard", "Mixed"]
        )
    
    grade_level_quiz = st.selectbox(
        "Grade Level:",
        ["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/Adult"]
    )
    
    if st.button("🎯 Generate Quiz", type="primary"):
        if quiz_subject:
            quiz_prompt = f"""
You are an expert assessment designer and educator.

Create a {difficulty.lower()} level {quiz_type.lower()} quiz about {quiz_subject} for {grade_level_quiz} students.

Requirements:
- {num_questions} questions total
- Age-appropriate language and content
- Clear, unambiguous questions
- Correct answers provided
- Brief explanations for answers

Format:
- Number each question
- For multiple choice: provide 4 options (A, B, C, D)
- For true/false: state the statement clearly
- Include an answer key at the end
- Add brief explanations for learning

Make questions that test understanding, not just memorization. Include a variety of cognitive levels (recall, comprehension, application, analysis).
"""
            
            with st.spinner("🎯 Creating your quiz..."):
                # Use the defined token limit for quizzes
                quiz_content = generate_ai_response(quiz_prompt, max_tokens=MAX_TOKENS_QUIZ)
            
            if not quiz_content.startswith("❌") and not quiz_content.startswith("⚠️"):
                st.success("✅ Quiz Generated!")
                st.markdown(quiz_content)
                
                st.download_button(
                    label="📥 Download Quiz",
                    data=quiz_content,
                    file_name=f"{quiz_subject}_quiz_{num_questions}q.txt",
                    mime="text/plain"
                )
            else:
                st.error(quiz_content)
        else:
            st.error("Please enter a subject or topic for the quiz.")

# FEATURE 3: FEEDBACK WRITER
elif feature == "📝 Feedback Writer":
    st.header("📝 Feedback Writer")
    st.markdown("Generate personalized student feedback and report comments!")
    
    student_name = st.text_input("Student Name:", placeholder="Enter student's first name")
    subject_area = st.text_input("Subject Area:", placeholder="e.g., Mathematics, Reading, Science")
    
    col1, col2 = st.columns(2)
    with col1:
        performance_level = st.selectbox(
            "Overall Performance:",
            ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsatisfactory"]
        )
    
    with col2:
        feedback_type = st.selectbox(
            "Feedback Type:",
            ["Report Card Comment", "Progress Report", "Parent Conference Notes", "Improvement Plan"]
        )
    
    strengths = st.text_area("Strengths Observed:", placeholder="What is the student doing well?")
    areas_for_growth = st.text_area("Areas for Growth:", placeholder="What needs improvement?")
    specific_examples = st.text_area("Specific Examples:", placeholder="Concrete examples of work or behavior")
    
    if st.button("✍️ Generate Feedback", type="primary"):
        if student_name and subject_area:
            feedback_prompt = f"""
You are a caring, professional teacher writing {feedback_type.lower()} for a student.

Student: {student_name}
Subject: {subject_area}
Performance Level: {performance_level}

Strengths: {strengths if strengths else "General positive attributes"}
Areas for Growth: {areas_for_growth if areas_for_growth else "General improvement areas"}
Specific Examples: {specific_examples if specific_examples else "Classroom observations"}

Write professional, constructive feedback that:
- Uses positive, encouraging language
- Is specific and actionable
- Balances strengths with growth areas
- Provides concrete next steps
- Is appropriate for parents/guardians to read
- Shows genuine care for the student's development

Tone: Professional but warm, constructive, future-focused
Length: 2-3 paragraphs for report cards, longer for progress reports
"""
            
            with st.spinner("✍️ Writing personalized feedback..."):
                # Use the defined token limit for feedback
                feedback_content = generate_ai_response(feedback_prompt, max_tokens=MAX_TOKENS_FEEDBACK)
            
            if not feedback_content.startswith("❌") and not feedback_content.startswith("⚠️"):
                st.success("✅ Feedback Generated!")
                st.markdown(feedback_content)
                
                st.download_button(
                    label="📥 Download Feedback",
                    data=feedback_content,
                    file_name=f"{student_name}_{subject_area}_feedback.txt",
                    mime="text/plain"
                )
            else:
                st.error(feedback_content)
        else:
            st.error("Please enter student name and subject area.")

# FEATURE 4: TEST SAFETY FEATURE
elif feature == "🧪 Test Safety Feature":
    st.header("🧪 Test Safety Feature")
    st.markdown("This feature allows you to test how the AI responds to different safety settings.")

    test_prompt = st.text_area("Enter a test prompt:", "Tell me about the historical context of World War 2, focusing on the causes and major events. Be detailed.")

    st.subheader("Safety Settings Options:")
    safety_option = st.radio(
        "Choose safety settings:",
        ("Default (Block Medium and Above)", "More Permissive (Block Low and Above)", "Most Permissive (Block None)"),
        index=0 # Default to "Block Medium and Above"
    )

    # Map user selection to actual safety settings
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
        # This is generally NOT recommended for production environments
        safety_settings_to_apply = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

    if st.button("Run Test"):
        with st.spinner("Testing AI response..."):
            # For testing, we can use a reasonable token count, e.g., 1000
            test_result = generate_ai_response(test_prompt, max_tokens=1000, safety_settings_override=safety_settings_to_apply)
        
        st.subheader("Test Result:")
        st.markdown(test_result)


# Placeholder for other features (these will show the "coming soon" message)
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

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for educators | Powered by AI & Prompt Engineering")

# Prompt Engineering Learning Section
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