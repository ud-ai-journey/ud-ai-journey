# user_profile.py
import os
from collections import Counter, defaultdict
from datetime import datetime
import math 

# --- Imports ---
from data_manager import load_walk_log # Load historical data
# Import analysis functions and configuration constants
from pattern_engine import (
    analyze_session_data, MIN_WALKS_FOR_INSIGHTS, MIN_WALKS_FOR_PREDICTIONS, 
    get_time_block # Needs to be accessible here if profile derives time-specific prefs independently
)
from moods import VALID_MOODS, get_mood_details # Helper functions for moods

# --- Constants for Preference Derivation ---
# Descriptive phrases for LLM prompt injection
PREFERENCE_STYLES = {
    "story": ["narrative", "engaging", "short story", "anecdote", "descriptive", "imaginative"],
    "learn": ["factual", "educational", "insightful", "concise", "bite-sized", "informative"],
    "reflect": ["calming", "mindful", "introspective", "question-based", "philosophical", "peaceful"],
    "humor": ["joke", "pun", "funny fact", "lighthearted", "witty", "humorous"],
    "surprise": ["unexpected", "creative", "mix of styles", "delightful", "curious", "novel"] 
}

# Map mood keys to descriptive phrases about user preference style for LLM prompts
STYLE_MAPPINGS = {
    "story": "a preference for engaging stories",
    "learn": "a preference for factual insights",
    "reflect": "a preference for mindful reflection and questions",
    "humor": "a liking for humorous content",
    "surprise": "a penchant for creative and surprising content" 
}

# Thresholds for preference strength based on feedback
# If average feedback for a mood is above this, we consider it a positive preference.
# Below this, it might be a negative preference.
FEEDBACK_POSITIVE_THRESHOLD = 4.0 
FEEDBACK_NEGATIVE_THRESHOLD = 2.5 

class UserProfile:
    """
    Manages user-specific data, analyzes it, and derives preferences for personalization.
    Uses the singleton pattern to ensure a single instance manages the user's profile.
    """
    _instance = None # Class attribute to hold the singleton instance

    def __init__(self):
        """Initializes the UserProfile, loads data, and derives preferences."""
        # Singleton pattern: If instance already exists, return it.
        if UserProfile._instance is not None:
            return UserProfile._instance 

        # Initialize attributes
        self.preferences = {}         # Dictionary storing derived preferences
        self.analysis_data = None     # Stores the result from pattern_engine.analyze_session_data
        self.is_initialized = False   # Flag: True if enough data for personalization exists

        # --- Load data and derive preferences ---
        self._load_and_derive_profile() 
        
        # Store the created instance in the class variable
        UserProfile._instance = self 

    def _load_and_derive_profile(self):
        """
        Loads walk log data, analyzes it using pattern_engine, and derives user preferences.
        Sets self.is_initialized based on whether enough data was available.
        """
        try:
            log_data = load_walk_log() # Load the walk history
            
            # Analyze the data to get patterns and statistics
            self.analysis_data = analyze_session_data(log_data)
            
            # Check if we have enough data for personalization
            if not self.analysis_data or self.analysis_data.get("total_sessions", 0) < MIN_WALKS_FOR_INSIGHTS:
                self.is_initialized = False
                return # Exit early if not enough data

            # If analysis produced results and we have enough data, derive preferences
            self.is_initialized = True
            self._derive_preferences()
            
        except Exception as e:
            # Catch errors during loading/analysis and mark profile as uninitialized
            import traceback
            print(f"Error loading or processing user profile data: {e}")
            print("Full traceback:")
            traceback.print_exc()
            self.is_initialized = False 

    def _derive_preferences(self):
        """
        Populates self.preferences dictionary using insights from self.analysis_data.
        Includes logic based on feedback scores.
        """
        if not self.is_initialized or not self.analysis_data:
            return # Do nothing if profile isn't ready

        prefs = self.preferences # Use a shorter alias for convenience
        analysis = self.analysis_data 

        # --- Preference 1: Overall Favorite Mood/Style ---
        mood_distribution = analysis.get("mood_distribution", {})
        if mood_distribution:
            # Find the most common mood from the distribution
            overall_fav_mood_key = max(mood_distribution.items(), key=lambda x: x[1], default=(None, 0))[0]
            if overall_fav_mood_key and STYLE_MAPPINGS.get(overall_fav_mood_key):
                # Add overall preferred style based on frequency
                prefs["overall_style_preference"] = STYLE_MAPPINGS[overall_fav_mood_key]
                prefs["preferred_mood"] = overall_fav_mood_key # Store the key of the generally preferred mood

        # --- Preference 2: Time-Specific Favorite Mood/Style & Feedback Adjustment ---
        time_patterns = analysis.get("mood_by_time_block", {}) # This is dict of dicts: {'TimeBlock': {'mood_key': count}}
        feedback_analysis = analysis.get("feedback_analysis", {})
        mood_effectiveness = feedback_analysis.get("mood_effectiveness", {})
        
        current_hour = datetime.now().hour
        current_time_block_name = get_time_block(current_hour) # Get the current time block name
        
        # Check if we have data for the current time block
        if current_time_block_name in time_patterns and time_patterns[current_time_block_name]:
            moods_in_current_block = time_patterns[current_time_block_name]
            
            if moods_in_current_block: # Ensure the dict for the block is not empty
                # Find the most frequent mood within this time block
                try:
                    top_mood_key_for_time, top_mood_count_for_time = max(
                        moods_in_current_block.items(), 
                        key=lambda item: item[1] # Compare based on count (item[1])
                    )
                    
                    total_walks_in_this_block = sum(moods_in_current_block.values())
                    
                    # Check dominance: Suggest mood if it accounts for >50% of walks in this block
                    if total_walks_in_this_block > 0 and (top_mood_count_for_time / total_walks_in_this_block > 0.5):
                        # Get feedback for this mood from the new structure
                        mood_feedback = mood_effectiveness.get(top_mood_key_for_time, {})
                        avg_feedback_for_top_mood = mood_feedback.get("avg_rating", 0)
                        feedback_count_for_top_mood = mood_feedback.get("count", 0)
                        
                        # --- Apply feedback influence ---
                        if avg_feedback_for_top_mood >= FEEDBACK_POSITIVE_THRESHOLD and feedback_count_for_top_mood > 1:
                            # If this mood is frequently chosen AND gets high ratings, strongly prefer it.
                            prefs["time_specific_style_preference"] = STYLE_MAPPINGS.get(top_mood_key_for_time, f"a generally positive experience with '{top_mood_key_for_time}'")
                            prefs["suggested_mood_for_time"] = top_mood_key_for_time
                        elif avg_feedback_for_top_mood <= FEEDBACK_NEGATIVE_THRESHOLD and feedback_count_for_top_mood > 1:
                            # If this mood is frequently chosen BUT gets low ratings, maybe avoid it or use caution.
                            # For now, we won't explicitly store a negative preference, but we could modify suggestion logic later.
                            pass # Don't add this as a preferred style if feedback is bad.
                        elif STYLE_MAPPINGS.get(top_mood_key_for_time):
                            # If no strong feedback signal, but it's the dominant mood, record it neutrally.
                            prefs["time_specific_style_preference"] = STYLE_MAPPINGS.get(top_mood_key_for_time, f"a general tendency towards '{top_mood_key_for_time}'")
                            prefs["suggested_mood_for_time"] = top_mood_key_for_time # Still suggest based on frequency

                except ValueError: 
                    # Handle case where moods_in_current_block dictionary is empty (shouldn't happen if logic above is correct)
                    pass 

        # If no dominant mood or preference found for this time block, stick with overall preferences.

    # --- Potential Future Preference Derivations ---
    # Example: If user often skips audio, lower preference for audio output.
    # Example: If user prefers shorter walk content based on feedback, adjust length prompts.

    def get_preference(self, key, default=None):
        """Safely retrieves a preference value from the profile."""
        return self.preferences.get(key, default)

    def get_all_preferences(self):
        """Returns the entire dictionary of learned user preferences."""
        return self.preferences

    def is_profile_initialized(self):
        """Returns True if the profile has enough data to derive meaningful preferences."""
        return self.is_initialized

# --- Singleton Getter Function ---
# This function ensures that only one instance of UserProfile is created and managed throughout the application's lifecycle.
_user_profile_instance = None 

def get_user_profile():
    """
    Returns the singleton instance of UserProfile. Creates it if it doesn't exist yet.
    Ensures that user data is loaded and analyzed only once.
    """
    global _user_profile_instance # Use the global instance variable
    if _user_profile_instance is None:
        # Create the instance if it hasn't been created yet.
        # The UserProfile constructor handles the loading and analysis.
        _user_profile_instance = UserProfile() 
    return _user_profile_instance # Return the single instance