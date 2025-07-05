import { useState, useEffect } from 'react'
import { useAuth } from './useAuth'
import { useApi } from './useApi'
import type { UserBadge, Badge } from '../types'

interface BadgeData {
  earned: Badge[]
  available: Badge[]
  total: number
}

export function useBadges() {
  const [badgeData, setBadgeData] = useState<BadgeData>({ earned: [], available: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const { getUserBadges } = useApi()

  useEffect(() => {
    if (user) {
      fetchBadges()
    }
  }, [user])

  const fetchBadges = async () => {
    if (!user) {
      setLoading(false)
      return
    }

    try {
      const response = await getUserBadges(user.id)
      setBadgeData(response.badges)
    } catch (error) {
      console.error('Error fetching badges:', error)
      setBadgeData({ earned: [], available: [], total: 0 })
    } finally {
      setLoading(false)
    }
  }

  const getAvailableBadges = () => {
    return [...badgeData.earned, ...badgeData.available]
  }

  return {
    userBadges: badgeData.earned,
    earnedBadges: badgeData.earned,
    availableBadges: badgeData.available,
    loading,
    getAvailableBadges,
    refetch: fetchBadges,
  }
}