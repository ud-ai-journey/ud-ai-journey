-- Fix RLS policy for rituals table to allow anonymous users to read
DROP POLICY IF EXISTS "Anyone can read rituals" ON rituals;

CREATE POLICY "Anyone can read rituals"
  ON rituals FOR SELECT
  TO anon, authenticated
  USING (true); 