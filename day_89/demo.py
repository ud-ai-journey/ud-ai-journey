#!/usr/bin/env python3
"""
SayThat Demo Script
Tests the core functionality of the SayThat app
"""

import json
import os
from datetime import datetime
from PIL import Image
import numpy as np

def create_sample_vocabulary():
    """Create sample vocabulary data for testing"""
    sample_words = [
        {
            "word": "apple",
            "pronunciation": "ˈæpəl",
            "date": "2025-01-13",
            "audio_file": "audio_apple_20250113_120000.mp3",
            "confidence": 0.95
        },
        {
            "word": "car",
            "pronunciation": "kɑːr",
            "date": "2025-01-13",
            "audio_file": "audio_car_20250113_120100.mp3",
            "confidence": 0.88
        },
        {
            "word": "book",
            "pronunciation": "bʊk",
            "date": "2025-01-13",
            "audio_file": "audio_book_20250113_120200.mp3",
            "confidence": 0.92
        },
        {
            "word": "phone",
            "pronunciation": "foʊn",
            "date": "2025-01-13",
            "audio_file": "audio_phone_20250113_120300.mp3",
            "confidence": 0.87
        },
        {
            "word": "laptop",
            "pronunciation": "ˈlæptɒp",
            "date": "2025-01-13",
            "audio_file": "audio_laptop_20250113_120400.mp3",
            "confidence": 0.91
        }
    ]
    
    # Save sample vocabulary
    with open('vocabulary.json', 'w') as f:
        json.dump(sample_words, f, indent=2)
    
    print("✅ Sample vocabulary created with 5 words")
    return sample_words

def create_sample_detection_history():
    """Create sample detection history for analytics"""
    sample_history = [
        {
            "date": "2025-01-13 12:00",
            "objects": ["apple", "car", "book"]
        },
        {
            "date": "2025-01-13 14:30",
            "objects": ["phone", "laptop"]
        },
        {
            "date": "2025-01-13 16:45",
            "objects": ["apple", "phone", "book"]
        },
        {
            "date": "2025-01-14 09:15",
            "objects": ["car", "laptop"]
        },
        {
            "date": "2025-01-14 11:30",
            "objects": ["book", "phone", "apple"]
        }
    ]
    
    print("✅ Sample detection history created")
    return sample_history

def test_pronunciation_conversion():
    """Test IPA pronunciation conversion"""
    test_words = ["apple", "car", "book", "phone", "laptop"]
    
    print("\n🧪 Testing pronunciation conversion:")
    print("-" * 40)
    
    for word in test_words:
        try:
            import eng_to_ipa as ipa
            pronunciation = ipa.convert(word)
            print(f"✅ {word} → /{pronunciation}/")
        except Exception as e:
            print(f"❌ {word} → Error: {e}")
    
    print("-" * 40)

def test_audio_generation():
    """Test audio generation functionality"""
    print("\n🎵 Testing audio generation:")
    print("-" * 40)
    
    test_word = "apple"
    audio_filename = f"demo_audio_{test_word}.mp3"
    
    try:
        from gtts import gTTS
        tts = gTTS(text=test_word, lang='en', slow=False)
        tts.save(audio_filename)
        print(f"✅ Audio generated: {audio_filename}")
        
        # Clean up demo file
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
            print("✅ Demo audio file cleaned up")
            
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
    
    print("-" * 40)

def test_object_detection_mock():
    """Test object detection with mock data"""
    print("\n🔍 Testing object detection (mock):")
    print("-" * 40)
    
    # Mock detection results
    mock_detections = [
        {"class_name": "apple", "confidence": 0.95, "bbox": [100, 100, 200, 200]},
        {"class_name": "car", "confidence": 0.88, "bbox": [300, 150, 500, 300]},
        {"class_name": "book", "confidence": 0.92, "bbox": [50, 400, 150, 500]}
    ]
    
    for detection in mock_detections:
        print(f"✅ Detected: {detection['class_name']} (confidence: {detection['confidence']:.2f})")
    
    print("-" * 40)

def create_sample_image():
    """Create a sample image for testing"""
    print("\n🖼️ Creating sample image:")
    print("-" * 40)
    
    # Create a simple test image
    img_array = np.random.randint(0, 255, (400, 600, 3), dtype=np.uint8)
    sample_image = Image.fromarray(img_array)
    sample_image.save('sample_image.jpg')
    
    print("✅ Sample image created: sample_image.jpg")
    print("-" * 40)

def run_demo():
    """Run the complete demo"""
    print("🎤 SayThat Demo - Testing Core Functionality")
    print("=" * 50)
    
    # Create sample data
    create_sample_vocabulary()
    create_sample_detection_history()
    
    # Test core functionality
    test_pronunciation_conversion()
    test_audio_generation()
    test_object_detection_mock()
    create_sample_image()
    
    print("\n🎉 Demo completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: streamlit run saythat_app.py")
    print("2. Upload sample_image.jpg to test the app")
    print("3. Check the vocabulary sidebar for sample data")
    print("4. View analytics with sample detection history")

if __name__ == "__main__":
    run_demo() 