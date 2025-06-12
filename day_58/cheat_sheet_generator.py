# day_58/cheat_sheet_generator.py

print("📘 Python Cheat Sheet Generator")
print("-" * 40)

# Predefined cheat sheets
cheat_sheets = {
    "loops": """
🔁 Python Loops Cheat Sheet

1. For Loop
   Syntax:
   for item in iterable:
       # do something

   Example:
   for i in range(5):
       print(i)  # Outputs: 0, 1, 2, 3, 4

2. While Loop
   Syntax:
   while condition:
       # do something

   Example:
   count = 0
   while count < 5:
       print(count)
       count += 1  # Outputs: 0, 1, 2, 3, 4

⚠️ Pitfalls:
   - Avoid infinite loops by ensuring the condition will eventually be False.
   - Use 'break' to exit early, or 'continue' to skip to the next iteration.
""",
    "functions": """
🔧 Python Functions Cheat Sheet

1. Defining a Function
   Syntax:
   def function_name(parameters):
       # code block
       return value

   Example:
   def greet(name):
       return f"Hello, {name}"
   print(greet("Alice"))  # Outputs: Hello, Alice

2. Default Arguments
   Syntax:
   def function_name(param1, param2="default"):
       # code block

   Example:
   def greet(name="World"):
       print(f"Hello, {name}")
   greet()  # Outputs: Hello, World

⚠️ Pitfalls:
   - Define functions before calling them.
   - Avoid mutable default arguments (e.g., lists) to prevent unexpected behavior.
""",
    "dict": """
📦 Python Dictionary Cheat Sheet

1. Creating a Dictionary
   Syntax:
   my_dict = {"key1": value1, "key2": value2}

   Example:
   person = {"name": "Alice", "age": 30}

2. Accessing Values
   Syntax:
   my_dict["key"] or my_dict.get("key")

   Example:
   print(person["name"])  # Outputs: Alice
   print(person.get("age"))  # Outputs: 30

3. Looping Through Dictionary
   Syntax:
   for key, value in my_dict.items():
       # do something

   Example:
   for key, value in person.items():
       print(f"{key}: {value}")

4. Common Methods
   - .get(key): Safely access value
   - .keys(): Get all keys
   - .values(): Get all values
   - .update(other_dict): Merge dictionaries

⚠️ Pitfalls:
   - Keys must be immutable (e.g., strings, numbers, tuples).
   - Using [] on a non-existent key raises KeyError; use .get() to avoid this.
"""
}

# Main loop for user interaction
while True:
    topic = input("\n📥 Enter topic (or 'exit' to quit): ").strip().lower()
    if topic == "exit":
        print("👋 Goodbye! Keep coding.")
        break
    elif topic in cheat_sheets:
        print("\n📄 Cheat Sheet:")
        print(cheat_sheets[topic])
    else:
        print(f"\n❌ No cheat sheet for '{topic}'. Try: loops, functions, dict.")