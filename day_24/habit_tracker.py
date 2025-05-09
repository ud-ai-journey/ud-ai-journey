import datetime
from streak_logic import check_milestones

def initialize_habits(habits, data):
    today_str = datetime.date.today().isoformat()
    for habit in habits:
        if habit not in data:
            data[habit] = {
                'last_date': None,
                'current_streak': 0,
                'milestones': {'3': False, '7': False, '30': False}
            }
    return data

def record_habits(habits, data):
    today = datetime.date.today()
    today_str = today.isoformat()
    print("\nDid you complete the following habits today? (yes/no)")
    for habit in habits:
        while True:
            response = input(f" - {habit}? ").strip().lower()
            if response in ['yes', 'y']:
                last_date_str = data[habit]['last_date']
                if last_date_str:
                    last_date = datetime.date.fromisoformat(last_date_str)
                    days_diff = (today - last_date).days
                    if days_diff == 1:
                        data[habit]['current_streak'] += 1
                    elif days_diff > 1:
                        # Missed days: apply penalty (reset streak)
                        data[habit]['current_streak'] = 1
                        print(f"⚠️ Missed {days_diff - 1} days. Streak reset for '{habit}'.")
                else:
                    data[habit]['current_streak'] = 1
                data[habit]['last_date'] = today_str
                check_milestones(habit, data[habit])
                break
            elif response in ['no', 'n']:
                # User didn't do the habit today, reset streak
                data[habit]['last_date'] = today_str
                data[habit]['current_streak'] = 0
                break
            else:
                print("Please answer 'yes' or 'no'.")
    return data

def add_habit(habits, data):
    new_habit = input("Enter the name of the new habit: ").strip()
    if new_habit not in habits:
        habits.append(new_habit)
        data[new_habit] = {
            'last_date': None,
            'current_streak': 0,
            'milestones': {'3': False, '7': False, '30': False}
        }
        print(f"Habit '{new_habit}' added.")
    else:
        print(f"Habit '{new_habit}' already exists.")
    return habits, data

def remove_habit(habits, data):
    print("Current habits:", habits)
    rem_habit = input("Enter the name of the habit to remove: ").strip()
    if rem_habit in habits:
        habits.remove(rem_habit)
        data.pop(rem_habit, None)
        print(f"Habit '{rem_habit}' removed.")
    else:
        print(f"Habit '{rem_habit}' not found.")
    return habits, data

def view_streaks(habits, data):
    print("\n--- Habit Streaks ---")
    today_str = datetime.date.today().isoformat()
    for habit in habits:
        streak = data[habit]['current_streak']
        last_date = data[habit]['last_date']
        last_date_obj = datetime.date.fromisoformat(last_date) if last_date else None
        days_since = (datetime.date.today() - last_date_obj).days if last_date_obj else None
        print(f"\nHabit: {habit}")
        print(f"  Current streak: {streak} days")
        if last_date:
            print(f"  Last done: {last_date}")
            print(f"  Days since last: {days_since}")
        else:
            print("  Not done yet.")