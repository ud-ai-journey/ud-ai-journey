# Day 45: Mood Calendar Generator (Updated with More Emojis)
# Generates a 7-day mood calendar, counts good/bad moods, allows re-roll or manual entry.

import random

def generate_mood_calendar(use_manual=False):
    """
    Generate a 7-day mood calendar, either randomly or with manual input.
    """
    # Expanded mood list with more emojis
    moods = ["🙂", "😔", "😡", "😎", "🥳", "😴", "🤗", "😱", "🤓", "🥰"]
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    mood_calendar = []

    if use_manual:
        print("✍️ Enter your mood for each day (choose: 🙂 😔 😡 😎 🥳 😴 🤗 😱 🤓 🥰):")
        for day in days:
            while True:
                mood = input(f"📅 {day}: ").strip()
                if mood in moods:
                    mood_calendar.append((day, mood))
                    break
                print("⚠️🚨 Invalid mood! Please choose: 🙂 😔 😡 😎 🥳 😴 🤗 😱 🤓 🥰")
    else:
        # Randomly assign moods
        mood_calendar = [(day, random.choice(moods)) for day in days]

    return mood_calendar

def analyze_moods(mood_calendar):
    """
    Analyze the mood calendar and count good/bad moods.
    """
    good_moods = ["🙂", "😎", "🥳", "🤗", "🤓", "🥰"]
    bad_moods = ["😔", "😡", "😴", "😱"]

    good_count = sum(1 for _, mood in mood_calendar if mood in good_moods)
    bad_count = sum(1 for _, mood in mood_calendar if mood in bad_moods)

    return good_count, bad_count

def display_mood_calendar(mood_calendar, good_count, bad_count):
    """
    Display the mood calendar and summary with more emojis.
    """
    print("\n🗓️✨ Your 7-Day Mood Calendar: ✨")
    print("=" * 30)
    for day, mood in mood_calendar:
        print(f"📅 {day}: {mood} 🌟")

    print("\n📊📈 Mood Summary: 📈")
    print(f"🌈 Good Moods (🙂 😎 🥳 🤗 🤓 🥰): {good_count}")
    print(f"🌧️ Bad Moods (😔 😡 😴 😱): {bad_count}")

def main():
    print("✨🌟 Day 45: Mood Calendar Generator 🌟✨")
    print("🗓️ Generate a 7-day mood calendar with random or manual moods. 📅")

    while True:
        # Ask user for mode with emoji prompt
        mode = input("\n🔢 Choose mode (1: Random 🎲, 2: Manual ✍️, 3: Exit 🚪): ").strip()
        
        if mode == "3":
            print("👋🌈 Goodbye!")
            break

        if mode not in ["1", "2"]:
            print("⚠️🚨 Invalid choice! Please choose 1, 2, or 3.")
            continue

        # Generate the mood calendar
        use_manual = (mode == "2")
        mood_calendar = generate_mood_calendar(use_manual)

        # Analyze and display results
        good_count, bad_count = analyze_moods(mood_calendar)
        display_mood_calendar(mood_calendar, good_count, bad_count)

        # Ask if user wants to re-roll
        if not use_manual:
            reroll = input("\n🎲 Would you like to re-roll the week? (y/n): ").strip().lower()
            if reroll != 'y':
                continue

if __name__ == "__main__":
    main()

#Committed after completing devotional trip to Shirdi & Shani Shignapur 