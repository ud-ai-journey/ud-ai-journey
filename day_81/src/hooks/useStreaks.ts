import { useState, useEffect } from 'react'
import { useAuth } from './useAuth'
import { useApi } from './useApi'
import type { UserStreak } from '../types'

export function useStreaks() {
  const [streak, setStreak] = useState<UserStreak | null>(null)
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const { getUserStats } = useApi()

  useEffect(() => {
    if (user) {
      fetchUserStats()
    }
  }, [user])

  const fetchUserStats = async () => {
    if (!user) {
      setLoading(false)
      return
    }

    try {
      const response = await getUserStats(user.id)
      setStreak({
        id: 'temp',
        user_id: user.id,
        current_streak: response.stats.currentStreak,
        longest_streak: response.stats.longestStreak,
        last_completion_date: response.stats.lastCompletionDate,
        updated_at: new Date().toISOString(),
      })
    } catch (error) {
      console.error('Error fetching user stats:', error)
      setStreak({
        id: 'temp',
        user_id: user.id,
        current_streak: 0,
        longest_streak: 0,
        last_completion_date: null,
        updated_at: new Date().toISOString(),
      })
    } finally {
      setLoading(false)
    }
  }

  const updateStreakFromCompletion = (newCurrentStreak: number, newLongestStreak: number) => {
    if (streak) {
      setStreak({
        ...streak,
        current_streak: newCurrentStreak,
        longest_streak: newLongestStreak,
        last_completion_date: new Date().toISOString().split('T')[0],
        updated_at: new Date().toISOString(),
      })
    }
  }

  return {
    streak,
    loading,
    updateStreakFromCompletion,
    refetch: fetchUserStats,
  }
}