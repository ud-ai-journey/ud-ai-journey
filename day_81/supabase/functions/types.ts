// Shared types for Supabase Edge Functions

export interface Database {
  public: {
    Tables: {
      user_profiles: {
        Row: {
          id: string
          username: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          username: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          username?: string
          created_at?: string
          updated_at?: string
        }
      }
      rituals: {
        Row: {
          id: string
          type: 'reflection' | 'task' | 'quiz' | 'meditation'
          title: string
          description: string
          content: any
          created_at: string
        }
        Insert: {
          id?: string
          type: 'reflection' | 'task' | 'quiz' | 'meditation'
          title: string
          description: string
          content?: any
          created_at?: string
        }
        Update: {
          id?: string
          type?: 'reflection' | 'task' | 'quiz' | 'meditation'
          title?: string
          description?: string
          content?: any
          created_at?: string
        }
      }
      daily_completions: {
        Row: {
          id: string
          user_id: string
          ritual_id: string
          completed_at: string
          date: string
        }
        Insert: {
          id?: string
          user_id: string
          ritual_id: string
          completed_at?: string
          date?: string
        }
        Update: {
          id?: string
          user_id?: string
          ritual_id?: string
          completed_at?: string
          date?: string
        }
      }
      user_badges: {
        Row: {
          id: string
          user_id: string
          badge_id: string
          earned_at: string
        }
        Insert: {
          id?: string
          user_id: string
          badge_id: string
          earned_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          badge_id?: string
          earned_at?: string
        }
      }
      user_streaks: {
        Row: {
          id: string
          user_id: string
          current_streak: number
          longest_streak: number
          last_completion_date: string | null
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          current_streak?: number
          longest_streak?: number
          last_completion_date?: string | null
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          current_streak?: number
          longest_streak?: number
          last_completion_date?: string | null
          updated_at?: string
        }
      }
      badges: {
        Row: {
          id: string
          name: string
          description: string
          icon: string
          criteria: any
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          name: string
          description: string
          icon: string
          criteria: any
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          description?: string
          icon?: string
          criteria?: any
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}

// API Request/Response types
export interface CompleteRitualRequest {
  user_id: string
  ritual_id: string
}

export interface CompleteRitualResponse {
  success: boolean
  completion: Database['public']['Tables']['daily_completions']['Row']
  newBadges: BadgeInfo[]
  currentStreak: number
  longestStreak: number
  error?: string
}

export interface BadgeInfo {
  id: string
  name: string
  description: string
  icon: string
}

export interface UserStatsResponse {
  stats: {
    currentStreak: number
    longestStreak: number
    totalCompletions: number
    earnedBadges: number
    completedToday: boolean
    lastCompletionDate: string | null
  }
  error?: string
}

export interface UserBadgesResponse {
  badges: {
    earned: BadgeWithProgress[]
    available: BadgeWithProgress[]
    total: number
  }
  error?: string
}

export interface BadgeWithProgress {
  id: string
  name: string
  description: string
  icon: string
  requirement: number
  type: 'streak' | 'completion' | 'special'
  earned: boolean
  progress: number
  currentValue: number
  earnedAt: string | null
}

// Badge criteria types
export interface BadgeCriteria {
  type: 'completion' | 'streak' | 'early_bird'
  value: number
}

// Helper types for streak calculation
export interface StreakUpdate {
  currentStreak: number
  longestStreak: number
  lastCompletionDate: string
  isNewRecord: boolean
} 