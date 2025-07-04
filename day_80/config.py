import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    NUMBEO_API_KEY = os.getenv('NUMBEO_API_KEY', '')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///relocation_guide.db')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # App Settings
    APP_NAME = "AI Relocation Guide"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Data Sources
    CITIES_DATA_FILE = "data/cities.json"
    PERSONALITY_QUESTIONS_FILE = "data/personality_questions.json"
    
    # AI Settings
    OPENAI_MODEL = "gpt-4"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # Cache Settings
    CACHE_DURATION = 3600  # 1 hour
    
    # Feature Flags
    ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'False').lower() == 'true'
    ENABLE_PDF_EXPORT = True
    ENABLE_MAPS = True
    
    # UI Settings
    THEME_COLOR = "#1f77b4"
    SECONDARY_COLOR = "#ff7f0e"
    SUCCESS_COLOR = "#2ca02c"
    WARNING_COLOR = "#d62728"
    
    # Default Cities for Demo
    DEFAULT_CITIES = [
        "New York, NY",
        "San Francisco, CA", 
        "Austin, TX",
        "Seattle, WA",
        "Denver, CO",
        "Miami, FL",
        "Chicago, IL",
        "Boston, MA",
        "Portland, OR",
        "Nashville, TN"
    ]
    
    # Cost Categories
    COST_CATEGORIES = [
        'housing',
        'food', 
        'transportation',
        'healthcare',
        'entertainment',
        'utilities',
        'taxes',
        'education'
    ]
    
    # Personality Dimensions
    PERSONALITY_DIMENSIONS = [
        'openness',
        'conscientiousness', 
        'extraversion',
        'agreeableness',
        'neuroticism'
    ]
    
    # Career Categories
    CAREER_CATEGORIES = [
        'Technology',
        'Healthcare',
        'Finance',
        'Education',
        'Marketing',
        'Sales',
        'Engineering',
        'Design',
        'Consulting',
        'Government',
        'Non-profit',
        'Other'
    ] 