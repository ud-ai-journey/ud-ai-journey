/*
  # Add more quiz content and variety

  1. Updates
    - Add multiple questions to existing quiz rituals
    - Add more diverse ritual content
    - Improve quiz variety

  2. Content Enhancement
    - Multiple questions per quiz ritual
    - More engaging reflection prompts
    - Additional meditation practices
*/

-- Update existing quiz rituals with multiple questions
UPDATE rituals 
SET content = '{"questions": [
  {"q": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correct": 2},
  {"q": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "correct": 1},
  {"q": "What is the largest mammal in the world?", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], "correct": 1}
]}'
WHERE title = 'Daily Knowledge';

UPDATE rituals 
SET content = '{"questions": [
  {"q": "How many hearts does an octopus have?", "options": ["1", "2", "3", "4"], "correct": 2},
  {"q": "What is the hardest natural substance on Earth?", "options": ["Gold", "Iron", "Diamond", "Platinum"], "correct": 2},
  {"q": "Which gas makes up about 78% of Earth''s atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "correct": 2}
]}'
WHERE title = 'Fun Fact';

-- Add more varied rituals
INSERT INTO rituals (type, title, description, content) VALUES
  ('quiz', 'Science Quiz', 'Test your science knowledge', '{"questions": [
    {"q": "What is the chemical symbol for gold?", "options": ["Go", "Gd", "Au", "Ag"], "correct": 2},
    {"q": "How many bones are in an adult human body?", "options": ["206", "208", "210", "212"], "correct": 0},
    {"q": "What is the speed of light?", "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"], "correct": 0}
  ]}'),
  
  ('reflection', 'Evening Reflection', 'Reflect on your day and prepare for tomorrow', '{"prompts": [
    "What was the highlight of your day?", 
    "What challenge did you overcome today?", 
    "What are you looking forward to tomorrow?",
    "How did you grow as a person today?"
  ]}'),
  
  ('task', 'Mindful Breathing', 'Practice conscious breathing for one minute', '{"steps": [
    "Sit comfortably with your back straight",
    "Place one hand on your chest, one on your belly",
    "Breathe in slowly through your nose for 4 counts",
    "Hold your breath for 2 counts",
    "Exhale slowly through your mouth for 6 counts",
    "Repeat this cycle for one minute"
  ]}'),
  
  ('meditation', 'Loving Kindness', 'Send positive thoughts to yourself and others', '{"instructions": [
    "Sit quietly and close your eyes",
    "Think of someone you love and send them good wishes",
    "Think of yourself and send yourself compassion",
    "Think of someone neutral and wish them well",
    "Think of someone difficult and try to send them peace",
    "Extend these wishes to all beings everywhere"
  ]}'),

  ('quiz', 'Geography Challenge', 'Test your world knowledge', '{"questions": [
    {"q": "Which is the longest river in the world?", "options": ["Amazon", "Nile", "Mississippi", "Yangtze"], "correct": 1},
    {"q": "What is the smallest country in the world?", "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"], "correct": 1},
    {"q": "Which mountain range contains Mount Everest?", "options": ["Andes", "Alps", "Himalayas", "Rockies"], "correct": 2}
  ]}'),

  ('reflection', 'Gratitude & Growth', 'Focus on appreciation and personal development', '{"prompts": [
    "What skill are you most grateful to have learned?",
    "Who has had the biggest positive impact on your life?",
    "What mistake taught you the most valuable lesson?",
    "What aspect of your personality are you most proud of?"
  ]}'),

  ('task', 'Digital Detox Minute', 'Take a break from screens and technology', '{"steps": [
    "Put away all electronic devices",
    "Look out a window or step outside",
    "Notice 5 things you can see in nature",
    "Take 3 deep breaths of fresh air",
    "Appreciate this moment of digital silence"
  ]}'),

  ('meditation', 'Body Gratitude', 'Appreciate your body and its capabilities', '{"instructions": [
    "Sit or lie down comfortably",
    "Start by thanking your feet for carrying you",
    "Thank your hands for all they help you do",
    "Thank your heart for beating faithfully",
    "Thank your mind for its creativity and thoughts",
    "End by thanking your whole body for supporting you"
  ]}');