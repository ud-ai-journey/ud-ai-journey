# Focus Buddy - Day 64 Project

## Overview
Focus Buddy is a console-based productivity tool designed to help you stay on track with your tasks using a Pomodoro-style timer. Enter a task, set a custom duration, and receive motivational tips at intervals to keep you focused. Timestamps are included to track your progress, and sessions are logged for review.

## Features
- Start a focus sprint with any task and custom duration (default 25 minutes).
- Receive a random motivational tip every interval, with timestamps for each update.
- Dynamic timer adjusts to the duration you set, providing updates proportional to the time.
- Logs each session with timestamps to `focus_log.txt`.
- Option to start another session or exit with a motivational farewell.

## Setup
1. **Prerequisites**:
   - Python 3.x installed on your system.
2. **Installation**:
   - Save the script as `focus_buddy_dynamic_timer.py` in your project directory.
   - Ensure you have write permissions to create `focus_log.txt`.
3. **Running the Program**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run:
     ```
     python focus_buddy_dynamic_timer.py
     ```

## Usage
1. Launch the application as described above.
2. Enter a task (e.g., "Complete today's code and push to GitHub") when prompted.
3. Specify a duration in minutes (press Enter for the default 25 minutes).
4. Watch for motivational tips at intervals, each with a timestamp, until the session ends.
5. Choose to start another session or exit.
6. Check `focus_log.txt` for a record of your sessions.

### Example
```
🎯 What task are you focusing on today?
> Complete today's code and push to GitHub
Enter focus duration (in minutes, default 25): 1

🔒 Starting a 1-minute Focus Sprint on: Complete today's code and push to GitHub [Started: 2025-06-18 19:18:09 IST]

⏳ 1 mins in... "Small steps today lead to big wins tomorrow." (0 mins left) [Time: 2025-06-18 19:19:09 IST]

✅ Great job! Complete today's code and push to GitHub session complete! [Ended: 2025-06-18 19:19:09 IST]

Want to do another session? (yes/no): no
👋 Thanks for using Focus Buddy! Stay focused and productive!
```

## Log File
- A `focus_log.txt` file is created or appended in the same directory.
- Each entry includes a timestamp, task name, and duration (e.g., `[2025-06-18 19:18:09 IST] Task: Complete today's code and push to GitHub, Duration: 1 mins`).

## Notes
- For testing, the script uses 1-second intervals (`time.sleep(1)`); for real use, change to `time.sleep(60)` for 1-minute intervals.
- The tool dynamically adjusts the number of updates based on the duration, ensuring a smooth experience for any time you set.

## Project Details
- **Date**: June 18, 2025
- **Version**: Dynamic Timer with Timestamps
- **File**: `focus_buddy_dynamic_timer.py`