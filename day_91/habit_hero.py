import json
import os
from datetime import datetime, timedelta

DATA_FILE = 'habit_hero_data.json'

DEFAULT_HABITS = [
    'Brush teeth',
    'Read a book',
    'Help at home',
    'Drink water',
    'Exercise',
]

REWARDS = [
    (3, 'Bronze Star ⭐'),
    (7, 'Silver Badge 🥈'),
    (14, 'Gold Medal 🥇'),
    (30, 'Diamond Trophy 💎'),
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'habits': DEFAULT_HABITS, 'progress': {}, 'rewards': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def show_habits(habits):
    print("\nYour Habits:")
    for idx, habit in enumerate(habits, 1):
        print(f"  {idx}. {habit}")

def add_habit(data):
    new_habit = input("Enter a new habit to track: ").strip()
    if new_habit and new_habit not in data['habits']:
        data['habits'].append(new_habit)
        print(f"Added '{new_habit}' to your habits!")
    else:
        print("Invalid or duplicate habit.")

def check_in(data):
    today = datetime.now().strftime('%Y-%m-%d')
    print("\nCheck-in for today!")
    for habit in data['habits']:
        done = input(f"Did you '{habit}' today? (y/n): ").strip().lower()
        if habit not in data['progress']:
            data['progress'][habit] = []
        if done == 'y':
            if today not in data['progress'][habit]:
                data['progress'][habit].append(today)
                print(f"Great job on '{habit}'! 🌟")
        else:
            print(f"Let's try to do '{habit}' tomorrow!")
    save_data(data)
    print("Check-in complete! Keep up the good work!")

def get_streak(dates):
    if not dates:
        return 0
    dates = sorted([datetime.strptime(d, '%Y-%m-%d') for d in dates], reverse=True)
    streak = 1
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            streak += 1
        else:
            break
    return streak

def show_progress(data):
    print("\nYour Habit Streaks:")
    for habit in data['habits']:
        streak = get_streak(data['progress'].get(habit, []))
        print(f"  {habit}: {streak} day streak")
        for days, reward in reversed(REWARDS):
            if streak >= days:
                print(f"    Reward: {reward}")
                break
    print()

def main():
    data = load_data()
    print("\nWelcome to Habit Hero: The Streak Adventure!")
    while True:
        print("\nMenu:")
        print("  1. Show habits")
        print("  2. Add a new habit")
        print("  3. Daily check-in")
        print("  4. Show progress & rewards")
        print("  5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == '1':
            show_habits(data['habits'])
        elif choice == '2':
            add_habit(data)
            save_data(data)
        elif choice == '3':
            check_in(data)
        elif choice == '4':
            show_progress(data)
        elif choice == '5':
            print("Goodbye, Habit Hero! Keep building those awesome habits!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 