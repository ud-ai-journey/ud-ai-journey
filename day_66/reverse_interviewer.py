import re

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Function to parse resume content
def parse_resume(content):
    # Extract sections using regex patterns
    sections = {
        'skills': re.findall(r'(?:Core:|Skills?:).*?(?:\n\n|\Z)', content, re.DOTALL | re.IGNORECASE),
        'experience': re.findall(r'(?:WORK EXPERIENCE|Experience:).*?(?:EDUCATION|PROJECTS|\Z)', content, re.DOTALL | re.IGNORECASE),
        'projects': re.findall(r'(?:PROJECTS:?).*?(?:ADDITIONAL|\Z)', content, re.DOTALL | re.IGNORECASE)
    }
    
    # Process skills
    skills = []
    if sections['skills']:
        skills_text = sections['skills'][0]
        skills = re.findall(r'\b\w+(?:[-]\w+)*\b', skills_text)
        skills = [s for s in skills if len(s) > 2 and s.lower() not in {'and', 'the', 'core', 'skills'}]
    
    # Process experience
    experience = []
    if sections['experience']:
        exp_lines = sections['experience'][0].split('\n')
        experience = [line.strip() for line in exp_lines if line.strip() and not line.strip().startswith(('WORK', 'Experience:'))]
    
    # Process projects
    projects = []
    if sections['projects']:
        proj_lines = sections['projects'][0].split('\n')
        projects = [line.strip() for line in proj_lines if line.strip() and not line.strip().startswith('PROJECTS')]
    
    return {
        'skills': skills if skills else ['AI', 'Python', 'Communication', 'Innovation'],
        'experience': experience if experience else ['AI Research at ADP', 'Full-time Contributor at Cognizant'],
        'projects': projects if projects else ['Client Onboarding & Unemployment Claims Automation', 'Smart Blind Stick']
    }

# Function to generate interview questions
def generate_questions(parsed_data):
    questions = []
    for skill in parsed_data['skills']:
        questions.append(f"Can you walk me through a time you worked with {skill}?")
    for exp in parsed_data['experience']:
        questions.append(f"Tell me about a challenge you faced in {exp.strip() or 'your experience'}.")
    for proj in parsed_data['projects']:
        questions.append(f"What was your biggest challenge during {proj.strip() or 'your project'}?")
    questions.append("How do you handle tight deadlines?")  # Behavioral question
    return questions

# Basic feedback engine (keyword match)
def provide_feedback(question, answer):
    keywords = {
        'AI': ['artificial intelligence', 'machine learning', 'research', 'innovation'],
        'Python': ['programming', 'development', 'coding', 'automation'],
        'Communication': ['presentation', 'interaction', 'leadership', 'team'],
        'Innovation': ['creativity', 'solution', 'ideation', 'design']
    }
    
    # STAR method keywords
    star_keywords = {
        'situation': ['when', 'while', 'during', 'at the time', 'situation', 'background'],
        'task': ['task', 'goal', 'objective', 'responsibility'],
        'action': ['action', 'did', 'handled', 'approach', 'steps', 'implemented', 'led'],
        'result': ['result', 'outcome', 'impact', 'achieved', 'success', 'improved', 'learned']
    }
    
    answer_lower = answer.lower()
    if len(answer.strip()) < 10:
        return "Please provide a more detailed answer with specific examples."
    
    # Check for STAR elements
    star_present = {k: any(word in answer_lower for word in v) for k, v in star_keywords.items()}
    missing = [k for k, present in star_present.items() if not present]
    if len(missing) >= 3:
        return "Try to use the STAR method: describe the Situation, Task, Action, and Result."
    elif missing:
        return f"Good start! Try to include the following in your answer: {', '.join(missing).capitalize()}."
    
    # Check for job title/date only answers
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

def get_resume_content():
    while True:
        print("Paste your resume, or type 'file' to upload a .txt or .pdf file (or 'upload'):")
        choice = input("> ").strip()
        if choice.lower() in ('file', 'upload'):
            file_path = input("Enter the path to your .txt or .pdf resume file: ").strip().strip('"')
            if file_path.lower().endswith('.pdf'):
                if PyPDF2 is None:
                    print("PDF support requires PyPDF2. Please install it with: pip install PyPDF2")
                    continue
                try:
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ''
                        for page in reader.pages:
                            text += page.extract_text() or ''
                        if not text.strip():
                            print("No text could be extracted from the PDF. Please try another file or convert to .txt.")
                            continue
                        return text
                except Exception as e:
                    print(f"Error reading PDF file: {e}\nPlease try again or paste your resume content.")
                    continue
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"Error reading file: {e}\nPlease try again or paste your resume content.")
                    continue
        elif choice:
            # If user pasted content, return it
            return choice
        else:
            # If nothing entered, confirm using default
            confirm = input("No input detected. Use default resume? (y/n): ").strip().lower()
            if confirm == 'y':
                return ""
            # Otherwise, reprompt

def get_answer():
    if sr is not None:
        print("Type your answer or type 'voice' to answer by speaking:")
        ans = input("Your answer: ").strip()
        if ans.lower() == 'voice':
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak now...")
                audio = recognizer.listen(source)
            try:
                transcript = recognizer.recognize_google(audio)
                print(f"(Transcribed): {transcript}")
                return transcript
            except Exception as e:
                print(f"Could not understand audio: {e}")
                return ""
        return ans
    else:
        return input("Your answer: ").strip()

# Main function
def reverse_interviewer():
    print("Welcome to Reverse GPT-Interviewer! Paste your resume content below (or press Enter for default):")
    content = get_resume_content() or """
    Skills: Python, Problem-solving
    Experience: Worked on various coding projects
    Projects: Personal coding project
    """
    
    # Parse resume
    parsed_data = parse_resume(content)
    print("\nParsed Data:", parsed_data)
    
    # Generate and ask questions
    questions = generate_questions(parsed_data)
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}/{len(questions)}: {question}")
        answer = get_answer()
        feedback = provide_feedback(question, answer)
        print(f"Feedback: {feedback}")

    print("\nInterview complete! Great job preparing!")

if __name__ == "__main__":
    reverse_interviewer()