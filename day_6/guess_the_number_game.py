# 🎯 Guess the Number Game | Practiced 'if-else' with random module | Day 5

import random

# System selects a random number between 1 and 20
random_num = random.randint(1, 20)

# Taking user's guess
user_num = int(input("Hey Mate!! I have already selected a number between 1-20.\nCan you guess it? If yes, then give the number you think I would have selected: "))

# Conditional logic to compare guesses
if user_num == random_num:
    print("🎉 Congratulations! You nailed it!")
elif user_num < random_num:
    print("📉 Your guess was a lil' low. My number was:", random_num)
elif user_num > random_num:
    print("📈 Your guess was a lil' high. My number was:", random_num)
