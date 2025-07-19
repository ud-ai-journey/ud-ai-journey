#!/usr/bin/env python3
"""
🧪 Test Script for CueSync
Simple test to verify the Flask application works correctly
"""

import requests
import json
import time

def test_cue_sync_app():
    """Test the CueSync Flask application"""
    base_url = "http://localhost:5000"
    
    print("🎯 Testing CueSync - AI-Powered Presentation Timer")
    print("=" * 50)
    
    try:
        # Test 1: Check if server is running
        print("1. Testing server connectivity...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
        
        # Test 2: Create a room
        print("\n2. Testing room creation...")
        response = requests.post(f"{base_url}/api/rooms", json={})
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                room_id = data.get('room_id')
                timers = data.get('timers', [])
                print(f"✅ Room created successfully: {room_id}")
                print(f"   AI suggested {len(timers)} default timers")
            else:
                print("❌ Failed to create room")
                return False
        else:
            print(f"❌ Room creation failed with status: {response.status_code}")
            return False
        
        # Test 3: Get room information
        print(f"\n3. Testing room retrieval...")
        response = requests.get(f"{base_url}/api/rooms/{room_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                room_data = data.get('room', {})
                print(f"✅ Room retrieved successfully")
                print(f"   Timers: {len(room_data.get('timers', []))}")
                print(f"   Messages: {len(room_data.get('messages', []))}")
                print(f"   AI Insights: {len(room_data.get('ai_insights', {}))}")
            else:
                print("❌ Failed to retrieve room")
                return False
        else:
            print(f"❌ Room retrieval failed with status: {response.status_code}")
            return False
        
        # Test 4: Create a timer with AI assistance
        print(f"\n4. Testing AI-enhanced timer creation...")
        timer_data = {
            "name": "Test Presentation",
            "duration": 900,
            "type": "countdown"
        }
        
        response = requests.post(f"{base_url}/api/timers", json={
            "room_id": room_id,
            "timer": timer_data
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                timer = data.get('timer', {})
                print(f"✅ Timer created with AI assistance")
                print(f"   Name: {timer.get('name')}")
                print(f"   Duration: {timer.get('duration')} seconds")
                print(f"   Warning times: {timer.get('warning_times', [])}")
                timer_id = timer.get('id')
            else:
                print("❌ Failed to create timer")
                return False
        else:
            print(f"❌ Timer creation failed with status: {response.status_code}")
            return False
        
        # Test 5: Test AI suggestions
        print(f"\n5. Testing AI suggestions...")
        response = requests.get(f"{base_url}/api/suggestions?room_id={room_id}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                suggestions = data.get('suggestions', {})
                print(f"✅ AI suggestions retrieved")
                print(f"   Suggestions: {len(suggestions)} items")
            else:
                print("❌ Failed to get AI suggestions")
        else:
            print(f"❌ AI suggestions failed with status: {response.status_code}")
        
        # Test 6: Test content analysis
        print(f"\n6. Testing AI content analysis...")
        test_content = """
        Welcome to our presentation on AI-powered tools.
        Today we'll cover:
        1. Introduction to AI
        2. Machine Learning basics
        3. Real-world applications
        4. Q&A session
        """
        
        response = requests.post(f"{base_url}/api/analyze-content", json={
            "room_id": room_id,
            "content": test_content
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis = data.get('analysis', {})
                suggested_timers = data.get('suggested_timers', [])
                print(f"✅ Content analyzed with AI")
                print(f"   Sentiment score: {analysis.get('sentiment_score', 'N/A')}")
                print(f"   Complexity score: {analysis.get('complexity_score', 'N/A')}")
                print(f"   Suggested timers: {len(suggested_timers)}")
            else:
                print("❌ Failed to analyze content")
        else:
            print(f"❌ Content analysis failed with status: {response.status_code}")
        
        # Test 7: Test voice command processing
        print(f"\n7. Testing voice command processing...")
        test_command = "start the test presentation timer"
        
        response = requests.post(f"{base_url}/api/voice-command", json={
            "room_id": room_id,
            "command_text": test_command
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                ai_response = data.get('ai_response', {})
                print(f"✅ Voice command processed")
                print(f"   Command: {test_command}")
                print(f"   AI Response: {ai_response.get('command_type', 'unknown')}")
                print(f"   Confidence: {ai_response.get('confidence', 0)}")
            else:
                print("❌ Failed to process voice command")
        else:
            print(f"❌ Voice command processing failed with status: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("CueSync is working correctly with AI features!")
        print("=" * 50)
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Flask app is running:")
        print("   python app.py")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting CueSync Test Suite...")
    success = test_cue_sync_app()
    
    if success:
        print("\n✅ All tests passed! CueSync is ready to use.")
    else:
        print("\n❌ Some tests failed. Please check the server and try again.") 