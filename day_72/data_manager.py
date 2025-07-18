# data_manager.py
import os
import json
import time
from datetime import datetime

# Define the directory where data will be stored
USER_DATA_DIR = "user_data"
WALK_LOG_FILE = os.path.join(USER_DATA_DIR, "walk_log.json")

# Ensure the data directory exists
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

def load_walk_log():
    """Loads the walk log from the JSON file. Returns an empty list if file not found or invalid."""
    if not os.path.exists(WALK_LOG_FILE):
        return []
    try:
        with open(WALK_LOG_FILE, 'r') as f:
            content = f.read()
            if not content:
                return []
            log = json.loads(content)
            return log if isinstance(log, list) else []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading walk log: {e}. Starting with an empty log.")
        return []

def save_walk_log(log_data):
    """Saves the entire walk log back to the JSON file."""
    try:
        with open(WALK_LOG_FILE, 'w') as f:
            json.dump(log_data, f, indent=4) 
    except IOError as e:
        print(f"Error saving walk log: {e}")

def log_walk_session(duration, mood, ai_text, audio_played):
    """
    Logs details of a completed walk session.
    
    Args:
        duration (int): The duration of the walk in minutes.
        mood (str): The chosen mood key (e.g., 'story').
        ai_text (str): The text content generated by the AI.
        audio_played (bool): True if audio output was used, False otherwise.
        
    Returns:
        int: The index of the newly added log entry.
    """
    
    current_log = load_walk_log()
    
    new_entry = {
        "id": len(current_log), 
        "timestamp": datetime.now().isoformat(), 
        "duration_minutes": duration,
        "mood": mood,
        "ai_content": ai_text,
        # Explicitly ensure audio_played is saved as a boolean
        "audio_played": bool(audio_played), 
        "feedback": None # Placeholder for feedback
    }
    
    current_log.append(new_entry)
    save_walk_log(current_log)
    
    return new_entry["id"] 

def save_feedback(log_id, feedback_score):
    """
    Adds feedback to a specific walk log entry.
    """
    if feedback_score is None:
        return 

    current_log = load_walk_log()
    
    if 0 <= log_id < len(current_log):
        current_log[log_id]["feedback"] = feedback_score
        save_walk_log(current_log)
        print(f"Feedback ({feedback_score} stars) saved for walk ID {log_id}.")
    else:
        print(f"Error: Could not find walk log entry with ID {log_id} to save feedback.")

# --- Helper for initial testing (optional) ---
def print_log_contents():
    """Prints the current contents of the walk log."""
    log = load_walk_log()
    if not log:
        print("Walk log is empty.")
    else:
        print("\n--- Current Walk Log ---")
        for i, entry in enumerate(log):
            print(f"Entry {i}: Mood={entry.get('mood', 'N/A')}, Duration={entry.get('duration_minutes', 'N/A')} min, Feedback={entry.get('feedback', 'None')}, AudioPlayed={entry.get('audio_played')}")
        print("----------------------")