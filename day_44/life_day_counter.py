# Day 44: Life Day Counter
# Calculates life statistics based on DOB, with a motivational quote.

from datetime import datetime, timedelta
import random

def get_weekday(date):
    """
    Return the weekday name for a given date.
    """
    return date.strftime("%A")

def calculate_life_stats(dob_str):
    """
    Calculate life statistics: total days lived, weekdays experienced, days to next birthday,
    and weekday born on.
    """
    try:
        # Parse the date of birth
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.now()

        # Calculate total days lived
        total_days = (today - dob).days

        # Calculate weekdays experienced (approximate: weekdays = 5/7 of total days)
        weekdays_approx = int(total_days * (5 / 7))

        # Calculate next birthday
        next_birthday = dob.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        days_to_birthday = (next_birthday - today).days

        # Get the weekday born on
        born_weekday = get_weekday(dob)

        return {
            "total_days": total_days,
            "weekdays_approx": weekdays_approx,
            "days_to_birthday": days_to_birthday,
            "born_weekday": born_weekday
        }
    except ValueError as e:
        print(f"❌ Invalid date format: {e}. Please use YYYY-MM-DD.")
        return None

def get_motivational_quote():
    """
    Return a random motivational quote.
    """
    quotes = [
        "The best way to predict the future is to create it. – Peter Drucker",
        "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
        "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "Your time is limited, don’t waste it living someone else’s life. – Steve Jobs"
    ]
    return random.choice(quotes)

def main():
    print("🎯 Day 44: Life Day Counter")
    # Get user input
    dob_str = input("Enter your date of birth (YYYY-MM-DD): ").strip()

    # Calculate life stats
    stats = calculate_life_stats(dob_str)
    if not stats:
        return

    # Display results
    print(f"\n📆 Life Statistics:")
    print(f"Total days lived: {stats['total_days']}")
    print(f"Approximate weekdays experienced: {stats['weekdays_approx']}")
    print(f"Days until your next birthday: {stats['days_to_birthday']}")
    print(f"You were born on a: {stats['born_weekday']}")

    # Display a motivational quote
    print("\n💡 Motivational Quote for Your Journey:")
    print(get_motivational_quote())

if __name__ == "__main__":
    main()

# Committed after Shani Shignapur Darshan on May 29th,2025

