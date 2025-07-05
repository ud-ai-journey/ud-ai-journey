import React, { useState } from 'react'
import { CheckCircle, Sparkles, AlertCircle, ArrowRight } from 'lucide-react'
import { useCompletions } from '../../hooks/useCompletions'
import { useStreaks } from '../../hooks/useStreaks'
import { useAuth } from '../../hooks/useAuth'
import { CompletionCelebration } from '../Celebrations/CompletionCelebration'
import { BadgeCelebration } from '../Celebrations/BadgeCelebration'
import type { Ritual } from '../../types'
import type { Badge } from '../../types'

interface CompletionButtonProps {
  ritual: Ritual
  onComplete: (newBadges: Badge[]) => void
}

export function CompletionButton({ ritual, onComplete }: CompletionButtonProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showCompletionCelebration, setShowCompletionCelebration] = useState(false)
  const [showBadgeCelebration, setShowBadgeCelebration] = useState(false)
  const [celebrationData, setCelebrationData] = useState<{
    newBadges: Badge[]
    streakCount: number
    isFirstCompletion: boolean
  } | null>(null)
  const { isCompletedToday, completeRitual } = useCompletions()
  const { updateStreakFromCompletion } = useStreaks()
  const { user } = useAuth()

  const handleComplete = async () => {
    if (!user) {
      setError('Please log in to complete rituals')
      return
    }

    if (isCompletedToday()) {
      setError('You have already completed today\'s ritual!')
      return
    }

    if (loading) return

    setLoading(true)
    setError(null)

    try {
      console.log('Starting ritual completion...', { ritualId: ritual.id, userId: user.id })
      
      const result = await completeRitual(ritual.id)
      
      if (result) {
        console.log('Ritual completed successfully!', result)
        
        // Update streak data from API response
        if (result.currentStreak !== undefined && result.longestStreak !== undefined) {
          updateStreakFromCompletion(result.currentStreak, result.longestStreak)
        }
        
        // Set up celebration data
        const newBadges = result.newBadges || []
        const streakCount = result.currentStreak || 1
        const isFirstCompletion = streakCount === 1
        
        setCelebrationData({
          newBadges,
          streakCount,
          isFirstCompletion
        })
        
        // Show completion celebration first
        setShowCompletionCelebration(true)
      } else {
        setError('Failed to complete ritual. Please try again.')
      }
    } catch (error: any) {
      console.error('Error completing ritual:', error)
      setError(error.message || 'An error occurred while completing the ritual')
    } finally {
      setLoading(false)
    }
  }

  const handleCompletionCelebrationComplete = () => {
    setShowCompletionCelebration(false)
    
    // If there are new badges, show badge celebration
    if (celebrationData?.newBadges && celebrationData.newBadges.length > 0) {
      setShowBadgeCelebration(true)
    } else {
      // No badges, just call the original onComplete
      onComplete(celebrationData?.newBadges || [])
    }
  }

  const handleBadgeCelebrationComplete = () => {
    setShowBadgeCelebration(false)
    onComplete(celebrationData?.newBadges || [])
  }
  const isCompleted = isCompletedToday()

  if (error) {
    return (
      <div className="space-y-4">
        <div className="bg-red-50 border border-red-100 rounded-2xl p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
          <span className="text-red-700">{error}</span>
        </div>
        <button
          onClick={() => setError(null)}
          className="w-full py-4 px-6 rounded-2xl font-semibold text-slate-600 border border-slate-300 hover:bg-slate-50 transition-all duration-200 bg-white"
        >
          Try again
        </button>
      </div>
    )
  }

  return (
    <>
      <button
        onClick={handleComplete}
        disabled={loading || isCompleted || !user}
        className={`w-full py-5 px-8 rounded-2xl font-semibold text-lg transition-all duration-300 transform ${
          isCompleted
            ? 'bg-gradient-to-r from-emerald-500 to-green-500 text-white cursor-not-allowed shadow-lg'
            : loading
            ? 'bg-slate-400 text-white cursor-not-allowed'
            : !user
            ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
            : 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:from-blue-600 hover:to-indigo-700 hover:scale-[1.02] active:scale-[0.98] cursor-pointer shadow-lg hover:shadow-xl'
        }`}
      >
        <div className="flex items-center justify-center gap-3">
          {isCompleted ? (
            <>
              <CheckCircle className="w-6 h-6" />
              <span>Completed today! 🎉</span>
            </>
          ) : loading ? (
            <>
              <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Completing...</span>
            </>
          ) : !user ? (
            <>
              <AlertCircle className="w-6 h-6" />
              <span>Please log in</span>
            </>
          ) : (
            <>
              <Sparkles className="w-6 h-6" />
              <span>Complete ritual</span>
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </div>
      {/* Celebration Components */}
      {showCompletionCelebration && celebrationData && (
        <CompletionCelebration
          onComplete={handleCompletionCelebrationComplete}
          streakCount={celebrationData.streakCount}
          isFirstCompletion={celebrationData.isFirstCompletion}
        />
      )}
      </button>
      {showBadgeCelebration && celebrationData?.newBadges && (
        <BadgeCelebration
          badges={celebrationData.newBadges}
          onComplete={handleBadgeCelebrationComplete}
        />
      )}
    </>
  )
}