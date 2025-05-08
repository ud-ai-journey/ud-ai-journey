def check_budget_status(expenses, monthly_budget, savings_goal):
    """
    Check the current spending against the budget and provide alerts/suggestions.
    expenses: List of (amount, category) tuples.
    Returns a tuple of (total_spent, alert_message).
    """
    total_spent = sum(amount for amount, _ in expenses)
    budget_percentage = (total_spent / monthly_budget) * 100
    remaining_budget = monthly_budget - total_spent
    alert_message = ""

    # Check if savings goal is at risk
    if remaining_budget < savings_goal:
        alert_message += "⚠️ Warning: Your remaining budget is less than your savings goal!\n"
        alert_message += f"Remaining: ${remaining_budget:.2f}, Savings Goal: ${savings_goal:.2f}\n"

    # Budget threshold alerts
    if budget_percentage >= 90:
        alert_message += f"⚠️ Critical Alert: You've reached {budget_percentage:.1f}% of your planned budget!\n"
    elif budget_percentage >= 75:
        alert_message += f"⚠️ Warning: You've reached {budget_percentage:.1f}% of your planned budget!\n"

    # Smart suggestions
    if budget_percentage >= 75:
        alert_message += "Suggestions to stay on track:\n"
        alert_message += " - Cut back on non-essential spending (e.g., dining out, entertainment).\n"
        alert_message += " - Review your category breakdown to identify high-spending areas.\n"

    if not alert_message:
        alert_message = f"You're at {budget_percentage:.1f}% of your budget. Keep up the good work!\n"

    return total_spent, alert_message