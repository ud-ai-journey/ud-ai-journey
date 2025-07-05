-- Fix RLS policies to use correct auth function

-- Drop existing policies
DROP POLICY IF EXISTS "Users can read own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can read own completions" ON daily_completions;
DROP POLICY IF EXISTS "Users can insert own completions" ON daily_completions;
DROP POLICY IF EXISTS "Users can read own badges" ON user_badges;
DROP POLICY IF EXISTS "Users can insert own badges" ON user_badges;
DROP POLICY IF EXISTS "Users can read own streaks" ON user_streaks;
DROP POLICY IF EXISTS "Users can insert own streaks" ON user_streaks;
DROP POLICY IF EXISTS "Users can update own streaks" ON user_streaks;

-- Create corrected policies using auth.uid()
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