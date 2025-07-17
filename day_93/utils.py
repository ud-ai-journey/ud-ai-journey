import re
import json

def extract_json(text):
    """Extract JSON object from a string, even if surrounded by code block markers."""
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)["flashcards"]
        except Exception:
            return []
    return []
