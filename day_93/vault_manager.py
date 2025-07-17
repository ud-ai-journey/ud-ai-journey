import json
from datetime import datetime, timedelta
import os
import uuid

class VaultManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.entries_file = os.path.join(data_dir, "entries.json")
        self.flashcards_file = os.path.join(data_dir, "flashcards.json")
        self._ensure_data_dir()
        self._load_data()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        for file in [self.entries_file, self.flashcards_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump([], f)

    def _load_data(self):
        """Load entries and flashcards from files. Migrate missing flashcard IDs."""
        with open(self.entries_file, 'r') as f:
            self.entries = json.load(f)
        with open(self.flashcards_file, 'r') as f:
            self.flashcards = json.load(f)
        # Migration: assign id to flashcards missing it
        changed = False
        for card in self.flashcards:
            if 'id' not in card:
                import uuid
                card['id'] = uuid.uuid4().hex
                changed = True
        if changed:
            self._save_data()

    def _save_data(self):
        """Save entries and flashcards to files."""
        with open(self.entries_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
        with open(self.flashcards_file, 'w') as f:
            json.dump(self.flashcards, f, indent=2)

    def add_entry(self, title, notes, tag, mood, summary, flashcards, next_review):
        """Add a new learning entry."""
        entry = {
            "id": len(self.entries) + 1,
            "title": title,
            "notes": notes,
            "tag": tag,
            "mood": mood,
            "summary": summary,
            "created_at": datetime.now().isoformat(),
            "next_review": next_review.isoformat()
        }
        self.entries.append(entry)
        # Add flashcards with reference to entry and assign unique id and next_review
        for card in flashcards:
            card["id"] = uuid.uuid4().hex
            card["entry_id"] = entry["id"]
            card["reviews"] = []
            card["ease_factor"] = 2.5
            card["interval"] = 1
            card["next_review"] = next_review.isoformat()
        self.flashcards.extend(flashcards)
        self._save_data()
        return entry["id"]

    def get_entries(self):
        """Get all learning entries."""
        return self.entries

    def get_flashcards_for_entry(self, entry_id):
        """Get flashcards for a specific entry."""
        return [card for card in self.flashcards if card["entry_id"] == entry_id]

    def get_due_flashcards(self):
        """Get flashcards due for review."""
        today = datetime.now().date()
        due_cards = []
        for card in self.flashcards:
            last_review = None
            if card["reviews"]:
                last_review = datetime.fromisoformat(card["reviews"][-1]["date"]).date()
            else:
                last_review = datetime.fromisoformat(card["next_review"]).date() if "next_review" in card else None
            if not last_review or (today - last_review).days >= card["interval"]:
                due_cards.append(card)
        return due_cards

    def record_review(self, card_id, quality, spaced_repetition=None):
        """Record a flashcard review and update scheduling."""
        for card in self.flashcards:
            if card.get("id") == card_id:
                review = {
                    "date": datetime.now().isoformat(),
                    "quality": quality
                }
                card["reviews"].append(review)
                # Update interval and ease factor using spaced repetition
                if spaced_repetition:
                    interval, ease = spaced_repetition.calculate_next_review(
                        card.get("interval", 1),
                        card.get("ease_factor", 2.5),
                        quality
                    )
                    card["interval"] = interval
                    card["ease_factor"] = ease
                    # Update next_review date
                    last_review_date = datetime.fromisoformat(review["date"]).date()
                    card["next_review"] = (last_review_date + timedelta(days=interval)).isoformat()
                self._save_data()
                break

    def export_entries_to_csv(self, csv_path):
        import pandas as pd
        df = pd.DataFrame(self.entries)
        df.to_csv(csv_path, index=False)

    def export_flashcards_to_csv(self, csv_path):
        import pandas as pd
        df = pd.DataFrame(self.flashcards)
        df.to_csv(csv_path, index=False)

    def export_entries_to_markdown(self, md_path):
        with open(md_path, 'w', encoding='utf-8') as f:
            for entry in self.entries:
                f.write(f"## {entry['title']}\n")
                f.write(f"**Tag:** {entry['tag']}  |  **Mood:** {entry['mood']}  |  **Date:** {entry['created_at']}\n\n")
                f.write(f"**Summary:** {entry['summary']}\n\n")
                f.write(f"**Notes:**\n{entry['notes']}\n\n")
                f.write(f"**Next Review:** {entry['next_review']}\n\n---\n\n")

    def export_entries_to_pdf(self, pdf_path):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for entry in self.entries:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, entry['title'], ln=True)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Tag: {entry['tag']}  |  Mood: {entry['mood']}  |  Date: {entry['created_at']}", ln=True)
            pdf.multi_cell(0, 10, f"Summary: {entry['summary']}")
            pdf.multi_cell(0, 10, f"Notes: {entry['notes']}")
            pdf.cell(0, 10, f"Next Review: {entry['next_review']}", ln=True)
            pdf.ln(5)
        pdf.output(pdf_path)

    def get_statistics(self):
        """Get learning statistics."""
        total_entries = len(self.entries)
        total_cards = len(self.flashcards)
        total_reviews = sum(len(card["reviews"]) for card in self.flashcards)
        # Calculate review completion rate for the week
        due_this_week = len([card for card in self.flashcards 
                            if any(r["date"].startswith(datetime.now().strftime("%Y-%m")) 
                                  for r in card["reviews"])])
        reviewed_this_week = len([card for card in self.flashcards 
                                if any(r["date"].startswith(datetime.now().strftime("%Y-%m")) 
                                      for r in card["reviews"])])
        weekly_completion = (reviewed_this_week / due_this_week * 100) if due_this_week > 0 else 0
        return {
            "total_entries": total_entries,
            "total_cards": total_cards,
            "total_reviews": total_reviews,
            "weekly_completion": weekly_completion
        }

    def edit_entry(self, entry_id, **kwargs):
        """Edit an entry by id. kwargs can include title, notes, tag, mood, summary, next_review."""
        for entry in self.entries:
            if entry["id"] == entry_id:
                for k, v in kwargs.items():
                    if k in entry:
                        entry[k] = v
                self._save_data()
                return True
        return False

    def delete_entry(self, entry_id):
        """Delete an entry and its flashcards."""
        self.entries = [e for e in self.entries if e["id"] != entry_id]
        self.flashcards = [c for c in self.flashcards if c["entry_id"] != entry_id]
        self._save_data()
        return True

    def edit_flashcard(self, card_id, **kwargs):
        """Edit a flashcard by id. kwargs can include question, answer, interval, ease_factor, etc."""
        for card in self.flashcards:
            if card["id"] == card_id:
                for k, v in kwargs.items():
                    if k in card:
                        card[k] = v
                self._save_data()
                return True
        return False

    def delete_flashcard(self, card_id):
        """Delete a flashcard by id."""
        self.flashcards = [c for c in self.flashcards if c["id"] != card_id]
        self._save_data()
        return True

    def backup_all_data(self, zip_path):
        import zipfile
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(self.entries_file, arcname='entries.json')
            zipf.write(self.flashcards_file, arcname='flashcards.json')
        return zip_path

    def restore_from_backup(self, zip_file):
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zipf:
            zipf.extract('entries.json', self.data_dir)
            zipf.extract('flashcards.json', self.data_dir)
        self._load_data()
        return True
