#!/usr/bin/env python3
"""
🤖 AI Engine for StageTimer Pro
Advanced AI functionality for intelligent presentation management
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import openai
from textblob import TextBlob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AIEngine:
    def __init__(self):
        """Initialize the AI engine with OpenAI and other AI components"""
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # AI configuration
        self.config = {
            'max_tokens': 150,
            'temperature': 0.7,
            'model': 'gpt-3.5-turbo'
        }
    
    def _parse_ai_response(self, response) -> dict:
        """Safely parse AI response content"""
        content = response.choices[0].message.content
        if not content:
            raise ValueError("AI response content is empty")
        return json.loads(content)
        
        # Presentation patterns and insights
        self.presentation_patterns = {
            'opening': ['welcome', 'introduction', 'agenda', 'overview'],
            'main_content': ['analysis', 'data', 'results', 'findings'],
            'interactive': ['questions', 'discussion', 'feedback', 'q&a'],
            'closing': ['summary', 'conclusion', 'next_steps', 'thank_you']
        }
        
        # Timer optimization rules
        self.timer_rules = {
            'short_presentation': {'min': 300, 'max': 900, 'warnings': [120, 60, 30]},
            'medium_presentation': {'min': 900, 'max': 1800, 'warnings': [180, 120, 60, 30]},
            'long_presentation': {'min': 1800, 'max': 3600, 'warnings': [300, 180, 120, 60, 30]},
            'workshop': {'min': 1800, 'max': 7200, 'warnings': [600, 300, 180, 120, 60]}
        }

    def suggest_default_timers(self) -> List[Dict]:
        """Suggest default timers based on common presentation patterns"""
        try:
            prompt = """
            Suggest 3-4 default timers for a professional presentation. 
            Include opening, main content, Q&A, and closing sections.
            Return as JSON array with: name, duration (seconds), type, warning_times
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            # Parse AI response
            content = response.choices[0].message.content
            if not content:
                raise ValueError("AI response content is empty")
            timers = json.loads(content)
            
            # Add IDs and metadata
            for i, timer in enumerate(timers):
                timer['id'] = f'default_timer_{i+1}'
                timer['created_at'] = datetime.now().isoformat()
                timer['ai_generated'] = True
                
            return timers
            
        except Exception as e:
            print(f"Error suggesting default timers: {e}")
            # Fallback to predefined timers
            return [
                {
                    'id': 'default_timer_1',
                    'name': 'Opening & Introduction',
                    'duration': 300,
                    'type': 'countdown',
                    'warning_times': [120, 60, 30],
                    'created_at': datetime.now().isoformat(),
                    'ai_generated': True
                },
                {
                    'id': 'default_timer_2',
                    'name': 'Main Presentation',
                    'duration': 900,
                    'type': 'countdown',
                    'warning_times': [180, 120, 60, 30],
                    'created_at': datetime.now().isoformat(),
                    'ai_generated': True
                },
                {
                    'id': 'default_timer_3',
                    'name': 'Q&A Session',
                    'duration': 600,
                    'type': 'countdown',
                    'warning_times': [120, 60, 30],
                    'created_at': datetime.now().isoformat(),
                    'ai_generated': True
                }
            ]

    def enhance_timer_creation(self, timer_data: Dict) -> Dict:
        """Enhance timer creation with AI suggestions"""
        try:
            # Analyze timer name for better suggestions
            name = timer_data.get('name', '')
            duration = timer_data.get('duration', 0)
            
            # AI analysis of timer name
            analysis_prompt = f"""
            Analyze this timer: "{name}" with duration {duration} seconds.
            Suggest improvements for:
            1. Better name if needed
            2. Optimal warning times
            3. Timer type (countdown/countup)
            4. Additional features
            
            Return as JSON with: enhanced_name, warning_times, timer_type, suggestions
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("AI response content is empty")
            ai_suggestions = json.loads(content)
            
            # Apply AI enhancements
            enhanced_timer = timer_data.copy()
            enhanced_timer['name'] = ai_suggestions.get('enhanced_name', name)
            enhanced_timer['warning_times'] = ai_suggestions.get('warning_times', [])
            enhanced_timer['type'] = ai_suggestions.get('timer_type', 'countdown')
            enhanced_timer['ai_suggestions'] = ai_suggestions.get('suggestions', [])
            
            return enhanced_timer
            
        except Exception as e:
            print(f"Error enhancing timer: {e}")
            return timer_data

    def suggest_warning_times(self, duration: int) -> List[int]:
        """Suggest optimal warning times based on duration"""
        try:
            # AI-powered warning time suggestions
            prompt = f"""
            For a {duration}-second timer, suggest optimal warning times.
            Consider presentation flow and audience engagement.
            Return as JSON array of seconds.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            
            warnings = self._parse_ai_response(response)
            return sorted(warnings, reverse=True)
            
        except Exception as e:
            print(f"Error suggesting warning times: {e}")
            # Fallback logic
            if duration <= 300:  # 5 minutes
                return [60, 30, 10]
            elif duration <= 900:  # 15 minutes
                return [120, 60, 30]
            elif duration <= 1800:  # 30 minutes
                return [180, 120, 60, 30]
            else:  # 30+ minutes
                return [300, 180, 120, 60, 30]

    def process_voice_command(self, command_text: str, room) -> Dict:
        """Process voice commands with AI understanding"""
        try:
            # Analyze command intent
            prompt = f"""
            Analyze this voice command: "{command_text}"
            
            Determine the intent and return JSON with:
            - command_type: start_timer, pause_timer, stop_timer, next_timer, show_time, etc.
            - timer_id: if applicable
            - confidence: 0-1 score
            - suggested_response: natural language response
            - additional_actions: any extra actions needed
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            ai_analysis = self._parse_ai_response(response)
            
            # Enhance with room context
            if ai_analysis.get('command_type') == 'start_timer' and not ai_analysis.get('timer_id'):
                # Find best matching timer
                timer_id = self._find_best_timer_match(command_text, room.timers)
                ai_analysis['timer_id'] = timer_id
            
            return ai_analysis
            
        except Exception as e:
            print(f"Error processing voice command: {e}")
            return {
                'command_type': 'unknown',
                'confidence': 0.0,
                'suggested_response': 'I did not understand that command. Please try again.',
                'error': str(e)
            }

    def analyze_timer_start(self, timer: Dict) -> Dict:
        """Analyze timer start and provide AI insights"""
        try:
            prompt = f"""
            Analyze this timer starting: "{timer['name']}" ({timer['duration']} seconds)
            
            Provide insights and suggestions:
            1. Speaking pace recommendations
            2. Audience engagement tips
            3. Time management advice
            4. Potential issues to watch for
            
            Return as JSON with: insights, recommendations, warnings
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.4
            )
            
            analysis = self._parse_ai_response(response)
            
            # Add calculated metrics
            analysis['estimated_speaking_pace'] = self._calculate_speaking_pace(timer)
            analysis['audience_attention_curve'] = self._generate_attention_curve(timer['duration'])
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing timer start: {e}")
            return {
                'insights': ['Timer started successfully'],
                'recommendations': ['Keep track of time'],
                'warnings': []
            }

    def analyze_presentation_content(self, content: str) -> Dict:
        """Analyze presentation content for timing and structure"""
        try:
            # Sentiment analysis (simplified)
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
            words = content.lower().split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            sentiment = (positive_count - negative_count) / max(len(words), 1)
            
            # Content complexity analysis
            words = content.split()
            avg_word_length = np.mean([len(word) for word in words])
            complexity_score = (avg_word_length * len(words)) / 1000
            
            # AI content analysis
            prompt = f"""
            Analyze this presentation content for timing and structure:
            
            {content[:1000]}...
            
            Provide analysis for:
            1. Estimated presentation duration
            2. Recommended breaks
            3. Content complexity
            4. Audience engagement factors
            5. Suggested timer structure
            
            Return as JSON with detailed analysis.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3
            )
            
            ai_analysis = self._parse_ai_response(response)
            
            # Combine AI and statistical analysis
            analysis = {
                'sentiment_score': sentiment,
                'complexity_score': complexity_score,
                'word_count': len(words),
                'estimated_duration': ai_analysis.get('estimated_duration', 900),
                'recommended_breaks': ai_analysis.get('recommended_breaks', []),
                'content_structure': ai_analysis.get('content_structure', {}),
                'engagement_factors': ai_analysis.get('engagement_factors', []),
                'suggested_timers': ai_analysis.get('suggested_timers', [])
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return {
                'sentiment_score': 0,
                'complexity_score': 0,
                'word_count': len(content.split()),
                'estimated_duration': 900,
                'error': str(e)
            }

    def suggest_timers_from_content(self, content: str) -> List[Dict]:
        """Suggest timers based on content analysis"""
        try:
            analysis = self.analyze_presentation_content(content)
            
            # Generate timers based on content structure
            suggested_timers = []
            
            # Opening timer
            suggested_timers.append({
                'name': 'Opening & Introduction',
                'duration': min(300, analysis['estimated_duration'] // 4),
                'type': 'countdown',
                'warning_times': [60, 30, 10],
                'ai_generated': True
            })
            
            # Main content timer
            main_duration = analysis['estimated_duration'] - 600  # Subtract opening and closing
            if main_duration > 0:
                suggested_timers.append({
                    'name': 'Main Presentation',
                    'duration': main_duration,
                    'type': 'countdown',
                    'warning_times': self.suggest_warning_times(main_duration),
                    'ai_generated': True
                })
            
            # Q&A timer
            suggested_timers.append({
                'name': 'Q&A Session',
                'duration': 300,
                'type': 'countdown',
                'warning_times': [120, 60, 30],
                'ai_generated': True
            })
            
            return suggested_timers
            
        except Exception as e:
            print(f"Error suggesting timers from content: {e}")
            return []

    def monitor_timer_progress(self, timer_data: Dict, room) -> Dict:
        """Monitor timer progress and provide AI insights"""
        try:
            current_time = timer_data.get('current_time', 0)
            duration = timer_data.get('duration', 0)
            progress_percentage = (duration - current_time) / duration if duration > 0 else 0
            
            # AI monitoring analysis
            prompt = f"""
            Monitor timer progress: {progress_percentage:.1%} complete
            Timer: {timer_data.get('name', 'Unknown')}
            Time remaining: {current_time} seconds
            
            Provide real-time insights:
            1. Pace analysis
            2. Time management advice
            3. Audience engagement status
            4. Recommendations
            
            Return as JSON with monitoring insights.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.4
            )
            
            monitoring = self._parse_ai_response(response)
            
            # Add calculated metrics
            monitoring['progress_percentage'] = progress_percentage
            monitoring['time_remaining'] = current_time
            monitoring['pace_status'] = self._analyze_pace(current_time, duration, progress_percentage)
            
            return monitoring
            
        except Exception as e:
            print(f"Error monitoring timer progress: {e}")
            return {
                'progress_percentage': 0,
                'time_remaining': 0,
                'insights': ['Monitoring active'],
                'error': str(e)
            }

    def generate_suggestions(self, room) -> Dict:
        """Generate AI suggestions for the current presentation"""
        try:
            active_timer = next((t for t in room.timers if t['id'] == room.active_timer_id), None)
            
            if not active_timer:
                return {'suggestions': ['No active timer to analyze']}
            
            prompt = f"""
            Generate AI suggestions for current presentation state:
            
            Active Timer: {active_timer.get('name', 'Unknown')}
            Duration: {active_timer.get('duration', 0)} seconds
            AI Insights: {room.ai_insights}
            
            Provide suggestions for:
            1. Time management
            2. Audience engagement
            3. Presentation flow
            4. Next steps
            
            Return as JSON with categorized suggestions.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            suggestions = self._parse_ai_response(response)
            return suggestions
            
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return {
                'suggestions': ['AI suggestions temporarily unavailable'],
                'error': str(e)
            }

    def enhance_message(self, message_data: Dict) -> Dict:
        """Enhance message with AI improvements"""
        try:
            text = message_data.get('text', '')
            message_type = message_data.get('type', 'normal')
            
            # AI message enhancement
            prompt = f"""
            Enhance this presentation message:
            Text: "{text}"
            Type: {message_type}
            
            Improve for:
            1. Clarity and impact
            2. Professional tone
            3. Audience engagement
            4. Timing appropriateness
            
            Return as JSON with enhanced message and suggestions.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.4
            )
            
            enhancement = self._parse_ai_response(response)
            
            enhanced_message = message_data.copy()
            enhanced_message['enhanced_text'] = enhancement.get('enhanced_text', text)
            enhanced_message['ai_suggestions'] = enhancement.get('suggestions', [])
            # Simple sentiment calculation
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
            words = text.lower().split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            enhanced_message['sentiment_score'] = (positive_count - negative_count) / max(len(words), 1)
            
            return enhanced_message
            
        except Exception as e:
            print(f"Error enhancing message: {e}")
            return message_data

    def continuous_monitoring(self, room) -> Dict:
        """Continuous AI monitoring of presentation"""
        try:
            # Analyze overall presentation health
            active_timer = next((t for t in room.timers if t['id'] == room.active_timer_id), None)
            
            if not active_timer:
                return {'status': 'no_active_timer'}
            
            # Calculate various metrics
            total_duration = sum(t.get('duration', 0) for t in room.timers)
            completed_duration = sum(t.get('duration', 0) - t.get('current_time', 0) 
                                   for t in room.timers if t.get('state') == 'completed')
            
            progress = completed_duration / total_duration if total_duration > 0 else 0
            
            # AI health check
            prompt = f"""
            Perform presentation health check:
            
            Progress: {progress:.1%}
            Active Timer: {active_timer.get('name', 'Unknown')}
            Viewers: {room.viewers}
            Messages: {len(room.messages)}
            
            Assess:
            1. Overall presentation health
            2. Time management effectiveness
            3. Audience engagement level
            4. Potential issues
            
            Return as JSON with health assessment.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.3
            )
            
            health_check = self._parse_ai_response(response)
            
            # Add calculated metrics
            health_check['overall_progress'] = progress
            health_check['viewer_engagement'] = room.viewers
            health_check['message_frequency'] = len(room.messages)
            health_check['significant_change'] = self._detect_significant_changes(room)
            
            return health_check
            
        except Exception as e:
            print(f"Error in continuous monitoring: {e}")
            return {
                'status': 'monitoring_error',
                'error': str(e)
            }

    # Helper Methods
    def _find_best_timer_match(self, command_text: str, timers: List[Dict]) -> Optional[str]:
        """Find the best matching timer for a voice command"""
        if not timers:
            return None
        
        # Simple keyword matching
        command_lower = command_text.lower()
        for timer in timers:
            timer_name_lower = timer.get('name', '').lower()
            if any(word in timer_name_lower for word in command_lower.split()):
                return timer['id']
        
        # Return first timer as fallback
        return timers[0]['id'] if timers else None

    def _calculate_speaking_pace(self, timer: Dict) -> float:
        """Calculate optimal speaking pace for timer"""
        duration = timer.get('duration', 0)
        name = timer.get('name', '')
        
        # Estimate words based on timer name and duration
        estimated_words = len(name.split()) * (duration / 60) * 150  # 150 words per minute
        return estimated_words / (duration / 60) if duration > 0 else 150

    def _generate_attention_curve(self, duration: int) -> List[float]:
        """Generate audience attention curve"""
        # Simplified attention curve (highest at start, dips in middle, rises at end)
        points = []
        for i in range(0, duration, 60):  # Every minute
            progress = i / duration
            if progress < 0.2:  # Opening
                attention = 0.9
            elif progress < 0.8:  # Middle
                attention = 0.6 + 0.2 * np.sin(progress * np.pi)
            else:  # Closing
                attention = 0.8
            points.append(attention)
        return points

    def _analyze_pace(self, current_time: int, duration: int, progress: float) -> str:
        """Analyze if the presentation is on pace"""
        if duration == 0:
            return 'unknown'
        
        expected_progress = 1 - (current_time / duration)
        if abs(progress - expected_progress) < 0.1:
            return 'on_pace'
        elif progress < expected_progress:
            return 'ahead_of_schedule'
        else:
            return 'behind_schedule'

    def _detect_significant_changes(self, room) -> bool:
        """Detect if there are significant changes requiring attention"""
        # Simple heuristic - can be enhanced
        if len(room.messages) > 10:  # High message activity
            return True
        if room.viewers == 0:  # No viewers
            return True
        return False 