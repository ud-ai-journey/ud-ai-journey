from habit_tracker import initialize_habits, record_habits, add_habit, remove_habit, view_streaks
from file_handler import load_data, save_data

def main():
    habits = ['meditate', 'exercise', 'read']
    data = load_data()

    data = initialize_habits(habits, data)

    while True:
        print("\n--- Habit Tracker Menu ---")
        print("1. Record today's habits")
        print("2. Add a habit")
        print("3. Remove a habit")
        print("4. View streaks and last done dates")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            data = record_habits(habits, data)
            save_data(data)
        elif choice == '2':
            habits, data = add_habit(habits, data)
            save_data(data)
        elif choice == '3':
            habits, data = remove_habit(habits, data)
            save_data(data)
        elif choice == '4':
            view_streaks(habits, data)
        elif choice == '5':
            print("Goodbye! Keep up the streaks!")
            save_data(data)
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()