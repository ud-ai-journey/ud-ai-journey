# 📬 MailMind: Smart Email Analyzer

MailMind is an open-source Streamlit app that summarizes, extracts action items, and analyzes the tone of any email or email thread using state-of-the-art AI models.

## 🚀 Features
- **Summarize** long or short emails instantly
- **Extract action items** automatically
- **Analyze tone** (positive, negative, apologetic, urgent, etc.)
- **Upload .txt or .eml files** or paste email text
- **Copy results** with one click and get instant feedback
- **View analysis history** for your session
- **Beautiful, modern UI** with logo and interactive feedback

## 🛠️ Requirements
- Python 3.8+
- See `requirements.txt` for dependencies:
  - streamlit
  - transformers
  - torch

## 🖥️ How to Run Locally
1. Clone this repo or copy the `day_68` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run MailMindFinal.py
   ```
4. Open the local URL shown in your terminal (usually http://localhost:8501).

## 🌐 Deploy on Streamlit Cloud
1. Push this folder to a GitHub repo.
2. Connect your repo to [Streamlit Cloud](https://streamlit.io/cloud).
3. Deploy and share your public app URL!

## ✨ Usage
- **Paste** or **upload** your email or thread.
- Click **Analyze Email**.
- Copy/share the summary, actions, and tone.
- Optionally, view your analysis history.

## 📦 File Structure
```
MailMindFinal.py        # Main Streamlit app
requirements.txt        # Dependencies
README.md              # This file
```

## 🙏 Credits
- Built with [Streamlit](https://streamlit.io/) and [HuggingFace Transformers](https://huggingface.co/transformers/)
- By [Uday Kumar](https://github.com/ud-ai-journey)

## 📝 License
MIT License. See [LICENSE](../LICENSE) if available.
