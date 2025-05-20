# EmpathyMail – Day 35 of 100 Days of Python + AI

**Emotion-Aware Email Drafting Assistant**

---

## 🔍 Overview

**EmpathyMail** is a Command Line Interface (CLI) tool that transforms negative or confrontational email drafts into polished, professional, and empathetic communication. Using sentiment analysis, it detects negative tones, suggests constructive rewrites, and polishes user modifications to ensure emails foster collaboration and understanding.

> A step toward emotionally intelligent AI assistants, aligning with the *Empathy Engine* vision.

---

## 🎯 Features

* ✉️ **Interactive email draft input** with tone selection (Casual, Professional, Empathetic)
* 💬 **Sentiment analysis** using Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`)
* ✅ **Negative tone prevention** with warnings to avoid confrontational sentences
* 📝 **Context-aware rewrite suggestions** based on triggers (e.g., "where is", "serious", "man")
* 🧹 **Grammar and style polishing** for user-modified sentences (e.g., fixes capitalization, "on the team’s")
* 📊 **Colored CLI feedback** with sentiment scores and polished outputs
* 💾 **CSV logging** of timestamp, original sentence, sentiment, score, suggestion, and user choice
* 📄 **Draft saving** to `empathy_draft.txt` for final email output

---

## 🧠 Concepts Practiced

* Transformers & NLP with Hugging Face `pipeline`
* Sentence tokenization using NLTK (`sent_tokenize`)
* Regular expressions for preprocessing and grammar polishing
* Real-time sentiment validation and user interaction
* File handling for draft saving and structured CSV logging
* Emotional design for professional communication
* CLI user experience with `colorama` for colored feedback

---

## 🚀 How to Run

1. **Install dependencies** (use a virtual environment or project folder):

   ```bash
   pip install transformers colorama nltk
   ```

2. **Run the script**:

   ```powershell
   $env:TF_ENABLE_ONEDNN_OPTS=0; python empathymail.py
   ```

   * Note: The `$env:TF_ENABLE_ONEDNN_OPTS=0` suppresses TensorFlow `oneDNN` warnings. Alternatively, set it globally in Windows Environment Variables.

3. **Use the tool**:

   * Select a tone (1: Casual, 2: Professional, 3: Empathetic).
   * Enter your email draft, ending with `---END---`.
   * Review sentiment analysis, accept/modify suggestions, or keep original sentences (with warnings for negative tones).
   * The final draft is saved to `empathy_draft.txt`, and interactions are logged to `empathy_draft_log.csv`.

---

## 📁 Sample Output

**Input Draft**:
```
Dear team,
IAM SERIOS, WHERE IS THE PROGRESS MAN?
---END---
```

**CLI Interaction**:
```
EmpathyMail: Start
Select tone: 1. Casual, 2. Professional, 3. Empathetic
Enter 1, 2, or 3: 2

Selected tone: Professional
Enter your email draft (type ---END--- to finish):
Dear team,
IAM SERIOS, WHERE IS THE PROGRESS MAN?
---END---

🧠 Analyzing Draft...

Original: Dear team.
Sentiment: NEUTRAL (0.50)
Original: IAM SERIOS.
Sentiment: NEGATIVE (0.84)
Suggestion: I propose we address this: I’m concerned about our progress—can we review updates together?
Choose an option:
1. Accept suggestion
2. Modify suggestion
3. Keep original
Enter 1, 2, or 3: 2
Enter your modified sentence: I WOULD LIKE TO DISCUSS ON THE TEAM'S PROGRESS.COULD WE CONNECT ONCE?
Modified Sentiment: POSITIVE (0.88)
Polished Version: I would like to discuss the team’s progress. Could we connect once?
Original: WHERE IS THE PROGRESS MAN?
Sentiment: NEGATIVE (1.00)
Suggestion: I propose we address this: I’m eager for immediate updates—can we discuss our team’s progress urgently?
Choose an option:
1. Accept suggestion
2. Modify suggestion
3. Keep original
Enter 1, 2, or 3: 1

✅ Final Draft:
Dear team. I would like to discuss the team’s progress. Could we connect once? I propose we address this: I’m eager for immediate updates—can we discuss our team’s progress urgently?

Saved to empathy_draft.txt. Draft history logged in empathy_draft_log.csv.
```

**Log Output** (`empathy_draft_log.csv`):
```csv
Timestamp,Original Sentence,Sentiment,Score,Suggested Rewrite,Accepted
2025-05-20 18:40:02,Dear team.,NEUTRAL,0.50,N/A,N/A
2025-05-20 18:40:02,IAM SERIOS.,NEGATIVE,0.84,I propose we address this: I’m concerned about our progress—can we review updates together?,Modified (Sentiment: POSITIVE, Score: 0.88)
2025-05-20 18:40:02,WHERE IS THE PROGRESS MAN?,NEGATIVE,1.00,I propose we address this: I’m eager for immediate updates—can we discuss our team’s progress urgently?,Accepted
```

---

## 📈 Sentiment Feedback Example

```
Original: IAM SERIOS.
Sentiment: NEGATIVE (0.84)
Suggestion: I propose we address this: I’m concerned about our progress—can we review updates together?
Modified: I WOULD LIKE TO DISCUSS ON THE TEAM'S PROGRESS.COULD WE CONNECT ONCE?
Modified Sentiment: POSITIVE (0.88)
Polished Version: I would like to discuss the team’s progress. Could we connect once?
```

---

## 🧩 Potential Improvements

* **Advanced Grammar Checking**: Integrate `language-tool-python` for deeper grammar and style corrections.
* **Generative Rewrites**: Use `facebook/bart-large` or an OpenAI API for more natural, dynamic suggestions.
* **Sentiment Trend Visualization**: Generate bar charts of sentiment scores using `chartjs` or `matplotlib`.
* **Real-Time Feedback**: Adapt the `keyboard` module from `EmotionLens` (Day 33) for live sentiment analysis.
* **GUI Interface**: Build a Tkinter or web-based React UI for easier interaction.
* **Multi-Paragraph Support**: Enhance tokenization to handle complex email structures.

---

## 🙌 Why It Matters

**EmpathyMail** is more than a coding exercise—it’s a tool that promotes **emotional intelligence** in professional communication. By detecting negative tones and guiding users toward constructive, empathetic emails, it bridges the gap between human intent and AI-assisted clarity.

Perfect for exploring:
* Human-AI collaboration in workplace communication
* Digital tools for emotional intelligence
* Building blocks for the larger **Empathy Engine** project

---

## 📆 Progress

🗓️ **Day 35 / 100** of my #100DaysOfPythonAI
🔗 Follow my journey and daily builds!

---