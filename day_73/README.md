# 🚶 WalkPal - AI-Powered Walking Companion

WalkPal is an intelligent walking companion that generates personalized, engaging content based on your mood and walk duration. Built with Python and local AI, it offers both text and audio output for a hands-free walking experience.

## ✨ Features

- **Mood-Based Content**: Choose from various moods (Learn, Reflect, Story, Humor, Surprise) or enter a custom topic
- **AI-Powered**: Generates unique content for every walk using local LLM (Phi-3 Mini via Ollama)
- **Audio Support**: Listen to content hands-free with configurable system TTS (pyttsx3)
- **Voice Customization**: Configure speaking voice, rate, and volume via environment variables
- **Personalized Experience**: Learns from your preferences and feedback
- **Data Privacy**: Everything runs locally on your machine
- **No Internet Required**: Works completely offline after initial setup
- **Multi-Language Support**: Supports English, Spanish, French, and Hindi

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **AI Model**: Ollama (Local LLM runner) + Phi-3 Mini
- **Text-to-Speech**: `pyttsx3` (Offline, System TTS)
- **Voice Configuration**: Environment variables for voice customization
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

### Phase 8: Day 73 - WalkPal TTS Improvements

## Features Implemented Today

### 1. Text-to-Speech Enhancements
- Added comprehensive TTS engine initialization and testing
- Implemented detailed logging for TTS operations
- Created robust error handling and recovery mechanisms
- Added text validation before speech
- Implemented proper engine state management

### 2. User Interface Improvements
- Removed redundant walk summaries for cleaner output
- Added clearer status messages during audio playback
- Improved feedback collection process

### 3. Code Organization
- Created dedicated `speak_content` function for better TTS control
- Improved error handling and recovery
- Added detailed logging throughout the application

## Technical Changes

### walkpal.py
- Removed redundant walk summary section
- Added dedicated `speak_content` function
- Improved TTS engine state management
- Added better error handling and logging

### voice_engine.py
- Enhanced TTS engine initialization
- Added better error recovery
- Improved engine state management
- Added detailed logging

## Current Status
- The application supports English language only
- TTS functionality is implemented with pyttsx3
- Audio playback is available in audio mode
- Text mode is available as an alternative

## Next Steps
- Further testing of TTS functionality
- Investigate remaining audio playback issues
- Consider alternative TTS engines if needed
- Add configuration options for speech rate and volume

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

## 📋 How to Run

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure Environment**:
- Create a `.env` file in the project root
- Set `OLLAMA_HOST` to your Ollama server URL (default: http://localhost:11434)
- Optional: Set `DEFAULT_LLM_MODEL` to your preferred model (default: phi3:mini)
- Optional: Configure language:
  - `WALKPAL_LANG`: Set to 'en' (English), 'es' (Spanish), 'fr' (French), or 'hi' (Hindi)
- Optional: Configure voice settings:
  - `WALKPAL_TTS_VOICE_ID`: System voice ID (use `python walkpal.py --list-voices` to find available voices)
  - `WALKPAL_TTS_RATE`: Speaking rate (default: 175)
  - `WALKPAL_TTS_VOLUME`: Volume level (0.0 to 1.0, default: 1.0)

3. **List Available Voices**:
```bash
python walkpal.py --list-voices
```

4. **Start WalkPal**:
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
- English language support

## 🌐 Language Support

WalkPal currently supports English language only. Multi-language support was previously attempted but has been reverted due to complexity and issues with maintaining consistent user experience across languages.

1. The application currently supports English language only.

2. The application UI will be displayed in your selected language
3. AI-generated content will be in the selected language
4. Voice output will use the system's TTS voices for the selected language (if available)

### Voice Output in Different Languages

For voice output in a specific language:
1. Ensure your system has TTS voices installed for that language
2. Use the `--list-voices` command to find available voices:
   ```bash
   python walkpal.py --list-voices
   ```
3. Set the appropriate voice ID in `.env` under `WALKPAL_TTS_VOICE_ID`

### Important Notes


- Voice quality depends on the system's TTS voices



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
