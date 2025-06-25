import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os

# --- API Configuration ---
# Best practice: Use Streamlit secrets for your API key.
# Create a .streamlit/secrets.toml file with:
# GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
# Then use: genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# For this example, we'll use the provided key, but remember to secure it.
GEMINI_API_KEY = "AIzaSyBuhkDZVZhXKtui6ElYYg5rhFrazshJUrk"
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"API Key configuration failed: {e}")
    st.stop() # Stop the app if API key is invalid or not configured

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
    page_title="ClassGenie - AI Assistant for Schools",
    page_icon="🎓",
    layout="wide"
)

# --- Title and Description ---
st.title("🎓 ClassGenie - AI Assistant for Schools")
st.markdown("*Empowering Teachers & Students with Smart AI Tools*")

# --- Sidebar for Feature Selection ---
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
        "🧪 Test Safety Feature"
    ]
)

# --- AI Response Generation Function ---
def generate_ai_response(prompt, max_tokens, safety_settings_override=None):
    """
    Generates AI response using Gemini API with robust error handling.
    """
    try:
        current_safety_settings = safety_settings_override if safety_settings_override is not None else DEFAULT_SAFETY_SETTINGS

        model = genai.GenerativeModel(
            MODEL_NAME,
            safety_settings=current_safety_settings
        )
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.7,
            }
        )

        if response and response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                text_response = "".join(part.text for part in candidate.content.parts)
                return text_response
            else:
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

    except Exception as e:
        return f"❌ **An error occurred:** {str(e)}"

# --- Feature Implementations ---

# FEATURE 1: LESSON PLAN GENERATOR (Existing)
if feature == "📚 Lesson Plan Generator":
    st.header("📚 Lesson Plan Generator")
    st.markdown("Create comprehensive lesson plans in minutes!")
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject:", ["Science", "Mathematics", "English", "History", "Geography", "Art", "Physical Education", "Music", "Other"])
        if subject == "Other": subject = st.text_input("Enter subject:")
        topic = st.text_input("Topic/Theme:", placeholder="e.g., Photosynthesis, Fractions, World War II")
    with col2:
        grade_level = st.selectbox("Grade Level:", ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"])
        duration = st.selectbox("Lesson Duration:", ["30 minutes", "45 minutes", "60 minutes", "90 minutes", "Custom"])
        if duration == "Custom": duration = st.text_input("Enter duration:")
    with st.expander("🔧 Advanced Options"):
        learning_style = st.selectbox("Learning Style Focus:", ["Mixed (Visual, Auditory, Kinesthetic)", "Visual", "Auditory", "Kinesthetic", "Reading/Writing"])
        special_requirements = st.text_area("Special Requirements:", placeholder="Any specific requirements, accommodations, or focus areas...")
    
    if st.button("🚀 Generate Lesson Plan", type="primary"):
        if topic and subject:
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
                lesson_plan = generate_ai_response(lesson_prompt, max_tokens=MAX_TOKENS_LESSON_PLAN)
            
            if not lesson_plan.startswith("❌") and not lesson_plan.startswith("⚠️"):
                st.success("✅ Lesson Plan Generated!")
                st.markdown(lesson_plan)
                st.download_button(label="📥 Download Lesson Plan", data=lesson_plan, file_name=f"{subject}_{topic}_{grade_level}_lesson_plan.txt", mime="text/plain")
            else:
                st.error(lesson_plan)
        else:
            st.error("Please fill in the subject and topic fields.")

# FEATURE 2: QUIZ MAKER (Existing)
elif feature == "❓ Quiz Maker":
    st.header("❓ Quiz Maker")
    st.markdown("Generate quizzes and assessments instantly!")
    
    col1, col2 = st.columns(2)
    with col1:
        quiz_subject = st.text_input("Subject/Topic:", placeholder="e.g., Ancient Rome, Algebra, Cell Biology")
        quiz_type = st.selectbox("Quiz Type:", ["Multiple Choice", "True/False", "Short Answer", "Mixed Format"])
    with col2:
        num_questions = st.slider("Number of Questions:", 5, 20, 10)
        difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard", "Mixed"])
    grade_level_quiz = st.selectbox("Grade Level:", ["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/Adult"])
    
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
                quiz_content = generate_ai_response(quiz_prompt, max_tokens=MAX_TOKENS_QUIZ)
            
            if not quiz_content.startswith("❌") and not quiz_content.startswith("⚠️"):
                st.success("✅ Quiz Generated!")
                st.markdown(quiz_content)
                st.download_button(label="📥 Download Quiz", data=quiz_content, file_name=f"{quiz_subject}_quiz_{num_questions}q.txt", mime="text/plain")
            else:
                st.error(quiz_content)
        else:
            st.error("Please enter a subject or topic for the quiz.")

# FEATURE 3: FEEDBACK WRITER (Existing)
elif feature == "📝 Feedback Writer":
    st.header("📝 Feedback Writer")
    st.markdown("Generate personalized student feedback and report comments!")
    
    student_name = st.text_input("Student Name:", placeholder="Enter student's first name")
    subject_area = st.text_input("Subject Area:", placeholder="e.g., Mathematics, Reading, Science")
    col1, col2 = st.columns(2)
    with col1: performance_level = st.selectbox("Overall Performance:", ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsatisfactory"])
    with col2: feedback_type = st.selectbox("Feedback Type:", ["Report Card Comment", "Progress Report", "Parent Conference Notes", "Improvement Plan"])
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