# AI Relocation Guide - Day 80

## 🏠 Overview

The AI Relocation Guide is a comprehensive, AI-powered application that helps users find the perfect city for their next move. Using advanced personality assessment, career analysis, and cost-of-living data, it provides personalized recommendations and detailed comparisons to make informed relocation decisions.

## ✨ Features

### 🧠 AI-Powered Personality Assessment
- **15-question personality quiz** based on psychological research
- **Multi-dimensional scoring** (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- **City compatibility matching** using personality traits
- **Visual personality radar charts** for easy understanding

### 💼 Career & Financial Analysis
- **Career field-specific job market analysis**
- **Salary comparison and adjustment recommendations**
- **Cost of living breakdown** by category (housing, food, transportation, etc.)
- **Financial impact projections** for relocation decisions

### 🌟 Lifestyle & Cultural Matching
- **Cultural diversity scoring**
- **Arts and entertainment scene analysis**
- **Outdoor recreation opportunities**
- **Safety and walkability metrics**
- **Public transportation accessibility**

### 📊 Advanced Analytics
- **City rankings** by different categories
- **Side-by-side city comparisons**
- **Interactive data visualizations**
- **Comprehensive cost analysis**
- **Export capabilities** (JSON, CSV)

### 🤖 AI Integration
- **OpenAI GPT-4 powered analysis** for detailed city insights
- **Personalized recommendations** based on user profile
- **Natural language explanations** of compatibility factors
- **Intelligent scoring algorithms** for city matching

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (optional, for enhanced AI analysis)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd day_80
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional):**
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run relocation_guide.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📋 How to Use

### 1. Welcome & Introduction
- Start your journey with an overview of the application
- Learn about the features and what to expect

### 2. Personality Assessment
- Complete the 15-question personality quiz
- Get your personalized personality profile
- View interactive radar charts of your traits

### 3. Profile Setup
- Enter your current city and salary
- Specify your career field and experience
- Set preferences for climate, lifestyle, and budget

### 4. AI Recommendations
- Receive personalized city recommendations
- View compatibility scores and detailed analysis
- Read AI-generated insights about each city

### 5. City Comparison
- Compare specific cities side by side
- Analyze cost differences and lifestyle factors
- Make informed decisions with detailed data

### 6. Cost Analysis
- Get detailed financial impact analysis
- Understand salary adjustments needed
- View category-by-category cost breakdowns

### 7. Analytics & Insights
- Explore city rankings by different categories
- View comprehensive statistics and trends
- Discover hidden gems and opportunities

### 8. Export Your Data
- Download your analysis as JSON or CSV
- Save recommendations for future reference
- Share insights with family or advisors

## 🏗️ Architecture

### Core Components

```
day_80/
├── relocation_guide.py      # Main Streamlit application
├── ai_engine.py            # AI analysis and recommendations
├── data_manager.py         # Data handling and caching
├── config.py              # Configuration and settings
├── requirements.txt        # Python dependencies
├── data/                  # Data files
│   ├── cities.json        # City database
│   └── personality_questions.json  # Assessment questions
└── README.md             # This file
```

### Data Structure

#### Cities Database (`data/cities.json`)
Each city includes:
- **Basic Info**: Name, state, country, coordinates, population
- **Cost of Living**: Housing, food, transportation, healthcare, etc.
- **Climate**: Temperature ranges, rainfall, snowfall
- **Culture**: Diversity, arts, nightlife, food, sports scores
- **Career**: Job opportunities by field, average salary
- **Lifestyle**: Walkability, public transit, safety, parks
- **Personality Fit**: Compatibility scores for personality dimensions

#### Personality Questions (`data/personality_questions.json`)
- **15 carefully crafted questions** based on psychological research
- **Multi-dimensional scoring** for personality traits
- **Weighted impact** on city compatibility

### AI Engine Features

#### Personality Analysis
```python
# Calculate personality scores from quiz answers
personality_scores = ai_engine.calculate_personality_scores(answers)
```

#### City Compatibility Analysis
```python
# Analyze compatibility between user and city
analysis = ai_engine.analyze_city_compatibility(user_profile, city_data)
```

#### Cost Analysis
```python
# Generate detailed cost comparison
cost_analysis = ai_engine.generate_cost_analysis(current_city, target_city, salary)
```

## 🎯 Key Features Explained

### Personality-City Matching
The application uses a sophisticated algorithm that:
1. **Analyzes personality dimensions** from the assessment
2. **Maps personality traits** to city characteristics
3. **Calculates compatibility scores** using weighted factors
4. **Provides AI-powered insights** about the match

### Cost Analysis Engine
- **Category-by-category breakdown** of living costs
- **Percentage change calculations** for easy comparison
- **Salary adjustment recommendations** based on cost differences
- **Visual charts and graphs** for clear understanding

### AI-Powered Recommendations
- **Multi-factor analysis** considering personality, career, and lifestyle
- **Natural language explanations** of why cities are recommended
- **Personalized insights** based on user preferences
- **Fallback algorithms** when AI is unavailable

## 📊 Data Sources

### City Information
- **Cost of living data** from multiple sources
- **Demographic information** from census data
- **Climate data** from weather services
- **Cultural metrics** from various indices
- **Career information** from job market data

### Personality Assessment
- **Research-based questions** from psychological studies
- **Validated scoring methods** for personality dimensions
- **City compatibility mapping** based on urban research

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=True/False
```

### Customization Options
- **Add new cities** to `data/cities.json`
- **Modify personality questions** in `data/personality_questions.json`
- **Adjust scoring weights** in `ai_engine.py`
- **Customize UI** in `relocation_guide.py`

## 🚀 Deployment

### Local Development
```bash
streamlit run relocation_guide.py
```

### Production Deployment
1. **Set up environment variables**
2. **Install dependencies**
3. **Configure web server** (nginx, Apache)
4. **Deploy with Streamlit Cloud** or similar service

## 📈 Future Enhancements

### Planned Features
- **International cities** support
- **Real-time data updates** from APIs
- **Mobile app** development
- **Social features** for community insights
- **Advanced visualizations** with 3D maps
- **Integration with job platforms**
- **Visa and immigration information**

### Technical Improvements
- **Machine learning models** for better predictions
- **Real-time cost data** from APIs
- **Advanced caching** for performance
- **Multi-language support**
- **Accessibility improvements**

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Data Contributions
- **Add new cities** to the database
- **Improve personality questions**
- **Enhance scoring algorithms**
- **Add new analysis features**

## 📄 License

This project is part of the 100 Days of AI Journey. Feel free to use, modify, and distribute according to your needs.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 integration
- **Streamlit** for the web framework
- **Plotly** for interactive visualizations
- **Psychological research** for personality assessment methodology
- **Urban planning data** for city characteristics

---

**Built with ❤️ as part of the 100 Days of AI Journey**

*Making relocation decisions easier with the power of AI* 