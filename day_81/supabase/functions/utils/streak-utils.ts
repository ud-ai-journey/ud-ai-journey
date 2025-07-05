import { Database, StreakUpdate } from '../types.ts'

type SupabaseClient = any // We'll use any for now since we're in Deno environment

/**
 * Calculate the number of days between two dates
 * Uses UTC to avoid timezone issues
 */
export function calculateDaysDifference(date1: string, date2: string): number {
  const d1 = new Date(date1 + 'T00:00:00Z')
  const d2 = new Date(date2 + 'T00:00:00Z')
  const diffTime = Math.abs(d2.getTime() - d1.getTime())
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

/**
 * Get today's date in YYYY-MM-DD format (UTC)
 */
export function getTodayDate(): string {
  return new Date().toISOString().split('T')[0]
}

/**
 * Calculate streak update based on last completion date
 * Handles edge cases like:
 * - First completion (no previous streak)
 * - Consecutive days (increment streak)
 * - Missed days (reset streak)
 * - Same day completion (no change)
 */
export function calculateStreakUpdate(
  lastCompletionDate: string | null,
  currentStreak: number = 0,
  longestStreak: number = 0
): StreakUpdate {
  const today = getTodayDate()
  
  // If no previous completion, start with streak of 1
  if (!lastCompletionDate) {
    return {
      currentStreak: 1,
      longestStreak: 1,
      lastCompletionDate: today,
      isNewRecord: false
    }
  }

  // If already completed today, no change
  if (lastCompletionDate === today) {
    return {
      currentStreak,
      longestStreak,
      lastCompletionDate,
      isNewRecord: false
    }
  }

  const daysDiff = calculateDaysDifference(lastCompletionDate, today)

  // Consecutive day - increment streak
  if (daysDiff === 1) {
    const newStreak = currentStreak + 1
    const newLongestStreak = Math.max(longestStreak, newStreak)
    
    return {
      currentStreak: newStreak,
      longestStreak: newLongestStreak,
      lastCompletionDate: today,
      isNewRecord: newStreak > longestStreak
    }
  }

  // Missed days or more than 1 day gap - reset streak
  return {
    currentStreak: 1,
    longestStreak: Math.max(longestStreak, 1),
    lastCompletionDate: today,
    isNewRecord: false
  }
}

/**
 * Update user streak in database
 */
export async function updateUserStreak(
  supabase: SupabaseClient,
  userId: string,
  streakUpdate: StreakUpdate
): Promise<void> {
  const { error } = await supabase
    .from('user_streaks')
    .upsert({
      user_id: userId,
      current_streak: streakUpdate.currentStreak,
      longest_streak: streakUpdate.longestStreak,
      last_completion_date: streakUpdate.lastCompletionDate,
      updated_at: new Date().toISOString()
    })

  if (error) {
    console.error('Error updating user streak:', error)
    throw new Error('Failed to update user streak')
  }
}

/**
 * Get or create user streak record
 */
export async function getUserStreak(
  supabase: SupabaseClient,
  userId: string
): Promise<Database['public']['Tables']['user_streaks']['Row'] | null> {
  const { data, error } = await supabase
    .from('user_streaks')
    .select('*')
    .eq('user_id', userId)
    .single()

  if (error && error.code !== 'PGRST116') { // PGRST116 = no rows returned
    console.error('Error fetching user streak:', error)
    throw new Error('Failed to fetch user streak')
  }

  return data
}

/**
 * Get total completions for a user
 */
export async function getUserTotalCompletions(
  supabase: SupabaseClient,
  userId: string
): Promise<number> {
  const { count, error } = await supabase
    .from('daily_completions')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)

  if (error) {
    console.error('Error counting user completions:', error)
    throw new Error('Failed to count user completions')
  }

  return count || 0
}

/**
 * Check if user has already completed a ritual today
 */
export async function checkTodayCompletion(
  supabase: SupabaseClient,
  userId: string
): Promise<boolean> {
  const today = getTodayDate()
  
  const { data, error } = await supabase
    .from('daily_completions')
    .select('id')
    .eq('user_id', userId)
    .eq('date', today)
    .single()

  if (error && error.code !== 'PGRST116') {
    console.error('Error checking today completion:', error)
    throw new Error('Failed to check today completion')
  }

  return !!data
} 