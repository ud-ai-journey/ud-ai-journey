# Day 61: Job Role Recommender Project

## 📖 Overview

Welcome to **Day 61** of your Python-AI journey! This project builds a **Job Role Recommender** Python script that helps users identify suitable tech career roles based on their skills. By selecting 3–5 skills from a predefined list, users receive a recommended tech role (e.g., Data Analyst, AI Engineer, DevOps Engineer) along with tailored tips for success. The results are displayed in the console and exported to a text file for reference.

This project focuses on:
- **Mapping logic**: Matching user inputs to predefined role profiles using set operations.
- **Data structures**: Utilizing lists, sets, and dictionaries for efficient skill-role mapping.
- **User interaction**: Handling multiple-choice inputs with validation.
- **File output**: Exporting results to a text file for persistence.

## 🎯 Features

- **Skill Selection**: Users choose 3–5 skills from a list of 20 tech-related skills (e.g., Python, SQL, React, Kubernetes, Cybersecurity).
- **Role Recommendation**: The script matches selected skills to role profiles and recommends the best-fit tech role.
- **Tailored Tips**: Provides actionable tips specific to the recommended role to guide career development.
- **Result Export**: Saves the recommendation, selected skills, and tips to `career_suggestion.txt`.

## 🛠️ Prerequisites

- **Python 3.x**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/) if needed.
- **Text Editor/IDE**: Use any editor like VS Code, PyCharm, or Notepad to view/edit the script.
- No external libraries are required, as the script uses standard Python.

## 📦 Setup Instructions

1. **Clone or Download the Project**:
   - If using a repository, clone it: `git clone <repository-url>`.
   - Alternatively, copy the `job_role_recommender.py` script to a local directory (e.g., `C:\Users\<YourUsername>\Python-AI\ud-ai-journey\day_61`).

2. **Verify Python Installation**:
   - Open a terminal/command prompt and run `python --version` or `python3 --version` to confirm Python is installed.
   - Ensure the Python executable is in your system's PATH.

3. **Navigate to Project Directory**:
   - Use the command: `cd C:\Users\<YourUsername>\Python-AI\ud-ai-journey\day_61`.

4. **Run the Script**:
   - Execute the script using: `python job_role_recommender.py` or `python3 job_role_recommender.py`.
   - On Windows, you can also use the full Python path, as you did: `& "C:/Users/uday kumar/AppData/Local/Programs/Python/Python312/python.exe" "job_role_recommender.py"`.

## 🚀 Usage Guide

1. **Start the Script**:
   - Run the script as described above. You'll see a welcome message: `👋 Hello! Let's find the perfect tech role for you.`

2. **Select Skills**:
   - A numbered list of 20 skills will be displayed (e.g., 1. Python, 2. SQL, etc.).
   - Enter 3–5 numbers corresponding to your top skills, separated by commas (e.g., `1,2,6,14,16`).
   - The script validates your input to ensure:
     - You select 3–5 skills.
     - Numbers are within the valid range (1–20).
     - Input is properly formatted.

3. **View Recommendation**:
   - The script matches your skills to predefined role profiles and displays the best-fit role (e.g., `👉 Data Analyst`).
   - It also shows role-specific tips (e.g., "Build portfolio projects using Pandas, SQL, and dashboards.").

4. **Check Output File**:
   - A file named `career_suggestion.txt` is created in the project directory.
   - It contains the recommended role, your selected skills, and the tips for reference.

### Sample Interaction

```bash
👋 Hello! Let's find the perfect tech role for you.

Pick your top 3–5 skills (enter numbers, separated by commas):
1. Python
2. SQL
3. Machine Learning
...
20. Cybersecurity

Enter your choices (e.g., 1,2,3): 1,16,14,2,6

🧠 Based on your skills, you could be a great:
👉 Data Analyst

💡 Tips:
- Build portfolio projects using Pandas, SQL, and dashboards.
- Master Tableau or Power BI for data visualization.
- Practice data cleaning and statistical analysis.

📄 Results exported to 'career_suggestion.txt'
```

## 📁 File Structure

```
day_61/
├── job_role_recommender.py    # Main Python script
├── career_suggestion.txt     # Output file (generated after running the script)
└── README.md                 # This documentation file
```

## 🧠 How It Works

1. **Skill Input**:
   - The `get_user_skills()` function displays a list of 20 skills and collects user input.
   - It validates the input to ensure 3–5 valid skill numbers are provided.

2. **Role Matching**:
   - The `recommend_role()` function uses a dictionary of role profiles, where each role is mapped to a set of required skills.
   - It calculates the overlap between user-selected skills and each role's required skills using set intersection.
   - The role with the highest overlap is recommended. If no overlap exists, it returns "No strong match found."

3. **Tips and Output**:
   - A dictionary of role-specific tips is used to provide career advice for the recommended role.
   - The `export_to_file()` function writes the recommendation, skills, and tips to `career_suggestion.txt`.

4. **Main Execution**:
   - The `main()` function orchestrates the flow: get skills, recommend a role, display results, and export to a file.

## 📚 Available Skills and Roles

### Skills (20)
- Python, SQL, Machine Learning, React, REST APIs, Excel, Cloud (AWS, GCP), Docker, JavaScript, Java, C++, Node.js, Tableau, Git, Kubernetes, HTML/CSS, MongoDB, TensorFlow, Linux, Cybersecurity

### Roles and Associated Skills
- **Data Analyst**: Python, SQL, Excel, Tableau
- **Backend Developer**: Python, REST APIs, Java, Docker, Node.js, MongoDB
- **Frontend Developer**: React, JavaScript, HTML/CSS
- **AI Engineer**: Python, Machine Learning, TensorFlow, Cloud (AWS, GCP)
- **DevOps Engineer**: Cloud (AWS, GCP), Docker, Kubernetes, Linux, Git
- **Security Engineer**: Cybersecurity, Linux, Python, Cloud (AWS, GCP)
- **Full Stack Developer**: React, Node.js, REST APIs, MongoDB, HTML/CSS

## 🌟 Extending the Project

Want to enhance the recommender? Here are some ideas:
- **Add More Skills/Roles**: Expand the `skills_list` and `role_profiles` to include additional skills (e.g., R, Angular) or roles (e.g., Data Scientist, Mobile Developer).
- **Weighted Skills**: Assign weights to skills based on their importance for each role.
- **GUI Interface**: Use a library like `tkinter` or `PyQt` to create a graphical interface.
- **Database Integration**: Store skills and recommendations in a SQLite database.
- **Skill Proficiency Levels**: Allow users to specify proficiency (e.g., beginner, intermediate) for each skill.

## 🐛 Troubleshooting

- **Script Not Running**:
  - Ensure Python is installed and accessible via the command line.
  - Check the script path in your command (e.g., `job_role_recommender.py` must exist in the current directory).
- **Invalid Input Error**:
  - Enter numbers separated by commas (e.g., `1,2,3`).
  - Ensure you select 3–5 skills within the range 1–20.
- **No Output File**:
  - Verify write permissions in the project directory.
  - Check if `career_suggestion.txt` was created after running the script.
- **Unexpected Role**:
  - The role is based on the highest skill overlap. Review your selected skills and the role profiles in the script.

## 🙌 Acknowledgments

- Built as part of your **Python-AI Journey** on Day 61.
- Powered by Python's standard library for simplicity and accessibility.
- Inspired by the need for career guidance in the tech industry.

Happy coding, and best of luck in your tech career journey! 🚀