#!/usr/bin/env python3
"""
🎤 Voice Processor for StageTimer Pro
Handles speech recognition and text-to-speech functionality
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
from typing import Optional, Callable, Dict, List
import json
import os

class VoiceProcessor:
    def __init__(self):
        """Initialize the voice processor"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Voice settings
        self.voice_settings = {
            'rate': 150,      # Speed of speech
            'volume': 0.8,    # Volume level
            'voice_id': None  # Voice ID for different voices
        }
        
        # Recognition settings
        self.recognition_settings = {
            'language': 'en-US',
            'timeout': 5,     # Seconds to wait for speech
            'phrase_time_limit': 10,  # Maximum phrase length
            'ambient_noise_adjustment': True
        }
        
        # Audio queue for processing
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.callback = None
        
        # Initialize voice engine
        self._setup_voice_engine()
        
        # Start background processing
        self.processing_thread = threading.Thread(target=self._process_audio_queue, daemon=True)
        self.processing_thread.start()

    def _setup_voice_engine(self):
        """Setup the text-to-speech engine"""
        try:
            # Configure voice settings
            self.engine.setProperty('rate', self.voice_settings['rate'])
            self.engine.setProperty('volume', self.voice_settings['volume'])
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a good voice (prefer female voices for clarity)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        self.voice_settings['voice_id'] = voice.id
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
                    self.voice_settings['voice_id'] = voices[0].id
            
        except Exception as e:
            print(f"Error setting up voice engine: {e}")

    def start_listening(self, callback: Callable[[str], None]):
        """Start listening for voice commands"""
        self.callback = callback
        self.is_listening = True
        
        # Start listening thread
        listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        listen_thread.start()
        
        return True

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.callback = None

    def _listen_loop(self):
        """Main listening loop"""
        with sr.Microphone() as source:
            # Adjust for ambient noise
            if self.recognition_settings['ambient_noise_adjustment']:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_listening:
                try:
                    # Listen for audio
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.recognition_settings['timeout'],
                        phrase_time_limit=self.recognition_settings['phrase_time_limit']
                    )
                    
                    # Add to processing queue
                    self.audio_queue.put(audio)
                    
                except sr.WaitTimeoutError:
                    # No speech detected, continue listening
                    continue
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    continue
                except Exception as e:
                    print(f"Error in listening loop: {e}")
                    time.sleep(1)

    def _process_audio_queue(self):
        """Process audio from the queue"""
        while True:
            try:
                # Get audio from queue
                audio = self.audio_queue.get(timeout=1)
                
                # Recognize speech
                text = self._recognize_speech(audio)
                
                if text and self.callback:
                    # Process the recognized text
                    self.callback(text)
                
            except queue.Empty:
                # No audio in queue, continue
                continue
            except Exception as e:
                print(f"Error processing audio: {e}")

    def _recognize_speech(self, audio) -> Optional[str]:
        """Recognize speech from audio"""
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(
                audio,
                language=self.recognition_settings['language']
            )
            
            # Handle case where text might be a list
            if isinstance(text, list):
                text = text[0] if text else ""
            
            return text.lower().strip()
            
        except sr.UnknownValueError:
            # Speech was unintelligible
            return None
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            return None

    def speak(self, text: str, interrupt: bool = True):
        """Speak text using text-to-speech"""
        try:
            if interrupt:
                # Stop any current speech
                self.engine.stop()
            
            # Speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Error speaking text: {e}")

    def speak_async(self, text: str):
        """Speak text asynchronously"""
        speak_thread = threading.Thread(target=self.speak, args=(text, True), daemon=True)
        speak_thread.start()

    def process_voice_command(self, command_text: str) -> Dict:
        """Process a voice command and return structured data"""
        try:
            # Common voice command patterns
            command_patterns = {
                'start_timer': [
                    r'start\s+(?:the\s+)?(.+?)(?:\s+timer)?',
                    r'begin\s+(?:the\s+)?(.+?)(?:\s+timer)?',
                    r'run\s+(?:the\s+)?(.+?)(?:\s+timer)?'
                ],
                'pause_timer': [
                    r'pause\s+(?:the\s+)?timer',
                    r'stop\s+(?:the\s+)?timer',
                    r'hold\s+(?:the\s+)?timer'
                ],
                'resume_timer': [
                    r'resume\s+(?:the\s+)?timer',
                    r'continue\s+(?:the\s+)?timer',
                    r'unpause\s+(?:the\s+)?timer'
                ],
                'next_timer': [
                    r'next\s+(?:timer|section)',
                    r'move\s+to\s+next',
                    r'advance\s+(?:timer|section)'
                ],
                'show_time': [
                    r'(?:what\s+)?time\s+(?:is\s+)?left',
                    r'(?:how\s+)?much\s+time\s+(?:is\s+)?remaining',
                    r'show\s+(?:the\s+)?time'
                ],
                'add_timer': [
                    r'add\s+(?:a\s+)?timer\s+(?:called\s+)?(.+)',
                    r'create\s+(?:a\s+)?timer\s+(?:called\s+)?(.+)',
                    r'new\s+timer\s+(?:called\s+)?(.+)'
                ]
            }
            
            # Check each command type
            for command_type, patterns in command_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, command_text, re.IGNORECASE)
                    if match:
                        result = {
                            'command_type': command_type,
                            'confidence': 0.9,
                            'original_text': command_text,
                            'extracted_data': match.groups() if match.groups() else []
                        }
                        
                        # Add specific data based on command type
                        if command_type == 'start_timer' and match.groups():
                            result['timer_name'] = match.group(1).strip()
                        elif command_type == 'add_timer' and match.groups():
                            result['timer_name'] = match.group(1).strip()
                        
                        return result
            
            # No pattern matched, return unknown command
            return {
                'command_type': 'unknown',
                'confidence': 0.0,
                'original_text': command_text,
                'error': 'Command not recognized'
            }
            
        except Exception as e:
            return {
                'command_type': 'error',
                'confidence': 0.0,
                'original_text': command_text,
                'error': str(e)
            }

    def get_voice_feedback(self, command_result: Dict) -> str:
        """Generate voice feedback for command results"""
        try:
            command_type = command_result.get('command_type')
            
            feedback_messages = {
                'start_timer': 'Starting the timer',
                'pause_timer': 'Timer paused',
                'resume_timer': 'Timer resumed',
                'next_timer': 'Moving to next timer',
                'show_time': 'Checking remaining time',
                'add_timer': 'Adding new timer',
                'unknown': 'I did not understand that command',
                'error': 'There was an error processing your command'
            }
            
            return feedback_messages.get(str(command_type or 'unknown'), 'Command processed')
            
        except Exception as e:
            return f"Error generating feedback: {e}"

    def set_voice_settings(self, settings: Dict):
        """Update voice settings"""
        try:
            # Update settings
            self.voice_settings.update(settings)
            
            # Apply to engine
            if 'rate' in settings:
                self.engine.setProperty('rate', settings['rate'])
            if 'volume' in settings:
                self.engine.setProperty('volume', settings['volume'])
            if 'voice_id' in settings and settings['voice_id']:
                self.engine.setProperty('voice', settings['voice_id'])
                
        except Exception as e:
            print(f"Error updating voice settings: {e}")

    def set_recognition_settings(self, settings: Dict):
        """Update speech recognition settings"""
        try:
            self.recognition_settings.update(settings)
        except Exception as e:
            print(f"Error updating recognition settings: {e}")

    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices"""
        try:
            voices = self.engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages if hasattr(voice, 'languages') else [],
                    'gender': voice.gender if hasattr(voice, 'gender') else 'unknown'
                }
                for voice in voices
            ]
        except Exception as e:
            print(f"Error getting available voices: {e}")
            return []

    def test_microphone(self) -> Dict:
        """Test microphone functionality"""
        try:
            with sr.Microphone() as source:
                # Test ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                # Test listening
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                
                # Test recognition
                text = self.recognizer.recognize_google(audio)
                
                return {
                    'success': True,
                    'message': 'Microphone test successful',
                    'recognized_text': text
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Microphone test failed: {e}',
                'error': str(e)
            }

    def speak_timer_status(self, timer_data: Dict):
        """Speak timer status information"""
        try:
            timer_name = timer_data.get('name', 'Timer')
            current_time = timer_data.get('current_time', 0)
            state = timer_data.get('state', 'stopped')
            
            # Format time
            minutes = current_time // 60
            seconds = current_time % 60
            
            if state == 'running':
                status_text = f"{timer_name} is running. {minutes} minutes and {seconds} seconds remaining."
            elif state == 'paused':
                status_text = f"{timer_name} is paused at {minutes} minutes and {seconds} seconds."
            elif state == 'completed':
                status_text = f"{timer_name} has completed."
            else:
                status_text = f"{timer_name} is stopped."
            
            self.speak_async(status_text)
            
        except Exception as e:
            print(f"Error speaking timer status: {e}")

    def speak_warning(self, warning_data: Dict):
        """Speak warning messages"""
        try:
            timer_name = warning_data.get('timer_name', 'Timer')
            remaining_time = warning_data.get('remaining_time', 0)
            
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            
            if minutes > 0:
                warning_text = f"Warning: {timer_name} has {minutes} minutes and {seconds} seconds remaining."
            else:
                warning_text = f"Warning: {timer_name} has {seconds} seconds remaining."
            
            self.speak_async(warning_text)
            
        except Exception as e:
            print(f"Error speaking warning: {e}")

    def cleanup(self):
        """Clean up voice processor resources"""
        try:
            self.stop_listening()
            self.engine.stop()
        except Exception as e:
            print(f"Error cleaning up voice processor: {e}")

# Import regex for pattern matching
import re 