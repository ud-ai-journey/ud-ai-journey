#!/usr/bin/env python3
"""
⏰ Timer Manager for StageTimer Pro
Handles timer operations, state management, and synchronization
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import json

class TimerManager:
    def __init__(self):
        """Initialize the timer manager"""
        self.active_timers = {}  # timer_id -> timer_data
        self.timer_threads = {}  # timer_id -> thread
        self.callbacks = {}  # timer_id -> callback functions
        self.lock = threading.Lock()
        
        # Timer states
        self.STATES = {
            'stopped': 'stopped',
            'running': 'running',
            'paused': 'paused',
            'completed': 'completed'
        }

    def start_timer(self, timer_id: str, room_id: str, callback: Optional[Callable] = None):
        """Start a timer with optional callback"""
        with self.lock:
            if timer_id in self.active_timers:
                # Timer already exists, resume if paused
                timer_data = self.active_timers[timer_id]
                if timer_data['state'] == self.STATES['paused']:
                    self._resume_timer(timer_id)
                return
            
            # Create new timer thread
            timer_thread = threading.Thread(
                target=self._timer_loop,
                args=(timer_id, room_id),
                daemon=True
            )
            
            self.timer_threads[timer_id] = timer_thread
            if callback:
                self.callbacks[timer_id] = callback
            
            timer_thread.start()

    def pause_timer(self, timer_id: str):
        """Pause an active timer"""
        with self.lock:
            if timer_id in self.active_timers:
                timer_data = self.active_timers[timer_id]
                if timer_data['state'] == self.STATES['running']:
                    timer_data['state'] = self.STATES['paused']
                    timer_data['paused_at'] = time.time()
                    self._notify_timer_update(timer_id)

    def stop_timer(self, timer_id: str):
        """Stop and reset a timer"""
        with self.lock:
            if timer_id in self.active_timers:
                timer_data = self.active_timers[timer_id]
                timer_data['state'] = self.STATES['stopped']
                timer_data['current_time'] = timer_data['duration']
                timer_data['start_time'] = None
                timer_data['paused_at'] = None
                self._notify_timer_update(timer_id)

    def reset_timer(self, timer_id: str):
        """Reset timer to initial state"""
        with self.lock:
            if timer_id in self.active_timers:
                timer_data = self.active_timers[timer_id]
                timer_data['current_time'] = timer_data['duration']
                timer_data['state'] = self.STATES['stopped']
                timer_data['start_time'] = None
                timer_data['paused_at'] = None
                self._notify_timer_update(timer_id)

    def get_timer_state(self, timer_id: str) -> Optional[Dict]:
        """Get current timer state"""
        with self.lock:
            return self.active_timers.get(timer_id)

    def get_all_timers(self) -> List[Dict]:
        """Get all active timers"""
        with self.lock:
            return list(self.active_timers.values())

    def create_timer(self, timer_data: Dict) -> Optional[str]:
        """Create a new timer"""
        timer_id = timer_data.get('id')
        if not timer_id:
            return None
        
        with self.lock:
            # Initialize timer state
            timer_state = {
                'id': timer_id,
                'name': timer_data.get('name', 'Untitled Timer'),
                'duration': timer_data.get('duration', 0),
                'current_time': timer_data.get('duration', 0),
                'type': timer_data.get('type', 'countdown'),
                'state': self.STATES['stopped'],
                'warning_times': timer_data.get('warning_times', []),
                'start_time': None,
                'paused_at': None,
                'created_at': datetime.now().isoformat(),
                'ai_generated': timer_data.get('ai_generated', False),
                'ai_suggestions': timer_data.get('ai_suggestions', [])
            }
            
            self.active_timers[timer_id] = timer_state
            return timer_id

    def update_timer(self, timer_id: str, updates: Dict):
        """Update timer properties"""
        with self.lock:
            if timer_id in self.active_timers:
                timer_data = self.active_timers[timer_id]
                
                # Only allow updates when timer is stopped
                if timer_data['state'] == self.STATES['stopped']:
                    for key, value in updates.items():
                        if key in ['name', 'duration', 'type', 'warning_times']:
                            timer_data[key] = value
                            if key == 'duration':
                                timer_data['current_time'] = value
                    
                    self._notify_timer_update(timer_id)

    def delete_timer(self, timer_id: str):
        """Delete a timer"""
        with self.lock:
            if timer_id in self.active_timers:
                # Stop the timer thread if running
                if timer_id in self.timer_threads:
                    self.active_timers[timer_id]['state'] = self.STATES['stopped']
                    time.sleep(0.1)  # Give thread time to stop
                
                # Clean up
                del self.active_timers[timer_id]
                if timer_id in self.timer_threads:
                    del self.timer_threads[timer_id]
                if timer_id in self.callbacks:
                    del self.callbacks[timer_id]

    def _timer_loop(self, timer_id: str, room_id: str):
        """Main timer loop"""
        while True:
            with self.lock:
                if timer_id not in self.active_timers:
                    break
                
                timer_data = self.active_timers[timer_id]
                
                if timer_data['state'] == self.STATES['running']:
                    # Update timer
                    self._update_timer_time(timer_id)
                    
                    # Check for warnings
                    self._check_warnings(timer_id)
                    
                    # Check for completion
                    if self._is_timer_complete(timer_id):
                        self._handle_timer_completion(timer_id, room_id)
                        break
                    
                    # Notify update
                    self._notify_timer_update(timer_id)
                
                elif timer_data['state'] == self.STATES['paused']:
                    # Timer is paused, just wait
                    pass
                
                elif timer_data['state'] == self.STATES['stopped']:
                    # Timer stopped, exit loop
                    break
            
            time.sleep(1)  # Update every second

    def _update_timer_time(self, timer_id: str):
        """Update timer current time"""
        timer_data = self.active_timers[timer_id]
        
        if timer_data['type'] == 'countdown':
            # Countdown timer
            if timer_data['current_time'] > 0:
                timer_data['current_time'] -= 1
        else:
            # Count up timer
            timer_data['current_time'] += 1

    def _check_warnings(self, timer_id: str):
        """Check if warning times have been reached"""
        timer_data = self.active_timers[timer_id]
        current_time = timer_data['current_time']
        
        for warning_time in timer_data['warning_times']:
            if current_time == warning_time:
                self._trigger_warning(timer_id, warning_time)

    def _is_timer_complete(self, timer_id: str) -> bool:
        """Check if timer has completed"""
        timer_data = self.active_timers[timer_id]
        
        if timer_data['type'] == 'countdown':
            return timer_data['current_time'] <= 0
        else:
            return timer_data['current_time'] >= timer_data['duration']

    def _handle_timer_completion(self, timer_id: str, room_id: str):
        """Handle timer completion"""
        timer_data = self.active_timers[timer_id]
        timer_data['state'] = self.STATES['completed']
        
        # Trigger completion callback
        if timer_id in self.callbacks:
            try:
                self.callbacks[timer_id](timer_data, room_id)
            except Exception as e:
                print(f"Error in timer completion callback: {e}")
        
        # Notify completion
        self._notify_timer_completion(timer_id, room_id)

    def _trigger_warning(self, timer_id: str, warning_time: int):
        """Trigger a warning notification"""
        timer_data = self.active_timers[timer_id]
        
        warning_data = {
            'timer_id': timer_id,
            'timer_name': timer_data['name'],
            'warning_time': warning_time,
            'remaining_time': timer_data['current_time'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Notify warning
        self._notify_warning(warning_data)

    def _resume_timer(self, timer_id: str):
        """Resume a paused timer"""
        timer_data = self.active_timers[timer_id]
        
        if timer_data['state'] == self.STATES['paused']:
            timer_data['state'] = self.STATES['running']
            timer_data['paused_at'] = None
            self._notify_timer_update(timer_id)

    def _notify_timer_update(self, timer_id: str):
        """Notify about timer update"""
        timer_data = self.active_timers[timer_id]
        
        # Create update notification
        update_data = {
            'timer_id': timer_id,
            'timer_data': timer_data.copy(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Call callback if exists
        if timer_id in self.callbacks:
            try:
                self.callbacks[timer_id](update_data)
            except Exception as e:
                print(f"Error in timer update callback: {e}")

    def _notify_timer_completion(self, timer_id: str, room_id: str):
        """Notify about timer completion"""
        timer_data = self.active_timers[timer_id]
        
        completion_data = {
            'timer_id': timer_id,
            'timer_name': timer_data['name'],
            'completion_time': datetime.now().isoformat(),
            'room_id': room_id
        }
        
        # Call callback if exists
        if timer_id in self.callbacks:
            try:
                self.callbacks[timer_id](completion_data, room_id)
            except Exception as e:
                print(f"Error in timer completion callback: {e}")

    def _notify_warning(self, warning_data: Dict):
        """Notify about warning"""
        # Call callback if exists
        timer_id = warning_data['timer_id']
        if timer_id in self.callbacks:
            try:
                self.callbacks[timer_id](warning_data)
            except Exception as e:
                print(f"Error in warning callback: {e}")

    def format_time(self, seconds: int) -> str:
        """Format seconds into MM:SS or HH:MM:SS"""
        if seconds < 0:
            seconds = 0
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def parse_duration(self, duration_input: str) -> Optional[int]:
        """Parse duration input into seconds"""
        try:
            # Handle different formats: "15:30", "1:30:45", "930"
            if ':' in duration_input:
                parts = duration_input.split(':')
                if len(parts) == 2:  # MM:SS
                    minutes, seconds = map(int, parts)
                    return minutes * 60 + seconds
                elif len(parts) == 3:  # HH:MM:SS
                    hours, minutes, seconds = map(int, parts)
                    return hours * 3600 + minutes * 60 + seconds
            else:
                # Assume seconds
                return int(duration_input)
        except ValueError:
            return None

    def get_timer_progress(self, timer_id: str) -> float:
        """Get timer progress as percentage"""
        with self.lock:
            if timer_id not in self.active_timers:
                return 0.0
            
            timer_data = self.active_timers[timer_id]
            duration = timer_data['duration']
            
            if duration == 0:
                return 0.0
            
            if timer_data['type'] == 'countdown':
                current = timer_data['current_time']
                return max(0.0, (duration - current) / duration)
            else:
                current = timer_data['current_time']
                return min(1.0, current / duration)

    def get_next_timer(self, current_timer_id: str, timers: List[Dict]) -> Optional[Dict]:
        """Get the next timer in sequence"""
        try:
            current_index = next((i for i, t in enumerate(timers) 
                               if t['id'] == current_timer_id), -1)
            
            if current_index >= 0 and current_index < len(timers) - 1:
                return timers[current_index + 1]
            
            return None
        except Exception as e:
            print(f"Error getting next timer: {e}")
            return None

    def cleanup(self):
        """Clean up all timers and threads"""
        with self.lock:
            # Stop all timers
            for timer_id in list(self.active_timers.keys()):
                self.stop_timer(timer_id)
            
            # Wait for threads to finish
            for thread in self.timer_threads.values():
                thread.join(timeout=1.0)
            
            # Clear all data
            self.active_timers.clear()
            self.timer_threads.clear()
            self.callbacks.clear() 