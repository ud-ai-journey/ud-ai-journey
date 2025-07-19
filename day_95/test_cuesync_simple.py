#!/usr/bin/env python3
"""
🧪 Simple Test Script for CueSync
Tests basic functionality without starting the full Flask app
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_components():
    """Test individual components"""
    print("🧪 Testing CueSync Components...")
    
    # Test 1: Environment Variables
    print("\n1. Testing Environment Variables...")
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key.startswith('sk-'):
        print("✅ OpenAI API Key loaded successfully!")
    else:
        print("❌ OpenAI API Key not found or invalid")
        return False
    
    # Test 2: Timer Manager
    print("\n2. Testing Timer Manager...")
    try:
        from timer_manager import TimerManager
        tm = TimerManager()
        
        # Test timer creation
        timer_data = {
            'id': 'test_timer_1',
            'name': 'Test Timer',
            'duration': 60,
            'type': 'countdown'
        }
        timer_id = tm.create_timer(timer_data)
        if timer_id:
            print("✅ Timer Manager working correctly!")
        else:
            print("❌ Timer creation failed")
            return False
    except Exception as e:
        print(f"❌ Timer Manager error: {e}")
        return False
    
    # Test 3: Voice Processor
    print("\n3. Testing Voice Processor...")
    try:
        from voice_processor import VoiceProcessor
        vp = VoiceProcessor()
        
        # Test voice command processing
        test_command = "start the presentation timer"
        result = vp.process_voice_command(test_command)
        if result and 'command_type' in result:
            print("✅ Voice Processor working correctly!")
        else:
            print("❌ Voice command processing failed")
            return False
    except Exception as e:
        print(f"❌ Voice Processor error: {e}")
        return False
    
    # Test 4: AI Engine (basic test)
    print("\n4. Testing AI Engine...")
    try:
        from ai_engine import AIEngine
        ai = AIEngine()
        print("✅ AI Engine initialized successfully!")
    except Exception as e:
        print(f"❌ AI Engine error: {e}")
        return False
    
    print("\n🎉 All components tested successfully!")
    return True

def test_api_endpoints():
    """Test API endpoints using requests"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        import requests
        
        base_url = "http://localhost:5000"
        
        # Test 1: Create Room
        print("1. Testing room creation...")
        response = requests.post(f"{base_url}/api/rooms", json={})
        if response.status_code == 200:
            room_data = response.json()
            room_id = room_data.get('room_id')
            print(f"✅ Room created: {room_id}")
            
            # Test 2: Get Room
            print("2. Testing room retrieval...")
            response = requests.get(f"{base_url}/api/rooms/{room_id}")
            if response.status_code == 200:
                print("✅ Room retrieved successfully!")
                
                # Test 3: Create Timer
                print("3. Testing timer creation...")
                timer_data = {
                    'room_id': room_id,
                    'timer': {
                        'name': 'Test Presentation',
                        'duration': 300,
                        'type': 'countdown'
                    }
                }
                response = requests.post(f"{base_url}/api/timers", json=timer_data)
                if response.status_code == 200:
                    print("✅ Timer created successfully!")
                else:
                    print(f"❌ Timer creation failed: {response.status_code}")
            else:
                print(f"❌ Room retrieval failed: {response.status_code}")
        else:
            print(f"❌ Room creation failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Flask app not running. Start with: python app.py")
        return False
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 CueSync Testing Suite")
    print("=" * 50)
    
    # Test components
    if test_components():
        print("\n✅ Component tests passed!")
        
        # Test API endpoints if app is running
        test_api_endpoints()
    else:
        print("\n❌ Component tests failed!")
        sys.exit(1) 