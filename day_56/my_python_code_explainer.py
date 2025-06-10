# Day 56: AI-Powered Code Explainer (Offline Version)
# Explains Python code in simple English using rule-based logic, with enhanced syntax error detection and CLI improvements

import textwrap
import re
import ast

def colored(text, color):
    """
    Add ANSI color codes to text for terminal output.
    Args:
        text (str): The text to color.
        color (str): The color to apply ('red', 'green', 'yellow', 'blue').
    Returns:
        str: The colored text.
    """
    codes = {'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m', 'blue': '\033[94m', 'reset': '\033[0m'}
    return f"{codes.get(color, '')}{text}{codes['reset']}"

def is_likely_python_code(code_snippet):
    """
    Check if the input resembles Python code by looking for common keywords.
    Args:
        code_snippet (str): The code to check.
    Returns:
        bool: True if the code contains Python keywords, False otherwise.
    """
    python_keywords = [
        "def", "class", "for", "while", "if", "elif", "else", "return",
        "print", "import", "try", "except", "raise", "with", "as"
    ]
    code_lower = code_snippet.lower()
    return any(keyword in code_lower for keyword in python_keywords)

def check_syntax_with_ast(code_snippet):
    """
    Check the syntax of the code using the ast module.
    Args:
        code_snippet (str): The code to check.
    Returns:
        tuple: (error_message, error_line) where error_message is a string or None,
               and error_line is the line number (0-based) or None.
    """
    try:
        ast.parse(code_snippet)
        return None, None
    except IndentationError as e:
        error_msg = f"Indentation error: {str(e)}. Check your spaces or tabs."
        error_line = getattr(e, 'lineno', None)
        return error_msg, (error_line - 1 if error_line is not None else None)
    except SyntaxError as e:
        error_msg = f"Syntax error: {str(e)}"
        error_line = getattr(e, 'lineno', None)
        return error_msg, (error_line - 1 if error_line is not None else None)
    except Exception as e:
        return f"Error parsing code: {str(e)}", None

def explain_code(code_snippet):
    """
    Generate simple English explanations for a Python code snippet using rule-based logic.
    Also suggests corrections for common syntax errors and uses ast for enhanced syntax checking.
    Args:
        code_snippet (str): The Python code to explain.
    Returns:
        list: A list of explanations for each line of code.
    """
    # Check if the input resembles Python code
    if not is_likely_python_code(code_snippet):
        return ["This doesn't look like valid Python code. Please enter actual Python code (e.g., 'def hello(): print(\"Hi\")')."] * code_snippet.count('\n')

    # Check syntax using ast
    syntax_error, error_line = check_syntax_with_ast(code_snippet)
    if syntax_error:
        lines = code_snippet.strip().split('\n')
        explanation = []
        for i, line in enumerate(lines):
            if error_line is not None and i == error_line:
                explanation.append(f"Error on this line: {syntax_error}")
            else:
                explanation.append("This line is part of code with a syntax error elsewhere.")
        return explanation

    lines = code_snippet.strip().split('\n')
    explanation = []

    for line in lines:
        # Check for indentation before stripping
        if line.startswith(("    ", "\t")):
            explanation.append("This is an indented block, likely part of a function, loop, or condition.")
            continue

        line_stripped = line.strip()
        if not line_stripped:  # Skip empty lines
            explanation.append("This is an empty line.")
            continue

        # Rule-based explanations for common Python constructs with correction suggestions
        if line_stripped.startswith("#"):
            explanation.append("This is a comment, ignored by Python.")
        elif line_stripped.startswith("def "):
            match = re.match(r"def\s+([a-zA-Z_]\w*)\s*\(([^()]*)\)\s*:", line_stripped)
            if match:
                func_name = match.group(1)
                params = match.group(2).strip()
                if params:
                    explanation.append(f"Defines a function '{func_name}' with parameter(s): {params}.")
                else:
                    explanation.append(f"Defines a function named '{func_name}' with no parameters.")
            else:
                if not "(" in line_stripped or not ")" in line_stripped:
                    explanation.append("Tries to define a function, but the syntax is incorrect (missing parentheses). Try: 'def name():'")
                elif not line_stripped.endswith(":"):
                    explanation.append("Tries to define a function, but the syntax is incorrect (missing colon at the end). Try: 'def name():'")
                else:
                    explanation.append("Tries to define a function, but the syntax is incorrect. A correct example is: 'def name():'")
        elif line_stripped.startswith("class "):
            match = re.match(r"class\s+([a-zA-Z_]\w*)\s*(?:\(|:)", line_stripped)
            if match:
                class_name = match.group(1)
                explanation.append(f"Defines a class named '{class_name}'.")
            else:
                explanation.append("Tries to define a class, but the syntax is incorrect. Try: 'class MyClass:'")
        elif line_stripped.startswith("for "):
            if " in " in line_stripped and line_stripped.endswith(":"):
                explanation.append("Starts a 'for' loop to iterate over a sequence.")
            else:
                explanation.append("Tries to start a 'for' loop, but the syntax is incorrect. Try: 'for item in range(5):'")
        elif line_stripped.startswith("while "):
            if line_stripped.endswith(":"):
                explanation.append("Starts a 'while' loop that runs as long as a condition is true.")
            else:
                explanation.append("Tries to start a 'while' loop, but the syntax is incorrect (missing colon). Try: 'while condition:'")
        elif "if " in line_stripped and not line_stripped.startswith("elif"):
            if line_stripped.endswith(":"):
                explanation.append("Checks a condition with an 'if' statement.")
            else:
                explanation.append("Tries to write an 'if' statement, but the syntax is incorrect (missing colon). Try: 'if condition:'")
        elif "elif " in line_stripped:
            if line_stripped.endswith(":"):
                explanation.append("Checks an alternative condition if the previous 'if' was false.")
            else:
                explanation.append("Tries to write an 'elif' statement, but the syntax is incorrect (missing colon). Try: 'elif condition:'")
        elif "else:" in line_stripped:
            explanation.append("Handles all other cases if the 'if' conditions are false.")
        elif line_stripped == "pass":
            explanation.append("Does nothing. It's a placeholder.")
        elif line_stripped == "continue":
            explanation.append("Skips to the next iteration of a loop.")
        elif line_stripped == "break":
            explanation.append("Exits the loop immediately.")
        elif "with " in line_stripped and " as " in line_stripped:
            if line_stripped.endswith(":"):
                explanation.append("Opens a resource (like a file) safely and assigns it to a variable.")
            else:
                explanation.append("Tries to use a 'with' statement, but the syntax is incorrect (missing colon). Try: 'with open(\"file.txt\") as f:'")
        elif "=" in line_stripped and "==" not in line_stripped and ">" not in line_stripped and "<" not in line_stripped:
            var_name = line_stripped.split("=")[0].strip()
            explanation.append(f"Assigns a value to the variable '{var_name}'.")
        elif "==" in line_stripped or ">" in line_stripped or "<" in line_stripped or "!=" in line_stripped:
            explanation.append("Compares values in a condition.")
        elif "return" in line_stripped:
            explanation.append("Returns a value from a function.")
        elif "print(" in line_stripped:
            if line_stripped.endswith(")"):
                explanation.append("Prints something to the console.")
            else:
                explanation.append("Tries to print something, but the syntax is incorrect (missing closing parenthesis). Try: 'print(\"text\")'")
        elif line_stripped.startswith("import "):
            module_name = line_stripped.split("import ")[1].split(" as ")[0]
            explanation.append(f"Imports the '{module_name}' module to use its features.")
        elif "try:" in line_stripped:
            explanation.append("Starts a 'try' block to handle potential errors.")
        elif "except" in line_stripped:
            explanation.append("Handles an error if the 'try' block fails.")
        else:
            if re.match(r"^[a-zA-Z_]\w*\s*\(", line_stripped):
                if line_stripped.endswith(")"):
                    explanation.append("Calls a function.")
                else:
                    explanation.append("Tries to call a function, but the syntax is incorrect (missing closing parenthesis). Try: 'function()'")
            elif re.match(r"^[a-zA-Z_]\w*$", line_stripped):
                explanation.append("This line might be a variable or an undefined operation, but it’s not clear without more context.")
            else:
                explanation.append("This line doesn’t match any common Python patterns and may be incorrect. Check your syntax.")

    return explanation

def get_user_code():
    """
    Get multiline code input from the user.
    Returns:
        str: The user's code snippet.
    """
    print("📥 Paste your Python code (end input with an empty line):")
    lines = []
    try:
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
    except KeyboardInterrupt:
        print("\n⚠️ Input interrupted. Using the code entered so far.")
        return "\n".join(lines)
    except EOFError:
        return "\n".join(lines)

    return "\n".join(lines)

def main():
    # Print welcome message
    print("🧠 AI-Powered Code Explainer (Offline Version) 🧠")
    print("Explains Python code in simple English and suggests fixes!")
    print("-" * 50)

    # Get user code
    user_code = get_user_code()
    if not user_code.strip():
        print("\n❌ No code provided! Please enter some Python code.")
        return

    # Generate explanations
    print("\n🔍 Explanation:\n")
    explanations = explain_code(user_code)
    code_lines = user_code.strip().split('\n')

    # Display line-by-line explanations with color
    for i, (line, note) in enumerate(zip(code_lines, explanations), 1):
        print(f"{i:02}. {colored(line.strip(), 'yellow')} ➜ {colored(note, 'green')}")

if __name__ == "__main__":
    main()