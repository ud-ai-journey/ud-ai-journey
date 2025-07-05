const API_BASE_URL = import.meta.env.VITE_SUPABASE_URL + '/functions/v1'

export function useApi() {
  const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    const url = `${API_BASE_URL}${endpoint}`
    
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
      ...options.headers,
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(errorData.error || `HTTP ${response.status}`)
    }

    return response.json()
  }

  const getTodayRitual = async () => {
    return apiCall('/today-ritual')
  }

  const completeRitual = async (userId: string, ritualId: string) => {
    return apiCall('/complete-ritual', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        ritual_id: ritualId,
      }),
    })
  }

  const getUserStats = async (userId: string) => {
    return apiCall(`/user-stats?user_id=${userId}`)
  }

  const getUserBadges = async (userId: string) => {
    return apiCall(`/user-badges?user_id=${userId}`)
  }

  return {
    getTodayRitual,
    completeRitual,
    getUserStats,
    getUserBadges,
  }
}