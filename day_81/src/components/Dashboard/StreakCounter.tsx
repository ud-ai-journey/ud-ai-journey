import React from 'react'
import { Flame, Trophy, Target, Calendar, TrendingUp } from 'lucide-react'
import { useStreaks } from '../../hooks/useStreaks'

const StreakCounter = () => {
  const { streak, loading } = useStreaks()

  if (loading) {
    return (
      <div className="bg-white/60 backdrop-blur-sm rounded-3xl shadow-lg p-6 animate-pulse border border-white/20">
        <div className="h-32 bg-slate-200 rounded-2xl"></div>
      </div>
    )
  }

  const currentStreak = streak?.current_streak || 0
  const longestStreak = streak?.longest_streak || 0

  const getStreakMessage = () => {
    if (currentStreak === 0) return "Ready to start your streak? 🚀"
    if (currentStreak === 1) return "Great start! Keep the momentum going! 💪"
    if (currentStreak >= 2 && currentStreak < 7) return "You're building momentum! 🔥"
    if (currentStreak >= 7 && currentStreak < 30) return "You're on fire! Unstoppable! ⚡"
    if (currentStreak >= 30) return "Legendary streak! You're a habit master! 👑"
    return "Keep going!"
  }

  const getNextMilestone = () => {
    if (currentStreak < 3) return 3
    if (currentStreak < 7) return 7
    if (currentStreak < 30) return 30
    return currentStreak + 10
  }

  const nextMilestone = getNextMilestone()
  const progress = Math.min(100, (currentStreak / nextMilestone) * 100)

  return (
    <div className="bg-white/60 backdrop-blur-sm rounded-3xl shadow-lg p-6 border border-white/20">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl shadow-lg">
            <Flame className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">Streak tracker</h2>
            <p className="text-slate-600 text-sm">Your consistency journey</p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          {[...Array(Math.min(currentStreak, 7))].map((_, i) => (
            <div
              key={i}
              className="w-2 h-2 bg-gradient-to-r from-orange-400 to-red-500 rounded-full animate-pulse"
              style={{ animationDelay: `${i * 0.1}s` }}
            />
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        {/* Current Streak */}
        <div className="text-center">
          <div className="relative mb-3">
            <div className="text-5xl font-bold bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
              {currentStreak}
            </div>
            {currentStreak > 0 && (
              <div className="absolute -top-2 -right-2 text-2xl animate-bounce">
                🔥
              </div>
            )}
          </div>
          <div className="text-sm font-semibold text-slate-700 mb-1">
            Current streak
          </div>
          <div className="text-xs text-slate-500">
            {currentStreak === 1 ? 'day' : 'days'} in a row
          </div>
        </div>

        {/* Best Streak */}
        <div className="text-center">
          <div className="relative mb-3">
            <div className="text-3xl font-bold text-slate-700">
              {longestStreak}
            </div>
            {longestStreak > 0 && (
              <div className="absolute -top-1 -right-1">
                <Trophy className="w-5 h-5 text-amber-500" />
              </div>
            )}
          </div>
          <div className="text-sm font-semibold text-slate-700 mb-1">
            Best streak
          </div>
          <div className="text-xs text-slate-500">
            personal record
          </div>
        </div>
      </div>

      {/* Progress to next milestone */}
      <div className="space-y-3 mb-6">
        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-600 font-medium">Next milestone</span>
          <span className="text-slate-500 font-medium">
            {currentStreak}/{nextMilestone}
          </span>
        </div>
        
        <div className="bg-slate-200 rounded-full h-3 overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-orange-400 via-red-500 to-pink-500 rounded-full transition-all duration-1000 ease-out relative"
            style={{ width: `${progress}%` }}
          >
            <div className="absolute inset-0 bg-white opacity-30 animate-pulse"></div>
          </div>
        </div>
      </div>

      {/* Motivational message */}
      <div className="text-center">
        <p className="text-sm text-slate-600 font-medium bg-slate-100/80 px-4 py-2 rounded-xl">
          {getStreakMessage()}
        </p>
      </div>

      {/* Last completion info */}
      {streak?.last_completion_date && (
        <div className="mt-4 pt-4 border-t border-slate-200/50">
          <div className="flex items-center justify-center gap-2 text-xs text-slate-500">
            <Calendar className="w-3 h-3" />
            <span>Last completed: {new Date(streak.last_completion_date).toLocaleDateString()}</span>
          </div>
        </div>
      )}
    </div>
  )
}

export { StreakCounter }