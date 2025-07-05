-- Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create rituals table
CREATE TABLE IF NOT EXISTS rituals (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type text NOT NULL CHECK (type IN ('reflection', 'task', 'quiz', 'meditation')),
  title text NOT NULL,
  description text NOT NULL,
  content jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Create daily_completions table
CREATE TABLE IF NOT EXISTS daily_completions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  ritual_id uuid NOT NULL REFERENCES rituals(id) ON DELETE CASCADE,
  completed_at timestamptz DEFAULT now(),
  date date NOT NULL DEFAULT CURRENT_DATE,
  UNIQUE(user_id, date)
);

-- Create user_badges table
CREATE TABLE IF NOT EXISTS user_badges (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  badge_id text NOT NULL,
  earned_at timestamptz DEFAULT now(),
  UNIQUE(user_id, badge_id)
);

-- Create user_streaks table
CREATE TABLE IF NOT EXISTS user_streaks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  current_streak integer DEFAULT 0,
  longest_streak integer DEFAULT 0,
  last_completion_date date,
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id)
);

-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE rituals ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_completions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_streaks ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can read own profile"
  ON user_profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Anyone can read rituals"
  ON rituals FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can read own completions"
  ON daily_completions FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own completions"
  ON daily_completions FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can read own badges"
  ON user_badges FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own badges"
  ON user_badges FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can read own streaks"
  ON user_streaks FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own streaks"
  ON user_streaks FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own streaks"
  ON user_streaks FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid());

-- Insert sample ritual data
INSERT INTO rituals (type, title, description, content) VALUES
  ('reflection', '3 Gratitudes', 'Take a moment to reflect on three things you''re grateful for today', '{"prompts": ["What made you smile today?", "Who are you grateful for?", "What small win did you have?"]}'),
  ('task', 'Desk Organization', 'Spend one minute organizing your workspace', '{"steps": ["Clear your desk surface", "Put items in their designated spots", "Wipe down your workspace"]}'),
  ('quiz', 'Daily Knowledge', 'Test your knowledge with a quick question', '{"questions": [{"q": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correct": 2}]}'),
  ('meditation', 'Breathing Space', 'Take 60 seconds to focus on your breath', '{"instructions": ["Find a comfortable position", "Close your eyes or soften your gaze", "Take 5 deep breaths", "Notice the present moment"]}'),
  ('reflection', 'Intention Setting', 'Set a clear intention for your day', '{"prompts": ["What do you want to accomplish today?", "How do you want to feel?", "What energy do you want to bring?"]}'),
  ('task', 'Hydration Check', 'Drink a glass of water mindfully', '{"steps": ["Get a glass of water", "Drink it slowly", "Notice the temperature and taste", "Appreciate your body"]}'),
  ('quiz', 'Fun Fact', 'Learn something new in 60 seconds', '{"questions": [{"q": "How many hearts does an octopus have?", "options": ["1", "2", "3", "4"], "correct": 2}]}'),
  ('meditation', 'Body Scan', 'Quick body awareness practice', '{"instructions": ["Sit comfortably", "Start at the top of your head", "Notice each part of your body", "Release any tension you find"]}');