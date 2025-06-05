# 📊 Day 51: Log Insight Extractor

A command-line Python tool that reads a `system.log` file, filters logs by date, analyzes log levels and messages, and generates a clean summary on both the terminal and a timestamped output file. Built as part of my 100 Days of Python + AI Challenge.

---

## ✨ Features

- ✅ Parses logs with format: `[LEVEL] YYYY-MM-DD HH:MM:SS - Message`
- 🧠 Extracts insights: counts of INFO, WARNING, ERROR, etc.
- 📅 Supports optional date filtering (start/end date)
- 📋 Displays top 3 most frequent log messages
- 💾 Saves a beautifully formatted summary to a text file
- 🤝 User-friendly CLI with emojis and error handling

---

## 📁 Example Log Format (`system.log`)

```

\[INFO] 2025-05-27 10:00:01 - System started
\[WARNING] 2025-05-27 10:02:00 - High memory usage
\[ERROR] 2025-05-27 10:05:33 - Database connection failed

````

---

## 🚀 How to Use

### 1. Clone or copy the script

```bash
git clone https://github.com/yourusername/ud-ai-journey.git
cd ud-ai-journey/day_51
````

### 2. Create a `system.log` file in the same folder (or replace the path in the script)

### 3. Run the tool

```bash
python log_insight_extractor.py
```

### 4. You’ll be prompted to:

* Filter logs by date (optional)
* View a summary
* Save the summary to a timestamped text file

---

## 📦 Sample Output (Terminal)

```
📊 === LOG SUMMARY === 📊
==============================

📈 Log Levels:
ℹ️ INFO: 8
⚠️ WARNING: 4
❌ ERROR: 2

📋 Top 3 Frequent Messages:
📌 System started (3 times)
📌 User logged in (2 times)
📌 Database connection failed (2 times)
```

---

## 💾 Sample Output File

Filename: `log_summary_2025-05-27_1740.txt`

Contents:

* Date range (if filtered)
* Log level counts with emojis
* Top 3 frequent messages
* Timestamp of generation

---

## 🛠 Customization Ideas

| Feature              | How                                              |
| -------------------- | ------------------------------------------------ |
| 📁 Multi-log support | Extend to read multiple `.log` files             |
| 🔍 Keyword filtering | Add message-level search                         |
| 📊 Charts            | Add bar chart output (e.g., with `matplotlib`)   |
| 🌐 Web UI            | Add a Flask interface to upload and analyze logs |

---

## 👨‍💻 Built With

* Python 3.x
* `datetime`, `collections.Counter`, `os`
* Pure CLI (no external dependencies)

---

## 🌈 Why This Project?

This is part of my **100-Day Python + AI Developer Challenge** to build practical, real-world tools. Logs are everywhere — from system debugging to ML ops monitoring — and learning how to extract insights from them is a valuable real-world dev skill.

---

## 📌 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 🙌 Follow My Journey

🔗 [GitHub Profile](https://github.com/ud-ai-journey)
📅 100 Days of Python + AI [Project Log](https://github.com/ud-ai-journey/ud-ai-journey)

---

