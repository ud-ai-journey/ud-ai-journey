def add_expense(expenses, categories):
    """
    Add a new expense entry with an optional category tag.
    expenses: List of (amount, category) tuples.
    categories: Dictionary to track total spending per category.
    """
    try:
        amount = float(input("Enter the expense amount: $"))
        if amount <= 0:
            raise ValueError("Expense amount must be positive.")
        
        category = input("Enter category (e.g., food, travel, emergency) or press Enter to skip: ").strip().lower()
        if not category:
            category = "miscellaneous"
        
        expenses.append((amount, category))
        
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount
        
        print(f"Added ${amount} to {category} category.")
    except ValueError as e:
        if "invalid literal" in str(e):
            print("Error: Please enter a valid number for the expense.")
        else:
            print(f"Error: {e}")

def get_category_breakdown(categories):
    """
    Return a string summary of spending by category.
    """
    if not categories:
        return "No expenses recorded yet."
    
    breakdown = "Spending Breakdown by Category:\n"
    for category, total in categories.items():
        breakdown += f" - {category.capitalize()}: ${total:.2f}\n"
    return breakdown