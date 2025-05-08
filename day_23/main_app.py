from budget_input import get_budget_and_savings
from expense_tracker import add_expense, get_category_breakdown
from smart_alerts import check_budget_status

def main():
    # Initialize data structures
    expenses = []  # List of (amount, category) tuples
    categories = {}  # Dictionary to track spending per category

    # Get budget and savings goal
    budget_data = get_budget_and_savings()
    if budget_data is None:
        print("Exiting due to invalid input.")
        return
    monthly_budget, savings_goal = budget_data

    print("\nBudget Breaker Detector is now running!")
    print(f"Monthly Budget: ${monthly_budget:.2f}, Savings Goal: ${savings_goal:.2f}\n")

    # Main loop
    while True:
        print("\nOptions:")
        print("1. Add an expense")
        print("2. View spending summary")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            add_expense(expenses, categories)
            total_spent, alert_message = check_budget_status(expenses, monthly_budget, savings_goal)
            print(f"\nTotal Spent: ${total_spent:.2f}")
            print(alert_message)

        elif choice == "2":
            total_spent, alert_message = check_budget_status(expenses, monthly_budget, savings_goal)
            print(f"\nTotal Spent: ${total_spent:.2f}")
            print(alert_message)
            print(get_category_breakdown(categories))

        elif choice == "3":
            print("\nFinal Summary:")
            total_spent, alert_message = check_budget_status(expenses, monthly_budget, savings_goal)
            print(f"Total Spent: ${total_spent:.2f}")
            print(alert_message)
            print(get_category_breakdown(categories))
            print("Thank you for using Budget Breaker Detector!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()