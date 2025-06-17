# AI-Powered Life Hack Generator (Day 63 Project)

## Overview
The AI-Powered Life Hack Generator is a Python-based tool designed to provide smart, witty life hacks based on user input. Users describe a problem or situation (e.g., "I'm procrastinating" or "I'm energetic"), and the tool responds with a relevant life hack. The project features a `tkinter` GUI, improved keyword detection, and logs interactions to a file.

## Features
- Accepts user input via a simple GUI.
- Matches input to a curated list of 16 life hacks using keyword detection (e.g., "energetic," "stress," "procrastinate").
- Logs all interactions with timestamps to `log.txt`.
- Displays the life hack in the GUI and as a pop-up message.

## Setup
1. **Prerequisites**:
   - Python 3.x installed on your system.
   - `tkinter` library (included with standard Python installations).

2. **Installation**:
   - Save the script as `life_hack_generator_updated.py` (or download it from the repository if applicable).
   - Ensure you have write permissions in the directory to create `log.txt`.

3. **Running the Program**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script:
     ```
     python life_hack_generator_updated.py
     ```
   - A GUI window will open, prompting you to enter a problem or situation.

## Usage
1. Launch the application as described above.
2. In the GUI, type a problem or situation (e.g., "I'm energetic" or "I'm stressed") into the text field.
3. Click the "Get Life Hack" button.
4. The tool will display a relevant life hack in the GUI and show a pop-up with the same message.
5. All interactions are logged to `log.txt` in the same directory.

### Example
- **Input**: "I'm energetic"
- **Output**: "You're feeling energetic? Channel that energy into a quick win—tackle a task you've been avoiding!"
- **Log Entry in `log.txt`**:
  ```
  [2025-06-17 21:19:00] Problem: I'm energetic
  Solution: You're feeling energetic? Channel that energy into a quick win—tackle a task you've been avoiding!
  ```

## Log File
- The tool automatically creates a `log.txt` file in the same directory.
- Each entry includes a timestamp, the user's input, and the generated life hack.
- The log file is appended with each new interaction, so it won't overwrite previous entries.

## Project Details
- **Date**: June 17, 2025
- **Version**: Updated with energetic state detection
- **File**: `life_hack_generator_updated.py`

## Notes
- The tool uses keyword matching to detect common problems (e.g., "lazy," "stress," "energetic"). If no match is found, it selects a random hack.
- The GUI is built with `tkinter` for a user-friendly experience.
- No external APIs are used; all hacks are predefined in the script.