# 📬 Email Tone Polisher

A smart command-line tool to detect the emotional tone of a raw email and automatically rewrite it into a professional, polished version using AI.

---

## 🔧 Features

- 🧠 Emotion detection using `roberta-base-go_emotions`
- ✍️ Polished email generation using `t5-base`
- 🎨 Interactive CLI with color-coded feedback
- 🔄 Option to rephrase in different tones like Friendly, Assertive, Polite, etc.
- ⚠️ Fallback generation for invalid model outputs

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `transformers`
- `colorama`

### Installation

```bash
git clone https://github.com/yourusername/email-tone-polisher.git
cd email-tone-polisher
pip install -r 

requirements.txt
```bash
transformers
colorama
---
▶️ Usage

```bash
python email_tone_polisher.py
Sample Flow:
Input your raw email (e.g., “Why haven’t you responded?”)

The script detects the emotional tone (e.g., Harsh)

It auto-generates a polished version.

Optionally, rephrase it in another tone.

🧠 Models Used
SamLowe/roberta-base-go_emotions for tone classification

t5-base for text-to-text generation

📎 Example Output
Detected Tone: Harsh (anger, confidence: 0.93)

Rewritten Email (Harsh):
Subject: Urgent Request

Dear [Recipient],

I noticed a delay in your response. Please provide an immediate update. Thank you.

Best regards,
[Your Name]
🙌 Acknowledgements
HuggingFace Transformers

Open-source models: SamLowe, T5 Authors