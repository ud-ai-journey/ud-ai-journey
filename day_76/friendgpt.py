import json
import os
import datetime
from typing import Dict, List, Optional, Any, Tuple
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
import random
import dateutil.parser # Added for more flexible date parsing
from dateutil.relativedelta import relativedelta # To handle year wrapping for birthdays
import re # Added for regular expressions

# --- Data Structures ---

@dataclass
class ConversationEntry:
    date: str # Stored as string '%Y-%m-%d %H:%M:%S'
    summary: str
    mood: Optional[str] = None
    follow_up: Optional[str] = None

@dataclass
class Friend:
    name: str
    details: Dict[str, str] # Stores parsed and general details/notes
    last_conversation: str # Summary of the last conversation
    last_contact: str # Timestamp of last contact '%Y-%m-%d %H:%M:%S'
    birthday: Optional[str] = None # Stored as string (e.g., "May 15", "1990-05-15", "March 30")
    important_dates: List[Dict[str, str]] = field(default_factory=list) # List of dicts with 'date' and 'description'
    conversation_history: List[ConversationEntry] = field(default_factory=list) # List of ConversationEntry objects
    tags: List[str] = field(default_factory=list) # e.g., 'friend', 'family', 'colleague', 'cricket fan'
    preferred_contact_method: str = "message" # message, call, email, etc.
    relationship_strength: int = 50 # 0-100 scale
    last_met: Optional[str] = None # Last in-person meeting date
    frequency_preference: str = "bi-weekly" # How often to stay in touch

    # __post_init__ is handled by default_factory now for lists

    def to_dict(self) -> Dict[str, Any]:
        """Convert Friend object to dictionary for saving."""
        data = asdict(self)
        # Convert ConversationEntry objects to dicts
        data['conversation_history'] = [asdict(entry) for entry in self.conversation_history]
        return data

    def days_since_last_contact(self) -> int:
        """Return number of days since last contact."""
        if not self.last_contact:
            return float('inf')
        last = datetime.strptime(self.last_contact, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - last).days

    def get_conversation_frequency(self) -> str:
        """Analyze conversation history to determine frequency."""
        if len(self.conversation_history) < 2:
            return "Not enough data"

        dates = [datetime.strptime(entry.date, "%Y-%m-%d %H:%M:%S") 
                for entry in self.conversation_history]
        dates.sort()

        if not dates:
            return "No conversations yet"

        # Calculate average days between conversations
        diffs = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
        avg_days = sum(diffs) / len(diffs)

        if avg_days < 3:
            return "Daily"
        elif avg_days < 8:
            return "Weekly"
        elif avg_days < 21:
            return "Bi-weekly"
        elif avg_days < 35:
            return "Monthly"
        return "Less than monthly"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Friend':
        """Create Friend object from dictionary loaded from JSON."""
        # Ensure default values for potentially missing keys in older data
        data.setdefault('details', {})
        data.setdefault('last_conversation', "")
        # Provide a default valid date if 'last_contact' is missing or invalid
        last_contact = data.get('last_contact')
        if last_contact:
             try:
                  datetime.strptime(last_contact, "%Y-%m-%d %H:%M:%S")
             except (ValueError, TypeError):
                  print(f"Warning: Invalid last_contact format for friend data: {last_contact}. Setting to now.")
                  last_contact = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
             last_contact = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             print(f"Warning: Missing last_contact for friend data. Setting to now.")

        data['last_contact'] = last_contact


        data.setdefault('birthday', None)
        data.setdefault('important_dates', [])
        data.setdefault('conversation_history', [])
        data.setdefault('tags', [])

        # Convert raw history dicts to ConversationEntry objects
        history_list = []
        for entry_data in data.get('conversation_history', []): # Use .get for safety
             # Ensure default values for mood/follow_up in older history entries
             entry_data.setdefault('mood', None)
             entry_data.setdefault('follow_up', None)
             # Add date validation for history entries too
             entry_date_str = entry_data.get('date')
             if entry_date_str:
                 try:
                     datetime.strptime(entry_date_str, "%Y-%m-%d %H:%M:%S")
                     history_list.append(ConversationEntry(**entry_data))
                 except (ValueError, TypeError):
                     print(f"Warning: Invalid history entry date format for {data.get('name', 'Unknown friend')}: {entry_date_str}. Skipping entry.")
             else:
                  print(f"Warning: Missing history entry date for {data.get('name', 'Unknown friend')}. Skipping entry.")


        data['conversation_history'] = history_list

        # Ensure list fields are lists even if loaded as None or other type
        if not isinstance(data['important_dates'], list): data['important_dates'] = []
        if not isinstance(data['tags'], list): data['tags'] = []


        return cls(**data)

# --- Core Logic ---

class FriendGPT:
    def __init__(self):
        self.friends_file = "friends_data.json"
        self.friends: Dict[str, Friend] = {}
        self.load_friends()

        # Conversation starters based on different contexts (Keep these as is)
        self.conversation_starters = {
            "work": [
                "How's the new job going?",
                "Any exciting projects you're working on?",
                "How's work-life balance these days?",
                "Any career updates or changes?"
            ],
            "family": [
                "How are the kids doing?",
                "How's the family?",
                "Any family trips planned?",
                "How are things at home?"
            ],
            "hobbies": [
                "Been up to any {hobby} lately?",
                "How's your {hobby} going?",
                "Any new {hobby} projects?",
                "Still enjoying {hobby}?"
            ],
            "location": [
                "How's {location} treating you?",
                "Any new places you've discovered in {location}?",
                "How's life in {location}?",
                "Any interesting events happening in {location}?"
            ],
            "general": [
                "How have you been?",
                "What's new with you?",
                "How's life treating you?",
                "Any exciting news?"
            ]
        }

        # Check-in message templates (Keep these as is)
        self.checkin_templates = [
            "Hey {name}! 👋 Just wanted to check in and see how you're doing. {context}",
            "Hi {name}! 😊 Been thinking about you. {context}",
            "Hey there {name}! 🌟 How's everything going? {context}",
            "Hello {name}! 💫 Hope you're doing well. {context}",
            "Hi {name}! ✨ Just dropping a quick hello. {context}"
        ]

        self.context_generators = [ # Used when specific details aren't easily found/used
            "Hope work is going great!",
            "How's the family?",
            "Any exciting plans coming up?",
            "Hope you're staying healthy and happy!",
            "How's everything in your world?",
            "Any new adventures lately?",
            "Hope you're enjoying life!",
            "How's your day going?"
        ]

    def load_friends(self):
        """Load friends data from JSON file"""
        self.friends = {} # Clear current data before loading
        if os.path.exists(self.friends_file):
            try:
                with open(self.friends_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert dictionaries back to Friend objects
                    for name, friend_data in data.items():
                         # Use the class method from Friend, handle potential errors
                         try:
                            self.friends[name] = Friend.from_dict(friend_data)
                         except Exception as e:
                             print(f"Error loading friend data for '{name}': {e}. Skipping this entry.")
                             # Decide how to handle corrupted entries - maybe log and skip?
                             # For now, just print error and skip.
            except FileNotFoundError:
                 pass # File doesn't exist yet, start fresh
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data from {self.friends_file}: {e}")
                messagebox.showerror("Load Error", f"Error decoding friends data: {e}\nFile may be corrupted.")
            except Exception as e:
                print(f"Error loading friends data: {e}")
                messagebox.showerror("Load Error", f"Error loading friends data: {e}")
        else:
            print(f"Data file not found: {self.friends_file}")

    def save_friends(self):
        """Save friends data to JSON file"""
        try:
            data = {}
            for name, friend in self.friends.items():
                # Use the to_dict method
                data[name] = friend.to_dict()

            # Create backup before saving
            if os.path.exists(self.friends_file):
                backup_file = f"{self.friends_file}.bak"
                try:
                    import shutil
                    shutil.copy2(self.friends_file, backup_file)
                except Exception as e:
                    print(f"Warning: Could not create backup: {e}")

            with open(self.friends_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving friends data: {e}")
            messagebox.showerror("Save Error", f"Error saving friends data: {e}")

    def get_friends_needing_contact(self, days_threshold: int = 14) -> List[Tuple[str, Friend]]:
        """Return list of friends who haven't been contacted in more than days_threshold days."""
        now = datetime.now()
        result = []
        
        for name, friend in self.friends.items():
            if not friend.last_contact:
                result.append((name, friend))
                continue
                
            last_contact = datetime.strptime(friend.last_contact, "%Y-%m-%d %H:%M:%S")
            days_since = (now - last_contact).days
            
            # Adjust threshold based on relationship strength and frequency preference
            threshold = days_threshold
            if friend.relationship_strength > 70:  # Close friends
                threshold = max(7, threshold // 2)
                
            if friend.frequency_preference == "weekly":
                threshold = min(threshold, 7)
            elif friend.frequency_preference == "bi-weekly":
                threshold = min(threshold, 14)
            elif friend.frequency_preference == "monthly":
                threshold = min(threshold, 30)
                
            if days_since > threshold:
                result.append((name, friend, days_since))
                
        # Sort by days since last contact (most overdue first)
        return sorted(result, key=lambda x: x[2] if len(x) > 2 else float('inf'), reverse=True)

    def analyze_conversation_patterns(self, friend_name: str) -> Dict[str, Any]:
        """Analyze conversation patterns for a specific friend."""
        if friend_name not in self.friends:
            return {"error": "Friend not found"}
            
        friend = self.friends[friend_name]
        if not friend.conversation_history:
            return {"total_conversations": 0, "common_topics": []}
            
        # Basic stats
        total_convs = len(friend.conversation_history)
        
        # Mood analysis
        mood_counter = {}
        for entry in friend.conversation_history:
            mood = entry.mood.lower() if entry.mood else "unknown"
            mood_counter[mood] = mood_counter.get(mood, 0) + 1
        
        # Common topics (simple word frequency for now)
        word_freq = {}
        for entry in friend.conversation_history:
            words = re.findall(r'\b\w+\b', entry.summary.lower())
            for word in words:
                if len(word) > 3 and word not in ['that', 'this', 'with', 'have', 'been', 'they', 'their']:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        common_topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_conversations": total_convs,
            "mood_distribution": mood_counter,
            "common_topics": common_topics,
            "conversation_frequency": friend.get_conversation_frequency(),
            "days_since_last_contact": friend.days_since_last_contact()
        }

    def generate_relationship_insights(self, friend_name: str) -> str:
        """Generate human-readable insights about the relationship."""
        if friend_name not in self.friends:
            return "Friend not found."
            
        friend = self.friends[friend_name]
        analysis = self.analyze_conversation_patterns(friend_name)
        
        insights = [f"# Relationship Insights for {friend_name}\n"]
        
        # Contact frequency
        if 'days_since_last_contact' in analysis:
            days = analysis['days_since_last_contact']
            if days == 0:
                insights.append("✅ You were in touch today!")
            elif days < 7:
                insights.append(f"✅ Last contact: {days} days ago - Good job keeping in touch!")
            elif days < 30:
                insights.append(f"⚠️  Last contact: {days} days ago - Consider reaching out soon.")
            else:
                insights.append(f"❌ Last contact: {days} days ago - It's been a while since you connected!")
        
        # Mood analysis
        if 'mood_distribution' in analysis and analysis['mood_distribution']:
            moods = analysis['mood_distribution']
            most_common_mood = max(moods.items(), key=lambda x: x[1])
            insights.append(f"\n😊 Most common mood in conversations: {most_common_mood[0].title()} ({most_common_mood[1]} mentions)")
        
        # Common topics
        if 'common_topics' in analysis and analysis['common_topics']:
            topics = ", ".join([f"{t[0]} ({t[1]})" for t in analysis['common_topics']])
            insights.append(f"\n🗣️  Common topics: {topics}")
        
        # Relationship strength
        strength = friend.relationship_strength
        if strength > 80:
            insights.append("\n💖 Strong relationship - Keep nurturing this connection!")
        elif strength > 50:
            insights.append("\n👍 Good relationship - Regular check-ins will help it grow stronger.")
        else:
            insights.append("\n🌱 Growing relationship - More frequent interactions will help strengthen your bond.")
        
        # Suggestions for next steps
        insights.append("\n### Suggestions:")
        if friend.days_since_last_contact() > 30:
            insights.append("- Send a friendly check-in message")
            if friend.birthday:
                insights.append("- Plan a get-together to catch up")
        if friend.important_dates:
            next_date = self.get_upcoming_important_date(friend_name)
            if next_date:
                insights.append(f"- {next_date['description']} is coming up on {next_date['date']}")
        
        return "\n".join(insights)

    def get_upcoming_important_date(self, friend_name: str, days_ahead: int = 30) -> Optional[Dict[str, str]]:
        """Get the next important date within the specified number of days."""
        if friend_name not in self.friends:
            return None
            
        friend = self.friends[friend_name]
        today = datetime.now().date()
        upcoming_dates = []
        
        # Check birthday if exists
        if friend.birthday:
            try:
                bday = self._parse_date(friend.birthday).date()
                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                days_until = (bday_this_year - today).days
                if 0 <= days_until <= days_ahead:
                    upcoming_dates.append({
                        'date': bday_this_year.strftime("%B %d"),
                        'description': f"{friend.name}'s birthday"
                    })
            except (ValueError, AttributeError):
                pass
        
        # Check other important dates
        for date_info in friend.important_dates:
            if not isinstance(date_info, dict) or 'date' not in date_info:
                continue
                
            try:
                date_obj = self._parse_date(date_info['date']).date()
                date_this_year = date_obj.replace(year=today.year)
                if date_this_year < today:
                    date_this_year = date_this_year.replace(year=today.year + 1)
                
                days_until = (date_this_year - today).days
                if 0 <= days_until <= days_ahead:
                    desc = date_info.get('description', 'Important date')
                    upcoming_dates.append({
                        'date': date_this_year.strftime("%B %d"),
                        'description': desc
                    })
            except (ValueError, AttributeError):
                continue
        
        # Return the next upcoming date
        if upcoming_dates:
            return min(upcoming_dates, key=lambda x: datetime.strptime(x['date'], "%B %d").date())
        return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse a date string into a datetime object, handling multiple formats."""
        if not date_str:
            return None
            
        # Try common date formats
        date_formats = [
            "%B %d",  # Month Day
            "%b %d",   # Abbreviated month
            "%m/%d",   # MM/DD
            "%Y-%m-%d", # YYYY-MM-DD
            "%d-%m-%Y", # DD-MM-YYYY
            "%m/%d/%Y"  # MM/DD/YYYY
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
                
        # Fallback to dateutil for more flexible parsing
        try:
            return dateutil.parser.parse(date_str)
        except (ValueError, OverflowError):
            return None


    def add_friend(self, name: str, details_string: str):
        """Add a new friend with details string"""
        # Parse details into structured format
        parsed_data = self.parse_details(details_string)

        # Extract specific fields from the parsed data, leaving the rest in the details dict
        birthday = parsed_data.pop('birthday', None)
        tags = parsed_data.pop('tags', [])
        important_dates = parsed_data.pop('important_dates', []) # Extract important_dates list


        friend = Friend(
            name=name,
            details=parsed_data, # The rest of the parsed data goes here into the details dict
            last_conversation="",
            last_contact=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            birthday=birthday,
            important_dates=important_dates,
            tags=tags
        )

        self.friends[name] = friend
        self.save_friends()
        return friend

    def parse_details(self, details_string: str) -> Dict[str, Any]:
        """
        Parse natural language details string into structured format (dict).
        Prioritizes Key: Value pairs, then looks for common phrases,
        and finally attempts generic date parsing if birthday wasn't found.
        """
        parsed: Dict[str, Any] = {}
        original_details = details_string.strip()
        parsed["original_details"] = original_details # Store original for reference

        # --- 1. Look for Key: Value Pairs (Highest Priority) ---
        # Process lines for Key:Value. Use a temporary dict to build parsed details
        # and remove processed parts from the string for further parsing.
        temp_parsed: Dict[str, Any] = {}
        lines = original_details.split('\n')
        remaining_lines = []

        for line in lines:
            if ":" in line:
                key_value = line.split(":", 1)
                if len(key_value) == 2:
                    key = key_value[0].strip().lower().replace(" ", "_") # Normalize key
                    value = key_value[1].strip()
                    if key and value:
                         if key == 'tags':
                             # Split comma-separated tags
                             temp_parsed[key] = [t.strip() for t in value.split(',') if t.strip()]
                         elif key == 'birthday':
                             # Store birthday as string
                             temp_parsed[key] = value
                         elif key in ['important_dates', 'important_date']: # Allow singular
                             # Append to important_dates list
                             if 'important_dates' not in temp_parsed:
                                 temp_parsed['important_dates'] = []
                             temp_parsed['important_dates'].extend([d.strip() for d in value.split(',') if d.strip()])
                         # Add other specific key handlers here if needed
                         # elif key == 'notes': temp_parsed['notes'] = value # Example
                         else:
                             # Add to generic details
                             temp_parsed[key] = value
                    # This line was processed by K:V, don't add to remaining_lines
                    continue
            # If the line doesn't contain a Key:Value pair, keep it for next step
            remaining_lines.append(line)

        # Join the remaining lines to continue parsing
        remaining_text = '\n'.join(remaining_lines)
        lower_remaining = remaining_text.lower()


        # --- 2. Basic Keyword/Phrase Parsing (Lower Priority) ---

        # Birthday keywords (apply only if birthday wasn't found by Key:Value)
        if 'birthday' not in temp_parsed:
            birthday_keywords = ["born on", "birthday is", "bday", "dob"]
            for keyword in birthday_keywords:
                if keyword in lower_remaining:
                    try:
                        # Try to parse a date string from the text following the keyword
                        parts_after_keyword = lower_remaining.split(keyword, 1)[1]
                        # Find the end of the potential date string (e.g., comma, period, end of string)
                        end_index_comma = parts_after_keyword.find(',')
                        end_index_period = parts_after_keyword.find('.')
                        end_index = len(parts_after_keyword)

                        if end_index_comma != -1: end_index = min(end_index, end_index_comma)
                        if end_index_period != -1: end_index = min(end_index, end_index_period)

                        date_str = parts_after_keyword[:end_index].strip()

                        if date_str:
                            # Store the string, can try to validate it later if needed
                            temp_parsed['birthday'] = date_str.title()
                            print(f"Parsed birthday '{temp_parsed['birthday']}' using keyword '{keyword}'.")
                            # Optional: Remove the matched part from remaining_text if needed

                    except Exception as e:
                        print(f"Warning: Could not parse birthday after keyword '{keyword}' from '{lower_remaining}': {e}")
                    # Even if parsing failed, the keyword suggests it was attempted
                    # Decide if we break here or continue searching other keywords - let's break
                    break

        # Location (apply to lower_remaining) - Only if location not found by K:V
        if 'location' not in temp_parsed and "lives in" in lower_remaining:
            parts = lower_remaining.split("lives in", 1)[1].split(",", 1)
            location = parts[0].strip()
            if location: temp_parsed["location"] = location.title()

        # Hobbies (apply to lower_remaining) - Only if hobbies not found by K:V
        if 'hobbies' not in temp_parsed:
            hobbies_keywords = ["loves", "enjoys", "hobby is", "hobbies include"]
            hobbies_list = []
            # Iterate and extract, could remove parts if necessary for complex parsing
            current_text = lower_remaining
            for keyword in hobbies_keywords:
                if keyword in current_text:
                    parts = current_text.split(keyword, 1)[1].split(",", 1)
                    hobby_part = parts[0].strip()
                    if hobby_part: hobbies_list.append(hobby_part)
                    current_text = parts[1] if len(parts) > 1 else "" # Process remaining text

            if hobbies_list:
                 temp_parsed["hobbies"] = ", ".join(hobbies_list).capitalize()


        # Work (apply to lower_remaining) - Only if work not found by K:V
        if 'work' not in temp_parsed:
            work_keywords = ["works at", "job is", "working as", "new job"]
            for keyword in work_keywords:
                if keyword in lower_remaining:
                    parts = lower_remaining.split(keyword, 1)[1].split(",", 1)
                    work_part = parts[0].strip()
                    if work_part:
                         temp_parsed["work"] = f"{keyword.replace(' is', '').replace('ing as', '').title()}: {work_part}"
                         break


        # Family (apply to lower_remaining) - Only if family_status not found by K:V
        if 'family_status' not in temp_parsed and ("has kids" in lower_remaining or "children" in lower_remaining or "family" in lower_remaining):
             temp_parsed["family_status"] = "Has family/children"


        # --- 3. Generic Date Scan (Lowest Priority, if birthday still not found) ---
        # This tries to find common month-day patterns anywhere in the original string
        # Use the original string or remaining_text? Let's use original for simplicity,
        # assuming K:V and keywords didn't overlap too much.
        if 'birthday' not in temp_parsed:
             # Regex for common date formats (Month Day, Day Month, Month.Day, Day.Month etc.) - simplistic
             month_names_full = ["january", "february", "march", "april", "may", "june",
                                 "july", "august", "september", "october", "november", "december"]
             month_names_abbr = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
             all_month_names = "|".join(month_names_full + month_names_abbr)

             # Pattern: Month Name followed by a number (optionally with space, period, dash, slash)
             # or a number followed by a month name.
             # (\b ensures word boundary)
             # (?:[.\-\/\s]*) allows zero or more separators
             date_pattern = re.compile(
                 rf"\b({all_month_names})(?:[.\-\/\s]*)(\d{{1,2}})\b" # e.g., March 30, Mar-30
                 rf"|" # OR
                 rf"\b(\d{{1,2}})(?:[.\-\/\s]*)({all_month_names})\b", # e.g., 30 March, 30/Mar
                 re.IGNORECASE
             )

             match = date_pattern.search(original_details) # Search in original string

             if match:
                 try:
                     # Extract month and day from regex match
                     # Groups: 1=Month(MD), 2=Day(MD), 3=Day(DM), 4=Month(DM)
                     month_str = match.group(1) or match.group(4)
                     day_str = match.group(2) or match.group(3)
                     day = int(day_str)

                     # Attempt to validate the date using dateutil.parser
                     # dateutil can parse "March 30". It validates if day is valid for month.
                     # We don't need the year for parsing here, dateutil handles it.
                     test_date = dateutil.parser.parse(f"{month_str} {day}")

                     # If parsing was successful and the date seems reasonable (day is valid for month)
                     # Store the standardized string (e.g., "March 30")
                     temp_parsed['birthday'] = f"{month_str.title()} {day}"
                     print(f"Parsed birthday '{temp_parsed['birthday']}' using generic scan from '{match.group(0)}'.")

                 except Exception as e:
                      print(f"Warning: Generic date scan found '{match.group(0)}' but failed to parse/validate it: {e}")


        # Return the collected parsed data
        # Put everything from temp_parsed into the main parsed dictionary
        # This merges the results from Key:Value and keyword/generic parsing
        parsed.update(temp_parsed)

        return parsed


    def get_conversation_suggestions(self, friend_name: str) -> List[str]:
        """Generate conversation suggestions based on friend's details"""
        if friend_name not in self.friends:
            return ["I don't have information about this friend yet."]

        friend = self.friends[friend_name]
        suggestions = []

        # Use the parsed details dictionary AND the dedicated fields (tags, birthday)
        details = friend.details

        # Work-related suggestions
        if "work" in details or "work_status" in details:
            suggestions.extend(self.conversation_starters["work"])

        # Family-related suggestions
        if "family_status" in details:
            suggestions.extend(self.conversation_starters["family"])

        # Hobby-related suggestions
        if "hobbies" in details:
            for starter in self.conversation_starters["hobbies"]:
                # Handle multiple hobbies - pick one randomly or just use the whole string
                hobby_display = details["hobbies"].split(',')[0].strip() # Use first hobby
                suggestions.append(starter.format(hobby=hobby_display))

        # Location-related suggestions
        if "location" in details:
            for starter in self.conversation_starters["location"]:
                suggestions.append(starter.format(location=details["location"]))

        # Suggest based on Tags
        if friend.tags:
             # Could add specific starters per tag type (e.g., "How's the project?" for 'colleague')
             # For now, add a general tag mention if tags exist
             suggestions.append(f"How are things with [{', '.join(friend.tags)}]?")

        # Suggest based on Important Dates (if close) or ask about them generally
        # This would require parsing important_dates strings like birthdays
        if friend.important_dates:
             suggestions.append("Anything interesting happening with your important dates/events?")
             # Could add logic here to check dates like birthdays

        # Check for any follow-up actions needed from past conversations
        follow_ups = [entry.follow_up for entry in friend.conversation_history if entry.follow_up]
        if follow_ups:
             # Add a suggestion based on the most recent follow-up
             suggestions.append(f"Follow up on: {follow_ups[-1]}")


        # Add general suggestions
        suggestions.extend(self.conversation_starters["general"])

        # Remove duplicates and shuffle for variety
        suggestions = list(dict.fromkeys(suggestions)) # Remove duplicates
        random.shuffle(suggestions)

        return suggestions[:10]  # Limit to 10 suggestions


    def generate_checkin_message(self, friend_name: str) -> str:
        """Generate a personalized check-in message"""
        if friend_name not in self.friends:
            return f"Hey {friend_name}! How are you doing?"

        friend = self.friends[friend_name]
        details = friend.details

        # Select random template
        template = random.choice(self.checkin_templates)

        # Try to generate context from specific details first
        context = None
        if "work" in details:
            context = f"How's {details['work'].replace('Works At:', 'work at').replace('Job Is:', '').strip()} going?"
        elif "hobbies" in details:
            # Use first hobby
            hobby_display = details["hobbies"].split(',')[0].strip()
            context = f"How's your {hobby_display} going?"
        elif "location" in details:
            context = f"How's {details['location']} treating you?"
        elif "family_status" in details:
             context = self.conversation_starters["family"][0] # How are the kids/family?

        # If no specific context generated, use a random general one
        if context is None:
             context = random.choice(self.context_generators)

        # Add a birthday mention if it's today or very soon
        bday_info = None
        upcoming_birthdays = self.get_upcoming_birthdays(days_ahead=7) # Check only next 7 days for check-ins
        for name, bday_str, when_str in upcoming_birthdays:
            if name == friend_name:
                 bday_info = when_str
                 break

        if bday_info:
             if "Today" in bday_info:
                  context = f"Hope you're having a wonderful birthday!" # Replace general context
             elif "Tomorrow" in bday_info:
                  context = f"Thinking of you with your birthday coming up tomorrow!" # Replace general context
             elif 'in ' in bday_info:
                  days = int(bday_info.split(' ')[1])
                  if days <= 3: # Mention if within 3 days
                      context = f"Hope you have a great time for your birthday coming up in {days} days!"


        return template.format(name=friend_name, context=context)


    def log_conversation(self, friend_name: str, conversation_summary: str, mood: Optional[str] = None, follow_up: Optional[str] = None):
        """Log a conversation with a friend, including mood and follow-up"""
        if friend_name not in self.friends:
            print(f"Error: Friend '{friend_name}' not found for logging conversation.")
            return

        friend = self.friends[friend_name]

        # Update last conversation and contact time
        friend.last_conversation = conversation_summary
        friend.last_contact = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add to conversation history
        conversation_entry = ConversationEntry(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=conversation_summary,
            mood=mood if mood else None, # Store None if empty string
            follow_up=follow_up if follow_up else None # Store None if empty string
        )
        friend.conversation_history.append(conversation_entry)

        # Keep only last 15 conversations
        if len(friend.conversation_history) > 15:
            friend.conversation_history = friend.conversation_history[-15:]

        self.save_friends()
        print(f"Logged conversation for {friend_name}")


    def get_friends_needing_contact(self, days_threshold: int = 14) -> List[Tuple[str, int]]:
        """Get friends who haven't been contacted recently (threshold updated to 14 days)"""
        threshold_date = datetime.now() - timedelta(days=days_threshold)
        friends_needing_contact = []

        for name, friend in self.friends.items():
            try:
                last_contact = datetime.strptime(friend.last_contact, "%Y-%m-%d %H:%M:%S")
                if last_contact < threshold_date:
                     days_since = (datetime.now() - last_contact).days
                     friends_needing_contact.append((name, days_since))
            except (ValueError, TypeError):
                 # Handle cases where last_contact is in an old/invalid format
                 print(f"Warning: Invalid date format for last_contact for {name}: {friend.last_contact}. Treating as needing contact.")
                 # Treat as needing contact if date is invalid or missing
                 # Use a large number or specific indicator for sorting
                 friends_needing_contact.append((name, 9999)) # Sort invalid dates as very overdue

        # Sort by days since last contact (most overdue first), handle 9999 as largest
        friends_needing_contact.sort(key=lambda item: item[1], reverse=True)
        return friends_needing_contact

    def get_upcoming_birthdays(self, days_ahead: int = 30) -> List[Tuple[str, str, str]]:
        """
        Get friends with birthdays in the next N days.
        Returns list of (name, birthday_string, days_until_string).
        Handles year wrapping correctly.
        """
        upcoming = []
        today = datetime.now().date()
        # Use dateutil.relativedelta for adding days across month/year boundaries
        end_date = today + timedelta(days=days_ahead)

        for name, friend in self.friends.items():
            if friend.birthday:
                try:
                    # Use dateutil.parser for flexible parsing of the stored string
                    # This handles formats like "March 30", "May 15, 1990", "7/4" etc.
                    # We only care about month and day for upcoming reminders
                    # parse() might guess the current or a past year if not specified.
                    # The important part is extracting month and day.
                    bday_parsed_date = dateutil.parser.parse(friend.birthday).date()

                    # Construct a date for this year using the parsed month and day
                    bday_this_year = bday_parsed_date.replace(year=today.year)

                    # If the birthday this year has already passed, calculate for next year
                    if bday_this_year < today:
                         bday_this_year = bday_parsed_date.replace(year=today.year + 1)

                    # Calculate difference between the upcoming birthday and today
                    delta = bday_this_year - today

                    # Check if it's within the next days_ahead (including today)
                    if 0 <= delta.days <= days_ahead:
                        days_until = delta.days
                        when_str = ""
                        if days_until == 0:
                            when_str = "Today! 🎉"
                        elif days_until == 1:
                            when_str = "Tomorrow!"
                        else:
                            when_str = f"in {days_until} days"

                        upcoming.append((name, friend.birthday, when_str))

                except Exception as e:
                    # Handle parsing errors gracefully for this specific friend's birthday
                    print(f"Warning: Could not parse birthday for {name}: '{friend.birthday}'. Error: {e}. Skipping for reminders.")
                    # Optionally add them to a "needs review" list or display error in GUI
                    pass # Skip friends with unparseable birthdays for this list

        # Sort by days until birthday (Today < Tomorrow < In X days)
        def get_sort_key(item):
            name, bday_str, when_str = item
            try:
                if 'Today' in when_str:
                    return 0
                elif 'Tomorrow' in when_str:
                    return 1
                elif 'in ' in when_str:
                    try:
                        # Extract the number of days from the string
                        days = int(when_str.split()[1])
                        return days + 1  # +1 to ensure it comes after Tomorrow
                    except (IndexError, ValueError):
                        return 999  # Put malformed entries at the end
                else:
                    return 999  # Put unknown formats at the end
            except Exception as e:
                print(f"Warning: Error sorting birthday for {name}: {e}")
                return 999  # Put errored entries at the end
        
        # Sort using our custom key function
        upcoming.sort(key=get_sort_key)


        return upcoming

    def search_friends(self, query: str) -> List[str]:
        """Search friends by name, details, tags, or conversation history"""
        query = query.lower()
        matches_set = set() # Use a set to avoid duplicates

        for name, friend in self.friends.items():
            # Search in Name
            if query in name.lower():
                matches_set.add(name)
                continue # Move to next friend once matched

            # Search in Details (keys and values)
            for key, value in friend.details.items():
                if query in key.lower() or query in str(value).lower():
                    matches_set.add(name)
                    continue

            # Search in Birthday string
            if friend.birthday and query in friend.birthday.lower():
                 matches_set.add(name)
                 continue

            # Search in Important Dates strings
            for date_str in friend.important_dates:
                 if query in date_str.lower():
                      matches_set.add(name)
                      continue

            # Search in Tags
            for tag in friend.tags:
                 if query in tag.lower():
                      matches_set.add(name)
                      continue

            # Search in Conversation History (summary, mood, follow-up)
            for entry in friend.conversation_history:
                if query in entry.summary.lower():
                    matches_set.add(name)
                    continue
                if hasattr(entry, 'mood') and entry.mood and query in entry.mood.lower():
                    matches_set.add(name)
                    continue
                if hasattr(entry, 'follow_up') and entry.follow_up and query in entry.follow_up.lower():
                    matches_set.add(name)
                    continue

        return list(matches_set)


# --- GUI ---

class FriendGPTGUI:
    def __init__(self):
        # Initialize core components first
        self.friendgpt = FriendGPT()
        self.current_friend = None
        
        # Initialize Tkinter
        self.root = tk.Tk()
        self.status_var = tk.StringVar()
        
        # Setup the GUI
        self.setup_styles()
        self.setup_gui()
        self.refresh_display()
        
        # Start the main loop
        self.root.mainloop()
        
    def update_conversation_filters(self, event=None):
        """Update the conversation list based on the selected filters"""
        self.update_conversation_list()
    
    def clear_conversation_filters(self):
        """Clear all conversation filters and reset to default values"""
        self.friend_filter_var.set('All Friends')
        self.mood_filter.current(0)
        self.date_range.current(0)
        self.update_conversation_list()
    
    def populate_conversation_filters(self):
        """Populate the friend filter dropdown with friend names"""
        friend_names = ['All Friends'] + sorted(self.friendgpt.friends.keys())
        self.friend_filter['values'] = friend_names
        if friend_names:
            self.friend_filter.current(0)
    
    def update_conversation_list(self):
        """Update the conversation list based on current filters"""
        # Clear existing items
        for item in self.conversation_tree.get_children():
            self.conversation_tree.delete(item)
        
        # Get filter values
        friend_filter = self.friend_filter_var.get()
        mood_filter = self.mood_filter_var.get()
        date_range = self.date_range_var.get()
        
        # Calculate date range if needed
        end_date = datetime.datetime.now()
        if date_range == 'Last 7 days':
            start_date = end_date - datetime.timedelta(days=7)
        elif date_range == 'Last 30 days':
            start_date = end_date - datetime.timedelta(days=30)
        elif date_range == 'Last 90 days':
            start_date = end_date - datetime.timedelta(days=90)
        elif date_range == 'Last year':
            start_date = end_date - datetime.timedelta(days=365)
        else:  # All time
            start_date = None
        
        # Collect all conversations that match the filters
        all_conversations = []
        
        for friend_name, friend in self.friendgpt.friends.items():
            # Skip if friend filter is set and doesn't match
            if friend_filter != 'All Friends' and friend_name != friend_filter:
                continue
                
            for conv in friend.conversation_history:
                # Skip if mood filter is set and doesn't match
                if mood_filter != 'All' and mood_filter not in conv.mood:
                    continue
                
                # Parse conversation date
                try:
                    conv_date = datetime.datetime.strptime(conv.date, '%Y-%m-%d')
                    # Skip if date is outside the selected range
                    if start_date and not (start_date <= conv_date <= end_date):
                        continue
                except (ValueError, TypeError):
                    # If date parsing fails, include the conversation
                    pass
                
                all_conversations.append((friend_name, conv))
        
        # Sort conversations by date (newest first)
        all_conversations.sort(key=lambda x: x[1].date, reverse=True)
        
        # Add conversations to the treeview
        for friend_name, conv in all_conversations:
            self.conversation_tree.insert(
                '', 'end',
                values=(
                    conv.date,
                    friend_name,
                    conv.summary[:100] + '...' if len(conv.summary) > 100 else conv.summary,
                    conv.mood or 'N/A'
                )
            )
    
    def view_conversation_details(self, event):
        """Display details of the selected conversation"""
        selected = self.conversation_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a conversation first.")
            return
            
        # Get the selected conversation
        item = self.conversation_tree.item(selected[0])
        friend_name = item['values'][1]
        conv_date = item['values'][0]
        
        # Find the conversation in the friend's history
        friend = self.friendgpt.friends.get(friend_name)
        if not friend:
            messagebox.showerror("Error", "Friend not found.")
            return
            
        # Find the specific conversation
        conv = next((c for c in friend.conversation_history if c.date == conv_date), None)
        if not conv:
            messagebox.showerror("Error", "Conversation not found.")
            return
        
        # Create a dialog to show conversation details
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Conversation with {friend_name} on {conv_date}")
        dialog.geometry("600x400")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create and pack widgets
        ttk.Label(dialog, text=f"Date: {conv.date}", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
        ttk.Label(dialog, text=f"Mood: {conv.mood or 'Not specified'}", font=('Segoe UI', 10)).pack(anchor='w', padx=10)
        
        ttk.Label(dialog, text="\nSummary:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
        summary_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=70, height=10, font=('Segoe UI', 10))
        summary_text.insert('1.0', conv.summary)
        summary_text.config(state='disabled')
        summary_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        if conv.follow_up:
            ttk.Label(dialog, text="\nFollow-up:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
            followup_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=70, height=3, font=('Segoe UI', 10))
            followup_text.insert('1.0', conv.follow_up)
            followup_text.config(state='disabled')
            followup_text.pack(padx=10, pady=5, fill=tk.X)
        
        # Close button
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def edit_conversation(self):
        """Edit the selected conversation"""
        selected = self.conversation_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a conversation to edit.")
            return
            
        # Get the selected conversation
        item = self.conversation_tree.item(selected[0])
        friend_name = item['values'][1]
        conv_date = item['values'][0]
        
        # Find the conversation in the friend's history
        friend = self.friendgpt.friends.get(friend_name)
        if not friend:
            messagebox.showerror("Error", "Friend not found.")
            return
            
        # Find the specific conversation
        conv_index = next((i for i, c in enumerate(friend.conversation_history) 
                          if c.date == conv_date), None)
        if conv_index is None:
            messagebox.showerror("Error", "Conversation not found.")
            return
            
        self.show_edit_conversation_dialog(friend, conv_index, friend.conversation_history[conv_index])
    
    def show_edit_conversation_dialog(self, friend, conv_index, conversation):
        """Show dialog to edit a conversation"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Conversation with {friend.name}")
        dialog.geometry("600x500")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create and pack widgets
        ttk.Label(dialog, text="Date:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
        date_var = tk.StringVar(value=conversation.date)
        ttk.Entry(dialog, textvariable=date_var, font=('Segoe UI', 10)).pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(dialog, text="Mood:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10)
        mood_var = tk.StringVar(value=conversation.mood or '')
        mood_combo = ttk.Combobox(
            dialog,
            textvariable=mood_var,
            values=['', '😊 Happy', '😐 Neutral', '😢 Sad', '😡 Angry', '😲 Surprised'],
            font=('Segoe UI', 10)
        )
        mood_combo.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(dialog, text="Summary:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10)
        summary_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=70, height=10, font=('Segoe UI', 10))
        summary_text.insert('1.0', conversation.summary)
        summary_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        ttk.Label(dialog, text="Follow-up:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
        followup_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=70, height=3, font=('Segoe UI', 10))
        followup_text.insert('1.0', conversation.follow_up or '')
        followup_text.pack(padx=10, pady=5, fill=tk.X)
        
        def save_changes():
            # Update the conversation object
            conversation.date = date_var.get()
            conversation.mood = mood_var.get() or None
            conversation.summary = summary_text.get('1.0', 'end-1c')
            follow_up = followup_text.get('1.0', 'end-1c').strip()
            conversation.follow_up = follow_up if follow_up else None
            
            # Update the friend's conversation history
            friend.conversation_history[conv_index] = conversation
            
            # Save changes
            self.friendgpt.save_friends()
            self.update_conversation_list()
            dialog.destroy()
            messagebox.showinfo("Success", "Conversation updated successfully!")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def delete_conversation(self):
        """Delete the selected conversation"""
        selected = self.conversation_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a conversation to delete.")
            return
            
        # Get the selected conversation
        item = self.conversation_tree.item(selected[0])
        friend_name = item['values'][1]
        conv_date = item['values'][0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete the conversation with {friend_name} on {conv_date}?"):
            return
        
        # Find the friend and conversation
        friend = self.friendgpt.friends.get(friend_name)
        if not friend:
            messagebox.showerror("Error", "Friend not found.")
            return
            
        # Find and remove the conversation
        for i, conv in enumerate(friend.conversation_history):
            if conv.date == conv_date:
                del friend.conversation_history[i]
                self.friendgpt.save_friends()
                self.update_conversation_list()
                messagebox.showinfo("Success", "Conversation deleted successfully!")
                return
        
        messagebox.showerror("Error", "Conversation not found.")
    
    def setup_conversations_tab(self):
        """Setup the Conversations tab with conversation history and filters"""
        # Create a frame for the Conversations tab
        self.conversations_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.conversations_tab, text="💬 Conversations")
        
        # Configure grid layout
        self.conversations_tab.columnconfigure(0, weight=1)
        self.conversations_tab.rowconfigure(1, weight=1)
        
        # Filter frame
        filter_frame = ttk.Frame(self.conversations_tab, padding=5)
        filter_frame.grid(row=0, column=0, sticky='ew')
        
        # Friend filter dropdown
        ttk.Label(filter_frame, text="Filter by friend:").pack(side=tk.LEFT, padx=5)
        self.friend_filter_var = tk.StringVar()
        self.friend_filter = ttk.Combobox(
            filter_frame, 
            textvariable=self.friend_filter_var,
            state='readonly',
            width=25
        )
        self.friend_filter.pack(side=tk.LEFT, padx=5)
        
        # Mood filter
        ttk.Label(filter_frame, text="Mood:").pack(side=tk.LEFT, padx=5)
        self.mood_filter_var = tk.StringVar()
        self.mood_filter = ttk.Combobox(
            filter_frame,
            textvariable=self.mood_filter_var,
            values=['All', '😊 Happy', '😐 Neutral', '😢 Sad', '😡 Angry', '😲 Surprised'],
            state='readonly',
            width=15
        )
        self.mood_filter.current(0)
        self.mood_filter.pack(side=tk.LEFT, padx=5)
        
        # Date range filter
        ttk.Label(filter_frame, text="Date range:").pack(side=tk.LEFT, padx=5)
        self.date_range_var = tk.StringVar()
        self.date_range = ttk.Combobox(
            filter_frame,
            textvariable=self.date_range_var,
            values=['All time', 'Last 7 days', 'Last 30 days', 'Last 90 days', 'Last year'],
            state='readonly',
            width=15
        )
        self.date_range.current(0)
        self.date_range.pack(side=tk.LEFT, padx=5)
        
        # Clear filters button
        clear_btn = ttk.Button(
            filter_frame,
            text="Clear Filters",
            command=self.clear_conversation_filters
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bind filter events
        self.friend_filter.bind('<<ComboboxSelected>>', self.update_conversation_filters)
        self.mood_filter.bind('<<ComboboxSelected>>', self.update_conversation_filters)
        self.date_range.bind('<<ComboboxSelected>>', self.update_conversation_filters)
        
        # Conversation list with scrollbar
        list_frame = ttk.Frame(self.conversations_tab)
        list_frame.grid(row=1, column=0, sticky='nsew', pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create a treeview to display conversations
        columns = ('date', 'friend', 'summary', 'mood')
        self.conversation_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Define headings
        self.conversation_tree.heading('date', text='Date', anchor='w')
        self.conversation_tree.heading('friend', text='Friend', anchor='w')
        self.conversation_tree.heading('summary', text='Summary', anchor='w')
        self.conversation_tree.heading('mood', text='Mood', anchor='center')
        
        # Configure column widths
        self.conversation_tree.column('date', width=120, minwidth=100, anchor='w')
        self.conversation_tree.column('friend', width=150, minwidth=120, anchor='w')
        self.conversation_tree.column('summary', width=400, minwidth=200, anchor='w')
        self.conversation_tree.column('mood', width=80, minwidth=60, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.conversation_tree.yview)
        self.conversation_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the tree and scrollbar
        self.conversation_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Bind double-click event to view conversation details
        self.conversation_tree.bind('<Double-1>', self.view_conversation_details)
        
        # Action buttons frame
        btn_frame = ttk.Frame(self.conversations_tab, padding=(0, 10, 0, 0))
        btn_frame.grid(row=2, column=0, sticky='w')
        
        # Add action buttons
        ttk.Button(
            btn_frame,
            text="View Details",
            command=lambda: self.view_conversation_details(None)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Edit",
            command=self.edit_conversation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Delete",
            command=self.delete_conversation
        ).pack(side=tk.LEFT, padx=5)
        
        # Populate the friend filter dropdown
        self.populate_conversation_filters()
        
        # Initial population of conversations
        self.update_conversation_list()
    
    def setup_insights_tab(self):
        """Setup the Insights tab with relationship statistics and visualizations"""
        # Create the insights tab
        self.insights_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.insights_tab, text="📊 Insights")
        
        # Configure grid
        self.insights_tab.columnconfigure(0, weight=1)
        self.insights_tab.rowconfigure(1, weight=1)
        
        # Create a notebook for different insight categories
        insights_notebook = ttk.Notebook(self.insights_tab)
        insights_notebook.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # Overview tab
        overview_frame = ttk.Frame(insights_notebook, padding=10)
        insights_notebook.add(overview_frame, text="Overview")
        
        # Add overview content
        ttk.Label(overview_frame, text="Relationship Overview", font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Stats frame
        stats_frame = ttk.Frame(overview_frame)
        stats_frame.pack(fill='x', pady=5)
        
        # Total friends
        total_friends = len(self.friendgpt.friends)
        ttk.Label(stats_frame, text=f"Total Friends: {total_friends}", font=('Segoe UI', 10)).pack(anchor='w')
        
        # Friends by contact frequency
        freq_count = {}
        for friend in self.friendgpt.friends.values():
            freq = getattr(friend, 'frequency_preference', 'bi-weekly')
            freq_count[freq] = freq_count.get(freq, 0) + 1
        
        freq_text = ", ".join([f"{k}: {v}" for k, v in freq_count.items()])
        ttk.Label(stats_frame, text=f"Contact Preferences: {freq_text}", font=('Segoe UI', 10)).pack(anchor='w', pady=5)
        
        # Recent activity
        recent_activity = []
        for name, friend in self.friendgpt.friends.items():
            if friend.conversation_history:
                last_conv = max(friend.conversation_history, key=lambda x: x.date)
                recent_activity.append((last_conv.date, name, last_conv.summary[:50] + '...'))
        
        # Sort by most recent
        recent_activity.sort(reverse=True)
        
        # Recent activity frame
        ttk.Label(overview_frame, text="Recent Activity", font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        
        activity_frame = ttk.Frame(overview_frame)
        activity_frame.pack(fill='both', expand=True)
        
        # Add recent activity
        for i, (date, name, summary) in enumerate(recent_activity[:5]):  # Show top 5
            frame = ttk.Frame(activity_frame, style='Card.TFrame')
            frame.pack(fill='x', pady=2, padx=5)
            
            ttk.Label(frame, text=f"{date.split()[0]} - {name}", font=('Segoe UI', 9, 'bold')).pack(anchor='w')
            ttk.Label(frame, text=summary, font=('Segoe UI', 9), wraplength=400, justify='left').pack(anchor='w')
        
        # Add more tabs for different insights
        self.setup_contact_frequency_tab(insights_notebook)
        self.setup_relationship_strength_tab(insights_notebook)
    
    def setup_contact_frequency_tab(self, notebook):
        """Setup the Contact Frequency tab"""
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="🔄 Contact Frequency")
        
        # Add content for contact frequency
        ttk.Label(tab, text="Contact Frequency Analysis", font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Calculate days since last contact
        now = datetime.now()
        days_since_contact = []
        
        for name, friend in self.friendgpt.friends.items():
            try:
                last_contact = datetime.strptime(friend.last_contact, "%Y-%m-%d %H:%M:%S")
                days = (now - last_contact).days
                days_since_contact.append((name, days))
            except (ValueError, AttributeError):
                continue
        
        # Sort by days since last contact
        days_since_contact.sort(key=lambda x: x[1], reverse=True)
        
        # Create a frame for the list
        list_frame = ttk.Frame(tab)
        list_frame.pack(fill='both', expand=True)
        
        # Add column headers
        ttk.Label(list_frame, text="Friend", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(list_frame, text="Days Since Last Contact", font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, sticky='e', padx=5, pady=2)
        
        # Add friend rows
        for i, (name, days) in enumerate(days_since_contact, 1):
            # Friend name
            ttk.Label(list_frame, text=name, font=('Segoe UI', 9)).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            # Days with color coding
            if days > 30:
                fg = '#e74c3c'  # Red for long time no contact
            elif days > 14:
                fg = '#f39c12'  # Orange for medium time
            else:
                fg = '#27ae60'  # Green for recent contact
                
            days_label = ttk.Label(list_frame, text=str(days), foreground=fg, font=('Segoe UI', 9, 'bold'))
            days_label.grid(row=i, column=1, sticky='e', padx=5, pady=2)
    
    def setup_relationship_strength_tab(self, notebook):
        """Setup the Relationship Strength tab"""
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="💪 Relationship Strength")
        
        # Add content for relationship strength
        ttk.Label(tab, text="Relationship Strength Analysis", font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Get friends with relationship strength
        friends_strength = []
        for name, friend in self.friendgpt.friends.items():
            strength = getattr(friend, 'relationship_strength', 50)  # Default to 50 if not set
            friends_strength.append((name, strength))
        
        # Sort by strength
        friends_strength.sort(key=lambda x: x[1], reverse=True)
        
        # Create a frame for the list
        list_frame = ttk.Frame(tab)
        list_frame.pack(fill='both', expand=True)
        
        # Add column headers
        ttk.Label(list_frame, text="Friend", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(list_frame, text="Strength", font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, sticky='e', padx=5, pady=2)
        
        # Add friend rows with strength bars
        for i, (name, strength) in enumerate(friends_strength, 1):
            # Friend name
            ttk.Label(list_frame, text=name, font=('Segoe UI', 9)).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            # Strength bar
            canvas = tk.Canvas(list_frame, height=20, width=200, bg='#f0f0f0', highlightthickness=0)
            canvas.grid(row=i, column=1, sticky='e', padx=5, pady=2)
            
            # Calculate bar color based on strength
            if strength > 75:
                color = '#27ae60'  # Green for strong
            elif strength > 50:
                color = '#3498db'  # Blue for medium-strong
            elif strength > 25:
                color = '#f39c12'  # Orange for medium-weak
            else:
                color = '#e74c3c'  # Red for weak
                
            # Draw the bar
            canvas.create_rectangle(0, 0, 2 * strength, 20, fill=color, outline='')
            canvas.create_text(100, 10, text=f"{strength}%", fill='white' if strength > 50 else 'black')
    
    def setup_conversations_tab(self):
        """Setup the Conversations tab with conversation history and filters"""
        # Create the conversations tab
        self.conversations_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.conversations_tab, text="💬 Conversations")
        
        # Configure grid
        self.conversations_tab.columnconfigure(0, weight=1)
        self.conversations_tab.rowconfigure(1, weight=1)
        
        # Filter frame
        filter_frame = ttk.Frame(self.conversations_tab, padding=10)
        filter_frame.grid(row=0, column=0, sticky='ew')
        
        # Friend filter
        ttk.Label(filter_frame, text="Filter by friend:").pack(side=tk.LEFT, padx=5)
        self.friend_filter_var = tk.StringVar()
        self.friend_filter = ttk.Combobox(
            filter_frame, 
            textvariable=self.friend_filter_var,
            state='readonly',
            width=30
        )
        self.friend_filter.pack(side=tk.LEFT, padx=5)
        self.friend_filter.bind('<<ComboboxSelected>>', self.update_conversation_filters)
        
        # Mood filter
        ttk.Label(filter_frame, text="Filter by mood:").pack(side=tk.LEFT, padx=5)
        self.mood_filter_var = tk.StringVar()
        self.mood_filter = ttk.Combobox(
            filter_frame, 
            textvariable=self.mood_filter_var,
            values=['All', '😊 Happy', '😐 Neutral', '😢 Sad', '😡 Angry', '😲 Surprised'],
            state='readonly',
            width=15
        )
        self.mood_filter.current(0)  # Default to 'All'
        self.mood_filter.pack(side=tk.LEFT, padx=5)
        self.mood_filter.bind('<<ComboboxSelected>>', self.update_conversation_filters)
        
        # Date range filter
        ttk.Label(filter_frame, text="Date range:").pack(side=tk.LEFT, padx=5)
        self.date_range_var = tk.StringVar()
        self.date_range = ttk.Combobox(
            filter_frame, 
            textvariable=self.date_range_var,
            values=['All time', 'Last 7 days', 'Last 30 days', 'Last 90 days', 'Last year'],
            state='readonly',
            width=15
        )
        self.date_range.current(0)  # Default to 'All time'
        self.date_range.pack(side=tk.LEFT, padx=5)
        self.date_range.bind('<<ComboboxSelected>>', self.update_conversation_filters)
        
        # Clear filters button
        clear_btn = ttk.Button(
            filter_frame, 
            text="Clear Filters", 
            command=self.clear_conversation_filters
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Conversation list with scrollbar
        list_frame = ttk.Frame(self.conversations_tab)
        list_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create a treeview to display conversations
        columns = ('date', 'friend', 'summary', 'mood')
        self.conversation_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show='headings',
            selectmode='browse',
            height=15
        )
        
        # Define headings
        self.conversation_tree.heading('date', text='Date', anchor='w')
        self.conversation_tree.heading('friend', text='Friend', anchor='w')
        self.conversation_tree.heading('summary', text='Summary', anchor='w')
        self.conversation_tree.heading('mood', text='Mood', anchor='w')
        
        # Configure column widths
        self.conversation_tree.column('date', width=150, minwidth=100, anchor='w')
        self.conversation_tree.column('friend', width=150, minwidth=100, anchor='w')
        self.conversation_tree.column('summary', width=400, minwidth=200, anchor='w')
        self.conversation_tree.column('mood', width=100, minwidth=80, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.conversation_tree.yview)
        self.conversation_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the tree and scrollbar
        self.conversation_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Bind double-click event to view conversation details
        self.conversation_tree.bind('<Double-1>', self.view_conversation_details)
        
        # Conversation details panel
        details_frame = ttk.LabelFrame(self.conversations_tab, text="Conversation Details", padding=10)
        details_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(0, 10))
        details_frame.columnconfigure(0, weight=1)
        
        self.conversation_details = scrolledtext.ScrolledText(
            details_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=8,
            font=('Segoe UI', 10)
        )
        self.conversation_details.grid(row=0, column=0, sticky='nsew')
        self.conversation_details.config(state=tk.DISABLED)
        
        # Action buttons
        button_frame = ttk.Frame(details_frame)
        button_frame.grid(row=1, column=0, sticky='e', pady=(10, 0))
        
        self.edit_btn = ttk.Button(
            button_frame, 
            text="✏️ Edit", 
            command=self.edit_conversation,
            state=tk.DISABLED
        )
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(
            button_frame, 
            text="🗑️ Delete", 
            command=self.delete_conversation,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Initialize conversation data
        self.populate_conversation_filters()
        self.update_conversation_list()
    
    def populate_conversation_filters(self):
        """Populate the friend filter dropdown with friend names"""
        friend_names = ["All Friends"] + sorted(self.friendgpt.friends.keys())
        self.friend_filter['values'] = friend_names
        if friend_names:
            self.friend_filter.current(0)  # Default to 'All Friends'
    
    def update_conversation_filters(self, event=None):
        """Update the conversation list based on selected filters"""
        self.update_conversation_list()
    
    def clear_conversation_filters(self):
        """Clear all conversation filters"""
        self.friend_filter.current(0)  # All Friends
        self.mood_filter.current(0)    # All moods
        self.date_range.current(0)     # All time
        self.update_conversation_list()
    
    def update_conversation_list(self):
        """Update the conversation list based on current filters"""
        # Clear existing items
        for item in self.conversation_tree.get_children():
            self.conversation_tree.delete(item)
        
        # Get filter values
        friend_filter = self.friend_filter_var.get()
        mood_filter = self.mood_filter_var.get()
        date_range = self.date_range_var.get()
        
        # Determine date range
        end_date = datetime.now()
        if date_range == 'Last 7 days':
            start_date = end_date - timedelta(days=7)
        elif date_range == 'Last 30 days':
            start_date = end_date - timedelta(days=30)
        elif date_range == 'Last 90 days':
            start_date = end_date - timedelta(days=90)
        elif date_range == 'Last year':
            start_date = end_date - timedelta(days=365)
        else:  # All time
            start_date = datetime.min
        
        # Collect all conversations
        all_conversations = []
        for friend_name, friend in self.friendgpt.friends.items():
            if friend_filter not in ['All Friends', ''] and friend_name != friend_filter:
                continue
                
            for conv in friend.conversation_history:
                try:
                    conv_date = datetime.strptime(conv.date, "%Y-%m-%d %H:%M:%S")
                    if conv_date < start_date or conv_date > end_date:
                        continue
                        
                    mood = getattr(conv, 'mood', '')
                    if mood_filter and mood_filter != 'All' and mood != mood_filter.replace(' ', ''):
                        continue
                        
                    all_conversations.append({
                        'friend': friend_name,
                        'date': conv_date,
                        'date_str': conv_date.strftime("%Y-%m-%d %H:%M"),
                        'summary': getattr(conv, 'summary', ''),
                        'mood': mood,
                        'follow_up': getattr(conv, 'follow_up', '')
                    })
                except (ValueError, AttributeError) as e:
                    print(f"Error processing conversation for {friend_name}: {e}")
        
        # Sort by date (newest first)
        all_conversations.sort(key=lambda x: x['date'], reverse=True)
        
        # Add to treeview
        for conv in all_conversations:
            self.conversation_tree.insert('', 'end', values=(
                conv['date_str'],
                conv['friend'],
                conv['summary'][:100] + '...' if len(conv['summary']) > 100 else conv['summary'],
                conv['mood']
            ))
        
        # Update status
        self.status_var.set(f"Showing {len(all_conversations)} conversations")
    
    def view_conversation_details(self, event):
        """Display details of the selected conversation"""
        selection = self.conversation_tree.selection()
        if not selection:
            return
            
        # Get the selected conversation
        item = self.conversation_tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 4:
            return
            
        friend_name = values[1]
        date_str = values[0]
        
        # Find the full conversation details
        friend = self.friendgpt.friends.get(friend_name)
        if not friend:
            return
            
        # Find the conversation with matching date
        for conv in friend.conversation_history:
            if conv.date.startswith(date_str):
                # Format the details
                details = f"Date: {conv.date}\n"
                details += f"Friend: {friend_name}\n"
                if hasattr(conv, 'mood') and conv.mood:
                    details += f"Mood: {conv.mood}\n"
                details += "\nSummary:\n"
                details += f"{conv.summary}\n\n"
                
                if hasattr(conv, 'follow_up') and conv.follow_up:
                    details += f"Follow-up: {conv.follow_up}\n"
                
                # Display in the details area
                self.conversation_details.config(state=tk.NORMAL)
                self.conversation_details.delete(1.0, tk.END)
                self.conversation_details.insert(tk.END, details)
                self.conversation_details.config(state=tk.DISABLED)
                
                # Enable action buttons
                self.edit_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
                
                break
    
    def edit_conversation(self):
        """Edit the selected conversation"""
        selection = self.conversation_tree.selection()
        if not selection:
            return
            
        # Get the selected conversation
        item = self.conversation_tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 4:
            return
            
        friend_name = values[1]
        date_str = values[0]
        
        friend = self.friendgpt.friends.get(friend_name)
        if not friend:
            return
            
        # Find the conversation with matching date
        for i, conv in enumerate(friend.conversation_history):
            if conv.date.startswith(date_str):
                # Create an edit dialog
                self.show_edit_conversation_dialog(friend, i, conv)
                break
    
    def show_edit_conversation_dialog(self, friend, conv_index, conversation):
        """Show dialog to edit a conversation"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Conversation with {friend.name}")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Configure grid
        dialog.columnconfigure(1, weight=1)
        
        # Date and time
        ttk.Label(dialog, text="Date and Time:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_var = tk.StringVar(value=conversation.date)
        date_entry = ttk.Entry(dialog, textvariable=date_var, width=25)
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Mood
        ttk.Label(dialog, text="Mood:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        mood_var = tk.StringVar(value=getattr(conversation, 'mood', ''))
        mood_frame = ttk.Frame(dialog)
        mood_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        moods = [
            ("😊 Happy", "😊"),
            ("😐 Neutral", "😐"),
            ("😢 Sad", "😢"),
            ("😡 Angry", "😡"),
            ("😲 Surprised", "😲")
        ]
        
        for i, (text, emoji) in enumerate(moods):
            rb = ttk.Radiobutton(
                mood_frame, 
                text=text, 
                variable=mood_var, 
                value=emoji
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Summary
        ttk.Label(dialog, text="Summary:").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        summary_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=60, height=10)
        summary_text.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        summary_text.insert(tk.END, getattr(conversation, 'summary', ''))
        
        # Follow-up
        ttk.Label(dialog, text="Follow-up:").grid(row=3, column=0, padx=5, pady=5, sticky="ne")
        followup_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=60, height=4)
        followup_text.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        followup_text.insert(tk.END, getattr(conversation, 'follow_up', ''))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        def save_changes():
            # Update the conversation
            conversation.date = date_var.get()
            conversation.mood = mood_var.get()
            conversation.summary = summary_text.get("1.0", tk.END).strip()
            conversation.follow_up = followup_text.get("1.0", tk.END).strip()
            
            # Save changes
            self.friendgpt.save_friends()
            self.update_conversation_list()
            dialog.destroy()
            
            # Show success message
            messagebox.showinfo("Success", "Conversation updated successfully", parent=self.root)
        
        ttk.Button(button_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Set focus to summary field
        summary_text.focus_set()
    
    def delete_conversation(self):
        """Delete the selected conversation"""
        selection = self.conversation_tree.selection()
        if not selection:
            return
            
        # Get the selected conversation
        item = self.conversation_tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 4:
            return
            
        friend_name = values[1]
        date_str = values[0]
        
        # Confirm deletion
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the conversation with {friend_name} on {date_str}?\n\nThis action cannot be undone.",
            parent=self.root
        ):
            return
            
        # Find and remove the conversation
        friend = self.friendgpt.friends.get(friend_name)
        if friend:
            for i, conv in enumerate(friend.conversation_history):
                if conv.date.startswith(date_str):
                    del friend.conversation_history[i]
                    self.friendgpt.save_friends()
                    self.update_conversation_list()
                    
                    # Clear details
                    self.conversation_details.config(state=tk.NORMAL)
                    self.conversation_details.delete(1.0, tk.END)
                    self.conversation_details.config(state=tk.DISABLED)
                    
                    # Disable action buttons
                    self.edit_btn.config(state=tk.DISABLED)
                    self.delete_btn.config(state=tk.DISABLED)
                    
                    # Show success message
                    messagebox.showinfo(
                        "Success", 
                        "Conversation deleted successfully",
                        parent=self.root
                    )
                    break
    
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')  # Start with a clean theme
        
        # Configure Treeview
        style.configure('Treeview', 
                      rowheight=30,
                      background="#ffffff",
                      fieldbackground="#ffffff",
                      foreground="#333333")
        style.map('Treeview',
                background=[('selected', '#3498db')],
                foreground=[('selected', 'white')])
        
        # Configure TNotebook
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', 
                      padding=[15, 5],
                      font=('Segoe UI', 10))
        style.map('TNotebook.Tab',
                background=[('selected', '#ffffff')],
                foreground=[('selected', '#2c3e50')])
        
        # Configure TFrame
        style.configure('TFrame', background='#ffffff')
        style.configure('Header.TFrame', background='#2c3e50')
        style.configure('Status.TFrame', background='#f8f9fa')
        
        # Configure TLabel
        style.configure('TLabel', background='#ffffff', foreground='#2c3e50')
        style.configure('Header.TLabel', 
                      font=('Segoe UI', 12, 'bold'), 
                      background='#2c3e50', 
                      foreground='white')
        
        # Configure TButton
        style.configure('TButton', 
                      padding=6,
                      font=('Segoe UI', 9))
        style.map('TButton',
                background=[('active', '#2980b9')],
                foreground=[('active', 'white')])
        
        # Configure TEntry
        style.configure('TEntry', 
                      fieldbackground='#ffffff',
                      padding=5)
        
        # Configure TCombobox
        style.configure('TCombobox', 
                      fieldbackground='#ffffff',
                      padding=5)
        
        # Configure TLabelframe
        style.configure('TLabelframe',
                      background='#ffffff')
        style.configure('TLabelframe.Label',
                      font=('Segoe UI', 10, 'bold'),
                      foreground='#2c3e50')
        
        # Configure Scrollbar
        style.configure('Vertical.TScrollbar',
                      background='#e0e0e0',
                      troughcolor='#f0f0f0',
                      arrowcolor='#2c3e50')
        style.map('Vertical.TScrollbar',
                background=[('active', '#3498db')])
        
        # Configure Accent buttons
        style.configure('Accent.TButton', 
                      padding=6,
                      font=('Segoe UI', 9),
                      background='#4CAF50',
                      foreground='white')
        style.map('Accent.TButton',
                background=[('active', '#3e8e41')],
                foreground=[('active', 'white')])
        
        # Configure Header buttons
        style.configure('Header.TButton', 
                      padding=6,
                      font=('Segoe UI', 9),
                      background='#2c3e50',
                      foreground='white')
        style.map('Header.TButton',
                background=[('active', '#233140')],
                foreground=[('active', 'white')])
        
        # Configure Entry and Text widgets
        style.configure('TEntry', font=('Segoe UI', 10), padding=5)
        style.configure('TCombobox', font=('Segoe UI', 10), padding=5)

    def setup_gui(self):
        """Setup the modern and responsive GUI interface"""
        self.root.title("FriendGPT - Your Personal Relationship Manager")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set application icon if available
        try:
            self.root.iconbitmap('friendgpt.ico')
        except:
            pass  # Icon file not found, use default

        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Header with title and quick actions
        header_frame = ttk.Frame(main_frame, style='Header.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # App title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Using emoji as icon for cross-platform compatibility
        ttk.Label(title_frame, text="👥 ", font=('Segoe UI', 24)).pack(side=tk.LEFT)
        ttk.Label(title_frame, text="FriendGPT", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Quick action buttons
        action_buttons = ttk.Frame(header_frame)
        action_buttons.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(action_buttons, text="➕ Add Friend", command=self.add_friend,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(action_buttons, text="🔄 Refresh", command=self.refresh_display).pack(side=tk.LEFT, padx=3)
        
        # Search and filter bar
        search_frame = ttk.LabelFrame(main_frame, text="Search & Filter", padding=10)
        search_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # Search box with icon
        search_container = ttk.Frame(search_frame)
        search_container.pack(fill=tk.X, expand=True)
        
        ttk.Label(search_container, text="🔍").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_container, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.search_friends)
        
        # Filter options
        filter_frame = ttk.Frame(search_frame)
        filter_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(filter_frame, text="Filter by:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, 
                       value="all", command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Needs Contact", variable=self.filter_var, 
                       value="needs_contact", command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Upcoming Events", variable=self.filter_var, 
                       value="upcoming_events", command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        content_frame.columnconfigure(1, weight=3)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel - Friends list with status indicators
        list_panel = ttk.LabelFrame(content_frame, text="Contacts", padding=5)
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_panel.columnconfigure(0, weight=1)
        list_panel.rowconfigure(1, weight=1)
        
        # Friends Treeview with multiple columns
        columns = ('name', 'last_contact', 'status')
        self.friends_tree = ttk.Treeview(list_panel, columns=columns, show='tree headings', 
                                       selectmode='browse', height=25)
        
        # Configure columns
        self.friends_tree.heading('name', text='Name', anchor='w', 
                                command=lambda: self.sort_treeview('name', False))
        self.friends_tree.heading('last_contact', text='Last Contact', anchor='w',
                                command=lambda: self.sort_treeview('last_contact', False))
        self.friends_tree.heading('status', text='Status', anchor='w')
        
        self.friends_tree.column('name', width=200, anchor='w')
        self.friends_tree.column('last_contact', width=150, anchor='w')
        self.friends_tree.column('status', width=100, anchor='w')
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(list_panel, orient="vertical", command=self.friends_tree.yview)
        x_scroll = ttk.Scrollbar(list_panel, orient="horizontal", command=self.friends_tree.xview)
        self.friends_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout
        self.friends_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        # Bind selection event
        self.friends_tree.bind('<<TreeviewSelect>>', self.on_friend_select)
        self.friends_tree.bind('<Double-1>', self.on_friend_double_click)
        
        # Right panel - Friend details in tabs
        right_panel = ttk.Frame(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Tab 1: Overview
        overview_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(overview_frame, text="Overview")
        
        # Create a frame for the upcoming birthdays section
        birthdays_frame = ttk.LabelFrame(overview_frame, text="Upcoming Birthdays", padding=10)
        birthdays_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        # Create treeview for upcoming birthdays
        columns = ('name', 'birthday', 'days_until')
        self.birthdays_tree = ttk.Treeview(birthdays_frame, columns=columns, show='headings', height=5)
        
        # Configure columns
        self.birthdays_tree.heading('name', text='Name')
        self.birthdays_tree.heading('birthday', text='Birthday')
        self.birthdays_tree.heading('days_until', text='Days Until')
        
        # Set column widths
        self.birthdays_tree.column('name', width=150)
        self.birthdays_tree.column('birthday', width=150, anchor='center')
        self.birthdays_tree.column('days_until', width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(birthdays_frame, orient='vertical', command=self.birthdays_tree.yview)
        self.birthdays_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.birthdays_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Update the display
        self.update_upcoming_birthdays_display()
        
        # Profile header
        self.profile_header = ttk.Frame(overview_frame)
        self.profile_header.pack(fill='x', pady=(0, 15))
        
        self.profile_icon = ttk.Label(self.profile_header, text="👤", font=('Segoe UI', 48))
        self.profile_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        self.profile_info = ttk.Frame(self.profile_header)
        self.profile_info.pack(side=tk.LEFT, fill='both', expand=True)
        
        self.name_label = ttk.Label(self.profile_info, text="", font=('Segoe UI', 16, 'bold'))
        self.name_label.pack(anchor='w')
        
        self.contact_label = ttk.Label(self.profile_info, text="", style='Status.TLabel')
        self.contact_label.pack(anchor='w')
        
        # Quick actions
        action_buttons = ttk.Frame(overview_frame)
        action_buttons.pack(fill='x', pady=(0, 15))
        
        ttk.Button(action_buttons, text="💬 Send Message", command=self.generate_checkin,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="📞 Call", command=self.initiate_call).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="📅 Schedule Meetup", command=self.schedule_meetup).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="📝 Log Conversation", command=self.log_conversation_dialog).pack(side=tk.LEFT, padx=2)
        
        # Details section
        details_frame = ttk.LabelFrame(overview_frame, text="Details", padding=10)
        details_frame.pack(fill='both', expand=True)
        
        # Use a text widget with tags for styling
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, font=('Segoe UI', 10), 
                                  padx=5, pady=5, height=10, relief='flat')
        self.details_text.pack(fill='both', expand=True)
        
        # Configure tags for styled text
        self.details_text.tag_configure('label', foreground='#666666')
        self.details_text.tag_configure('value', font=('Segoe UI', 10, 'normal'))
        self.details_text.tag_configure('section', font=('Segoe UI', 11, 'bold'), 
                                      spacing1=10, spacing3=5)
        self.details_text.tag_configure('warning', foreground='#e74c3c')
        self.details_text.tag_configure('success', foreground='#27ae60')
        
        # Tab 2: Conversations
        self.setup_conversations_tab()
        
        # Tab 3: Insights
        self.setup_insights_tab()
        
        # Status bar
        status_bar = ttk.Frame(main_frame, style='Status.TFrame', height=24)
        status_bar.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(15, 0))
        status_bar.grid_propagate(False)
        
        self.status_label = ttk.Label(status_bar, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Add a progress bar for relationship strength
        self.status_progress = ttk.Progressbar(status_bar, orient=tk.HORIZONTAL, length=150, mode='determinate')
        self.status_progress.pack(side=tk.RIGHT, padx=10, pady=2)
        
        # Initialize with welcome message
        self.update_status(f"Ready • {len(self.friendgpt.friends)} contacts loaded")
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.add_friend())
        self.root.bind('<F5>', lambda e: self.refresh_display())
        self.root.bind('<Control-f>', lambda e: search_entry.focus())
        
        # Center the window on screen
        self.center_window()

    def add_friend(self):
        """Show a dialog to add a new friend"""
        # Create a new top-level window as a dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Friend")
        dialog.transient(self.root)  # Set to be on top of the main window
        dialog.grab_set()  # Make the dialog modal
        
        # Position the dialog relative to the main window
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + 50
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Configure dialog grid
        dialog.columnconfigure(1, weight=1)
        
        # Name field
        ttk.Label(dialog, text="Name:", font=('Segoe UI', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        name_entry = ttk.Entry(dialog, font=('Segoe UI', 10), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='we')
        name_entry.focus_set()
        
        # Details field
        ttk.Label(dialog, text="Details:", font=('Segoe UI', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='ne')
        details_text = tk.Text(dialog, font=('Segoe UI', 10), width=30, height=4)
        details_text.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        # Add scrollbar to the details text
        scrollbar = ttk.Scrollbar(dialog, command=details_text.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        details_text['yscrollcommand'] = scrollbar.set
        
        # Button frame
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Add button
        def add_friend_action():
            name = name_entry.get().strip()
            details = details_text.get("1.0", tk.END).strip()
            
            if not name:
                messagebox.showwarning("Warning", "Please enter the friend's name.", parent=dialog)
                return
                
            if name in self.friendgpt.friends:
                messagebox.showwarning("Warning", f"Friend '{name}' already exists.", parent=dialog)
                return
                
            # Add the friend
            self.friendgpt.add_friend(name, details)
            self.refresh_display()
            self.status_var.set(f"Added friend: {name}")
            dialog.destroy()
            
            # Select the newly added friend
            self.select_friend_in_tree(name)
        
        ttk.Button(button_frame, text="Add Friend", command=add_friend_action, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to add friend
        dialog.bind('<Return>', lambda e: add_friend_action())

    def refresh_display(self):
        """Refresh both friends list and upcoming birthdays list"""
        self.refresh_friends_list()
        self.update_upcoming_birthdays_display()
        # Clear details pane if no friend is selected
        if not self.friends_tree.selection():
             self.details_text.config(state=tk.NORMAL)
             self.details_text.delete(1.0, tk.END)
             self.details_text.insert(tk.END, "Select a friend to see details.")
             self.details_text.config(state=tk.DISABLED)


    def refresh_friends_list(self):
        """Refresh the friends list display in the Treeview"""
        # Clear existing items
        for item in self.friends_tree.get_children():
            self.friends_tree.delete(item)

        # Add friends to tree, sorting by last contact
        friends_list = list(self.friendgpt.friends.values())
        # Sort by last contact (oldest first). Handle invalid dates by putting them last.
        def sort_key(friend):
             try:
                  return datetime.strptime(friend.last_contact, "%Y-%m-%d %H:%M:%S")
             except (ValueError, TypeError):
                  return datetime.min # Puts invalid dates at the very beginning (oldest)
        friends_list.sort(key=sort_key)


        for friend in friends_list:
            name = friend.name
            location = friend.details.get('location', 'Unknown')

            # Calculate days since last contact
            days_since_display = "N/A"
            status = "❓ Unknown"
            tags = () # For treeview item coloring

            try:
                last_contact_date = datetime.strptime(friend.last_contact, "%Y-%m-%d %H:%M:%S")
                days_since = (datetime.now() - last_contact_date).days

                if days_since >= 0:
                    days_since_display = f"{days_since} days ago"

                    if days_since > 30:
                        status = "⚠️ Long time"
                        self.friends_tree.tag_configure('long_time', foreground='orange')
                        tags = ('long_time',)
                    elif days_since >= 14: # Threshold set in get_friends_needing_contact
                        status = "🕐 Due for contact"
                        self.friends_tree.tag_configure('due', foreground='red')
                        tags = ('due',)
                    else:
                        status = "✅ Recent"
                        self.friends_tree.tag_configure('recent', foreground='green')
                        tags = ('recent',)
                else: # Future date? Invalid somehow?
                    days_since_display = friend.last_contact # Show raw date if calculation failed/future
                    status = "❓ Future?" # Or another indicator
                    self.friends_tree.tag_configure('future', foreground='blue')
                    tags = ('future',)

            except (ValueError, TypeError) as e:
                # Handle cases where last_contact was saved in an invalid format
                print(f"Error calculating days since contact for {name} (invalid format: {friend.last_contact}): {e}")
                days_since_display = "Invalid Date"
                status = "❌ Error"
                self.friends_tree.tag_configure('error', foreground='red')
                tags = ('error',)
            except Exception as e:
                print(f"Error calculating days since contact for {name}: {e}")
                days_since_display = "Error"
                status = "❌ Error"
                self.friends_tree.tag_configure('error', foreground='red')
                tags = ('error',)
                break  # Only one such message

            # Add friend to the treeview
            self.friends_tree.insert('', 'end', values=(name, location, days_since_display, status), tags=tags)
            
        # Update the birthdays display in a separate method
        self.update_upcoming_birthdays_display()

    def update_upcoming_birthdays_display(self):
        """Update the upcoming birthdays list display"""
        if not hasattr(self, 'birthdays_tree'):
            return
            
        # Clear existing items
        for item in self.birthdays_tree.get_children():
            self.birthdays_tree.delete(item)
            
        # Get upcoming birthdays
        upcoming_birthdays = self.friendgpt.get_upcoming_birthdays(days_ahead=30)
        
        if not upcoming_birthdays:
            self.birthdays_tree.insert('', 'end', values=("", "No upcoming birthdays in 30 days", ""))
            self.birthdays_tree.tag_configure('info', foreground='gray')
            for item_id in self.birthdays_tree.get_children():
                if "No upcoming birthdays" in self.birthdays_tree.item(item_id, 'values')[1]:
                    self.birthdays_tree.item(item_id, tags=('info',))
                    break
        else:
            for name, bday_str, when_str in upcoming_birthdays:
                tags = ()
                if "Today" in when_str:
                    self.birthdays_tree.tag_configure('today', foreground='blue', font=('Arial', 10, 'bold'))
                    tags = ('today',)
                elif "Tomorrow" in when_str:
                    self.birthdays_tree.tag_configure('tomorrow', foreground='navy')
                    tags = ('tomorrow',)
                elif 'in ' in when_str:
                    try:
                        days = int(when_str.split(' ')[1])
                        if days <= 7:
                            self.birthdays_tree.tag_configure('soon', foreground='darkgreen')
                            tags = ('soon',)
                        else:
                            self.birthdays_tree.tag_configure('later', foreground='gray')
                            tags = ('later',)
                    except (ValueError, IndexError):
                        pass
                
                self.birthdays_tree.insert('', 'end', values=(name, bday_str, when_str), tags=tags)


    def search_friends(self, event=None):
        """Search friends based on input"""
        query = self.search_entry.get().strip()

        # Clear existing items
        for item in self.friends_tree.get_children():
            self.friends_tree.delete(item)

        if not query:
            self.refresh_friends_list() # If search is empty, show all friends
            return

        # Add matching friends
        matches = self.friendgpt.search_friends(query)
        if not matches:
            self.friends_tree.insert('', tk.END, values=("", "No friends found matching search", "", ""))
            self.friends_tree.tag_configure('info', foreground='gray')
            for item_id in self.friends_tree.get_children():
                  if "No friends found" in self.friends_tree.item(item_id, 'values')[1]:
                       self.friends_tree.item(item_id, tags=('info',))
                       break

        else:
            # Display search results
            for name in matches:
                friend = self.friendgpt.friends[name]
                location = friend.details.get('location', 'Unknown')

                # Calculate days since last contact
                days_since_display = "N/A"
                status = "❓ Unknown"
                tags = ()

                try:
                    last_contact_date = datetime.strptime(friend.last_contact, "%Y-%m-%d %H:%M:%S")
                    days_since = (datetime.now() - last_contact_date).days
                    days_since_display = f"{days_since} days ago" if days_since >= 0 else friend.last_contact # Handle future/invalid here too

                    if days_since > 30:
                         status = "⚠️ Long time"
                         tags = ('long_time',)
                    elif days_since >= 14:
                         status = "🕐 Due for contact"
                         tags = ('due',)
                    elif days_since >= 0: # Recent contact within threshold
                         status = "✅ Recent"
                         tags = ('recent',)
                    else: # Negative days, likely future date or error
                        status = "❓ Future?"
                        tags = ('future',)

                except (ValueError, TypeError):
                    days_since_display = "Invalid Date"
                    status = "❌ Error"
                    tags = ('error',)
                except Exception as e:
                     print(f"Error calculating days since contact for {name} during search: {e}")
                     days_since_display = "Error"
                     status = "❌ Error"
                     tags = ('error',)


                self.friends_tree.insert('', tk.END, values=(name, location, days_since_display, status), tags=tags)


    def on_friend_double_click(self, event):
        """Handle double-click on a friend in the list to log a conversation."""
        # Get the item that was clicked
        item = self.friends_tree.identify('item', event.x, event.y)
        if item:
            # Get the friend's name from the first column
            friend_name = self.friends_tree.item(item, 'values')[0]
            # Only proceed if this is a valid friend (not a header or info message)
            if friend_name and friend_name not in ["", "No friends found matching search", "No upcoming birthdays in 30 days"]:
                # Open the log conversation dialog for this friend
                self.show_log_conversation_dialog(friend_name)

    def on_friend_select(self, event):
        """Handle friend selection"""
        selection = self.friends_tree.selection()
        if not selection:
            # Clear details if nothing is selected
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "Select a friend to see details.")
            self.details_text.config(state=tk.DISABLED)
            return

        item = self.friends_tree.item(selection[0])
        friend_name = item['values'][0] # Get name from the first column

        # Check if the selected item is one of the info messages (like "No friends found")
        if friend_name in ["", "No friends found matching search", "No friends found matching search", "No upcoming birthdays in 30 days"]: # Also handle birthday tree info message
             self.details_text.config(state=tk.NORMAL)
             self.details_text.delete(1.0, tk.END)
             self.details_text.insert(tk.END, "Select a valid friend entry to see details.")
             self.details_text.config(state=tk.DISABLED)
             return


        if friend_name in self.friendgpt.friends:
            friend = self.friendgpt.friends[friend_name]
            self.display_friend_details(friend)
        else:
             # This case should ideally not happen if list is populated correctly
             messagebox.showerror("Error", f"Friend data not found for '{friend_name}'.")
             self.details_text.config(state=tk.NORMAL)
             self.details_text.delete(1.0, tk.END)
             self.details_text.insert(tk.END, f"Error: Could not retrieve details for '{friend_name}'.")
             self.details_text.config(state=tk.DISABLED)


    def display_friend_details(self, friend: Friend):
        """Display friend details in the text area"""
        self.details_text.config(state=tk.NORMAL) # Enable editing temporarily
        self.details_text.delete(1.0, tk.END)

        details_text = f"👤 {friend.name}\n"
        details_text += "=" * 50 + "\n\n"

        # Display Birthday first if available
        if friend.birthday:
            details_text += f"🎂 Birthday: {friend.birthday}\n"
            # Optional: Try to parse and show days until
            try:
                today = datetime.now().date()
                # Attempt to parse the stored string
                bday_parsed = dateutil.parser.parse(friend.birthday).date()
                # Get date for this year, wrapping to next year if already passed
                bday_this_year = bday_parsed.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_parsed.replace(year=today.year + 1)
                delta = bday_this_year - today
                days_until = delta.days

                if days_until == 0:
                     details_text += "  (Today! 🎉)\n"
                elif days_until == 1:
                     details_text += "  (Tomorrow!)\n"
                elif days_until > 0:
                     details_text += f"  (in {days_until} days)\n"
                # If delta.days is negative after checking next year, it means the date parsing
                # somehow resulted in a date far in the past relative to today's month/day,
                # or the original string implied a past year that confused dateutil.
                # We can just show the parsed date without "in X days" in this case.
            except Exception as e:
                 details_text += f"  (Error parsing birthday for reminder: {e})\n"
                 # Optionally show the raw stored string again if parsing failed
                 # details_text += f"  Raw stored: {friend.birthday}\n"


        # Display Tags if available
        if friend.tags:
             details_text += f"\n🏷️ Tags: {', '.join(friend.tags)}\n"

        # Display Important Dates if available
        if friend.important_dates:
            details_text += f"\n🗓️ Important Dates:\n"
            for date_str in friend.important_dates:
                 details_text += f"  • {date_str}\n" # Could try parsing/displaying 'when' here too


        # Display parsed details (excluding those already shown or internal ones)
        details_text += "\n📋 Other Details:\n" # Changed label slightly
        known_specific_fields = ['birthday', 'tags', 'important_dates'] # Fields handled above
        internal_fields = ['original_details'] # Fields not meant for main display

        other_details_found = False # Flag to see if we printed anything in this section

        # Sort details keys for consistent display
        sorted_detail_keys = sorted(friend.details.keys())

        for key in sorted_detail_keys:
            value = friend.details[key]
            if key not in known_specific_fields and key not in internal_fields:
                display_key = key.replace('_', ' ').title()
                details_text += f"  • {display_key}: {value}\n"
                other_details_found = True

        if not other_details_found:
             details_text += "  No other structured details found.\n"


        if friend.details.get('original_details'):
            details_text += f"\n📝 Original Input String:\n  {friend.details['original_details']}\n" # Changed label


        details_text += f"\n📅 Last Contact: {friend.last_contact}\n"

        if friend.last_conversation:
            details_text += f"\n💬 Last Conversation Summary:\n  {friend.last_conversation}\n"

        # Display full conversation history
        details_text += f"\n📚 Conversation History ({len(friend.conversation_history)} entries):\n"
        if friend.conversation_history:
            # Iterate through history, showing all entries (most recent last is fine as it's appended)
            # Let's reverse to show most recent first in the display for clarity
            for i, conv in enumerate(reversed(friend.conversation_history)):
                # Calculate original index for display number
                original_index = len(friend.conversation_history) - 1 - i
                details_text += f"-- Entry {original_index + 1} ({conv.date}) --\n"
                details_text += f"  Summary: {conv.summary}\n"
                if conv.mood:
                    details_text += f"  Mood: {conv.mood}\n"
                if conv.follow_up:
                    details_text += f"  Follow-up: {conv.follow_up}\n"
                details_text += "\n"
        else:
             details_text += "  No conversation history logged yet.\n"


        self.details_text.insert(1.0, details_text)
        self.details_text.config(state=tk.DISABLED) # Make it read-only again


    def schedule_meetup(self):
        """Schedule a meetup with the selected friend"""
        selection = self.friends_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend first", parent=self.root)
            return
            
        friend_name = self.friends_tree.item(selection[0], 'values')[0]
        friend = self.friendgpt.friends.get(friend_name)
        
        if not friend:
            messagebox.showerror("Error", f"Could not find details for {friend_name}", parent=self.root)
            return
        
        # Create a dialog for scheduling a meetup
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Schedule Meetup with {friend_name}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        self._center_window(dialog)
        
        # Configure grid
        dialog.columnconfigure(1, weight=1)
        
        # Date and time selection
        ttk.Label(dialog, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(dialog, textvariable=date_var)
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(dialog, text="Time:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        time_entry = ttk.Entry(dialog, textvariable=time_var)
        time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Location
        ttk.Label(dialog, text="Location:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        location_var = tk.StringVar()
        location_entry = ttk.Entry(dialog, textvariable=location_var)
        location_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Notes
        ttk.Label(dialog, text="Notes:").grid(row=3, column=0, padx=5, pady=5, sticky="ne")
        notes_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=50, height=10)
        notes_text.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        def save_meetup():
            date_str = date_var.get().strip()
            time_str = time_var.get().strip()
            location = location_var.get().strip()
            notes = notes_text.get("1.0", tk.END).strip()
            
            if not all([date_str, time_str, location]):
                messagebox.showwarning("Warning", "Please fill in all required fields (Date, Time, Location)", parent=dialog)
                return
                
            try:
                # Parse the date and time
                meetup_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                
                # Add to friend's important dates
                meetup_info = {
                    'date': meetup_time.strftime("%Y-%m-%d %H:%M"),
                    'description': f"Meetup with {friend_name} at {location}",
                    'location': location,
                    'notes': notes
                }
                
                if not hasattr(friend, 'important_dates'):
                    friend.important_dates = []
                friend.important_dates.append(meetup_info)
                
                # Save changes
                self.friendgpt.save_friends()
                self.refresh_display()
                
                messagebox.showinfo("Success", f"Meetup scheduled with {friend_name} on {meetup_time.strftime('%B %d, %Y at %H:%M')}", parent=dialog)
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.", parent=dialog)
        
        ttk.Button(button_frame, text="Schedule", command=save_meetup).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
        # Set focus to location field
        location_entry.focus_set()
        
        # Bind Enter key to save
        dialog.bind("<Return>", lambda e: save_meetup())
        
        # Bind Escape key to close
        dialog.bind("<Escape>", lambda e: dialog.destroy())
        
        return

    def initiate_call(self):
        """Initiate a call to the selected friend"""
        selection = self.friends_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend first", parent=self.root)
            return
            
        friend_name = self.friends_tree.item(selection[0], 'values')[0]
        
        # Get the friend's phone number if available
        friend = self.friendgpt.friends.get(friend_name)
        if not friend:
            messagebox.showerror("Error", f"Could not find details for {friend_name}", parent=self.root)
            return
            
        phone_number = friend.details.get('phone') or friend.details.get('mobile') or friend.details.get('number')
        
        if not phone_number:
            messagebox.showinfo("No Phone Number", 
                              f"No phone number found for {friend_name}.\n\n"
                              f"Please add a phone number to their details.", 
                              parent=self.root)
            return
            
        # Ask for confirmation before calling
        if messagebox.askyesno("Confirm Call", 
                              f"Call {friend_name} at {phone_number}?", 
                              parent=self.root):
            try:
                # This will open the default dialer with the number
                import webbrowser
                webbrowser.open(f"tel:{phone_number}")
                self.status_var.set(f"Calling {friend_name}...")
            except Exception as e:
                messagebox.showerror("Error", f"Could not initiate call: {str(e)}", parent=self.root)

    def generate_checkin(self):
        """Generate a check-in message for selected friend"""
        selection = self.friends_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend first", parent=self.root)
            return

        item = self.friends_tree.item(selection[0])
        friend_name = item['values'][0]

        if friend_name not in self.friendgpt.friends:
             messagebox.showerror("Error", f"Friend data not found for '{friend_name}'.", parent=self.root)
             return

        message = self.friendgpt.generate_checkin_message(friend_name)

        # Create a new window to show the message
        msg_window = tk.Toplevel(self.root)
        msg_window.title(f"Check-in Message for {friend_name}")
        msg_window.geometry("500x350") # Slightly taller
        msg_window.transient(self.root) # Keep window on top of main window
        msg_window.grab_set() # Modal behavior

        ttk.Label(msg_window, text=f"Personalized Message for {friend_name}:", font=('Arial', 12, 'bold')).pack(pady=10)

        msg_text = scrolledtext.ScrolledText(msg_window, height=8, width=60, wrap=tk.WORD)
        msg_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        msg_text.insert(1.0, message)
        msg_text.config(state=tk.DISABLED) # Make read-only

        button_frame = ttk.Frame(msg_window)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Copy to Clipboard",
                  command=lambda: self.copy_to_clipboard(message, msg_window)).grid(row=0, column=0, padx=5) # Pass msg_window
        ttk.Button(button_frame, text="Close", command=msg_window.destroy).grid(row=0, column=1, padx=5)

        msg_window.mainloop() # Start local mainloop for dialog

    def get_suggestions(self):
        """Get conversation suggestions for selected friend"""
        selection = self.friends_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend first", parent=self.root)
            return

        item = self.friends_tree.item(selection[0])
        friend_name = item['values'][0]

        if friend_name not in self.friendgpt.friends:
             messagebox.showerror("Error", f"Friend data not found for '{friend_name}'.", parent=self.root)
             return

        suggestions = self.friendgpt.get_conversation_suggestions(friend_name)

        # Create a new window to show suggestions
        sugg_window = tk.Toplevel(self.root)
        sugg_window.title(f"Conversation Suggestions for {friend_name}")
        sugg_window.geometry("600x400")
        sugg_window.transient(self.root)
        sugg_window.grab_set()

        ttk.Label(sugg_window, text=f"Suggested questions/topics for {friend_name}:",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        sugg_text = scrolledtext.ScrolledText(sugg_window, height=15, width=70, wrap=tk.WORD)
        sugg_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        if not suggestions or (len(suggestions) == 1 and "don't have information" in suggestions[0]):
             sugg_text.insert(tk.END, "No specific suggestions based on details. Try general ones.")
        else:
            for i, suggestion in enumerate(suggestions, 1):
                sugg_text.insert(tk.END, f"{i}. {suggestion}\n\n")

        sugg_text.config(state=tk.DISABLED) # Make read-only

        ttk.Button(sugg_window, text="Close", command=sugg_window.destroy).pack(pady=10)

        sugg_window.mainloop()

    # New method to open the log conversation dialog
    def log_conversation_dialog(self):
        """Open a dialog to log conversation details"""
        selection = self.friends_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend first", parent=self.root)
            return

        item = self.friends_tree.item(selection[0])
        friend_name = item['values'][0]

        if friend_name not in self.friendgpt.friends:
             messagebox.showerror("Error", f"Friend data not found for '{friend_name}'.", parent=self.root)
             return

        # Create a dialog for conversation summary, mood, and follow-up
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Log Conversation with {friend_name}")
        dialog.geometry("550x450") # Increased size
        dialog.transient(self.root)
        dialog.grab_set() # Make it modal

        # Labels and Entry widgets
        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        date_label = ttk.Label(form_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        date_label.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)

        ttk.Label(form_frame, text="Summary:").grid(row=1, column=0, sticky=tk.NW, pady=2, padx=5)
        summary_text = scrolledtext.ScrolledText(form_frame, height=8, width=50, wrap=tk.WORD)
        summary_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=2, padx=5)

        ttk.Label(form_frame, text="Mood (Optional):").grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
        mood_entry = ttk.Entry(form_frame, width=50)
        mood_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

        ttk.Label(form_frame, text="Follow-up (Optional):").grid(row=3, column=0, sticky=tk.W, pady=2, padx=5)
        follow_up_entry = ttk.Entry(form_frame, width=50)
        follow_up_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

        # Button frame
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)


        def save_conversation():
            summary = summary_text.get(1.0, tk.END).strip()
            mood = mood_entry.get().strip()
            follow_up = follow_up_entry.get().strip()

            if not summary:
                messagebox.showwarning("Warning", "Please enter a conversation summary", parent=dialog)
                return

            # Call the modified log_conversation method
            self.friendgpt.log_conversation(friend_name, summary, mood if mood else None, follow_up if follow_up else None)

            # Refresh display and close dialog
            self.refresh_display()
            # Reselect the friend to show updated details immediately
            # Need to find the item in the treeview by name after refresh
            self.select_friend_in_tree(friend_name)

            dialog.destroy()
            self.status_var.set(f"Logged conversation with {friend_name}")

        ttk.Button(button_frame, text="Save", command=save_conversation).grid(row=0, column=0, padx=5, sticky=tk.E)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).grid(row=0, column=1, padx=5, sticky=tk.W)

        # Ensure dialog stays on top
        dialog.wait_window()

    def select_friend_in_tree(self, friend_name: str):
        """Selects a friend in the friends treeview by name and displays their details."""
        for item_id in self.friends_tree.get_children():
            if self.friends_tree.item(item_id, 'values')[0] == friend_name:
                self.friends_tree.selection_set(item_id)
                self.friends_tree.see(item_id) # Scroll to friend
                # Explicitly call display details after setting selection
                self.display_friend_details(self.friendgpt.friends[friend_name])
                return

    def delete_friend(self):
        """Delete selected friend"""
        selection = self.friends_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend first", parent=self.root)
            return

        item = self.friends_tree.item(selection[0])
        friend_name = item['values'][0]

        if friend_name not in self.friendgpt.friends:
             # This shouldn't happen if selection is from the list, but safety check
             messagebox.showerror("Error", f"Friend data not found for '{friend_name}'.", parent=self.root)
             return
             
        # Check if the selected item is one of the info messages (like "No friends found")
        if friend_name in ["", "No friends found matching search", "No friends found matching search", "No upcoming birthdays in 30 days"]:
             messagebox.showwarning("Warning", "Cannot delete informational row.", parent=self.root)
             return


        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {friend_name}? This cannot be undone.", parent=self.root):
            del self.friendgpt.friends[friend_name]
            self.friendgpt.save_friends()
            self.refresh_display() # Refresh both lists
            self.status_var.set(f"Deleted friend: {friend_name}")

    def copy_to_clipboard(self, text, parent_window=None):
        """Copy text to clipboard, optionally updating status in a parent window's label"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status_var.set("Copied to clipboard")
            if parent_window:
                 # You could add a label in the parent_window to show "Copied!" temporarily
                 # For now, just setting the main status bar.
                 pass # Add code here if you want dialog-specific status updates
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            self.status_var.set("Failed to copy to clipboard")


    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def update_status(self, message: str):
        """Update the status bar with the given message"""
        self.status_var.set(message)
        self.root.update_idletasks()

    def run(self):
        """Start the GUI application"""
        # Mainloop is now called in __init__
        pass

def main():
    """Main function to run FriendGPT"""
    # Configure console to handle Unicode properly on Windows
    import sys
    import os
    
    if os.name == 'nt':  # Windows
        sys.stdout.reconfigure(encoding='utf-8')
    
    try:
        print("🤖 Starting FriendGPT - Remember My People")
    except UnicodeEncodeError:
        print("Starting FriendGPT - Remember My People")
    
    print("=" * 50)

    # The GUI will handle its own mainloop
    app = FriendGPTGUI()

if __name__ == "__main__":
    main()