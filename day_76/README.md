# 🤖 FriendGPT - "Remember My People" Bot

A smart Python application that helps you remember details about your friends and generate thoughtful interactions. Never forget birthdays, kids' names, or last conversations again!

## 🚀 Features

### 📝 Friend Profile Management
- **Add friends** with natural language details (e.g., "Akhil, lives in Bangalore, loves cricket, just got a new job")
- **Smart parsing** of details into structured information
- **Search and filter** friends by name or details
- **Visual status indicators** showing when you last contacted each friend

### 💬 Conversation Intelligence
- **Generate personalized check-in messages** based on friend's details
- **Get conversation suggestions** tailored to each friend's interests and life events
- **Track conversation history** with timestamps and summaries
- **Smart reminders** for friends you haven't contacted recently

### 🎯 Smart Features
- **Automatic detail extraction** from natural language input
- **Context-aware suggestions** based on work, family, hobbies, and location
- **Birthday and important date tracking**
- **Conversation memory thread** for each person

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Installation
1. Clone or download the project
2. Navigate to the project directory
3. Run the application:

```bash
python friendgpt.py
```

## 📖 How to Use

### 1. Adding Friends
1. Enter the friend's name in the "Name" field
2. Add details in natural language in the "Details" field
3. Click "Add Friend"

**Example details:**
- "Akhil, lives in Bangalore, loves cricket, just got a new job"
- "Sarah, works at Google, has 2 kids, enjoys hiking"
- "Mike, lives in New York, birthday March 15th, loves photography"

### 2. Managing Friends
- **Search**: Type in the search box to find friends by name or details
- **View Details**: Click on a friend to see their full profile and conversation history
- **Delete**: Select a friend and click "Delete Friend" to remove them

### 3. Generating Interactions
- **Check-in Messages**: Click "Generate Check-in" for personalized greeting messages
- **Conversation Suggestions**: Click "Get Suggestions" for questions to ask based on their details
- **Log Conversations**: Click "Log Conversation" to record what you talked about

### 4. Smart Reminders
The system automatically tracks:
- ⚠️ Friends you haven't contacted in over 30 days
- 🕐 Friends due for contact (7+ days)
- ✅ Recently contacted friends

## 🎨 Features in Detail

### Smart Detail Parsing
The system automatically extracts:
- **Location**: "lives in [city]"
- **Hobbies**: "loves [activity]" or "enjoys [activity]"
- **Work**: "works at [company]" or "new job"
- **Family**: "has kids" or "children"
- **Birthdays**: "birthday [date]"

### Personalized Check-in Messages
Generated messages include:
- Friend's name
- Emojis for warmth
- Context-aware content based on their details
- Varied templates to avoid repetition

### Conversation Suggestions
Context-aware questions based on:
- **Work**: Job updates, projects, work-life balance
- **Family**: Kids, family trips, home life
- **Hobbies**: Specific activities they enjoy
- **Location**: Local events, discoveries, life in their city
- **General**: Universal conversation starters

### Memory Thread System
Each friend has a persistent memory thread including:
- Original details and parsed information
- Last contact timestamp
- Last conversation summary
- Conversation history (last 10 interactions)
- Important dates and events

## 📁 File Structure

```
day_76/
├── friendgpt.py          # Main application
├── friends_data.json     # Friend data storage (auto-generated)
└── README.md            # This file
```

## 🔧 Technical Details

### Data Storage
- Uses JSON format for persistent storage
- Automatic backup and recovery
- UTF-8 encoding for international character support

### GUI Framework
- Built with tkinter for cross-platform compatibility
- Modern UI with scrollable lists and text areas
- Responsive design with proper grid layout

### Smart Algorithms
- Natural language processing for detail extraction
- Context-aware message generation
- Intelligent conversation suggestion system
- Time-based reminder algorithms

## 🎯 Use Cases

### For Busy Professionals
- Remember colleague details and family information
- Generate appropriate work-related conversation starters
- Track professional relationships and networking

### For Social Butterflies
- Never forget important details about new acquaintances
- Generate personalized messages for different friend groups
- Maintain meaningful connections with large social circles

### For Family Members
- Remember extended family details and important dates
- Generate thoughtful check-ins for distant relatives
- Track family conversations and updates

## 🚀 Future Enhancements

Potential features for future versions:
- **Email integration** for automatic check-ins
- **Calendar integration** for birthday reminders
- **Social media integration** for relationship insights
- **Voice interface** for hands-free operation
- **Mobile app** for on-the-go access
- **AI-powered conversation analysis**
- **Relationship strength scoring**
- **Meeting scheduling suggestions**

## 🤝 Contributing

Feel free to enhance this project by:
- Adding new conversation templates
- Improving the detail parsing algorithm
- Enhancing the GUI design
- Adding new features and integrations

## 📄 License

This project is open source and available under the MIT License.

---

**Remember: The best relationships are built on genuine care and attention. FriendGPT helps you show that care by remembering the details that matter!** 💙 