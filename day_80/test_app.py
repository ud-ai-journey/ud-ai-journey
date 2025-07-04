#!/usr/bin/env python3
"""
Test script for AI Relocation Guide
Verifies all components are working correctly
"""

import sys
import os
import json
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from data_manager import DataManager
        print("✅ DataManager imported successfully")
    except ImportError as e:
        print(f"❌ DataManager import failed: {e}")
        return False
    
    try:
        from ai_engine import AIEngine
        print("✅ AIEngine imported successfully")
    except ImportError as e:
        print(f"❌ AIEngine import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test that data files can be loaded"""
    print("\n📊 Testing data loading...")
    
    # Test cities data
    try:
        with open('data/cities.json', 'r') as f:
            cities_data = json.load(f)
        
        if 'cities' in cities_data and len(cities_data['cities']) > 0:
            print(f"✅ Cities data loaded: {len(cities_data['cities'])} cities")
        else:
            print("❌ Cities data is empty or malformed")
            return False
    except FileNotFoundError:
        print("❌ cities.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ cities.json is not valid JSON: {e}")
        return False
    
    # Test personality questions
    try:
        with open('data/personality_questions.json', 'r') as f:
            questions_data = json.load(f)
        
        if 'questions' in questions_data and len(questions_data['questions']) > 0:
            print(f"✅ Personality questions loaded: {len(questions_data['questions'])} questions")
        else:
            print("❌ Personality questions data is empty or malformed")
            return False
    except FileNotFoundError:
        print("❌ personality_questions.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ personality_questions.json is not valid JSON: {e}")
        return False
    
    return True

def test_data_manager():
    """Test DataManager functionality"""
    print("\n🗄️ Testing DataManager...")
    
    try:
        from data_manager import DataManager
        dm = DataManager()
        
        # Test cities retrieval
        cities = dm.get_cities()
        if len(cities) > 0:
            print(f"✅ DataManager cities: {len(cities)} cities loaded")
        else:
            print("❌ DataManager returned no cities")
            return False
        
        # Test city search
        search_results = dm.search_cities("New York")
        if len(search_results) > 0:
            print(f"✅ City search working: found {len(search_results)} results for 'New York'")
        else:
            print("❌ City search not working")
            return False
        
        # Test statistics
        stats = dm.get_city_statistics()
        if stats and 'total_cities' in stats:
            print(f"✅ City statistics: {stats['total_cities']} cities, avg cost ${stats.get('avg_cost_of_living', 0):,.0f}")
        else:
            print("❌ City statistics not working")
            return False
        
        return True
    except Exception as e:
        print(f"❌ DataManager test failed: {e}")
        return False

def test_ai_engine():
    """Test AIEngine functionality"""
    print("\n🤖 Testing AIEngine...")
    
    try:
        from ai_engine import AIEngine
        ai = AIEngine()
        
        # Test personality scoring
        test_answers = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2]  # 15 answers
        personality_scores = ai.calculate_personality_scores(test_answers)
        
        if personality_scores and all(key in personality_scores for key in ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']):
            print("✅ Personality scoring working")
            print(f"   Sample scores: {personality_scores}")
        else:
            print("❌ Personality scoring failed")
            return False
        
        # Test city compatibility (without OpenAI)
        test_user_profile = {
            'personality_scores': personality_scores,
            'career_info': {'field': 'Technology', 'salary': 75000},
            'preferences': {'climate': 'Mild', 'lifestyle_priority': 'Career opportunities'}
        }
        
        cities = ai.cities_data
        if cities:
            test_city = cities[0]
            analysis = ai.analyze_city_compatibility(test_user_profile, test_city)
            
            if analysis and 'compatibility_score' in analysis:
                print(f"✅ City compatibility analysis working: {analysis['city_name']} - {analysis['compatibility_score']:.0f}%")
            else:
                print("❌ City compatibility analysis failed")
                return False
        else:
            print("❌ No cities available for testing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ AIEngine test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        config = Config()
        
        print(f"✅ App name: {config.APP_NAME}")
        print(f"✅ Version: {config.APP_VERSION}")
        print(f"✅ Default cities: {len(config.DEFAULT_CITIES)} cities")
        print(f"✅ Cost categories: {len(config.COST_CATEGORIES)} categories")
        print(f"✅ Personality dimensions: {len(config.PERSONALITY_DIMENSIONS)} dimensions")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_dependencies():
    """Test that required packages are available"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'openai',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} not available")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 AI Relocation Guide - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Data Loading", test_data_loading),
        ("Data Manager", test_data_manager),
        ("AI Engine", test_ai_engine)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The AI Relocation Guide is ready to run.")
        print("\n🚀 To start the application:")
        print("   streamlit run relocation_guide.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 