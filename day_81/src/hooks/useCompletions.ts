import { useState, useEffect } from 'react'
import { useAuth } from './useAuth'
import { useApi } from './useApi'
import type { DailyCompletion } from '../types'

export function useCompletions() {
  const [completedToday, setCompletedToday] = useState(false)
  const [totalCompletions, setTotalCompletions] = useState(0)
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const { getUserStats, completeRitual } = useApi()

  useEffect(() => {
    if (user) {
      fetchUserStats()
    } else {
      setCompletedToday(false)
      setTotalCompletions(0)
      setLoading(false)
    }
  }, [user])

  const fetchUserStats = async () => {
    if (!user) {
      setCompletedToday(false)
      setTotalCompletions(0)
      setLoading(false)
      return
    }

    try {
      const response = await getUserStats(user.id)
      setCompletedToday(response.stats.completedToday)
      setTotalCompletions(response.stats.totalCompletions)
    } catch (error) {
      console.error('Error fetching user stats:', error)
      setCompletedToday(false)
      setTotalCompletions(0)
    } finally {
      setLoading(false)
    }
  }

  const isCompletedToday = () => {
    return completedToday
  }

  const completeRitualAction = async (ritualId: string) => {
    if (!user) {
      throw new Error('User not authenticated')
    }

    if (completedToday) {
      throw new Error('Ritual already completed today')
    }

    try {
      const response = await completeRitual(user.id, ritualId)
      
      // Update local state immediately
      setCompletedToday(true)
      setTotalCompletions(prev => prev + 1)
      
      return response
    } catch (error) {
      console.error('Error completing ritual:', error)
      throw error
    }
  }

  const getCompletionCount = () => totalCompletions

  return {
    completedToday,
    totalCompletions,
    loading,
    isCompletedToday,
    completeRitual: completeRitualAction,
    getCompletionCount,
    refetch: fetchUserStats,
  }
}