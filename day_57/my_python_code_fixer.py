import textwrap
import re
import ast

def colored(text, color):
    codes = {'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m', 'blue': '\033[94m', 'reset': '\033[0m'}
    return f"{codes.get(color, '')}{text}{codes['reset']}"

class PythonCodeAutoFixer:
    def __init__(self, code):
        self.original_code = code
        self.fixed_code = ""
        self.fixed_lines = []

    def auto_fix(self):
        lines = self.original_code.split('\n')
        fixed_lines = []

        for idx, line in enumerate(lines):
            original_line = line
            fixed_line = line

            # Convert CamelCase and ALL_CAPS to snake_case first
            def camel_to_snake(match):
                word = match.group(0)
                if word.isupper():
                    return word.lower()
                return re.sub(r'(?<!^)(?=[A-Z])', '_', word).lower()

            words = re.findall(r'\b[A-Z][a-zA-Z0-9]*\b|\b[A-Z]+\b', fixed_line)
            for word in words:
                fixed_line = fixed_line.replace(word, camel_to_snake(re.match(r'\b[A-Z][a-zA-Z0-9]*\b|\b[A-Z]+\b', word)))

            # Fix spacing around '='
            fixed_line = re.sub(r'(?<![=!<>])=(?!=)', ' = ', fixed_line)

            # Fix incomplete function definitions (with or without trailing colon)
            def_match = re.match(r'^\s*(def)\s+([a-zA-Z_]\w*)\s*:?\s*$', fixed_line)
            if def_match:
                fixed_line = f"{def_match.group(1)} {def_match.group(2)}():"
                fixed_lines.append(fixed_line)
                fixed_lines.append("    pass")  # Add single pass statement
                self.fixed_lines.append(idx + 1)
                continue

            # Add missing colons (for other control structures, excluding def)
            if re.match(r'^\s*(if|for|while|elif|else|try|except|with)\b.*[^:]\s*$', fixed_line):
                fixed_line = fixed_line.rstrip() + ':'

            if fixed_line != original_line:
                self.fixed_lines.append(idx + 1)

            fixed_lines.append(fixed_line)

        self.fixed_code = '\n'.join(fixed_lines)

    def get_fixed_code(self):
        return self.fixed_code

    def get_fixed_lines(self):
        return self.fixed_lines

def is_likely_python_code(code_snippet):
    python_keywords = ["def", "class", "for", "while", "if", "elif", "else", "return", "print", "import", "try", "except", "raise", "with", "as"]
    code_lower = code_snippet.lower()
    return any(keyword in code_lower for keyword in python_keywords)

def check_syntax_with_ast(code_snippet):
    try:
        ast.parse(code_snippet)
        return None, None
    except IndentationError as e:
        return f"Indentation error: {str(e)}. Check your spaces or tabs.", getattr(e, 'lineno', None)
    except SyntaxError as e:
        return f"Syntax error: {str(e)}", getattr(e, 'lineno', None)
    except Exception as e:
        return f"Error parsing code: {str(e)}", None

def explain_code(code_snippet):
    if not code_snippet.strip():
        return ["No code provided to explain."]

    if not is_likely_python_code(code_snippet):
        return ["This doesn't look like valid Python code. Please enter actual Python code."] * code_snippet.count('\n')

    syntax_error, error_line = check_syntax_with_ast(code_snippet)
    lines = code_snippet.strip().split('\n')
    if syntax_error:
        return [f"Error on this line: {syntax_error}" if i + 1 == error_line else "This line is part of code with a syntax error elsewhere." for i in range(len(lines))]

    explanation = []
    for line in lines:
        line_stripped = line.strip()
        if line.startswith(("    ", "\t")):
            if line_stripped == "pass":
                explanation.append("A 'pass' statement, used as a placeholder for an empty block.")
            else:
                explanation.append("This is an indented block, likely part of a function, loop, or condition.")
            continue

        if not line_stripped:
            explanation.append("This is an empty line.")
        elif line_stripped.startswith("#"):
            explanation.append("This is a comment, ignored by Python.")
        elif line_stripped.startswith("def "):
            match = re.match(r"def\s+([a-zA-Z_]\w*)\s*\(([^()]*)\)\s*:", line_stripped)
            if match:
                func_name = match.group(1)
                params = match.group(2).strip()
                explanation.append(f"Defines a function '{func_name}' with parameter(s): {params if params else 'none'}.")
            else:
                explanation.append("Incorrect function syntax. Try: def name():")
        elif line_stripped.startswith("class "):
            match = re.match(r"class\s+([a-zA-Z_]\w*)\s*(?:\(|:)", line_stripped)
            if match:
                explanation.append(f"Defines a class named '{match.group(1)}'.")
            else:
                explanation.append("Incorrect class syntax. Try: class MyClass:")
        elif line_stripped.startswith("for ") and line_stripped.endswith(":"):
            explanation.append("Starts a 'for' loop to iterate over a sequence.")
        elif line_stripped.startswith("while ") and line_stripped.endswith(":"):
            explanation.append("Starts a 'while' loop that runs as long as a condition is true.")
        elif "if " in line_stripped and line_stripped.endswith(":"):
            explanation.append("Checks a condition with an 'if' statement.")
        elif "elif " in line_stripped and line_stripped.endswith(":"):
            explanation.append("Checks another condition if the previous ones were false.")
        elif line_stripped == "else:":
            explanation.append("Handles all other cases if previous conditions are false.")
        elif "try:" in line_stripped:
            explanation.append("Starts a 'try' block to handle potential errors.")
        elif "except" in line_stripped:
            explanation.append("Handles an error if the 'try' block fails.")
        elif "with " in line_stripped and " as " in line_stripped and line_stripped.endswith(":"):
            explanation.append("Opens a resource (like a file) safely and assigns it to a variable.")
        elif "print(" in line_stripped:
            explanation.append("Prints something to the console.")
        elif "return" in line_stripped:
            explanation.append("Returns a value from a function.")
        elif "=" in line_stripped and "==" not in line_stripped:
            var_name = line_stripped.split("=")[0].strip()
            explanation.append(f"Assigns a value to the variable '{var_name}'.")
        elif re.match(r"^[a-zA-Z_]\w*\s*\(.*\)$", line_stripped):
            explanation.append("Calls a function.")
        else:
            explanation.append("This line doesn’t match common Python patterns. Check your syntax.")

    return explanation

def get_user_code():
    print("📥 Paste your Python code (end input with an empty line):")
    lines = []
    try:
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
    except (KeyboardInterrupt, EOFError):
        print("\n⚠️ Input interrupted. Using the code entered so far.")
    return "\n".join(lines)

def main():
    print("🧠 AI-Powered Code Explainer with Auto-Fixer (Offline Version) 🧠")
    print("Fixes and explains Python code in simple English!")
    print("-" * 50)

    user_code = get_user_code()
    if not user_code.strip():
        print("\n❌ No code provided! Please run the script again with actual Python code.")
        return

    print("\n🔍 Auto-fixing code...\n")
    fixer = PythonCodeAutoFixer(user_code)
    fixer.auto_fix()
    fixed_code = fixer.get_fixed_code()

    print("✅ Fixed Code:")
    print("-" * 50)
    print(fixed_code)
    print("-" * 50)

    print("\n💡 Explaining your code:\n")
    explanations = explain_code(fixed_code)
    for i, (line, explanation) in enumerate(zip(fixed_code.split('\n'), explanations), start=1):
        print(f"{colored(f'{i:>3}: {line}', 'blue')}")
        print(f"     {colored('→ ' + explanation, 'green')}")

if __name__ == "__main__":
    main()