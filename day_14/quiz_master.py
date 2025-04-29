import json

# Load quiz data from a JSON file directly
import os
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'quiz.json')
with open(file_path, 'r') as file:
    quiz_data = json.load(file)

# Ask for the difficulty level
difficulty = input("Choose difficulty level (Easy / Medium / Hard): ").strip().lower()

# Depending on the difficulty level, load appropriate questions (assuming you modify the quiz.json accordingly)
# Here we assume that all questions are in the same bank for simplicity
questions = quiz_data["questions"]  # Modify this line if you structure your JSON differently

score = 0
total_questions = len(questions)

print("Welcome to the Quiz! Please answer the following questions:\n")

# Loop through each question
for index, q in enumerate(questions):
    print(f"Q{index + 1}: {q['question']}")
    for option in q['options']:
        print(option)
    
    user_answer = input("Your answer (A/B/C/D): ").strip().upper()
    
    # Check if the answer is correct
    if user_answer == q['answer']:
        print("Correct!\n")
        score += 1
    else:
        print(f"Wrong! The correct answer was {q['answer']}\n")

# Display the final score
print(f"Your final score: {score} out of {total_questions}")

if score == total_questions:
    print("Perfect Score! You're a genius!")
elif score >= total_questions / 2:
    print("Good job! You passed the quiz.")
else:
    print("Better luck next time!")