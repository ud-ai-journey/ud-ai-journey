export interface User {
  id: string
  username: string
  created_at: string
  updated_at: string
}

export interface Ritual {
  id: string
  type: 'reflection' | 'task' | 'quiz' | 'meditation'
  title: string
  description: string
  content: any
  created_at: string
}

export interface DailyCompletion {
  id: string
  user_id: string
  ritual_id: string
  completed_at: string
  date: string
}

export interface UserBadge {
  id: string
  user_id: string
  badge_id: string
  earned_at: string
}

export interface UserStreak {
  id: string
  user_id: string
  current_streak: number
  longest_streak: number
  last_completion_date: string | null
  updated_at: string
}

export interface Badge {
  id: string
  name: string
  description: string
  icon: string
  requirement: number
  type: 'streak' | 'completion' | 'special'
}