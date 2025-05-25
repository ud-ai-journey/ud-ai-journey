# Day 40: Resume Keyword Scanner

## 📖 Overview

This project is part of my **100 Days of Python + AI** journey, where I, Boya Uday Kumar, aim to build practical AI-driven tools to enhance my skills and portfolio. On Day 40, I developed a **Resume Keyword Scanner** to help optimize my resume for specific job descriptions, a critical tool for my job hunt as an aspiring **AI Applications Researcher/Vibe Coder**.

The Resume Keyword Scanner analyzes a job description and a resume, extracts key tech-related keywords, and calculates a match percentage. It then provides recommendations to improve the resume by identifying missing keywords. This project leverages Natural Language Processing (NLP) techniques using Python's `nltk` library and demonstrates my ability to build practical, job-focused AI tools.

## 🎯 Goals

- Build a tool to compare my resume against a job description and calculate a keyword match percentage.
- Identify missing keywords in my resume to improve alignment with job requirements.
- Apply NLP techniques (tokenization, stopword removal, lemmatization) to extract relevant tech keywords.
- Achieve a 100% match score by tailoring my resume to a specific job description for an **AI Applications Researcher/Vibe Coder** role.

## 🛠️ Features

- **Keyword Extraction**: Extracts tech-related keywords from a job description using NLP techniques (`nltk` for tokenization, stopword removal, and lemmatization).
- **Keyword Matching**: Compares extracted keywords against the resume and calculates a match percentage.
- **Recommendations**: Suggests missing keywords to add to the resume for better alignment with the job description.
- **Color-Coded Output**: Uses `termcolor` to display matched (green) and missing (red) keywords for easy visualization.
- **Multi-Word Phrase Support**: Handles multi-word tech terms like `natural language processing` and `vibe coding`.

## 📂 Project Structure

```
day_40_resume_keyword_matcher/
├── matcher.py              # Main script for the Resume Keyword Scanner
├── resume.txt              # My updated resume text
├── job_description.txt     # Job description for AI Applications Researcher/Vibe Coder
└── README.md               # Project documentation (this file)
```

- **`matcher.py`**: The core script that processes the resume and job description, extracts keywords, and calculates the match percentage.
- **`resume.txt`**: My resume, updated to include keywords like `natural language processing`, `machine learning`, `software development`, `vibe coding`, `cursor`, and `replit`.
- **`job_description.txt`**: A job description for an AI Applications Researcher/Vibe Coder role, used to test the scanner.

## ⚙️ How It Works

1. **Input Files**:
   - `resume.txt`: Contains my resume text.
   - `job_description.txt`: Contains the job description text.

2. **Keyword Extraction**:
   - The script preprocesses both files by lowercasing, removing punctuation/numbers, tokenizing, removing stopwords, and lemmatizing using `nltk`.
   - It extracts tech-related keywords from the job description, filtered against a predefined `TECH_KEYWORDS` list (e.g., `python`, `machine learning`, `vibe coding`).
   - Multi-word phrases like `natural language processing` are preserved by directly searching for them in the text.

3. **Matching**:
   - Compares the extracted keywords against the resume to identify matches.
   - Calculates a match percentage: `(matched_keywords / total_keywords) * 100`.

4. **Output**:
   - Displays the extracted keywords, matched/missing keywords (with color coding), match percentage, and recommendations for missing keywords.

## 🏆 Achievements

- **Initial Match**: Started with a match score of 42.86% when testing my resume against the AI Applications Researcher/Vibe Coder job description.
- **Improvements**:
  - Updated the script to handle multi-word phrases like `natural language processing` and `vibe coding`.
  - Added absolute paths to ensure the script can find files regardless of the running directory.
  - Updated my resume to include missing keywords like `natural language processing`, `vibe coding`, `cursor`, `machine learning`, `software development`, and `replit`.
- **Final Match**: Achieved a **100% match score** (7/7 keywords) after adding a Replit project to my resume:
  ```
  Chatbot Prototype: Developed a simple chatbot using Python on Replit, demonstrating cloud-based development skills.
  ```

## 🚀 How to Run

### Prerequisites
- Python 3.12
- Install required libraries:
  ```bash
  pip install nltk termcolor
  ```
- Download NLTK data (run in Python):
  ```python
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  ```

### Steps
1. **Navigate to the directory**:
   ```powershell
   cd "C:\Users\uday kumar\Python-AI\ud-ai-journey\day_40_resume_keyword_matcher"
   ```

2. **Prepare input files**:
   - Ensure `resume.txt` contains your resume.
   - Ensure `job_description.txt` contains the target job description.

3. **Run the script**:
   ```powershell
   $env:TF_ENABLE_ONEDNN_OPTS=0; & "C:/Users/uday kumar/AppData/Local/Programs/Python/Python312/python.exe" "C:/Users/uday kumar/Python-AI/ud-ai-journey/day_40/matcher.py"
   ```

4. **View the output**:
   - The script will display the extracted keywords, matched/missing keywords, match percentage, and recommendations.

## 📈 Results

After several iterations and improvements, I tested the scanner with my updated resume and a job description for an **AI Applications Researcher/Vibe Coder** role. The final output was:

```
📋 Job Description Keywords:
replit, machine learning, python, software development, natural language processing, vibe coding, cursor

🔍 Match Results:
Matched Keywords (7/7):
  🟩 replit
  🟩 machine learning
  🟩 python
  🟩 software development
  🟩 natural language processing
  🟩 vibe coding
  🟩 cursor

📊 Match Percentage: 100.00%

🎉 All keywords matched! Your resume aligns well with the job description.
```

This tool has proven invaluable for tailoring my resume to specific job roles, ensuring I stand out as a candidate.

## 🔮 Future Improvements

- **Extract `ai` Keyword**: The script occasionally misses `ai` as a keyword due to tokenization. I can tweak the `extract_keywords` function to ensure it’s always captured.
- **Add a GUI**: Integrate a Tkinter GUI for easier interaction, similar to my **Voiceify Live Plus** project.
- **Expand `TECH_KEYWORDS`**: Add more tech-related terms (e.g., `claude`, `gpt-4`) to make the scanner more comprehensive.
- **Dynamic Paths**: Make the script more portable by using dynamic paths (`os.path.dirname(os.path.abspath(__file__))`) instead of hardcoding `BASE_DIR`.

## 📚 What I Learned

- Advanced NLP techniques using `nltk` (tokenization, stopword removal, lemmatization).
- Handling multi-word phrases in text processing.
- Building a practical tool for job hunting, directly applicable to my career goals.
- Debugging and iterating on a project to achieve a specific goal (100% match).
- Version control and documentation best practices.

## 💡 Why This Matters

As an aspiring **AI Applications Researcher/Vibe Coder**, tailoring my resume to match job descriptions is crucial for landing interviews. This project not only demonstrates my Python and AI skills but also shows my ability to build tools that solve real-world problems. The Resume Keyword Scanner will continue to help me optimize my resume for future job applications, increasing my chances of success in the competitive tech industry.

## 📞 Contact

- **Email**: 20udaykumar02@gmail.com
- **Website**: https://ud-ai-kumar.vercel.app/

Feel free to reach out if you’d like to collaborate or learn more about my journey!

---

**Part of my 100 Days of Python + AI Journey**  
**May 25, 2025**