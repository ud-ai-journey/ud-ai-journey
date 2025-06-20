import streamlit as st
import re

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# --- Resume Parsing Logic (from your script) ---
def parse_resume(content):
    import string
    import re
    # Helper filters
    def is_valid_skill(skill):
        skill = skill.strip()
        if not skill or len(skill) < 2 or len(skill) > 40:
            return False
        if any(char.isdigit() for char in skill):
            return False
        if re.search(r'\+?\d{6,}', skill):  # phone numbers
            return False
        if skill.lower() in {'and', 'the', 'core', 'skills', 'project', 'projects', 'experience', 'summary', 'address', 'phone', 'email', 'website', 'languages', 'certifications', 'club', 'leadership', 'major', 'ssc', 'cbse', 'bachelor', 'gold', 'medalist', 'school', 'college', 'technology', 'jntua', 'india', 'intern', 'present', 'year', 'date', 'month', 'role', 'team', 'user', 'use', 'with', 'on', 'in', 'at', 'for', 'to', 'by', 'of', 'from', 'as', 'is', 'it', 'that', 'this', 'a', 'an', 'or', 'but', 'if', 'so', 'do', 'did', 'done', 'be', 'are', 'was', 'were', 'has', 'have', 'had', 'will', 'can', 'may', 'might', 'should', 'would', 'could', 'must', 'shall', 'not', 'no', 'yes', 'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'them', 'who', 'whom', 'which', 'what', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'than', 'too', 'very', 's', 't', 'just', 'don', 'now', 'then', 'there', 'here', 'out', 'up', 'down', 'off', 'over', 'under', 'again', 'further', 'once', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'in', 'on', 'at', 'by', 'with', 'about', 'against', 'among', 'around', 'as', 'because', 'beside', 'besides', 'beyond', 'but', 'concerning', 'considering', 'despite', 'except', 'following', 'inside', 'like', 'minus', 'near', 'onto', 'opposite', 'outside', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'throughout', 'toward', 'towards', 'underneath', 'unlike', 'until', 'upon', 'versus', 'via', 'within', 'without'}:
            return False
        if skill.isdigit() or len(skill) == 1:
            return False
        if '@' in skill or 'www.' in skill or 'http' in skill or skill.replace('.', '').isdigit():
            return False
        if any(c in skill for c in string.punctuation.replace('-', '')):
            return False
        # Only allow likely skill words/phrases (no full sentences)
        if len(skill.split()) > 5:
            return False
        return True
    def is_valid_project(line):
        line = line.strip()
        if not line or len(line) < 4 or len(line) > 80:
            return False
        if any(char.isdigit() for char in line):
            return False
        if re.search(r'\+?\d{6,}', line):
            return False
        if any(x in line.lower() for x in ['email', 'phone', 'address', 'website', 'gmail', 'linkedin', 'http', 'www.', '@', 'resume', 'summary', 'languages:', 'certifications:', 'club', 'leadership', 'major', 'ssc', 'cbse', 'bachelor', 'gold', 'medalist', 'school', 'college', 'technology', 'jntua', 'india', 'intern', 'present', 'date', 'month', 'role', 'team', 'user', 'use', 'with', 'on', 'in', 'at', 'for', 'to', 'by', 'of', 'from', 'as', 'is', 'it', 'that', 'this', 'a', 'an', 'or', 'but', 'if', 'so', 'do', 'did', 'done', 'be', 'are', 'was', 'were', 'has', 'have', 'had', 'will', 'can', 'may', 'might', 'should', 'would', 'could', 'must', 'shall', 'not', 'no', 'yes', 'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'them', 'who', 'whom', 'which', 'what', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'than', 'too', 'very', 's', 't', 'just', 'don', 'now', 'then', 'there', 'here', 'out', 'up', 'down', 'off', 'over', 'under', 'again', 'further', 'once', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'in', 'on', 'at', 'by', 'with', 'about', 'against', 'among', 'around', 'as', 'because', 'beside', 'besides', 'beyond', 'but', 'concerning', 'considering', 'despite', 'except', 'following', 'inside', 'like', 'minus', 'near', 'onto', 'opposite', 'outside', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'throughout', 'toward', 'towards', 'underneath', 'unlike', 'until', 'upon', 'versus', 'via', 'within', 'without']):
            return False
        if line.isdigit() or len(line) == 1:
            return False
        if line.isupper():
            return False
        # Only allow likely project titles (not full sentences)
        if len(line.split()) > 10:
            return False
        return True
    def is_valid_experience(line):
        line = line.strip()
        if not line or len(line) < 4 or len(line) > 60:
            return False
        if any(char.isdigit() for char in line):
            return False
        if re.search(r'\+?\d{6,}', line):
            return False
        if any(x in line.lower() for x in ['email', 'phone', 'address', 'website', 'gmail', 'linkedin', 'http', 'www.', '@', 'resume', 'summary', 'languages:', 'certifications:', 'club', 'leadership', 'major', 'ssc', 'cbse', 'bachelor', 'gold', 'medalist', 'school', 'college', 'technology', 'jntua', 'india', 'intern', 'present', 'date', 'month', 'role', 'team', 'user', 'use', 'with', 'on', 'in', 'at', 'for', 'to', 'by', 'of', 'from', 'as', 'is', 'it', 'that', 'this', 'a', 'an', 'or', 'but', 'if', 'so', 'do', 'did', 'done', 'be', 'are', 'was', 'were', 'has', 'have', 'had', 'will', 'can', 'may', 'might', 'should', 'would', 'could', 'must', 'shall', 'not', 'no', 'yes', 'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'them', 'who', 'whom', 'which', 'what', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'than', 'too', 'very', 's', 't', 'just', 'don', 'now', 'then', 'there', 'here', 'out', 'up', 'down', 'off', 'over', 'under', 'again', 'further', 'once', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'in', 'on', 'at', 'by', 'with', 'about', 'against', 'among', 'around', 'as', 'because', 'beside', 'besides', 'beyond', 'but', 'concerning', 'considering', 'despite', 'except', 'following', 'inside', 'like', 'minus', 'near', 'onto', 'opposite', 'outside', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'throughout', 'toward', 'towards', 'underneath', 'unlike', 'until', 'upon', 'versus', 'via', 'within', 'without']):
            return False
        if line.isdigit() or len(line) == 1:
            return False
        if line.isupper():
            return False
        # Only allow likely job titles or company names (not full sentences)
        if len(line.split()) > 8:
            return False
        return True
    sections = {
        'skills': re.findall(r'(?:Core:|Skills?:).*?(?:\n\n|\Z)', content, re.DOTALL | re.IGNORECASE),
        'experience': re.findall(r'(?:WORK EXPERIENCE|Experience:).*?(?:EDUCATION|PROJECTS|\Z)', content, re.DOTALL | re.IGNORECASE),
        'projects': re.findall(r'(?:PROJECTS:?).*?(?:ADDITIONAL|\Z)', content, re.DOTALL | re.IGNORECASE)
    }
    # Skills: split on comma/semicolon, filter
    skills = []
    if sections['skills']:
        skills_text = sections['skills'][0]
        for part in re.split(r'[;,\n]', skills_text):
            part = part.strip()
            if is_valid_skill(part):
                skills.append(part)
    skills = list(dict.fromkeys(skills))  # Remove duplicates, preserve order
    # Experience: keep only lines that look like real experience
    experience = []
    if sections['experience']:
        exp_lines = sections['experience'][0].split('\n')
        for line in exp_lines:
            line = line.strip()
            if is_valid_experience(line):
                experience.append(line)
    experience = list(dict.fromkeys(experience))
    # Projects: keep only lines that look like real projects
    projects = []
    if sections['projects']:
        proj_lines = sections['projects'][0].split('\n')
        for line in proj_lines:
            line = line.strip()
            if is_valid_project(line):
                projects.append(line)
    projects = list(dict.fromkeys(projects))
    return {
        'skills': skills if skills else ['AI', 'Python', 'Communication', 'Innovation'],
        'experience': experience if experience else ['AI Research at ADP', 'Full-time Contributor at Cognizant'],
        'projects': projects if projects else ['Client Onboarding & Unemployment Claims Automation', 'Smart Blind Stick']
    }

def generate_questions(parsed_data):
    questions = []
    for skill in parsed_data['skills']:
        questions.append(f"Can you walk me through a time you worked with {skill}?")
    for exp in parsed_data['experience']:
        questions.append(f"Tell me about a challenge you faced in {exp.strip() or 'your experience'}.")
    for proj in parsed_data['projects']:
        questions.append(f"What was your biggest challenge during {proj.strip() or 'your project'}?")
    questions.append("How do you handle tight deadlines?")
    return questions

def provide_feedback(question, answer):
    keywords = {
        'AI': ['artificial intelligence', 'machine learning', 'research', 'innovation'],
        'Python': ['programming', 'development', 'coding', 'automation'],
        'Communication': ['presentation', 'interaction', 'leadership', 'team'],
        'Innovation': ['creativity', 'solution', 'ideation', 'design']
    }
    star_keywords = {
        'situation': ['when', 'while', 'during', 'at the time', 'situation', 'background'],
        'task': ['task', 'goal', 'objective', 'responsibility'],
        'action': ['action', 'did', 'handled', 'approach', 'steps', 'implemented', 'led'],
        'result': ['result', 'outcome', 'impact', 'achieved', 'success', 'improved', 'learned']
    }
    answer_lower = answer.lower()
    if len(answer.strip()) < 10:
        return "Please provide a more detailed answer with specific examples."
    star_present = {k: any(word in answer_lower for word in v) for k, v in star_keywords.items()}
    missing = [k for k, present in star_present.items() if not present]
    if len(missing) >= 3:
        return "Try to use the STAR method: describe the Situation, Task, Action, and Result."
    elif missing:
        return f"Good start! Try to include the following in your answer: {', '.join(missing).capitalize()}."
    if re.match(r'^[\w\s,&|\-]+\d{4}', answer) or re.match(r'^[A-Za-z\s,&|\-]+$', answer):
        return "Please provide a story or example, not just a job title or date."
    q_keywords = next((k for k in keywords if k.lower() in question.lower()), None)
    if q_keywords and any(k in answer_lower for k in keywords[q_keywords]):
        return "Good answer! You effectively highlighted relevant experience."
    suggestions = {
        'AI': "Consider mentioning specific AI projects or research experiences.",
        'Python': "Try to include specific coding projects or technical achievements.",
        'Communication': "Highlight your team collaboration and leadership experiences.",
        'Innovation': "Share examples of creative problem-solving or new ideas you've implemented."
    }
    if q_keywords:
        return suggestions.get(q_keywords, "Consider providing more specific examples related to the question.")
    return "Try to structure your answer with a specific situation, the actions you took, and the results achieved."

# --- Streamlit UI ---
st.set_page_config(page_title="🧠 Reverse GPT-Interviewer", layout="centered")
st.title("🧠 Reverse GPT-Interviewer – Your AI Interview Trainer!")
st.write("""
Upload your resume (.txt or .pdf) or paste your content below. Get personalized interview questions and instant feedback!
""")

resume_text = ""
resume_file = st.file_uploader("Upload your resume (.txt or .pdf)", type=["txt", "pdf"])
resume_paste = st.text_area("Or paste your resume here:", height=200)

# Example resume button
example_resume = """
Skills: Python, AI, Leadership, Communication, Deep Learning
Experience: AI Intern at ADP, Contributor at OpenAI Community
Projects: AI Resume Parser, Smart Blind Stick, Chatbot with Emotion Recognition
"""
if not resume_file and not resume_paste.strip():
    if st.button("Try with Example Resume"):
        resume_paste = example_resume
        st.session_state["resume_example"] = True
    elif st.session_state.get("resume_example"):
        resume_paste = example_resume

if resume_file is not None:
    if resume_file.name.lower().endswith('.pdf'):
        if PyPDF2 is None:
            st.error("PDF support requires PyPDF2. Please install it with: pip install PyPDF2")
        else:
            try:
                reader = PyPDF2.PdfReader(resume_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
                resume_text = text
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
    else:
        resume_text = resume_file.read().decode('utf-8', errors='ignore')
elif resume_paste.strip():
    resume_text = resume_paste
else:
    st.info("Please upload or paste your resume to begin.")

if resume_text.strip():
    parsed_data = parse_resume(resume_text)
    st.subheader("Parsed Resume Data")
    st.json(parsed_data)
    questions = generate_questions(parsed_data)
    st.subheader("Interview Questions")
    if 'answers' not in st.session_state or len(st.session_state.answers) != len(questions):
        st.session_state.answers = [''] * len(questions)
    num_answered = sum(1 for a in st.session_state.answers if a.strip())
    st.progress(num_answered / len(questions))
    for i, question in enumerate(questions):
        st.markdown(f"**Q{i+1}: {question}**")
        answer = st.text_area(f"Your answer to Q{i+1}", value=st.session_state.answers[i], key=f"answer_{i}")
        st.session_state.answers[i] = answer
        if answer.strip():
            feedback = provide_feedback(question, answer)
            # Color-coded feedback
            if "Good answer" in feedback:
                st.success(f"Feedback: {feedback}")
            elif "Good start" in feedback:
                st.warning(f"Feedback: {feedback}")
            elif "Please provide" in feedback or "Try to use" in feedback:
                st.error(f"Feedback: {feedback}")
            else:
                st.info(f"Feedback: {feedback}")
    if num_answered == len(questions):
        st.success("Interview complete! Great job preparing!")
        # Export Q&A+feedback as .txt
        export_lines = []
        for i, question in enumerate(questions):
            export_lines.append(f"Q{i+1}: {question}")
            export_lines.append(f"A{i+1}: {st.session_state.answers[i]}")
            export_lines.append(f"Feedback: {provide_feedback(question, st.session_state.answers[i])}\n")
        export_txt = "\n".join(export_lines)
        st.download_button("Download Q&A + Feedback as .txt", export_txt, file_name="interview_feedback.txt")
