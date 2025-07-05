/*
  # Add Sample Rituals

  1. New Data
    - Insert sample rituals for testing the application
    - Includes different types: reflection, task, quiz, meditation
    - Each ritual has structured content for the frontend to display

  2. Content Structure
    - Reflection: prompts array
    - Task: steps array  
    - Quiz: questions array with options and correct answers
    - Meditation: instructions array
*/

-- Insert sample rituals
INSERT INTO rituals (type, title, description, content) VALUES
(
  'reflection',
  'Morning Gratitude',
  'Start your day by reflecting on what you''re grateful for',
  '{
    "prompts": [
      "What are three things you''re grateful for today?",
      "Who in your life brings you joy and why?",
      "What small moment yesterday made you smile?"
    ]
  }'
),
(
  'task',
  'Desk Organization',
  'Take a minute to organize your workspace for better focus',
  '{
    "steps": [
      "Clear any unnecessary items from your desk surface",
      "Organize your most-used items within arm''s reach",
      "Put away or file any loose papers",
      "Wipe down your desk surface",
      "Take a deep breath and appreciate your clean space"
    ]
  }'
),
(
  'quiz',
  'Mindfulness Knowledge',
  'Test your understanding of mindfulness principles',
  '{
    "questions": [
      {
        "q": "What is the primary goal of mindfulness practice?",
        "options": [
          "To eliminate all thoughts",
          "To be present and aware in the moment",
          "To achieve perfect relaxation",
          "To solve all your problems"
        ],
        "correct": 1
      },
      {
        "q": "How long should you practice mindfulness to see benefits?",
        "options": [
          "Only during formal meditation sessions",
          "At least 2 hours daily",
          "Even a few minutes can be beneficial",
          "Only when you''re stressed"
        ],
        "correct": 2
      }
    ]
  }'
),
(
  'meditation',
  'One-Minute Breathing',
  'A simple breathing exercise to center yourself',
  '{
    "instructions": [
      "Sit comfortably with your back straight",
      "Close your eyes or soften your gaze",
      "Take a deep breath in through your nose for 4 counts",
      "Hold your breath gently for 2 counts",
      "Exhale slowly through your mouth for 6 counts",
      "Repeat this cycle 3-4 times",
      "Notice how you feel when you''re done"
    ]
  }'
),
(
  'reflection',
  'Evening Review',
  'Reflect on your day and set intentions for tomorrow',
  '{
    "prompts": [
      "What was the highlight of your day?",
      "What challenge did you overcome today?",
      "How do you want to feel tomorrow?",
      "What one thing can you do tomorrow to move closer to your goals?"
    ]
  }'
),
(
  'task',
  'Hydration Check',
  'Ensure you''re staying properly hydrated',
  '{
    "steps": [
      "Fill up a glass or bottle with water",
      "Drink at least 8 ounces slowly",
      "Notice how the water feels and tastes",
      "Set a reminder to drink water again in 2 hours",
      "Appreciate your body for all it does for you"
    ]
  }'
),
(
  'quiz',
  'Habit Formation',
  'Learn about building lasting habits',
  '{
    "questions": [
      {
        "q": "According to research, how long does it typically take to form a new habit?",
        "options": [
          "Exactly 21 days",
          "It varies, but averages around 66 days",
          "One week with enough motivation",
          "It''s impossible to predict"
        ],
        "correct": 1
      },
      {
        "q": "What''s the most effective way to build a new habit?",
        "options": [
          "Start with big, dramatic changes",
          "Rely purely on willpower",
          "Start small and be consistent",
          "Only practice when you feel motivated"
        ],
        "correct": 2
      }
    ]
  }'
),
(
  'meditation',
  'Body Scan',
  'A quick body awareness exercise',
  '{
    "instructions": [
      "Sit or lie down in a comfortable position",
      "Close your eyes and take three deep breaths",
      "Start by noticing the top of your head",
      "Slowly move your attention down through your face, neck, and shoulders",
      "Continue scanning down through your arms, chest, and stomach",
      "Notice your hips, legs, and feet",
      "Take a moment to appreciate your whole body"
    ]
  }'
);