import json
from datetime import datetime, timedelta
import math

class SpacedRepetition:
    """Implements the SuperMemo 2 algorithm for spaced repetition."""
    
    def __init__(self):
        self.default_ease = 2.5
        self.default_interval = 1
    
    def calculate_next_review(self, current_interval, ease_factor, quality):
        """Calculate the next review interval and ease factor based on user feedback (0-5)."""
        if quality < 3:
            interval = 1
        elif current_interval == 1:
            interval = 6
        else:
            interval = math.ceil(current_interval * ease_factor)
        # Update ease factor
        ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        return interval, ease_factor

    def get_initial_review_date(self):
        """Get the first review date (tomorrow)."""
        return datetime.now().date() + timedelta(days=1)

    def get_next_review_date(self, last_review_date, interval):
        """Calculate the next review date given the last review date and interval (in days)."""
        return last_review_date + timedelta(days=interval)
