# MemoryVault.ai 🧠 - Day 93

A powerful AI-driven learning companion that helps you retain and review knowledge effectively.

## Features

- 📝 Log daily learnings with title, notes, and tags
- 🤖 AI-powered smart summaries using Groq (Llama3)
- 🎯 Auto-generated flashcards for effective review
- 📊 Spaced repetition system for optimal learning
- 📈 Progress dashboard with learning analytics
- 🎭 Mood tracking for emotional learning journey

## ✨ Why This Matters
- **Lifelong Learning**: Helps you truly remember and apply what you learn, not just consume it
- **Emotional Reflection**: Connects your mood and mindset to your learning journey
- **Productivity & Growth**: Turns scattered notes into actionable, reviewable knowledge
- **Confidence Building**: Spaced repetition and flashcards make you feel prepared for real-world challenges
- **Personal Knowledge Vault**: Your own second brain, ready for interviews, projects, and life

---

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file
   - Add your Groq API key: `GROQ_API_KEY=your_key_here`

## Running the App

```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `ai_helper.py`: AI integration with Groq (Llama3)
- `vault_manager.py`: Data management and persistence
- `spaced_repetition.py`: Spaced repetition algorithm
- `data/`: Directory for storing entries and flashcards

## Usage

1. **Add Entry**: Record what you've learned with notes and tags
2. **Review**: Practice with AI-generated flashcards
3. **Dashboard**: Track your learning progress and patterns

## Future Enhancements

- Export entries to Markdown/PDF
- Voice input for entries
- Integration with learning platforms
- Mobile app version
- Collaborative learning features

---

**Built with 🚀 for Day 93 of the 100 Days Python & AI Challenge – a day of memory, mastery, and unstoppable growth!**
