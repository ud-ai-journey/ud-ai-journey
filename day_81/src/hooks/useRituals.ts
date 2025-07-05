import { useState, useEffect } from 'react'
import { useApi } from './useApi'
import type { Ritual } from '../types'

export function useRituals() {
  const [rituals, setRituals] = useState<Ritual[]>([])
  const [todayRitual, setTodayRitual] = useState<Ritual | null>(null)
  const [loading, setLoading] = useState(true)
  const { getTodayRitual } = useApi()

  useEffect(() => {
    fetchTodayRitual()
  }, [])

  const fetchTodayRitual = async () => {
    try {
      const response = await getTodayRitual()
      setTodayRitual(response.ritual)
    } catch (error) {
      console.error('Error fetching today\'s ritual:', error)
      setTodayRitual(null)
    } finally {
      setLoading(false)
    }
  }

  const getTodayRitualData = () => {
    return todayRitual
  }

  return {
    rituals,
    todayRitual,
    loading,
    getTodayRitual: getTodayRitualData,
    refetch: fetchTodayRitual,
  }
}