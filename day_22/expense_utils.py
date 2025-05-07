def get_monthly_income():
    """Gets the user's monthly income."""
    while True:
        try:
            income = float(input("Enter your monthly income: "))
            if income < 0:
                print("Income cannot be negative. Please try again.")
            else:
                return income
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_fixed_expenses():
    """Gets the user's fixed monthly expenses."""
    print("\nEnter your fixed monthly expenses:")
    while True:
        try:
            rent = float(input("Rent: "))
            food = float(input("Food/Groceries: "))
            utilities = float(input("Utilities (Electricity, Water, Internet): "))
            other_fixed = float(input("Other fixed expenses: "))
            if any(exp < 0 for exp in [rent, food, utilities, other_fixed]):
                 print("Expenses cannot be negative. Please try again.")
            else:
                return rent + food + utilities + other_fixed
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_optional_expenses():
    """Gets the user's optional monthly expenses."""
    print("\nEnter your optional monthly expenses:")
    while True:
        try:
            entertainment = float(input("Entertainment (Movies, Hobbies): "))
            travel = float(input("Travel/Trips: "))
            dining_out = float(input("Dining out: "))
            other_optional = float(input("Other optional expenses: "))
            if any(exp < 0 for exp in [entertainment, travel, dining_out, other_optional]):
                 print("Expenses cannot be negative. Please try again.")
            else:
                return entertainment + travel + dining_out + other_optional
        except ValueError:
            print("Invalid input. Please enter a number.")

def calculate_total_expenses(fixed, optional):
    """Calculates the total of fixed and optional expenses."""
    return fixed + optional