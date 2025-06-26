# pattern_engine.py
import json
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
import math 
from typing import List, Dict, Tuple, Optional, Any

# --- Imports ---
from data_manager import load_walk_log 
from moods import VALID_MOODS, get_mood_details 

# --- Configuration for Pattern Analysis ---
# Define time blocks for analyzing patterns (hours are 0-23)
TIME_BLOCKS = {
    "Night": (0, 3),      
    "Early Morning": (4, 7),   
    "Morning": (8, 11),        
    "Midday": (12, 13),       
    "Afternoon": (14, 17),     
    "Evening": (18, 21),       
    "Late Evening": (22, 23)   
}

# Minimum data points required for specific insights/predictions
MIN_WALKS_FOR_INSIGHTS = 3 
MIN_WALKS_FOR_PREDICTIONS = 5 

# Feedback analysis configuration
FEEDBACK_POSITIVE_THRESHOLD = 4.0  # 4-5 stars is considered positive
FEEDBACK_NEUTRAL_THRESHOLD = 3.5   # 3.5-4 is neutral
FEEDBACK_NEGATIVE_THRESHOLD = 2.5  # Below 2.5 is negative

# Recent feedback window (in days)
RECENT_FEEDBACK_WINDOW_DAYS = 30

# Mood variety settings
MIN_SESSIONS_FOR_VARIETY = 3  # Minimum sessions before considering variety
VARIETY_THRESHOLD = 0.7      # If any mood is used more than this percentage, suggest variety

class FeedbackAnalyzer:
    """Helper class to analyze feedback patterns."""
    
    def __init__(self, feedback_data: List[Dict]):
        """Initialize with feedback data."""
        self.feedback_data = feedback_data or []
        self.now = datetime.now()
    
    def get_recent_feedback(self, days: int = 30) -> List[Dict]:
        """Get feedback from the last N days."""
        cutoff = self.now - timedelta(days=days)
        return [
            f for f in self.feedback_data 
            if datetime.fromisoformat(f['timestamp']) >= cutoff
        ]
    
    def get_feedback_trend(self, window_days: int = 14) -> float:
        """Calculate the trend of feedback scores over time."""
        recent = self.get_recent_feedback(window_days)
        if len(recent) < 2:
            return 0.0
            
        # Split into two halves and compare averages
        half = len(recent) // 2
        first_half = recent[:half]
        second_half = recent[half:]
        
        avg_first = sum(f.get('rating', 0) for f in first_half) / len(first_half)
        avg_second = sum(f.get('rating', 0) for f in second_half) / len(second_half)
        
        return avg_second - avg_first  # Positive means improving, negative means declining
    
    def get_mood_effectiveness(self, min_feedback: int = 3) -> Dict[str, Dict]:
        """Calculate effectiveness metrics for each mood based on feedback."""
        mood_stats = {}
        recent_feedback = self.get_recent_feedback(RECENT_FEEDBACK_WINDOW_DAYS)
        
        for mood in VALID_MOODS:
            mood_feedback = [f for f in recent_feedback if f.get('mood') == mood]
            if len(mood_feedback) < min_feedback:
                continue
                
            ratings = [f.get('rating', 0) for f in mood_feedback]
            avg_rating = sum(ratings) / len(ratings)
            
            mood_stats[mood] = {
                'count': len(mood_feedback),
                'avg_rating': avg_rating,
                'effectiveness': self._calculate_effectiveness_score(avg_rating, len(mood_feedback))
            }
            
        return mood_stats
    
    def _calculate_effectiveness_score(self, avg_rating: float, count: int) -> float:
        """Calculate an effectiveness score that considers both rating and sample size."""
        # Base score is the average rating (0-5 scale)
        base_score = avg_rating
        
        # Apply a confidence multiplier based on sample size
        # More feedback = more confident in the score
        confidence = min(1.0, count / 10)  # Max confidence at 10+ samples
        
        # Recent feedback is more valuable
        recent_feedback = self.get_recent_feedback(7)  # Last 7 days
        recent_count = len([f for f in recent_feedback if f.get('rating', 0) >= 4])
        recency_bonus = min(0.5, recent_count * 0.1)  # Up to 0.5 bonus for recent positive feedback
        
        return (base_score * confidence) + recency_bonus

# --- Helper Functions ---
def get_time_block(hour):
    """Maps an hour (0-23) to a named time block."""
    for block_name, (start_hour, end_hour) in TIME_BLOCKS.items():
        # Check if the hour falls within the block's range
        if start_hour <= hour <= end_hour:
            return block_name
    return "Unknown Time" # Fallback if hour doesn't fit any defined block

# --- Core Analysis Function ---
def analyze_session_data(log_data: List[Dict]) -> Optional[Dict]:
    """
    Analyzes walk log data, identifying patterns, calculating statistics,
    and deriving preferences based on moods, times, and feedback.
    
    Args:
        log_data: A list of dictionaries, where each dict represents a walk session.
        
    Returns:
        A dictionary containing analyzed data, or None if input is invalid/empty.
    """
    if not log_data or not isinstance(log_data, list):
        return None
        
    # Extract feedback data for analysis
    feedback_data = []
    mood_usage = defaultdict(int)
    time_block_usage = defaultdict(int)
    mood_time_block = defaultdict(lambda: defaultdict(int))
    mood_ratings = defaultdict(list)
    recent_sessions = deque(maxlen=10)  # Track recent sessions for variety
    
    # Process each session
    for session in log_data:
        mood = session.get('mood')
        timestamp = session.get('timestamp')
        feedback = session.get('feedback')
        
        if not all([mood, timestamp]):
            continue
            
        # Track mood usage
        mood_usage[mood] += 1
        
        # Track time block usage
        session_time = datetime.fromisoformat(timestamp)
        hour = session_time.hour
        time_block = get_time_block(hour)
        time_block_usage[time_block] += 1
        
        # Track mood by time block
        mood_time_block[time_block][mood] += 1
        
        # Track feedback if available
        if feedback:
            # Handle case where feedback might be a rating number directly
            if isinstance(feedback, (int, float)):
                rating = float(feedback)
            elif isinstance(feedback, dict) and 'rating' in feedback:
                rating = float(feedback['rating'])
            else:
                # Skip invalid feedback format
                continue
                
            feedback_entry = {
                'mood': mood,
                'time_block': time_block,
                'rating': rating,
                'timestamp': timestamp
            }
            feedback_data.append(feedback_entry)
            mood_ratings[mood].append(rating)
            
        # Track recent sessions for variety
        recent_sessions.append(mood)
    
    # Calculate average ratings per mood
    avg_ratings = {}
    for mood, ratings in mood_ratings.items():
        if ratings:
            avg_ratings[mood] = sum(ratings) / len(ratings)
    
    # Calculate mood variety score
    variety_score = _calculate_variety_score(recent_sessions)
    
    # Analyze feedback patterns
    feedback_analyzer = FeedbackAnalyzer(feedback_data)
    mood_effectiveness = feedback_analyzer.get_mood_effectiveness()
    feedback_trend = feedback_analyzer.get_feedback_trend()
    
    # Prepare analysis results
    analysis = {
        'total_sessions': len(log_data),
        'mood_distribution': dict(mood_usage),
        'time_block_distribution': dict(time_block_usage),
        'mood_by_time_block': {k: dict(v) for k, v in mood_time_block.items()},
        'average_ratings': avg_ratings,
        'feedback_analysis': {
            'mood_effectiveness': mood_effectiveness,
            'recent_trend': feedback_trend,
            'total_feedback': len(feedback_data)
        },
        'variety_score': variety_score,
        'last_updated': datetime.now().isoformat()
    }
    
    return analysis

def _calculate_variety_score(recent_sessions: List[str]) -> float:
    """Calculate a variety score based on recent mood usage."""
    if not recent_sessions or len(recent_sessions) < MIN_SESSIONS_FOR_VARIETY:
        return 1.0  # Not enough data, assume good variety
        
    mood_counts = Counter(recent_sessions)
    most_common_count = max(mood_counts.values())
    variety_ratio = 1 - (most_common_count / len(recent_sessions) - 1/len(mood_counts))
    
    return max(0.0, min(1.0, variety_ratio))  # Ensure between 0 and 1

def analyze_session_data_legacy(log_data):
    """Legacy implementation of session data analysis."""
    if not log_data:
        return None 
        
    # Initialize dictionaries to store analysis results
    analysis_results = {
        "total_walks": 0,
        "mood_counts": {},
        "time_blocks": {},
        "mood_by_time": {},
        "feedback_by_mood": {},
        "feedback_scores": []
    }
    feedback_by_mood = defaultdict(lambda: {"total_score": 0.0, "count": 0})

    total_walks = len(log_data)
    
    for entry in log_data:
        mood = entry.get("mood")
        duration = entry.get("duration_minutes")
        timestamp_str = entry.get("timestamp")
        feedback = entry.get("feedback")

        if mood: mood_counts[mood] += 1
        if duration: duration_list.append(duration)
            
        if isinstance(feedback, (int, float)): 
            feedback_scores.append(float(feedback)) 

        if timestamp_str and mood: 
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                hour = timestamp.hour
                day_of_week = timestamp.strftime("%A") 
                time_block = get_time_block(hour) 
                
                mood_by_time[time_block][mood] += 1
                mood_by_day_of_week[day_of_week][mood] += 1
                    
            except ValueError:
                print(f"Warning: Could not parse timestamp '{timestamp_str}' for temporal analysis.")
            except Exception as e:
                 print(f"Warning: Error processing temporal data: {e}")
        
        if mood and isinstance(feedback, (int, float)):
            feedback_data = feedback_by_mood[mood]
            feedback_data["total_score"] += float(feedback)
            feedback_data["count"] += 1

    # --- Calculate derived statistics ---
    analysis = {
        "total_walks": total_walks,
        "most_common_mood": mood_counts.most_common(1)[0][0] if mood_counts else None,
        "average_duration": sum(duration_list) / len(duration_list) if duration_list else 0,
        "mood_distribution": dict(mood_counts), 
        "mood_by_time": {k: dict(v) for k, v in mood_by_time.items()}, 
        "mood_by_day_of_week": {k: dict(v) for k, v in mood_by_day_of_week.items()},
        "average_feedback_overall": sum(feedback_scores) / len(feedback_scores) if feedback_scores else None,
        "feedback_given_count": len(feedback_scores),
        "feedback_by_mood": {
            mood: {
                "average_feedback": data["total_score"] / data["count"] if data["count"] > 0 else 0,
                "count": data["count"]
            } for mood, data in feedback_by_mood.items()
        }
    }
    
    return analysis

def generate_insights(analysis_data):
    """Generates user-friendly insights based on analysis data."""
    if not analysis_data or analysis_data.get("total_sessions", 0) < MIN_WALKS_FOR_INSIGHTS:
        return "Not enough walk data yet to generate insights. Keep walking!"
        
    insights = []
    
    # Extract data from analysis
    mood_distribution = analysis_data.get("mood_distribution", {})
    time_block_distribution = analysis_data.get("time_block_distribution", {})
    mood_by_time = analysis_data.get("mood_by_time_block", {})
    feedback_analysis = analysis_data.get("feedback_analysis", {})
    variety_score = analysis_data.get("variety_score", 1.0)
    
    # --- Mood Popularity ---
    if mood_distribution:
        total_walks = analysis_data["total_sessions"]
        most_common_mood, most_common_count = max(
            mood_distribution.items(), 
            key=lambda x: x[1], 
            default=(None, 0)
        )
        
        if most_common_mood and total_walks > 0:
            mood_details = get_mood_details(most_common_mood)
            mood_name = mood_details.get("name", most_common_mood.title())
            percentage = (most_common_count / total_walks) * 100
            insights.append(f"Your most frequent mood is '{mood_name}' ({percentage:.0f}% of walks).")
    
    # --- Time Patterns ---
    if mood_by_time:
        for time_block, moods in mood_by_time.items():
            if moods:  # If there are moods for this time block
                most_common_mood = max(moods.items(), key=lambda x: x[1], default=(None, 0))[0]
                if most_common_mood:
                    mood_details = get_mood_details(most_common_mood)
                    mood_name = mood_details.get("name", most_common_mood.title())
                    insights.append(f"You often prefer '{mood_name}' during {time_block}.")
    
    # --- Feedback Analysis ---
    mood_effectiveness = feedback_analysis.get("mood_effectiveness", {})
    if mood_effectiveness:
        # Find most effective mood
        effective_moods = [
            (mood, data["avg_rating"], data["count"])
            for mood, data in mood_effectiveness.items()
            if data.get("count", 0) >= 3  # Only consider moods with enough data
        ]
        
        if effective_moods:
            effective_moods.sort(key=lambda x: x[1], reverse=True)
            best_mood, best_rating, best_count = effective_moods[0]
            mood_details = get_mood_details(best_mood)
            mood_name = mood_details.get("name", best_mood.title())
            insights.append(
                f"Your highest rated mood is '{mood_name}' with an average rating of {best_rating:.1f}/5.0 "
                f"(based on {best_count} ratings)."
            )
    
    # Feedback trend
    feedback_trend = feedback_analysis.get("recent_trend", 0)
    if abs(feedback_trend) > 0.2:  # Only show if there's a noticeable trend
        trend_direction = "improving" if feedback_trend > 0 else "declining"
        insights.append(f"Your session ratings are {trend_direction} recently.")
    
    # Variety suggestion
    if variety_score < VARIETY_THRESHOLD and len(mood_distribution) > 1:
        insights.append(
            "You've been sticking to similar moods. Try something different for variety!"
        )
    
    if not insights:
        return "No significant patterns detected yet. Keep walking to generate insights!"

    return "\n  - " + "\n  - ".join(insights)

def suggest_mood_for_time(current_hour: int, analysis_data: Dict) -> Optional[str]:
    """
    Suggests a mood based on current time, historical patterns, and feedback.
    
    Args:
        current_hour: The current hour (0-23)
        analysis_data: The analyzed session data
        
    Returns:
        The suggested mood key, or None if no suggestion can be made
    """
    if not analysis_data:
        return None
        
    current_block = get_time_block(current_hour)
    
    # Get mood distribution for the current time block
    mood_distribution = analysis_data.get('mood_by_time_block', {}).get(current_block, {})
    if not mood_distribution:
        # If no data for this time block, use overall distribution
        mood_distribution = analysis_data.get('mood_distribution', {})
        if not mood_distribution:
            return None
    
    # Get feedback-based mood effectiveness
    mood_effectiveness = analysis_data.get('feedback_analysis', {}).get('mood_effectiveness', {})
    
    # Calculate scores for each mood
    mood_scores = {}
    total_sessions = analysis_data.get('total_sessions', 1)
    
    for mood in set(mood_distribution.keys()).union(set(mood_effectiveness.keys())):
        # Base score is the frequency in this time block (or overall if no time block data)
        freq = mood_distribution.get(mood, 0)
        total = sum(mood_distribution.values()) or 1  # Avoid division by zero
        score = freq / total
        
        # Adjust based on feedback effectiveness if available
        if mood in mood_effectiveness:
            # Weight the effectiveness score more heavily than frequency
            effectiveness = mood_effectiveness[mood].get('effectiveness', 1.0)
            # Give more weight to moods with higher confidence (more data points)
            confidence = min(1.0, mood_effectiveness[mood].get('count', 0) / 5)
            score = (0.7 * effectiveness) + (0.3 * score) * confidence
        
        # Slight penalty for overused moods
        if mood in mood_distribution and total_sessions > 5:
            usage_ratio = mood_distribution[mood] / total_sessions
            if usage_ratio > 0.5:  # If mood is used in >50% of sessions
                score *= 0.8  # 20% penalty
                
        mood_scores[mood] = score
    
    if not mood_scores:
        return None
    
    # Get the mood with the highest score
    suggested_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
    
    # Check if we should suggest a different mood for variety
    variety_score = analysis_data.get('variety_score', 1.0)
    if variety_score < VARIETY_THRESHOLD and len(mood_scores) > 1:
        # Sort by score and pick the best mood that's different from recent ones
        sorted_moods = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Try to find a mood that's not in the recent sessions
        recent_moods = analysis_data.get('recent_moods', [])
        for mood, score in sorted_moods:
            if mood not in recent_moods[-3:]:  # Not in last 3 moods
                suggested_mood = mood
                break
    
    return suggested_mood

def suggest_mood_for_time_legacy(current_hour, analysis_data):
    """Legacy implementation of mood suggestion."""
    if not analysis_data or analysis_data.get("total_walks", 0) < MIN_WALKS_FOR_PREDICTIONS:
        return None

    current_time_block_name = get_time_block(current_hour)
    time_patterns = analysis_data.get("mood_by_time", {}) 
    
    feedback_by_mood = analysis_data.get("feedback_by_mood", {}) 

    # --- Check for dominant mood in the current time block ---
    moods_in_current_block = time_patterns.get(current_time_block_name, {}) 
    
    if moods_in_current_block:
        try:
            # Safely calculate total walks in this block FIRST
            total_walks_in_block = sum(moods_in_current_block.values())
            
            if total_walks_in_block > 0:
                top_mood_key, top_mood_count = max(
                    moods_in_current_block.items(), 
                    key=lambda item: item[1] 
                )
                
                if (top_mood_count / total_walks_in_block > 0.5): 
                    mood_feedback = feedback_by_mood.get(top_mood_key, {})
                    avg_feedback = mood_feedback.get("average_feedback", 0)
                    feedback_count = mood_feedback.get("count", 0)
                    
                    if avg_feedback >= FEEDBACK_POSITIVE_THRESHOLD and feedback_count >= 2:
                        return top_mood_key 
                    elif not (avg_feedback <= FEEDBACK_NEGATIVE_THRESHOLD and feedback_count >= 2):
                        return top_mood_key
        except ValueError: 
            pass
    
    return None