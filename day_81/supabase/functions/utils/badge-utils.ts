import { Database, BadgeCriteria, BadgeInfo } from '../types.ts'

type SupabaseClient = any

/**
 * Check if user meets badge criteria
 */
export function checkBadgeCriteria(
  criteria: BadgeCriteria,
  userStats: {
    totalCompletions: number
    currentStreak: number
    earlyBirdCompletions?: number
  }
): boolean {
  switch (criteria.type) {
    case 'completion':
      return userStats.totalCompletions >= criteria.value
    case 'streak':
      return userStats.currentStreak >= criteria.value
    case 'early_bird':
      return (userStats.earlyBirdCompletions || 0) >= criteria.value
    default:
      return false
  }
}

/**
 * Get all available badges from database
 */
export async function getAllBadges(
  supabase: SupabaseClient
): Promise<Database['public']['Tables']['badges']['Row'][]> {
  const { data, error } = await supabase
    .from('badges')
    .select('*')
    .order('created_at', { ascending: true })

  if (error) {
    console.error('Error fetching badges:', error)
    throw new Error('Failed to fetch badges')
  }

  return data || []
}

/**
 * Get user's earned badges
 */
export async function getUserEarnedBadges(
  supabase: SupabaseClient,
  userId: string
): Promise<string[]> {
  const { data, error } = await supabase
    .from('user_badges')
    .select('badge_id')
    .eq('user_id', userId)

  if (error) {
    console.error('Error fetching user badges:', error)
    throw new Error('Failed to fetch user badges')
  }

  return data?.map(badge => badge.badge_id) || []
}

/**
 * Award badge to user
 */
export async function awardBadge(
  supabase: SupabaseClient,
  userId: string,
  badgeId: string
): Promise<void> {
  const { error } = await supabase
    .from('user_badges')
    .insert({
      user_id: userId,
      badge_id: badgeId,
      earned_at: new Date().toISOString()
    })

  if (error) {
    console.error('Error awarding badge:', error)
    throw new Error('Failed to award badge')
  }
}

/**
 * Check and award badges based on current user stats
 */
export async function checkAndAwardBadges(
  supabase: SupabaseClient,
  userId: string,
  userStats: {
    totalCompletions: number
    currentStreak: number
    earlyBirdCompletions?: number
  }
): Promise<BadgeInfo[]> {
  const [allBadges, earnedBadgeIds] = await Promise.all([
    getAllBadges(supabase),
    getUserEarnedBadges(supabase, userId)
  ])

  const newBadges: BadgeInfo[] = []

  for (const badge of allBadges) {
    // Skip if user already has this badge
    if (earnedBadgeIds.includes(badge.id)) {
      continue
    }

    // Check if user meets criteria
    const criteria = badge.criteria as BadgeCriteria
    if (checkBadgeCriteria(criteria, userStats)) {
      try {
        await awardBadge(supabase, userId, badge.id)
        newBadges.push({
          id: badge.id,
          name: badge.name,
          description: badge.description,
          icon: badge.icon
        })
      } catch (error) {
        console.error(`Failed to award badge ${badge.id}:`, error)
        // Continue with other badges even if one fails
      }
    }
  }

  return newBadges
}

/**
 * Get early bird completions (completions before 9 AM)
 * This is a placeholder for the early bird badge logic
 */
export async function getEarlyBirdCompletions(
  supabase: SupabaseClient,
  userId: string
): Promise<number> {
  // For now, we'll return 0 as the early bird logic requires
  // storing completion time, which isn't implemented yet
  // In a real implementation, you'd query completions with time < 9 AM
  return 0
}

/**
 * Get comprehensive user stats for badge checking
 */
export async function getUserStatsForBadges(
  supabase: SupabaseClient,
  userId: string
): Promise<{
  totalCompletions: number
  currentStreak: number
  earlyBirdCompletions: number
}> {
  // Get total completions
  const { count: totalCompletions } = await supabase
    .from('daily_completions')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)

  // Get user streak
  const { data: streak } = await supabase
    .from('user_streaks')
    .select('*')
    .eq('user_id', userId)
    .single()

  // Get early bird completions (placeholder)
  const earlyBirdCompletions = await getEarlyBirdCompletions(supabase, userId)

  return {
    totalCompletions: totalCompletions || 0,
    currentStreak: streak?.current_streak || 0,
    earlyBirdCompletions
  }
} 