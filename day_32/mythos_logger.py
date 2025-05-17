import json
import os
from datetime import datetime

JOURNAL_FILE = "mythos_journal.json"

def load_journal():
    """Load existing journal entries."""
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            return json.load(f)
    return []

def save_journal(question, mood, deity, wisdom):
    """Save a new journal entry."""
    entries = load_journal()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "mood": mood,
        "deity": deity,
        "wisdom": wisdom
    }
    entries.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=4)