import random

def generate_question(level):
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(['+', '-'])
    elif level == 2:
        a, b = random.randint(2, 12), random.randint(2, 12)
        op = random.choice(['*', '/'])
        if op == '/':
            a = a * b  # ensure integer division
    else:
        a, b = random.randint(10, 99), random.randint(10, 99)
        op = random.choice(['+', '-', '*'])
    question = f"{a} {op} {b}"
    answer = eval(question)
    if op == '/':
        answer = int(answer)
    return question, answer

def play_game():
    print("\nWelcome to Math Quest: The Adventure of Numbers!")
    print("Answer math questions to help your hero on their journey!\n")
    score = 0
    level = 1
    for i in range(1, 11):
        if i == 4:
            level = 2
        elif i == 8:
            level = 3
        question, answer = generate_question(level)
        print(f"Q{i}: What is {question}?")
        try:
            user = int(input("Your answer: "))
            if user == answer:
                print(random.choice([
                    "Great job! 🏆", "Correct! 🎉", "You did it! 🌟", "Awesome! 👍"
                ]))
                score += 1
            else:
                print(f"Oops! The correct answer was {answer}. Keep going!")
        except ValueError:
            print(f"Please enter a valid number! The answer was {answer}.")
        print()
    print(f"Game Over! Your score: {score}/10")
    if score == 10:
        print("Perfect! You're a Math Quest Master! 🥇")
    elif score >= 7:
        print("Well done! Keep practicing to reach perfection!")
    else:
        print("Don't worry, every hero starts somewhere. Try again!")

def main():
    while True:
        play_game()
        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing Math Quest! See you next time!")
            break

if __name__ == "__main__":
    main() 