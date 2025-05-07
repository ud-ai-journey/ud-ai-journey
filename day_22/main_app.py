from expense_utils import get_monthly_income, get_fixed_expenses, get_optional_expenses, calculate_total_expenses
from savings_advisor import calculate_monthly_savings, advise_on_savings

def run_forecaster():
    """Runs the personal expense forecaster application."""
    print("--- Personal Expense Forecaster ---")

    # Get income and expenses
    income = get_monthly_income()
    fixed_expenses = get_fixed_expenses()
    optional_expenses = get_optional_expenses()

    # Calculate totals
    total_expenses = calculate_total_expenses(fixed_expenses, optional_expenses)
    monthly_savings = calculate_monthly_savings(income, total_expenses)

    # Display results
    print(f"\n--- Summary ---")
    print(f"Monthly Income: ${income:.2f}")
    print(f"Total Fixed Expenses: ${fixed_expenses:.2f}")
    print(f"Total Optional Expenses: ${optional_expenses:.2f}")
    print(f"Total Monthly Expenses: ${total_expenses:.2f}")
    print(f"Calculated Monthly Savings: ${monthly_savings:.2f}")

    # Provide advice
    advise_on_savings(monthly_savings)

    print("\n-----------------------------------")

# Run the application
if __name__ == "__main__":
    run_forecaster()