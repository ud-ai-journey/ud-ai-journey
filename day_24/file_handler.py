import json
import os

def load_data(filename='habit_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_data(data, filename='habit_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)