# Emoji Cipher Decoder & Encoder - Day 49

## Overview
Welcome to the **Emoji Cipher Decoder & Encoder**, a fun and interactive Python project designed for Day 49 of a coding streak! This script lets you decode secret messages written in emojis, encode text messages into emoji sequences, and play a guessing game to test your decoding skills. Each emoji represents a letter (e.g., 🐍 = S, 🍎 = A), and the script uses a dictionary to map emojis to letters and vice versa. It’s a creative way to practice core Python concepts like dictionaries, loops, string handling, and user input while having a blast with emojis! 😄

This project is perfect for Python learners who want a travel-friendly, engaging challenge that combines logic and creativity. Whether you’re decoding a cryptic emoji message, encoding a secret note for a friend, or battling it out in the guessing game, this script is designed to be both educational and entertaining.

## Features
- **Decode Emoji Messages**: Enter a sequence of emojis (e.g., 🐍🍎🐝) to decode it into a text message (e.g., SAB).
- **Encode Text Messages**: Convert a text message (e.g., HELLO) into an emoji sequence (e.g., 🏠🐘🦁🦁🐙).
- **Emoji Guessing Game**: Guess the word behind a randomly generated emoji sequence across 3 rounds, with a score tracker.
- **Emoji Support**: Uses a predefined emoji-to-letter mapping with fun emojis like 🐍, 🍎, and 🌝.
- **Error Handling**: Handles invalid inputs, empty inputs, and interruptions (e.g., Ctrl+C or EOF).
- **User-Friendly**: Clear prompts and feedback, with emojis for visual flair (✅, ❌, 🔓, 🔒).

## Learning Objectives
This project reinforces key Python concepts:
- **Dictionaries**: Mapping emojis to letters and vice versa.
- **Loops**: Iterating over strings to decode/encode messages.
- **String Handling**: Processing user input with `.strip()`, `.upper()`, and splitting emojis.
- **Input/Output**: Using `input()` for interactive gameplay and printing results.
- **Error Handling**: Managing exceptions like `EOFError` and invalid inputs.
- **Randomization**: Using `random.choice()` for the guessing game.

## Prerequisites
- **Python 3.x**: The script was tested with Python 3.12 but should work with any Python 3.x version.
- **No External Libraries**: Uses only core Python modules (`random`, `unicodedata`).
- **UTF-8 Compatible Terminal**: For proper emoji display, especially on Windows (see [Setup](#setup) for details).

## Setup
1. **Save the Script**:
   - Download or copy the `decode_emoji.py` script to your local machine (e.g., `C:/Users/uday kumar/Python-AI/ud-ai-journey/day_49/decode_emoji.py`).
   - Ensure the file is saved with a `.py` extension.

2. **Set Up Your Terminal (Windows)**:
   - Emojis may display as `����` in Windows Command Prompt or PowerShell due to encoding issues.
   - For proper emoji display, use **Windows Terminal** or set PowerShell to UTF-8:
     ```bash
     chcp 65001
     ```
   - Run this command in PowerShell before executing the script to ensure emojis render correctly.

3. **Run the Script**:
   - Open your terminal or command prompt.
   - Navigate to the script’s directory:
     ```bash
     cd "C:/Users/uday kumar/Python-AI/ud-ai-journey/day_49"
     ```
   - Execute the script:
     ```bash
     python decode_emoji.py
     ```

## How to Use
The script offers a menu with three main modes and an exit option. Here’s how each works:

### 1. Decode an Emoji Message
- **What it does**: Converts a sequence of emojis into a text message using the emoji-to-letter map (e.g., 🐍🍎🐝 → SAB).
- **How to use**:
  - Select option `1` from the menu.
  - Enter emojis using the Windows emoji picker (`Windows Key + .`) or copy-paste from the script’s output or a text editor.
  - Example: For 🐍🍎🐝, enter the emojis directly (not "snake,apple,bee").
  - The script will output the decoded message (e.g., "SAB").
  - If you enter invalid emojis, they’ll be replaced with `?` in the output.
  - If no valid emojis are found, you’ll get a warning to use emojis from the map.

### 2. Encode a Text Message
- **What it does**: Converts a text message (A-Z letters only) into an emoji sequence (e.g., HELLO → 🏠🐘🦁🦁🐙).
- **How to use**:
  - Select option `2`.
  - Enter a word or phrase using letters A-Z (spaces are allowed, but non-letters are kept as-is).
  - Example: Enter "HELLO" to get 🏠🐘🦁🦁🐙.
  - If you include non-letters (e.g., numbers or symbols), you’ll be prompted to use letters only.

### 3. Play the Emoji Guessing Game
- **What it does**: Challenges you to guess the word behind a randomly generated emoji sequence across 3 rounds.
- **How to use**:
  - Select option `3`.
  - For each round, you’ll see an emoji sequence (e.g., 🐱🍎🌴 for "CAT").
  - Enter a single word as your guess (e.g., "CAT", not "cat,apple,tree").
  - The script checks if your guess matches the word and tracks your score.
  - After 3 rounds, you’ll see your score (e.g., 2/3) with a fun message.

### 4. Exit
- Select option `4` to quit the program.

### Emoji Map
The script uses the following emoji-to-letter mapping:
- 🍎 = A, 🐝 = B, 🐱 = C, 🐶 = D, 🐘 = E
- 🐸 = F, 🦒 = G, 🏠 = H, 🍦 = I, 🕹️ = J
- 🎋 = K, 🦁 = L, 🌝 = M, 🎶 = N, 🐙 = O
- 🥞 = P, 👸 = Q, 🤖 = R, 🐍 = S, 🌴 = T
- 🦄 = U, 🎻 = V, 🌊 = W, ❌ = X, 🪀 = Y, 🦓 = Z

Refer to this map when decoding or guessing to understand what each emoji represents.

## Example Run
Here’s what a typical session looks like:

```
🔐 Emoji Cipher Decoder & Encoder 😄

Choose an option:
1. Decode an emoji message
2. Encode a text message
3. Play the emoji guessing game
4. Exit
Enter 1-4: 1
Enter emojis (e.g., 🐍🍎🐝 for SAB). Use Windows Key + . to open emoji picker.
Emoji message: 🐍🍎🐝
🔓 Decoded Message: SAB

Choose an option:
1. Decode an emoji message
2. Encode a text message
3. Play the emoji guessing game
4. Exit
Enter 1-4: 2
Enter a word or phrase (letters A-Z only, e.g., HELLO).
Text message: HELLO
🔒 Encoded Message: 🏠🐘🦁🦁🐙

Choose an option:
1. Decode an emoji message
2. Encode a text message
3. Play the emoji guessing game
4. Exit
Enter 1-4: 3

🎮 Emoji Guessing Game! Guess the word for each emoji sequence (3 rounds).
Hint: Enter a single word (e.g., CAT, not 'cat,apple,tree').

Round 1/3: Decode this: 🐱🍎🌴
Your guess (one word): CAT
✅ Correct! You're an emoji master!

Round 2/3: Decode this: 🐶🐙🦒
Your guess (one word): DOG
✅ Correct! You're an emoji master!

Round 3/3: Decode this: 🏠🐙🌝🐘
Your guess (one word): HOME
✅ Correct! You're an emoji master!

🏆 Game Over! Score: 3/3
Emoji Mastermind! 🧠

Choose an option:
1. Decode an emoji message
2. Encode a text message
3. Play the emoji guessing game
4. Exit
Enter 1-4: 4
👋 Thanks for playing! Stay cryptic!
```

## Troubleshooting
- **Emojis Display as `����` in Terminal**:
  - This is a Windows terminal issue (PowerShell or Command Prompt uses `cp1252` encoding).
  - Fix: Run `chcp 65001` in PowerShell before executing the script, or use **Windows Terminal** (which supports UTF-8 by default).
  - The script still processes emojis correctly, even if the display is garbled.

- **Decoding Shows Only `?` Characters**:
  - You likely entered emoji names (e.g., "snake,apple,bee") instead of emojis (🐍🍎🐝).
  - Fix: Use the Windows emoji picker (`Windows Key + .`) or copy-paste emojis from the script’s output or a text editor.

- **Guessing Game Rejects Correct Guesses**:
  - Ensure you’re entering a single word (e.g., "CAT", not "cat,apple,tree").
  - The script is case-insensitive, but commas or spaces will trigger an error message.
  - Check the emoji map to understand the sequence (e.g., 🐱🍎🌴 = C+A+T = CAT).

- **Input Errors (EOFError or KeyboardInterrupt)**:
  - If you interrupt the script (e.g., Ctrl+C), it will exit gracefully with a message.
  - Empty inputs or invalid choices (e.g., not 1-4) will prompt you to try again.

## Tips for Success
- **Entering Emojis**: On Windows, press `Windows Key + .` to open the emoji picker. Select emojis like 🐍, 🍎, or 🐝 directly. Avoid typing emoji names (e.g., "snake").
- **Guessing Game**: Look at the number of emojis to guess the word length (e.g., 3 emojis = 3-letter word like CAT). Use the emoji map to decode manually if needed.
- **Encoding**: Use only letters A-Z for encoding to avoid errors. Spaces are preserved, but numbers or symbols will trigger a warning.
- **Have Fun**: Experiment with silly messages or challenge friends to decode your emoji sequences!

## Project Structure
- **`decode_emoji.py`**: The main Python script containing the decoder, encoder, and guessing game.
- No additional files are created, but you can save encoded/decoded messages manually if desired.

## Extending the Project
Want to make it even cooler? Try these ideas:
- **Multi-Word Decoding**: Allow decoding phrases with spaces (e.g., 🐍🍎🐝 🐶🐙🦒 → SAB DOG).
- **Save Messages**: Add an option to save decoded/encoded messages to a file (like the Story Generator from Day 47).
- **More Words**: Expand the guessing game’s word list or add difficulty levels (e.g., longer words).
- **Hints**: Provide hints in the guessing game (e.g., "This is an animal" for CAT).
- **Custom Emoji Map**: Let users define their own emoji-to-letter mappings.

## Contributing
This project is part of a daily Python coding streak, but you’re welcome to fork it, add features, or suggest improvements! Submit ideas or code via pull requests or share them with the community. Let’s make emoji coding even more fun! 😎

## License
This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and share it as per the license terms.

## Acknowledgments
- Built as part of a 49-day Python coding streak! 🐍
- Inspired by cryptic puzzles and the joy of emojis in coding.
- Thanks to the Python community for making learning fun and accessible.

---

Happy decoding, encoding, and guessing! If you have questions or want to tweak the script, just let me know. Ready for 