# 📬 Email Tone Polisher

A smart command-line tool that detects the emotional tone of a raw email and automatically rewrites it into a professional, polished version using AI.

---

## 🔧 Features
- 🧠 **Emotion detection** using `roberta-base-go_emotions`  
- ✍️ **Polished email generation** using `t5-base`  
- 🎨 **Interactive CLI** with color-coded feedback for better user experience  
- 🔄 **Tone customization** including options like Friendly, Assertive, Polite, etc.  
- ⚠️ **Fallback generation** to handle invalid or unexpected model outputs  

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher  
- `transformers` library  
- `colorama` library  

### Installation
```bash
git clone https://github.com/yourusername/email-tone-polisher.git
cd email-tone-polisher
pip install -r requirements.txt
```

*(Ensure your `requirements.txt` includes:)*

```plaintext
transformers
colorama
```

---

## ▶️ Usage

```bash
python email_tone_polisher.py
```

### Sample Flow:
1. Input your raw email (e.g., *“Why haven’t you responded?”*)  
2. The script detects the emotional tone (e.g., *Harsh*)  
3. It automatically generates a polished, professional version of the email  
4. Optionally, rephrase the email in another tone (e.g., Friendly, Assertive, Polite)  

---

## 🧠 Models Used
- **Tone Classification:** `SamLowe/roberta-base-go_emotions`  
- **Text Generation:** `t5-base`  

---

## 📎 Example Output

```
Detected Tone: Harsh (anger, confidence: 0.93)

Rewritten Email (Harsh):
Subject: Urgent Request

Dear [Recipient],

I noticed a delay in your response. Please provide an immediate update. Thank you.

Best regards,  
[Your Name]
```

---

## 🙌 Acknowledgements
- Hugging Face Transformers library  
- Open-source models by SamLowe, T5 Authors  