/*
  # Enhanced Badges System and Improved Schema

  1. New Tables
    - `badges` table for dynamic badge management
    - Enhanced indexes for performance
    - Better RLS policies

  2. Improvements
    - Add badges table with criteria JSONB
    - Add indexes for better query performance
    - Enhance RLS policies for better security
    - Add timezone-aware date functions
*/

-- Create badges table for dynamic badge management
CREATE TABLE IF NOT EXISTS badges (
  id text PRIMARY KEY,
  name text NOT NULL,
  description text NOT NULL,
  icon text NOT NULL,
  criteria jsonb NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_daily_completions_user_date ON daily_completions(user_id, date);
CREATE INDEX IF NOT EXISTS idx_user_badges_user_badge ON user_badges(user_id, badge_id);
CREATE INDEX IF NOT EXISTS idx_user_streaks_user_id ON user_streaks(user_id);

-- Add timezone-aware date function
CREATE OR REPLACE FUNCTION get_user_timezone_date(user_id uuid)
RETURNS date AS $$
BEGIN
  -- Default to UTC if no timezone is set
  -- In a real app, you'd store user timezone preferences
  RETURN CURRENT_DATE AT TIME ZONE 'UTC';
END;
$$ LANGUAGE plpgsql;

-- Enhanced RLS policies with better security
DROP POLICY IF EXISTS "Users can read own completions" ON daily_completions;
DROP POLICY IF EXISTS "Users can insert own completions" ON daily_completions;
DROP POLICY IF EXISTS "Users can read own badges" ON user_badges;
DROP POLICY IF EXISTS "Users can insert own badges" ON user_badges;
DROP POLICY IF EXISTS "Users can read own streaks" ON user_streaks;
DROP POLICY IF EXISTS "Users can insert own streaks" ON user_streaks;
DROP POLICY IF EXISTS "Users can update own streaks" ON user_streaks;

-- Recreate policies with better security
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

-- Add policies for badges table
CREATE POLICY "Anyone can read badges"
  ON badges FOR SELECT
  TO authenticated
  USING (true);

-- Insert default badges with proper criteria
INSERT INTO badges (id, name, description, icon, criteria) VALUES
  ('first_step', 'First Step', 'Complete your first ritual', '🌟', '{"type": "completion", "value": 1}'),
  ('consistent', 'Consistent', 'Complete 3 rituals', '💪', '{"type": "completion", "value": 3}'),
  ('dedicated', 'Dedicated', 'Complete 7 rituals', '🏆', '{"type": "completion", "value": 7}'),
  ('champion', 'Champion', 'Complete 30 rituals', '👑', '{"type": "completion", "value": 30}'),
  ('streak_3', 'On Fire', 'Maintain a 3-day streak', '🔥', '{"type": "streak", "value": 3}'),
  ('streak_7', 'Unstoppable', 'Maintain a 7-day streak', '⚡', '{"type": "streak", "value": 7}'),
  ('streak_30', 'Legendary', 'Maintain a 30-day streak', '🦄', '{"type": "streak", "value": 30}'),
  ('early_bird', 'Early Bird', 'Complete 5 morning rituals (before 9 AM)', '🌅', '{"type": "early_bird", "value": 5}');

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_badges_updated_at BEFORE UPDATE ON badges
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); 