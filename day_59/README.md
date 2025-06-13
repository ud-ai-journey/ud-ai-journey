# 🧠 Python Code Pattern Visualizer (Day 59)

An interactive CLI-based Python tool that showcases popular coding patterns with explanations and real-time demo outputs. Perfect for beginners, interview prep, or brushing up on Python tricks!

---

## 🚀 Features

- ✅ Displays commonly used Python code patterns
- 📘 Provides simple explanations for each pattern
- 🧪 Runs demo code snippets live and shows output
- 🔁 Choose a specific pattern or explore all at once

---

## 📋 Supported Patterns

| Pattern      | Description                                      |
|--------------|--------------------------------------------------|
| `swap`       | Swap variables in one line (no temp variable)    |
| `listcomp`   | List comprehension with condition                |
| `dictcomp`   | Dictionary comprehension                         |
| `set`        | Remove duplicates from a list using `set()`      |
| `mostfreq`   | Find the most frequent item in a list            |
| `reverse`    | Reverse a string using slicing                   |
| `palindrome` | Check if a string is a palindrome                |

---

## 🧑‍💻 How to Use

1. Run the script:
   ```bash
   python day_59/code_pattern_visualizer.py
````

2. Choose a pattern from the prompt:

   * Type `swap`, `listcomp`, `dictcomp`, etc.
   * Or type `all` to view everything at once
   * Type `exit` to quit

---

## 📷 Sample Output

```
📋 Available patterns: swap, listcomp, dictcomp, set, mostfreq, reverse, palindrome, all
📥 Enter pattern (or 'exit' to quit): swap

📄 Pattern: swap

📝 Code:
a, b = b, a

📚 Explanation:
Swap Two Variables Without Temp
- Uses Python's multiple assignment to swap values in one line.
...

🚀 Demo Output:
Before: a=5, b=10
After: a=10, b=5
```

---

## 📎 Use Cases

* 📖 Quick revision for Python learners
* 🎓 Preparing for coding interviews
* 🔍 Understanding and visualizing idiomatic code

---

## 📁 File Structure

```
day_59/
└── code_pattern_visualizer.py   # Main script
```

---

## ❤️ Credits

Built with curiosity and love for clean, Pythonic code patterns!

