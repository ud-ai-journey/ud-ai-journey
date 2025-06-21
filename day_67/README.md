# MailMind - Email Summarizer & Action Extractor

**Day 67 Project: Portfolio-Ready Micro SaaS Tool**

## Overview
MailMind is a simple, robust Streamlit app that helps busy professionals quickly extract value from their email threads. Paste any email, and MailMind will:
- Summarize the main announcement or message
- Extract action items (if any)
- Analyze the tone (Polite, Assertive, Apologetic, Neutral)

## Features
- **No AI API keys or heavy models required**
- Fast, works offline (pure Python logic)
- Handles marketing, product update, and regular emails
- Clean, minimal UI

## How to Use
1. Run the app:
   ```bash
   streamlit run day_67/MailMind.py
   ```
2. Paste your email content into the text area.
3. Click **Analyze Email**.
4. View the summary, action items, and tone instantly.

## Example Output
```
Summary
Lovable is free for everyone over this weekend, starting now until Sunday 15th of June 23:59 CET! During this time, credits will not be deducted when making prompts. There might be rate limits during high demand, where paid users get prioritized access.

Action Items
No action items found

Tone
Assertive
```

## How it Works
- **Summarization:** Extracts the first 2-3 meaningful lines after a greeting or announcement, skipping headers/footers.
- **Action Extraction:** Uses regex to find tasks, requests, or deadlines.
- **Tone Analysis:** Simple keyword-based classifier.

## Author
Made with ❤️ by Uday Kumar - Day 67 Project

---
*This project is part of the 100 Days of Python-AI Journey.*
