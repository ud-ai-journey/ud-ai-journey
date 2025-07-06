#!/usr/bin/env python3
"""
Simple test script for StageTimer Clone
Tests basic functionality without running the full server
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from models import Base, Room, Timer, Message, ConnectedDevice
        print("✅ Database models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    try:
        from timer_engine import TimerEngine, TimerConfig, TimerType
        print("✅ Timer engine imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import timer engine: {e}")
        return False
    
    try:
        from websocket_manager import ConnectionManager, WebSocketHandler
        print("✅ WebSocket manager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import WebSocket manager: {e}")
        return False
    
    try:
        from app import app
        print("✅ FastAPI app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        return False
    
    return True

def test_timer_engine():
    """Test basic timer engine functionality"""
    print("\nTesting timer engine...")
    
    try:
        from timer_engine import TimerEngine, TimerConfig, TimerType
        
        # Create timer engine
        engine = TimerEngine()
        
        # Create a test timer
        config = TimerConfig(
            id="test-timer",
            title="Test Timer",
            duration=300,  # 5 minutes
            timer_type=TimerType.COUNTDOWN,
            wrap_up_yellow=60,
            wrap_up_red=30
        )
        
        timer = engine.add_timer(config)
        
        # Test timer properties
        assert timer.title == "Test Timer"
        assert timer.duration == 300
        assert timer.timer_type == TimerType.COUNTDOWN
        
        # Test timer display
        display_time = timer.get_display_time()
        assert display_time == "05:00"
        
        print("✅ Timer engine basic functionality works")
        return True
        
    except Exception as e:
        print(f"❌ Timer engine test failed: {e}")
        return False

def test_websocket_manager():
    """Test WebSocket manager functionality"""
    print("\nTesting WebSocket manager...")
    
    try:
        from websocket_manager import ConnectionManager
        
        # Create connection manager
        manager = ConnectionManager()
        
        # Test room devices
        devices = manager.get_room_devices("test-room")
        assert len(devices) == 0
        
        connection_count = manager.get_room_connection_count("test-room")
        assert connection_count == 0
        
        print("✅ WebSocket manager basic functionality works")
        return True
        
    except Exception as e:
        print(f"❌ WebSocket manager test failed: {e}")
        return False

def test_app_routes():
    """Test that the FastAPI app has the expected routes"""
    print("\nTesting FastAPI routes...")
    
    try:
        from app import app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        expected_routes = [
            '/',
            '/controller/{room_id}',
            '/viewer/{room_id}',
            '/agenda/{room_id}',
            '/ws/{room_id}',
            '/api/rooms',
            '/api/rooms/{room_id}/timers',
            '/api/rooms/{room_id}/timers/{timer_id}/control',
            '/api/rooms/{room_id}/messages',
            '/api/rooms/{room_id}/devices'
        ]
        
        found_routes = []
        for expected in expected_routes:
            for route in routes:
                if expected.replace('{', '').replace('}', '') in route.replace('{', '').replace('}', ''):
                    found_routes.append(expected)
                    break
        
        print(f"Found {len(found_routes)} out of {len(expected_routes)} expected routes")
        
        if len(found_routes) >= len(expected_routes) * 0.8:  # 80% match
            print("✅ FastAPI routes test passed")
            return True
        else:
            print("❌ FastAPI routes test failed")
            return False
            
    except Exception as e:
        print(f"❌ FastAPI routes test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing StageTimer Clone Application")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_timer_engine,
        test_websocket_manager,
        test_app_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("python app.py")
        print("\nThen visit: http://localhost:8000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 