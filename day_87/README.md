# 📧 Email Auto-Reply AI Assistant - Day 87

Automatically replies to new Gmail messages using Google Gemini AI.

---

## 🚀 Features
- **Event-driven automation:** Checks for new, unread emails every minute and replies automatically.
- **AI-powered responses:** Uses Gemini 2.5 Pro to summarize and generate polite, helpful replies.
- **Robust error handling:** Handles newsletters, bounces, and quota errors gracefully.
- **Customizable prompt:** Easily adjust the reply style and filtering logic.

---

## 🛠️ Setup

### 1. Clone the repo and navigate to the project folder
```bash
cd day_87
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Google Cloud Setup
- Enable the Gmail API and Gemini API in your Google Cloud project.
- Download your `credentials.json` (OAuth 2.0 Client ID for Desktop) and place it in `day_87/`.

### 4. Set your Gemini API key
- Create a `.env` file in `day_87/` with:
  ```
  GOOGLE_API_KEY=your_gemini_api_key_here
  ```
- Or set it in your shell before running:
  ```powershell
  $env:GOOGLE_API_KEY="your_gemini_api_key_here"
  ```

### 5. Run the app
```bash
uvicorn app:app --reload
```
- On first run, authenticate with your Gmail account in the browser popup.

---

## ✉️ How It Works
- The app checks for new, unread emails in your inbox every 60 seconds.
- For each email:
  - Filters out images/captions and truncates long content.
  - Sends the content to Gemini for summarization and reply generation.
  - Sends the reply and marks the email as read.
- Handles newsletters, bounces, and quota errors gracefully.

---

## 🧠 Tips & Troubleshooting
- **Quota errors:** The free Gemini API tier has strict per-minute and per-day limits. Wait for reset or upgrade for more usage.
- **No reply for newsletters:** This is expected; Gemini is best for real, conversational emails.
- **Environment variable issues:** Use a `.env` file or set `GOOGLE_API_KEY` in your shell before running.
- **FileNotFoundError:** Ensure `credentials.json` is in the same directory as `app.py`.
- **Run from the correct directory:**
  - From inside `day_87`: `uvicorn app:app --reload`
  - From project root: `uvicorn day_87.app:app --reload`

---

## 🏆 Credits
Built by Uday as part of the 100 Days of Python & AI Challenge.

---

**Happy automating!** 