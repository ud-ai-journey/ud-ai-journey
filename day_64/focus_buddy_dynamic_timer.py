import time
import random
from datetime import datetime

# Motivational tips list
tips = [
    "Your focus determines your future.",
    "Don’t multitask. Single-task and finish fast.",
    "Discipline beats motivation. Show up anyway.",
    "Block distractions before they block your dreams.",
    "Focus is a muscle. Train it daily.",
    "Small steps today lead to big wins tomorrow.",
    "Turn off notifications to own your time.",
    "Every focused minute brings you closer to success."
]

# Function to log task
def log_task(task, duration):
    with open("focus_log.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        f.write(f"[{timestamp}] Task: {task}, Duration: {duration} mins\n")

# Main focus session function
def focus_session():
    # Get task and custom duration
    task = input("🎯 What task are you focusing on today?\n> ").strip()
    try:
        duration = int(input("Enter focus duration (in minutes, default 25): ") or 25)
        if duration <= 0:
            duration = 25
    except ValueError:
        duration = 25

    timestamp_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"\n🔒 Starting a {duration}-minute Focus Sprint on: {task} [Started: {timestamp_start}]\n")
    log_task(task, duration)

    # Convert duration to seconds
    total_seconds = duration * 60
    interval_seconds = max(60, total_seconds // 4)  # At least 1-minute intervals, up to 4 updates

    # Run timer with dynamic updates
    elapsed = 0
    while elapsed < total_seconds:
        time.sleep(1)  # Test with 1 second; use 60 for 1-min intervals
        elapsed += 1
        if elapsed % interval_seconds == 0 or elapsed >= total_seconds:
            remaining = max(0, (total_seconds - elapsed) // 60)
            timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
            if remaining > 0:
                tip = random.choice(tips)
                print(f"⏳ {elapsed // 60} mins in... \"{tip}\" ({remaining} mins left) [Time: {timestamp_now}]")
            else:
                tip = random.choice(tips)
                print(f"⏳ {duration} mins in... \"{tip}\" (0 mins left) [Time: {timestamp_now}]")

    timestamp_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"\n✅ Great job! {task} session complete! [Ended: {timestamp_end}]")

# Main loop
while True:
    focus_session()
    if input("\nWant to do another session? (yes/no): ").lower().strip() != "yes":
        print("👋 Thanks for using Focus Buddy! Stay focused and productive!")
        break