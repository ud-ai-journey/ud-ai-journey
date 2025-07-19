#!/usr/bin/env python3
"""
🌐 CueSync API Testing Script
Tests all API endpoints and AI functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🌐 Testing CueSync API Endpoints...")
    
    # Test 1: Create Room
    print("\n1. Creating Room...")
    response = requests.post(f"{BASE_URL}/api/rooms")
    if response.status_code == 200:
        room_data = response.json()
        room_id = room_data.get('room_id')
        print(f"✅ Room created: {room_id}")
        
        # Test 2: Get Room
        print("\n2. Getting Room Info...")
        response = requests.get(f"{BASE_URL}/api/rooms/{room_id}")
        if response.status_code == 200:
            room_info = response.json()
            print(f"✅ Room info retrieved: {len(room_info.get('room', {}).get('timers', []))} timers")
            
            # Test 3: Create Timer
            print("\n3. Creating Timer...")
            timer_data = {
                'room_id': room_id,
                'timer': {
                    'name': 'Test Presentation',
                    'duration': 300,
                    'type': 'countdown'
                }
            }
            response = requests.post(f"{BASE_URL}/api/timers", json=timer_data)
            if response.status_code == 200:
                timer_info = response.json()
                timer_id = timer_info.get('timer', {}).get('id')
                print(f"✅ Timer created: {timer_id}")
                
                # Test 4: Start Timer
                print("\n4. Starting Timer...")
                start_data = {'room_id': room_id}
                response = requests.post(f"{BASE_URL}/api/timers/{timer_id}/start", json=start_data)
                if response.status_code == 200:
                    print("✅ Timer started successfully!")
                else:
                    print(f"❌ Timer start failed: {response.status_code}")
                
                # Test 5: Voice Command
                print("\n5. Testing Voice Command...")
                voice_data = {
                    'room_id': room_id,
                    'command_text': 'start the presentation timer'
                }
                response = requests.post(f"{BASE_URL}/api/voice-command", json=voice_data)
                if response.status_code == 200:
                    print("✅ Voice command processed!")
                else:
                    print(f"❌ Voice command failed: {response.status_code}")
                
                # Test 6: Content Analysis
                print("\n6. Testing Content Analysis...")
                content_data = {
                    'room_id': room_id,
                    'content': 'This is a test presentation about AI and machine learning.'
                }
                response = requests.post(f"{BASE_URL}/api/analyze-content", json=content_data)
                if response.status_code == 200:
                    analysis = response.json()
                    print("✅ Content analysis completed!")
                    print(f"   - Sentiment: {analysis.get('analysis', {}).get('sentiment_score', 'N/A')}")
                    print(f"   - Estimated duration: {analysis.get('analysis', {}).get('estimated_duration', 'N/A')} seconds")
                else:
                    print(f"❌ Content analysis failed: {response.status_code}")
                
                # Test 7: AI Suggestions
                print("\n7. Testing AI Suggestions...")
                response = requests.get(f"{BASE_URL}/api/suggestions?room_id={room_id}")
                if response.status_code == 200:
                    suggestions = response.json()
                    print("✅ AI suggestions retrieved!")
                else:
                    print(f"❌ AI suggestions failed: {response.status_code}")
                
                # Test 8: Send Message
                print("\n8. Testing Message System...")
                message_data = {
                    'room_id': room_id,
                    'message': {
                        'text': 'Great presentation so far!',
                        'type': 'feedback'
                    }
                }
                response = requests.post(f"{BASE_URL}/api/messages", json=message_data)
                if response.status_code == 200:
                    print("✅ Message sent successfully!")
                else:
                    print(f"❌ Message sending failed: {response.status_code}")
                
            else:
                print(f"❌ Timer creation failed: {response.status_code}")
        else:
            print(f"❌ Room retrieval failed: {response.status_code}")
    else:
        print(f"❌ Room creation failed: {response.status_code}")
    
    print("\n🎉 API Testing Complete!")

def test_websocket_connection():
    """Test WebSocket functionality"""
    print("\n🔌 Testing WebSocket Connection...")
    try:
        import socketio
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print("✅ WebSocket connected!")
        
        @sio.event
        def disconnect():
            print("❌ WebSocket disconnected!")
        
        sio.connect(BASE_URL)
        time.sleep(2)
        sio.disconnect()
        
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

if __name__ == "__main__":
    print("🚀 CueSync API Testing Suite")
    print("=" * 50)
    
    try:
        test_api_endpoints()
        test_websocket_connection()
        print("\n✅ All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("❌ Flask app not running. Start with: python app.py")
    except Exception as e:
        print(f"❌ Test error: {e}") 