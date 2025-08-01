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


def export_walk_log(filename=None):
    """
    Exports the walk log to a specified file.
    
    Args:
        filename (str, optional): The filename to save the export to. If None, prompts user.
    
    Returns:
        bool: True if export was successful, False otherwise.
    """
    try:
        # Load the current walk log
        log_data = load_walk_log()
        if not log_data:
            print("No walks to export.")
            return False

        # If no filename provided, use default with timestamp
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"walkpal_export_{timestamp}.json"

        # Ensure filename is safe and doesn't overwrite critical files
        if filename == os.path.basename(WALK_LOG_FILE):
            print("Cannot export to walk_log.json - this is the main data file.")
            return False

        # Generate analysis data
        from pattern_engine import analyze_session_data
        analysis = analyze_session_data(log_data)
        
        # Create export data structure with metrics
        export_data = {
            'walk_history': log_data,
            'user_metrics': {
                'total_walks': len(log_data),
                'total_duration_minutes': sum(entry.get('duration_minutes', 0) for entry in log_data),
                'average_duration_minutes': sum(entry.get('duration_minutes', 0) for entry in log_data) / len(log_data) if log_data else 0,
                'mood_distribution': analysis.get('mood_distribution', {}),
                'time_block_usage': analysis.get('time_block_usage', {}),
                'feedback_analysis': analysis.get('feedback_analysis', {}),
                'favorite_moods': analysis.get('favorite_moods', []),
                'time_preferences': analysis.get('time_preferences', {}),
                'last_walk_timestamp': log_data[-1]['timestamp'] if log_data else None
            }
        }
        
        # Write to file
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=4)
        
        print(f"Successfully exported walk log to {filename}")
        return True
    
    except IOError as e:
        print(f"Error exporting walk log: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def create_backup():
    """
    Creates a backup of the current walk log.
    
    Returns:
        str: The filename of the created backup, or None if failed.
    """
    try:
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"walk_log_backup_{timestamp}.json"
        backup_path = os.path.join(USER_DATA_DIR, backup_filename)

        # Load current log data
        log_data = load_walk_log()
        
        # Save backup
        with open(backup_path, 'w') as f:
            json.dump(log_data, f, indent=4)
        
        print(f"Backup created successfully: {backup_filename}")
        return backup_filename
    
    except IOError as e:
        print(f"Error creating backup: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def list_backups():
    """
    Lists all available backup files.
    
    Returns:
        list: List of backup filenames.
    """
    try:
        # Get all files in user_data directory
        backup_files = []
        if os.path.exists(USER_DATA_DIR):
            for file in os.listdir(USER_DATA_DIR):
                # Look for files that match our backup naming pattern
                if file.startswith("walk_log_backup_") and file.endswith(".json"):
                    backup_files.append(file)
        
        return backup_files
    
    except FileNotFoundError:
        print("User data directory not found.")
        return []
    except Exception as e:
        print(f"Error listing backups: {e}")
        return []


def restore_from_backup(filename):
    """
    Restores the walk log from a backup file.
    
    Args:
        filename (str): The name of the backup file to restore from.
    
    Returns:
        bool: True if restore was successful, False otherwise.
    """
    try:
        # Get full path to backup file
        backup_path = os.path.join(USER_DATA_DIR, filename)
        
        # Check if file exists and is a valid backup
        if not os.path.exists(backup_path):
            print(f"Backup file not found: {filename}")
            return False

        # Confirm with user before proceeding
        confirmation = input(f"This will overwrite your current walk log. Are you sure? (y/n): ").lower()
        if confirmation != 'y':
            print("Restore cancelled.")
            return False

        # Load backup data
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        # Basic validation - must be a list
        if not isinstance(backup_data, list):
            print("Invalid backup file format.")
            return False

        # Save to main log file
        save_walk_log(backup_data)
        print(f"Successfully restored from backup: {filename}")
        return True
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON in backup file.")
        return False
    except IOError as e:
        print(f"Error restoring backup: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False