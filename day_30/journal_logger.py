import json
import os
from datetime import datetime

JOURNAL_FILE = "whispers.json"

def load_journal():
    """Load existing journal entries."""
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            return json.load(f)
    return []

def save_journal(wish, mood, affirmation):
    """Save a new journal entry."""
    entries = load_journal()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "wish": wish,
        "mood": mood,
        "affirmation": affirmation
    }
    entries.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=4)