import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re
from collections import Counter
from termcolor import colored
import sys
import os

# Fix Unicode encoding for Windows PowerShell
sys.stdout.reconfigure(encoding='utf-8')

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Define tech-related keywords to prioritize (including multi-word phrases)
TECH_KEYWORDS = {
    'python', 'django', 'flask', 'sql', 'postgresql', 'aws', 'machine learning', 'data science',
    'ai', 'web development', 'software development', 'unit testing', 'cloud', 'nlp', 'pandas',
    'scikit-learn', 'javascript', 'java', 'database', 'restful', 'api', 'vibe coding', 'cursor', 'replit',
    'natural language processing'
}

# Define the base directory for files
BASE_DIR = "C:/Users/uday kumar/Python-AI/ud-ai-journey/day_40"

def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and len(token) > 2]
    return tokens

def extract_keywords(text, top_n=10):
    # Preprocess text for single-word tokens
    tokens = preprocess_text(text)
    # Also look for multi-word phrases directly in the text
    text_lower = text.lower()
    multi_word_keywords = []
    for keyword in TECH_KEYWORDS:
        if ' ' in keyword:  # Multi-word keyword
            if keyword in text_lower:
                multi_word_keywords.append(keyword)
    
    # Filter single-word tokens for tech-related keywords
    tech_tokens = [token for token in tokens if token in TECH_KEYWORDS]
    # Include all tech keywords that appear at least once (no frequency threshold)
    single_word_keywords = list(set(tech_tokens))
    
    # Combine single-word and multi-word keywords
    keywords = list(set(single_word_keywords + multi_word_keywords))
    # Limit to top_n
    return keywords[:top_n]

def load_file(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)

def match_keywords(resume_tokens, jd_keywords):
    matched = []
    missing = []
    # For resume, also check for multi-word phrases
    resume_text = " ".join(resume_tokens)
    for keyword in jd_keywords:
        if ' ' in keyword:  # Multi-word keyword
            if keyword in resume_text:
                matched.append(keyword)
            else:
                missing.append(keyword)
        else:  # Single-word keyword
            if keyword in resume_tokens:
                matched.append(keyword)
            else:
                missing.append(keyword)
    return matched, missing

def main():
    print("🎯 Day 40: Resume Keyword Scanner")

    # Load resume and job description using absolute paths
    resume_text = load_file("resume.txt")
    jd_text = load_file("job_description.txt")

    # Preprocess both texts
    resume_tokens = preprocess_text(resume_text)
    jd_tokens = preprocess_text(jd_text)

    # Extract keywords from job description
    jd_keywords = extract_keywords(jd_text, top_n=10)
    if not jd_keywords:
        print("No relevant keywords found in the job description. Please check the input.")
        sys.exit(1)
    print("\n📋 Job Description Keywords:")
    print(", ".join(jd_keywords))

    # Match keywords in resume
    matched_keywords, missing_keywords = match_keywords(resume_tokens, jd_keywords)

    # Calculate match percentage
    total_keywords = len(jd_keywords)
    matched_count = len(matched_keywords)
    match_percentage = (matched_count / total_keywords) * 100 if total_keywords > 0 else 0

    # Display results with colored output
    print("\n🔍 Match Results:")
    print(f"Matched Keywords ({matched_count}/{total_keywords}):")
    for keyword in jd_keywords:
        if keyword in matched_keywords:
            print(f"  🟩 {colored(keyword, 'green')}")
        else:
            print(f"  🟥 {colored(keyword, 'red')}")

    print(f"\n📊 Match Percentage: {match_percentage:.2f}%")

    # Recommend top 3 missing keywords
    if missing_keywords:
        print("\n💡 Recommendations:")
        print("Add these top 3 missing keywords to improve your match:")
        for i, keyword in enumerate(missing_keywords[:3], 1):
            print(f"{i}. {keyword}")
    else:
        print("\n🎉 All keywords matched! Your resume aligns well with the job description.")

if __name__ == "__main__":
    main()