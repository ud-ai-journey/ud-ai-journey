# Day 97 -⚡ Energy Lens - Pattern Optimizer

**Discover your energy patterns to optimize productivity**

---

## 🚀 What's New in Day 97? (User-Driven Enhancements)

Thanks to valuable feedback and suggestions from our users, we've made major improvements to Energy Lens to make it more intuitive, friendly, and ready for real-world use:

- **Modern Tabbed Layout:** Navigation is now via clear tabs (Energy Check, Your Data, Profile) for a smoother, more organized experience.
- **Onboarding & 'Start Here' Button:** New users are greeted with a friendly welcome and a clear call-to-action to begin their journey.
- **Tooltips & Inline Help:** Helpful tooltips and info messages guide users at every step, making the app easy for everyone.
- **Friendly Error Handling:** User-friendly, actionable messages for camera/model/face detection issues, so users always know what to do next.
- **Downloadable CSV Report:** Instantly export your energy/emotion data for further analysis or sharing.
- **Cleaner Structure:** All code and data now live directly in the day_97 folder for simplicity and transparency.
- **Improved UX:** Layout, guidance, and feedback are all optimized for clarity and ease of use.
- **Correct Ordinal Suffixes:** Reading counts now display as 1st, 2nd, 3rd, etc., for a more polished experience.

These enhancements are a direct response to real user needs and feedback—thank you for helping us make Energy Lens better for everyone!

---

Energy Lens is an intelligent energy tracking application that uses computer vision to detect your energy levels and provides actionable insights to optimize your productivity patterns.

## 🎯 Features

### 📸 **Smart Energy Detection**
- **Camera/Upload Support:** Take photos or upload images for energy analysis
- **Local ML Processing:** Uses DeepFace for offline emotion detection
- **Realistic Expectations:** Focuses on energy levels (High/Medium/Low) rather than precise emotions
- **Fallback Analysis:** OpenCV-based detection when DeepFace fails

### 📊 **Pattern Analysis**
- **Time-based Insights:** Discover your peak energy hours
- **Weekly Patterns:** Identify your most productive days
- **Trend Analysis:** Track energy changes over time
- **Confidence Tracking:** Monitor detection accuracy

### 🎯 **Productivity Optimization**
- **Personalized Tips:** Get advice based on your energy patterns
- **Scheduling Suggestions:** Optimize your calendar based on energy data
- **Progress Tracking:** Visualize your energy journey

### 🔒 **Privacy-First**
- **No External APIs:** Everything runs locally
- **Local Database:** SQLite storage for your data
- **Offline Processing:** No internet required for analysis

## 🚀 Quick Start

### Installation

1. **Clone or navigate to the project directory**
```bash
cd day_97
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run energy_lens_app.py
```

4. **Open your browser**
Navigate to `http://localhost:8501`

## 📁 Project Structure

```
day_97/
├── energy_lens_app.py      # Main Streamlit application (Day 97 enhancements)
├── energy_detector.py      # DeepFace + energy classification
├── data_manager.py         # SQLite database operations
├── pattern_analyzer.py     # Energy pattern analysis
├── visualizations.py       # Charts and graphs
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🎨 How It Works

### 1. **Energy Detection**
- Take a photo or upload an image
- DeepFace analyzes facial expressions
- Maps emotions to energy levels (Happy/Surprise → High, Neutral → Medium, Sad/Angry/Fear → Low)
- Provides confidence scores for accuracy

### 2. **Pattern Analysis**
- Tracks energy levels over time
- Identifies peak productivity hours
- Discovers weekly patterns
- Analyzes trends and changes

### 3. **Insights & Tips**
- Personalized productivity recommendations
- Scheduling optimization suggestions
- Energy-based task planning advice

## 📊 Key Insights You'll Discover

- **Peak Energy Times:** When you're most productive
- **Energy Dips:** When to plan lighter activities
- **Best Days:** Your most productive days of the week
- **Trends:** Whether your energy is improving or declining
- **Confidence:** How accurate the detection is for you

## 🛠️ Technical Details

### **Tech Stack**
- **Frontend:** Streamlit (beautiful, interactive UI)
- **Computer Vision:** DeepFace + OpenCV
- **Data Storage:** SQLite (local, private)
- **Visualization:** Plotly (interactive charts)
- **Analysis:** Pandas + NumPy

### **Energy Detection Algorithm**
1. **Primary:** DeepFace emotion detection
2. **Fallback:** OpenCV face/eye detection
3. **Mapping:** Emotions → Energy levels
4. **Confidence:** Realistic confidence scoring

### **Data Privacy**
- All data stored locally in SQLite
- No external API calls
- No data sent to cloud services
- Complete privacy and control

## 🎯 Use Cases

### **For Productivity**
- Schedule important meetings during peak energy
- Plan creative work during high-energy periods
- Schedule breaks during energy dips

### **For Self-Awareness**
- Understand your natural energy rhythms
- Identify patterns in your mood/energy
- Track the impact of lifestyle changes

### **For Optimization**
- Optimize your daily schedule
- Plan tasks based on energy levels
- Improve work-life balance

## 🔧 Customization

### **Adding New Energy Levels**
Edit `energy_detector.py`:
```python
self.energy_mapping = {
    'happy': 'High',
    'surprise': 'High', 
    'neutral': 'Medium',
    'sad': 'Low',
    'angry': 'Low',
    'fear': 'Low',
    'disgust': 'Low',
    'your_emotion': 'your_energy_level'  # Add here
}
```

### **Customizing Tips**
Edit `pattern_analyzer.py` to add personalized productivity tips based on your patterns.

## 🚨 Troubleshooting

### **DeepFace Installation Issues**
```bash
pip install deepface --upgrade
```

### **Camera Not Working**
- Ensure camera permissions are granted
- Try uploading an image instead
- Check browser camera access

### **Low Confidence Scores**
- Try better lighting
- Face the camera directly
- Use manual entry for unclear results

## 📈 Future Enhancements

- **Calendar Integration:** Link energy data with your schedule
- **Export Features:** Share insights with coaches/therapists
- **Mobile App:** Native mobile experience
- **Team Features:** Compare patterns with colleagues
- **AI Coaching:** Personalized energy optimization advice

## 🤝 Contributing

This is Day 97 of a 100-day Python and AI challenge. The project demonstrates:
- Computer vision with local ML
- Data analysis and visualization
- Privacy-first design
- Real-world problem solving

## 📄 License

This project is part of a learning journey. Feel free to use, modify, and build upon it!

---

**⚡ Energy Lens - Because knowing your patterns is power!** 