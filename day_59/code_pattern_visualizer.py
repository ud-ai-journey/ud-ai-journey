# day_59/code_pattern_visualizer.py

print("🧠 Python Code Pattern Visualizer")
print("-" * 40)

# Dictionary of patterns: {name: (code, explanation, demo_code)}
patterns = {
    "swap": (
        "a, b = b, a",
        """
💡 Swap Two Variables Without Temp
- Uses Python's multiple assignment to swap values in one line.
- No need for a temporary variable like in other languages.
- Works with any data types (int, str, etc.).
        """,
        """
a, b = 5, 10
print(f"Before: a={a}, b={b}")
a, b = b, a
print(f"After: a={a}, b={b}")
        """
    ),
    "listcomp": (
        "[f(x) for x in iterable if condition]",
        """
💡 List Comprehension vs. For Loop
- Concise way to create lists based on iterables.
- Faster and more Pythonic than equivalent for loops.
- Syntax: [expression for item in iterable if condition].
        """,
        """
# List comprehension
squares = [x**2 for x in range(5) if x % 2 == 0]
print(f"List comprehension: {squares}")

# Equivalent for loop
squares_loop = []
for x in range(5):
    if x % 2 == 0:
        squares_loop.append(x**2)
print(f"For loop: {squares_loop}")
        """
    ),
    "dictcomp": (
        "{key: value for item in iterable}",
        """
💡 Dictionary Comprehension
- Creates dictionaries in a single line.
- Similar to list comprehension but produces key-value pairs.
- Useful for transforming or filtering data into a dict.
        """,
        """
names = ['Alice', 'Bob', 'Charlie']
name_lengths = {name: len(name) for name in names}
print(f"Dictionary comprehension: {name_lengths}")
        """
    ),
    "set": (
        "set(my_list)",
        """
💡 Set from List to Remove Duplicates
- Converts a list to a set to eliminate duplicate elements.
- Sets only store unique values (unordered).
- Fast for checking membership and removing duplicates.
        """,
        """
my_list = [1, 2, 2, 3, 3, 4]
unique = set(my_list)
print(f"List: {my_list}")
print(f"Set (duplicates removed): {unique}")
        """
    ),
    "mostfreq": (
        "max(set(lst), key=lst.count)",
        """
💡 Find Most Frequent Element
- Uses max() with a key function to find the element with highest count.
- set(lst) ensures unique elements; lst.count() counts occurrences.
- Simple and efficient for small to medium lists.
        """,
        """
numbers = [1, 2, 2, 3, 3, 3, 4]
most_frequent = max(set(numbers), key=numbers.count)
print(f"List: {numbers}")
print(f"Most frequent element: {most_frequent}")
        """
    ),
    "reverse": (
        "string[::-1]",
        """
💡 Reverse a String Using Slicing
- Uses Python's slice notation [start:end:step] with step=-1.
- Concise and readable compared to loops or reversed().
- Works for any sequence (str, list, tuple).
        """,
        """
text = "Python"
reversed_text = text[::-1]
print(f"Original: {text}")
print(f"Reversed: {reversed_text}")
        """
    ),
    "palindrome": (
        "string == string[::-1]",
        """
💡 Check if a String is a Palindrome
- Compares a string with its reverse using slicing.
- Case-sensitive and includes spaces/punctuation by default.
- Simple one-liner for basic palindrome checks.
        """,
        """
word = "radar"
is_palindrome = word == word[::-1]
print(f"Word: {word}")
print(f"Is palindrome? {is_palindrome}")

word = "python"
is_palindrome = word == word[::-1]
print(f"Word: {word}")
print(f"Is palindrome? {is_palindrome}")
        """
    )
}

# Main loop for user interaction
while True:
    print("\n📋 Available patterns: swap, listcomp, dictcomp, set, mostfreq, reverse, palindrome, all")
    choice = input("📥 Enter pattern (or 'exit' to quit): ").strip().lower()
    
    if choice == "exit":
        print("👋 Goodbye! Keep coding.")
        break
    elif choice == "all":
        print("\n📄 All Patterns:")
        print("-" * 40)
        for name, (code, explanation, demo) in patterns.items():
            print(f"\n🔍 Pattern: {name}")
            print("\n📝 Code:")
            print(code)
            print("\n📚 Explanation:")
            print(explanation.strip())
            print("\n🚀 Demo Output:")
            try:
                exec(demo, {})
            except Exception as e:
                print(f"Error in demo: {e}")
            print("-" * 40)
    elif choice in patterns:
        code, explanation, demo = patterns[choice]
        print(f"\n📄 Pattern: {choice}")
        print("\n📝 Code:")
        print(code)
        print("\n📚 Explanation:")
        print(explanation.strip())
        print("\n🚀 Demo Output:")
        try:
            exec(demo, {})
        except Exception as e:
            print(f"Error in demo: {e}")
    else:
        print(f"\n❌ Invalid pattern '{choice}'. Try: swap, listcomp, dictcomp, set, mostfreq, reverse, palindrome, all")