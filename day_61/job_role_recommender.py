# Job Role Recommender based on user skills

def get_user_skills():
    skills_list = [
        "Python", "SQL", "Machine Learning", "React", "REST APIs",
        "Excel", "Cloud (AWS, GCP)", "Docker", "JavaScript", "Java",
        "C++", "Node.js", "Tableau", "Git", "Kubernetes", "HTML/CSS",
        "MongoDB", "TensorFlow", "Linux", "Cybersecurity"
    ]
    print("👋 Hello! Let's find the perfect tech role for you.\n")
    print("Pick your top 3–5 skills (enter numbers, separated by commas):")
    for i, skill in enumerate(skills_list, 1):
        print(f"{i}. {skill}")
    
    while True:
        try:
            choices = input("\nEnter your choices (e.g., 1,2,3): ").split(',')
            choices = [int(c.strip()) for c in choices]
            if not (3 <= len(choices) <= 5):
                print("Please select 3 to 5 skills.")
                continue
            if any(c < 1 or c > len(skills_list) for c in choices):
                print(f"Please select numbers between 1 and {len(skills_list)}.")
                continue
            return [skills_list[c-1] for c in choices]
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")

def recommend_role(skills):
    # Role profiles with required skills
    role_profiles = {
        "Data Analyst": {"Python", "SQL", "Excel", "Tableau"},
        "Backend Developer": {"Python", "REST APIs", "Java", "Docker", "Node.js", "MongoDB"},
        "Frontend Developer": {"React", "JavaScript", "HTML/CSS"},
        "AI Engineer": {"Python", "Machine Learning", "TensorFlow", "Cloud (AWS, GCP)"},
        "DevOps Engineer": {"Cloud (AWS, GCP)", "Docker", "Kubernetes", "Linux", "Git"},
        "Security Engineer": {"Cybersecurity", "Linux", "Python", "Cloud (AWS, GCP)"},
        "Full Stack Developer": {"React", "Node.js", "REST APIs", "MongoDB", "HTML/CSS"}
    }
    
    # Calculate match score for each role
    best_role = None
    highest_score = 0
    for role, required_skills in role_profiles.items():
        match_count = len(set(skills) & required_skills)
        if match_count > highest_score:
            highest_score = match_count
            best_role = role
    
    if highest_score == 0:
        return "No strong match found", []
    
    # Tips for the recommended role
    tips = {
        "Data Analyst": [
            "Build portfolio projects using Pandas, SQL, and dashboards.",
            "Master Tableau or Power BI for data visualization.",
            "Practice data cleaning and statistical analysis."
        ],
        "Backend Developer": [
            "Create RESTful APIs using Flask, Django, or Express.",
            "Learn database management with MongoDB or PostgreSQL.",
            "Understand microservices and server scaling."
        ],
        "Frontend Developer": [
            "Build responsive UIs with React and Tailwind CSS.",
            "Learn state management with Redux or Context API.",
            "Focus on accessibility and UX principles."
        ],
        "AI Engineer": [
            "Work on ML projects using TensorFlow or PyTorch.",
            "Study cloud-based ML deployment (AWS SageMaker, GCP AI).",
            "Deepen knowledge in statistics and neural networks."
        ],
        "DevOps Engineer": [
            "Master CI/CD pipelines with Jenkins or GitHub Actions.",
            "Learn Kubernetes for container orchestration.",
            "Understand infrastructure-as-code with Terraform."
        ],
        "Security Engineer": [
            "Study penetration testing and vulnerability assessment.",
            "Learn about cloud security (AWS IAM, GCP policies).",
            "Practice scripting for security automation with Python."
        ],
        "Full Stack Developer": [
            "Build end-to-end apps with React and Node.js.",
            "Learn both SQL and NoSQL databases.",
            "Focus on API integration and deployment."
        ]
    }
    
    return best_role, tips.get(best_role, [])

def export_to_file(role, skills, tips):
    with open("career_suggestion.txt", "w") as f:
        f.write(f"Recommended Role: {role}\n")
        f.write("\nBased on Your Skills:\n")
        for skill in skills:
            f.write(f"- {skill}\n")
        f.write("\nTips for Success:\n")
        for tip in tips:
            f.write(f"- {tip}\n")

def main():
    skills = get_user_skills()
    role, tips = recommend_role(skills)
    
    print(f"\n🧠 Based on your skills, you could be a great:")
    print(f"👉 {role}\n")
    
    if tips:
        print("💡 Tips:")
        for tip in tips:
            print(f"- {tip}")
    
    export_to_file(role, skills, tips)
    print("\n📄 Results exported to 'career_suggestion.txt'")

if __name__ == "__main__":
    main()