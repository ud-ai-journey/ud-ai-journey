# Day 51: Log Insight Extractor
# Analyzes a system.log file, extracts insights, and saves a summary.

from collections import Counter
from datetime import datetime
import os

def read_log_file(filename):
    """
    Read the content of the log file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def parse_log_line(line):
    """
    Parse a log line to extract level, timestamp, and message.
    Returns (level, timestamp, message) or None if parsing fails.
    """
    try:
        if "]" not in line or " - " not in line:
            return None
        level = line.split("]")[0][1:].strip()  # e.g., INFO, WARNING, ERROR
        timestamp_str = line.split("]")[1].split(" - ")[0].strip()  # e.g., 2025-05-27 10:00:01
        message = line.split(" - ")[-1].strip()  # e.g., System started
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return level, timestamp, message
    except (IndexError, ValueError):
        return None

def filter_by_date(log_lines, start_date=None, end_date=None):
    """
    Filter log lines by date range.
    start_date and end_date should be in format 'YYYY-MM-DD'.
    """
    filtered_lines = []
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            _, timestamp, _ = parsed
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                if timestamp.date() < start.date():
                    continue
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if timestamp.date() > end.date():
                    continue
            filtered_lines.append(line)
    return filtered_lines

def analyze_logs(log_lines):
    """
    Analyze log lines to count levels and messages.
    """
    levels = Counter()
    messages = Counter()

    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            level, _, message = parsed
            levels[level] += 1
            messages[message] += 1

    return levels, messages

def display_summary(levels, messages):
    """
    Display the log summary in the terminal with emojis.
    """
    print("\n📊 === LOG SUMMARY === 📊")
    print("=" * 30)
    print("\n📈 Log Levels:")
    for level, count in levels.items():
        emoji = "ℹ️" if level == "INFO" else "⚠️" if level == "WARNING" else "❌" if level == "ERROR" else "📝"
        print(f"{emoji} {level}: {count}")

    print("\n📋 Top 3 Frequent Messages:")
    for msg, count in messages.most_common(3):
        print(f"📌 {msg} ({count} time{'s' if count != 1 else ''})")

def save_summary_to_file(levels, messages, start_date=None, end_date=None):
    """
    Save the log summary to a file with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_filename = f"log_summary_{timestamp}.txt"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("📊 === LOG SUMMARY === 📊\n")
            file.write("=" * 30 + "\n\n")
            if start_date or end_date:
                date_range = f"Date Range: {start_date or 'Beginning'} to {end_date or 'End'}\n"
                file.write(date_range)
            file.write("\n📈 Log Levels:\n")
            for level, count in levels.items():
                emoji = "ℹ️" if level == "INFO" else "⚠️" if level == "WARNING" else "❌" if level == "ERROR" else "📝"
                file.write(f"{emoji} {level}: {count}\n")
            file.write("\n📋 Top 3 Frequent Messages:\n")
            for msg, count in messages.most_common(3):
                file.write(f"📌 {msg} ({count} time{'s' if count != 1 else ''})\n")
            file.write(f"\n📅 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        return output_filename
    except Exception as e:
        print(f"❌ Error saving summary: {e}")
        return None

def main():
    print("✨📊 Day 51: Log Insight Extractor 📊✨")
    print("Extract insights from your system.log file! Type 'exit' to quit.")

    while True:
        # Check if system.log exists
        filename = r"C:\Users\uday kumar\Python-AI\ud-ai-journey\day_51\system.log"

        if not os.path.exists(filename):
            print(f"❌ Error: '{filename}' not found. Please create a system.log file.")
            break

        # Ask for date range filter
        use_filter = input("\n🔎 Filter by date range? (y/n): ").strip().lower()
        start_date = None
        end_date = None
        if use_filter == 'y':
            start_date = input("📅 Enter start date (YYYY-MM-DD, or press Enter for beginning): ").strip()
            if not start_date:
                start_date = None
            else:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                except ValueError:
                    print("⚠️ Invalid date format! Using all logs.")
                    start_date = None
            end_date = input("📅 Enter end date (YYYY-MM-DD, or press Enter for end): ").strip()
            if not end_date:
                end_date = None
            else:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                except ValueError:
                    print("⚠️ Invalid date format! Using all logs.")
                    end_date = None

        # Read and filter logs
        log_lines = read_log_file(filename)
        if log_lines is None:
            break

        if start_date or end_date:
            log_lines = filter_by_date(log_lines, start_date, end_date)

        if not log_lines:
            print("⚠️ No log entries found for the selected date range.")
            continue_choice = input("\n🔄 Try again? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("👋🌈 Goodbye!")
                break
            continue

        # Analyze logs
        levels, messages = analyze_logs(log_lines)

        # Display and save summary
        display_summary(levels, messages)
        output_file = save_summary_to_file(levels, messages, start_date, end_date)
        if output_file:
            print(f"\n💾 Saved to: {output_file}")

        # Ask if user wants to analyze again
        again = input("\n🔄 Analyze again with different filters? (y/n): ").strip().lower()
        if again != 'y':
            print("👋🌈 Goodbye!")
            break

if __name__ == "__main__":
    main()