# 🚶 WalkPal - AI-Powered Walking Companion

WalkPal is an intelligent walking companion that generates personalized, engaging content based on your mood and walk duration. Built with Python and local AI, it offers both text and audio output for a hands-free walking experience.

## ✨ Features

- **Mood-Based Content**: Choose from various moods (Learn, Reflect, Story, Humor, Surprise) or enter a custom topic
- **AI-Powered**: Generates unique content for every walk using local LLM (Phi-3 Mini via Ollama)
- **Audio Support**: Listen to content hands-free with system TTS (pyttsx3)
- **Personalized Experience**: Learns from your preferences and feedback
- **Data Privacy**: Everything runs locally on your machine
- **No Internet Required**: Works completely offline after initial setup

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **AI Model**: Ollama (Local LLM runner) + Phi-3 Mini
- **Text-to-Speech**: `pyttsx3` (Offline, System TTS)
- **Data Storage**: JSON files (Local)
- **Environment Management**: `python-dotenv`
- **Core Libraries**: `json`, `os`, `sys`, `datetime`, `collections`, `math`

## 🚀 Development Journey

### Phase 1: Basic CLI Foundation
**Goal**: Establish core user interaction loop  
**Key Components**:
- Simple command-line interface
- Basic mood and duration selection
- Hardcoded content responses

**Challenges & Solutions**:
- Created a simple, intuitive CLI flow
- Implemented basic input validation
- Established the foundation for future expansion

### Phase 2: AI Content Generation
**Goal**: Replace static content with dynamic AI responses  
**Key Components**:
- Integrated Ollama with Phi-3 Mini model
- Dynamic prompt templates
- Local LLM inference

**Challenges & Solutions**:
- **Challenge**: Initial connection issues with Ollama  
  **Solution**: Added setup instructions and error handling
- **Challenge**: Model performance on consumer hardware  
  **Solution**: Selected `phi3:mini` for optimal performance

### Phase 3: Open Source Voice Output
**Goal**: Add audio support for hands-free walking  
**Key Components**:
- `pyttsx3` for text-to-speech
- Audio/text output mode selection
- System voice configuration

**Challenges & Solutions**:
- **Challenge**: Cross-platform voice quality  
  **Solution**: Used system voices for maximum compatibility
- **Challenge**: Audio file saving issues  
  **Solution**: Implemented direct playback instead of file-based

### Phase 4: Basic Data Tracking
**Goal**: Collect user interaction data  
**Key Components**:
- JSON-based data storage
- Session logging
- Feedback collection (1-5 stars)

**Implementation**:
- Created `data_manager.py` for data persistence
- Structured JSON schema for walk logs
- Simple feedback collection after each session

### Phase 5: Pattern Recognition & Insights
**Goal**: Analyze user data for personalization  
**Key Components**:
- `pattern_engine.py` for data analysis
- Mood and time-based pattern detection
- Personalized insights generation

**Technical Details**:
- Implemented statistical analysis of walk history
- Added time-of-day based mood suggestions
- Generated natural language summaries of user habits

### Phase 6: Personalized AI Prompts
**Goal**: Tailor AI responses to user preferences  
**Key Components**:
- `user_profile.py` for preference management
- Dynamic prompt construction
- Context-aware content generation

**Implementation**:
- Created user profile singleton
- Developed prompt builder with preference injection
- Integrated with AI engine for contextual responses

### Phase 7: Smarter & Interactive Content
**Goal**: Enable iterative, engaging content  
**Key Components**:
- Chunked content generation
- Conversation history tracking
- Real-time feedback integration

**Technical Challenges**:
- **Challenge**: Maintaining conversation context  
  **Solution**: Implemented conversation history management
- **Challenge**: Content validation issues  
  **Solution**: Simplified validation rules and improved error handling

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Phi-3 Mini model downloaded (`ollama pull phi3:mini`)

### Installation
```bash
# Clone the repository
git clone [your-repo-url]
cd walkpal

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your preferences
```

### Usage
```bash
python walkpal.py
```

## 📊 Project Structure

```
walkpal/
├── ai_engine.py         # AI content generation
├── config.py            # Configuration settings
├── data_manager.py      # Data persistence
├── pattern_engine.py    # User pattern analysis
├── prompt_builder.py    # Dynamic prompt construction
├── prompts.py           # System prompts and templates
├── user_profile.py      # User preference management
├── walkpal.py           # Main application
├── requirements.txt     # Dependencies
└── user_data/           # User data storage
    └── walk_log.json    # Walk history
```

## 🛠️ Technical Highlights

### AI Integration
- Local LLM inference with Ollama
- Dynamic prompt engineering
- Context-aware response generation

### Data Management
- JSON-based storage
- Session tracking
- Feedback analysis

### User Experience
- Interactive CLI interface
- Audio/text output modes
- Personalized content suggestions

## 📈 Future Enhancements

- [ ] **Improved UI**: Rich terminal interface with `rich` or `click`
- [ ] **Advanced Personalization**: Content style and complexity adaptation
- [ ] **Journaling**: Session notes and reflections
- [ ] **Voice Selection**: Multiple TTS voice options
- [ ] **Content Expansion**: More content types and categories
- [ ] **Walk Tracking**: Integration with fitness trackers
- [ ] **Cloud Sync**: Cross-device data synchronization
- [ ] **GUI/Mobile App**: More accessible user interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✍️ Author

Boya Uday Kumar  

*   Built with ❤️ during the **100-Day AI Build Challenge**.

---

## 💬 Contact

Reach out on GitHub or connect via [Portfolio](https://ud-ai-kumar.vercel.app/) to collaborate on educational AI projects.
