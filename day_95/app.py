#!/usr/bin/env python3
"""
🎯 Day 95: CueSync - AI-Powered Presentation Timer
A sophisticated Flask application with AI features for professional presentations
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from dotenv import load_dotenv
import threading
import time

# Import our custom modules
from ai_engine import AIEngine
from timer_manager import TimerManager
from voice_processor import VoiceProcessor

# Load environment variables (optional)
try:
    load_dotenv()
except:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize our AI and timer components
ai_engine = AIEngine()
timer_manager = TimerManager()
voice_processor = VoiceProcessor()

# Global storage for rooms and sessions
rooms = {}
active_sessions = {}

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.timers = []
        self.messages = []
        self.agenda = []
        self.active_timer_id = None
        self.viewers = 0
        self.controller = None
        self.settings = {
            'theme': 'default',
            'sounds_enabled': True,
            'auto_advance': True,
            'ai_suggestions': True
        }
        self.ai_insights = {
            'speaking_pace': 0,
            'audience_engagement': 0,
            'suggested_breaks': [],
            'time_estimations': {}
        }

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/rooms', methods=['POST'])
def create_room():
    """Create a new presentation room"""
    try:
        room_id = generate_room_id()
        rooms[room_id] = Room(room_id)
        
        # Initialize with AI-suggested default timers
        default_timers = ai_engine.suggest_default_timers()
        rooms[room_id].timers = default_timers
        
        return jsonify({
            'success': True,
            'room_id': room_id,
            'timers': default_timers
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    """Get room information"""
    if room_id not in rooms:
        return jsonify({'success': False, 'error': 'Room not found'}), 404
    
    room = rooms[room_id]
    return jsonify({
        'success': True,
        'room': {
            'id': room.room_id,
            'timers': room.timers,
            'messages': room.messages,
            'agenda': room.agenda,
            'active_timer_id': room.active_timer_id,
            'viewers': room.viewers,
            'settings': room.settings,
            'ai_insights': room.ai_insights
        }
    })

@app.route('/api/timers', methods=['POST'])
def create_timer():
    """Create a new timer with AI assistance"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        timer_data = data.get('timer')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        # Use AI to enhance timer creation
        enhanced_timer = ai_engine.enhance_timer_creation(timer_data)
        
        # Add AI-suggested warning times if not provided
        if 'warning_times' not in enhanced_timer:
            enhanced_timer['warning_times'] = ai_engine.suggest_warning_times(
                enhanced_timer['duration']
            )
        
        timer_id = str(uuid.uuid4())
        enhanced_timer['id'] = timer_id
        enhanced_timer['created_at'] = datetime.now().isoformat()
        
        rooms[room_id].timers.append(enhanced_timer)
        
        # Broadcast to all viewers
        socketio.emit('timer_created', enhanced_timer, to=room_id)
        
        return jsonify({
            'success': True,
            'timer': enhanced_timer
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/timers/<timer_id>/start', methods=['POST'])
def start_timer(timer_id):
    """Start a timer with AI monitoring"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        room = rooms[room_id]
        timer = next((t for t in room.timers if t['id'] == timer_id), None)
        
        if not timer:
            return jsonify({'success': False, 'error': 'Timer not found'}), 404
        
        # Start the timer
        timer_manager.start_timer(timer_id, room_id)
        room.active_timer_id = timer_id
        
        # AI analysis and suggestions
        ai_suggestions = ai_engine.analyze_timer_start(timer)
        room.ai_insights.update(ai_suggestions)
        
        # Broadcast to all viewers
        socketio.emit('timer_started', {
            'timer_id': timer_id,
            'ai_suggestions': ai_suggestions
        }, to=room_id)
        
        return jsonify({
            'success': True,
            'ai_suggestions': ai_suggestions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice-command', methods=['POST'])
def process_voice_command():
    """Process voice commands with AI understanding"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        audio_data = data.get('audio_data')
        command_text = data.get('command_text')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        # Process voice command with AI
        ai_response = ai_engine.process_voice_command(command_text, rooms[room_id])
        
        # Execute the command
        result = execute_ai_command(ai_response, room_id)
        
        # Broadcast to all viewers
        socketio.emit('voice_command_processed', {
            'command': command_text,
            'response': ai_response,
            'result': result
        }, to=room_id)
        
        return jsonify({
            'success': True,
            'ai_response': ai_response,
            'result': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze-content', methods=['POST'])
def analyze_presentation_content():
    """Analyze presentation content with AI"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        content = data.get('content')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        # AI content analysis
        analysis = ai_engine.analyze_presentation_content(content)
        
        # Update room with AI insights
        rooms[room_id].ai_insights.update(analysis)
        
        # Generate suggested timers based on content
        suggested_timers = ai_engine.suggest_timers_from_content(content)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'suggested_timers': suggested_timers
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/suggestions', methods=['GET'])
def get_ai_suggestions():
    """Get AI suggestions for the current presentation"""
    try:
        room_id = request.args.get('room_id')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        room = rooms[room_id]
        suggestions = ai_engine.generate_suggestions(room)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/messages', methods=['POST'])
def send_message():
    """Send a message with AI enhancement"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        message_data = data.get('message')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        # Enhance message with AI
        enhanced_message = ai_engine.enhance_message(message_data)
        
        message_id = str(uuid.uuid4())
        enhanced_message['id'] = message_id
        enhanced_message['timestamp'] = datetime.now().isoformat()
        
        rooms[room_id].messages.append(enhanced_message)
        
        # Broadcast to all viewers
        socketio.emit('message_sent', enhanced_message, to=room_id)
        
        return jsonify({
            'success': True,
            'message': enhanced_message
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# WebSocket Events
@socketio.on('join')
def on_join(data):
    """Handle viewer joining a room"""
    room_id = data['room_id']
    join_room(room_id)
    
    if room_id in rooms:
        rooms[room_id].viewers += 1
        emit('viewer_count_updated', {'count': rooms[room_id].viewers}, to=room_id)

@socketio.on('leave')
def on_leave(data):
    """Handle viewer leaving a room"""
    room_id = data['room_id']
    leave_room(room_id)
    
    if room_id in rooms:
        rooms[room_id].viewers = max(0, rooms[room_id].viewers - 1)
        emit('viewer_count_updated', {'count': rooms[room_id].viewers}, to=room_id)

@socketio.on('timer_update')
def on_timer_update(data):
    """Handle timer updates"""
    room_id = data['room_id']
    timer_data = data['timer']
    
    # AI monitoring of timer progress
    if room_id in rooms:
        ai_insights = ai_engine.monitor_timer_progress(timer_data, rooms[room_id])
        rooms[room_id].ai_insights.update(ai_insights)
        
        # Broadcast with AI insights
        emit('timer_updated', {
            'timer': timer_data,
            'ai_insights': ai_insights
        }, to=room_id)

# Utility Functions
def generate_room_id():
    """Generate a unique 8-character room ID"""
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

def execute_ai_command(ai_response, room_id):
    """Execute AI-suggested commands"""
    command_type = ai_response.get('command_type')
    room = rooms[room_id]
    
    if command_type == 'start_timer':
        timer_id = ai_response.get('timer_id')
        if timer_id:
            timer_manager.start_timer(timer_id, room_id)
            room.active_timer_id = timer_id
            return {'action': 'timer_started', 'timer_id': timer_id}
    
    elif command_type == 'pause_timer':
        if room.active_timer_id:
            timer_manager.pause_timer(room.active_timer_id)
            return {'action': 'timer_paused', 'timer_id': room.active_timer_id}
    
    elif command_type == 'next_timer':
        # Find next timer in sequence
        current_index = next((i for i, t in enumerate(room.timers) 
                           if t['id'] == room.active_timer_id), -1)
        if current_index < len(room.timers) - 1:
            next_timer = room.timers[current_index + 1]
            timer_manager.start_timer(next_timer['id'], room_id)
            room.active_timer_id = next_timer['id']
            return {'action': 'next_timer_started', 'timer_id': next_timer['id']}
    
    return {'action': 'command_executed', 'command_type': command_type}

# Background task for AI monitoring
def ai_monitoring_task():
    """Background task for continuous AI monitoring"""
    while True:
        try:
            for room_id, room in rooms.items():
                if room.active_timer_id:
                    # Continuous AI monitoring
                    insights = ai_engine.continuous_monitoring(room)
                    room.ai_insights.update(insights)
                    
                    # Broadcast insights if significant
                    if insights.get('significant_change'):
                        socketio.emit('ai_insights_updated', insights, to=room_id)
            
            time.sleep(30)  # Check every 30 seconds
        except Exception as e:
            print(f"AI monitoring error: {e}")
            time.sleep(60)

# Start AI monitoring in background
if __name__ == '__main__':
    # Start AI monitoring thread
    monitoring_thread = threading.Thread(target=ai_monitoring_task, daemon=True)
    monitoring_thread.start()
    
    # Run the Flask app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 