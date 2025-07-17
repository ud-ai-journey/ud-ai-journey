import os
import requests
from dotenv import load_dotenv

class AIHelper:
    def __init__(self, model=None):
        load_dotenv()
        self.api_key = os.getenv('GROQ_API_KEY', 'REMOVED_SECRET ')
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.model = model or 'llama3-8b-8192'  # Default model

    def set_model(self, model_name):
        self.model = model_name

    def _call_groq(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 512,
            'temperature': 0.7
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"[AI Error: Could not generate response. Please try again later. Details: {e}]"

    def generate_summary(self, title, notes, tag):
        prompt = f"""
        Title: {title}
        Notes: {notes}
        Tag: {tag}
        
        Create a concise 2-3 sentence summary of this learning material.
        Focus on the key concepts and main takeaways.
        """
        return self._call_groq(prompt)

    def generate_flashcards(self, title, notes, tag, num_cards=3):
        prompt = f"""
        Based on this learning material:
        Title: {title}
        Notes: {notes}
        Tag: {tag}
        
        Generate {num_cards} flashcards in JSON format like this:
        {{
            "flashcards": [
                {{"question": "Q1", "answer": "A1"}},
                {{"question": "Q2", "answer": "A2"}},
                ...
            ]
        }}
        
        Make questions that test understanding, not just memorization.
        """
        return self._call_groq(prompt)
