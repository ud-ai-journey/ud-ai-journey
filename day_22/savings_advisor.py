def calculate_monthly_savings(income, total_expenses):
    """Calculates the user's monthly savings."""
    return income - total_expenses

def advise_on_savings(savings):
    """Provides advice based on the calculated savings."""
    print("\n--- Savings Advice ---")
    if savings < 0:
        print("🚨 Warning: Your expenses exceed your income. You are in debt this month.")
    elif savings < 500:
        print("⚠️ Your savings are quite low. Consider reducing optional expenses.")
    elif savings < 1500:
        print("👍 You are saving a reasonable amount.")
    else:
        print("✅ Excellent! You are saving well.")
