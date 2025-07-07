import random

def get_user_choice():
    choices = ['rock', 'paper', 'scissors']
    while True:
        user_input = input("Choose rock, paper, or scissors: ").strip().lower()
        if user_input in choices:
            return user_input
        print("Invalid choice. Please try again.")

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user, computer):
    if user == computer:
        return 'tie'
    if (
        (user == 'rock' and computer == 'scissors') or
        (user == 'scissors' and computer == 'paper') or
        (user == 'paper' and computer == 'rock')
    ):
        return 'user'
    return 'computer'

def main():
    print("Welcome to Rock, Paper, Scissors! Best of 3 rounds.")
    user_score = 0
    computer_score = 0
    rounds = 0
    while user_score < 2 and computer_score < 2 and rounds < 3:
        print(f"\nRound {rounds + 1}:")
        user = get_user_choice()
        computer = get_computer_choice()
        print(f"You chose: {user}")
        print(f"Computer chose: {computer}")
        winner = determine_winner(user, computer)
        if winner == 'tie':
            print("It's a tie!")
        elif winner == 'user':
            print("You win this round!")
            user_score += 1
        else:
            print("Computer wins this round!")
            computer_score += 1
        rounds += 1
        print(f"Score: You {user_score} - Computer {computer_score}")
    print("\nGame Over!")
    if user_score > computer_score:
        print("Congratulations! You are the winner!")
    elif computer_score > user_score:
        print("Computer wins the game. Better luck next time!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main() 