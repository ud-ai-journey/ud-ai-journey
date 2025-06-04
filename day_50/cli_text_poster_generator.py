import shutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ASCII art definitions using 'X' as a placeholder for the fill character
art = {
    'A': [
        "  X  ",
        " X X ",
        "XXXXX",
        "X   X",
        "X   X"
    ],
    'B': [
        "XXXX ",
        "X   X",
        "XXXX ",
        "X   X",
        "XXXX "
    ],
    'C': [
        " XXX ",
        "X    ",
        "X    ",
        "X    ",
        " XXX "
    ],
    'D': [
        "XXXX ",
        "X   X",
        "X   X",
        "X   X",
        "XXXX "
    ],
    'E': [
        "XXXXX",
        "X    ",
        "XXXX ",
        "X    ",
        "XXXXX"
    ],
    'F': [
        "XXXXX",
        "X    ",
        "XXXX ",
        "X    ",
        "X    "
    ],
    'G': [
        " XXX ",
        "X    ",
        "X  XX",
        "X   X",
        " XXX "
    ],
    'H': [
        "X   X",
        "X   X",
        "XXXXX",
        "X   X",
        "X   X"
    ],
    'I': [
        "XXXXX",
        "  X  ",
        "  X  ",
        "  X  ",
        "XXXXX"
    ],
    'J': [
        "XXXXX",
        "    X",
        "    X",
        "X   X",
        " XXX "
    ],
    'K': [
        "X   X",
        "X  X ",
        "XXX  ",
        "X  X ",
        "X   X"
    ],
    'L': [
        "X    ",
        "X    ",
        "X    ",
        "X    ",
        "XXXXX"
    ],
    'M': [
        "X   X",
        "XX XX",
        "X X X",
        "X   X",
        "X   X"
    ],
    'N': [
        "X   X",
        "XX  X",
        "X X X",
        "X  XX",
        "X   X"
    ],
    'O': [
        " XXX ",
        "X   X",
        "X   X",
        "X   X",
        " XXX "
    ],
    'P': [
        "XXXX ",
        "X   X",
        "XXXX ",
        "X    ",
        "X    "
    ],
    'Q': [
        " XXX ",
        "X   X",
        "X X X",
        "X  X ",
        " XX X"
    ],
    'R': [
        "XXXX ",
        "X   X",
        "XXXX ",
        "X  X ",
        "X   X"
    ],
    'S': [
        " XXX ",
        "X    ",
        " XXX ",
        "    X",
        " XXX "
    ],
    'T': [
        "XXXXX",
        "  X  ",
        "  X  ",
        "  X  ",
        "  X  "
    ],
    'U': [
        "X   X",
        "X   X",
        "X   X",
        "X   X",
        " XXX "
    ],
    'V': [
        "X   X",
        "X   X",
        "X   X",
        " X X ",
        "  X  "
    ],
    'W': [
        "X   X",
        "X   X",
        "X X X",
        "XX XX",
        "X   X"
    ],
    'X': [
        "X   X",
        " X X ",
        "  X  ",
        " X X ",
        "X   X"
    ],
    'Y': [
        "X   X",
        "X   X",
        " X X ",
        "  X  ",
        "  X  "
    ],
    'Z': [
        "XXXXX",
        "   X ",
        "  X  ",
        " X   ",
        "XXXXX"
    ],
    '0': [
        " XXX ",
        "X  X ",
        "X X X",
        "X  X ",
        " XXX "
    ],
    '1': [
        "  X  ",
        " XX  ",
        "  X  ",
        "  X  ",
        " XXX "
    ],
    '2': [
        " XXX ",
        "X   X",
        "  XX ",
        " X   ",
        "XXXXX"
    ],
    '3': [
        " XXX ",
        "X   X",
        "  XX ",
        "X   X",
        " XXX "
    ],
    '4': [
        "X   X",
        "X   X",
        "XXXXX",
        "    X",
        "    X"
    ],
    '5': [
        "XXXXX",
        "X    ",
        "XXXX ",
        "    X",
        "XXXX "
    ],
    '6': [
        " XXX ",
        "X    ",
        "XXXX ",
        "X   X",
        " XXX "
    ],
    '7': [
        "XXXXX",
        "    X",
        "   X ",
        "  X  ",
        " X   "
    ],
    '8': [
        " XXX ",
        "X   X",
        " XXX ",
        "X   X",
        " XXX "
    ],
    '9': [
        " XXX ",
        "X   X",
        " XXXX",
        "    X",
        " XXX "
    ],
    ' ': [
        "     ",
        "     ",
        "     ",
        "     ",
        "     "
    ],
    '!': [
        "  X  ",
        "  X  ",
        "  X  ",
        "     ",
        "  X  "
    ],
    '?': [
        " XXX ",
        "X   X",
        "  XX ",
        "     ",
        "  X  "
    ],
    '.': [
        "     ",
        "     ",
        "     ",
        "     ",
        "  X  "
    ]
}

# Default art for undefined characters
default_art = [
    "XXXXX",
    "X   X",
    "X   X",
    "X   X",
    "XXXXX"
]

def get_art(char, fill_char):
    """
    Retrieve the ASCII art for a character and replace 'X' with the fill character.
    If the character is not defined, use the default art.
    """
    if char in art:
        return [line.replace('X', fill_char) for line in art[char]]
    else:
        return [line.replace('X', fill_char) for line in default_art]

def generate_ascii_art(text, fill_char):
    """
    Generate ASCII art for the input text using the specified fill character.
    Supports multiple lines by splitting the text by '\n'.
    """
    lines = text.split('\n')
    all_lines = []
    for line in lines:
        arts = [get_art(char, fill_char) for char in line.upper()]
        for i in range(5):  # Fixed 5-line height for each character
            combined_line = " ".join(art[i] for art in arts)
            all_lines.append(combined_line)
        all_lines.append("")  # Add a blank line between input lines
    return all_lines[:-1]  # Remove the last blank line

def display_art(lines, frame_style, color):
    """
    Display the ASCII art with the specified frame style and color.
    """
    terminal_width = shutil.get_terminal_size().columns
    max_line_length = max(len(line) for line in lines)
    
    if frame_style == "basic":
        frame_top = "=" * (max_line_length + 4)
        frame_bottom = "=" * (max_line_length + 4)
        print(color + frame_top + Style.RESET_ALL)
        for line in lines:
            framed_line = f"| {line.ljust(max_line_length)} |"
            print(color + framed_line.center(terminal_width) + Style.RESET_ALL)
        print(color + frame_bottom.center(terminal_width) + Style.RESET_ALL)
    elif frame_style == "double":
        frame_top = "═" * (max_line_length + 4)
        frame_bottom = "═" * (max_line_length + 4)
        print(color + frame_top + Style.RESET_ALL)
        for line in lines:
            framed_line = f"║ {line.ljust(max_line_length)} ║"
            print(color + framed_line.center(terminal_width) + Style.RESET_ALL)
        print(color + frame_bottom.center(terminal_width) + Style.RESET_ALL)
    else:
        for line in lines:
            print(color + line.center(terminal_width) + Style.RESET_ALL)
def save_to_file(lines, frame_style):
    max_line_length = max(len(line) for line in lines)
    if frame_style == "none":
        frame_top = ""
        frame_bottom = ""
        frame_left = ""
        frame_right = ""
    elif frame_style == "basic":
        frame_top = "=" * (max_line_length + 4)
        frame_bottom = "=" * (max_line_length + 4)
        frame_left = "= "
        frame_right = " ="
    elif frame_style == "double":
        frame_top = "═" * (max_line_length + 4)
        frame_bottom = "═" * (max_line_length + 4)
        frame_left = "║ "
        frame_right = " ║"

    with open("portrait.txt", "w", encoding="utf-8") as f:
        if frame_style != "none":
            f.write(frame_top + "\n")
        for line in lines:
            f.write(f"{frame_left}{line}{frame_right}\n")
        if frame_style != "none":
            f.write(frame_bottom + "\n")

def display_menu():
    print("\n=== Text Poster Generator ===")
    print("1. Create new poster")
    print("2. Change fill character")
    print("3. Choose frame style")
    print("4. Choose color")
    print("5. Save design")
    print("6. Exit")

def main():
    fill_char = '*'
    frame_style = "none"
    color = Fore.WHITE
    lines = []
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            try:
                text = input("Enter text to render (use \\n for new lines): ")
                lines = generate_ascii_art(text, fill_char)
                display_art(lines, frame_style, color)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "2":
            fill_char = input("Enter fill character (e.g., *, #, ❤️): ").strip() or fill_char
            print(f"Fill character set to '{fill_char}'")
            if 'lines' in locals():
                display_art(lines, frame_style, color)
        elif choice == "3":
            print("Frame styles:\n1. None\n2. Basic (e.g., ============)\n3. Double (e.g., ════════════)")
            frame_choice = input("Choose frame style (1-3): ").strip()
            if frame_choice == "1":
                frame_style = "none"
            elif frame_choice == "2":
                frame_style = "basic"
            elif frame_choice == "3":
                frame_style = "double"
            else:
                print("Invalid choice, defaulting to 'none'")
                frame_style = "none"
            if 'lines' in locals():
                display_art(lines, frame_style, color)
        elif choice == "4":
            print("Colors: 1. White, 2. Red, 3. Green, 4. Blue, 5. Yellow")
            color_choice = input("Choose color (1-5): ").strip()
            if color_choice == "1":
                color = Fore.WHITE
            elif color_choice == "2":
                color = Fore.RED
            elif color_choice == "3":
                color = Fore.GREEN
            elif color_choice == "4":
                color = Fore.BLUE
            elif color_choice == "5":
                color = Fore.YELLOW
            else:
                print("Invalid choice, defaulting to white")
                color = Fore.WHITE
            if 'lines' in locals():
                display_art(lines, frame_style, color)
        elif choice == "5":
            if 'lines' in locals():
                save_to_file(lines, frame_style)
            else:
                print("No design to save. Create a poster first!")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()