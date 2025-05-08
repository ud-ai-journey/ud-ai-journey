def get_budget_and_savings():
    """
    Get the user's monthly budget and savings goal.
    Returns a tuple of (monthly_budget, savings_goal).
    """
    try:
        monthly_budget = float(input("Enter your monthly budget: $"))
        savings_goal = float(input("Enter your monthly savings goal: $"))
        if monthly_budget <= 0 or savings_goal < 0:
            raise ValueError("Budget must be positive, and savings goal cannot be negative.")
        if savings_goal > monthly_budget:
            raise ValueError("Savings goal cannot exceed the monthly budget.")
        return monthly_budget, savings_goal
    except ValueError as e:
        if "invalid literal" in str(e):
            print("Error: Please enter valid numbers.")
        else:
            print(f"Error: {e}")
        return None