import React, { useEffect, useState } from 'react'
import { Sparkles, Trophy, Target, CheckCircle, Star } from 'lucide-react'
import confetti from 'canvas-confetti'

interface CompletionCelebrationProps {
  onComplete: () => void
  streakCount: number
  isFirstCompletion: boolean
}

export function CompletionCelebration({ onComplete, streakCount, isFirstCompletion }: CompletionCelebrationProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [showConfetti, setShowConfetti] = useState(false)

  useEffect(() => {
    // Trigger confetti
    if (typeof window !== 'undefined') {
      const duration = 3000
      const end = Date.now() + duration

      const colors = ['#3B82F6', '#6366F1', '#8B5CF6', '#EC4899', '#F59E0B']

      const frame = () => {
        confetti({
          particleCount: 3,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: colors
        })
        confetti({
          particleCount: 3,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors: colors
        })

        if (Date.now() < end) {
          requestAnimationFrame(frame)
        }
      }
      frame()
    }

    setIsVisible(true)
    setShowConfetti(true)

    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(onComplete, 500)
    }, 4000)

    return () => clearTimeout(timer)
  }, [onComplete])

  const getCelebrationMessage = () => {
    if (isFirstCompletion) {
      return {
        title: "🎉 Amazing! You did it!",
        subtitle: "You've completed your first ritual!",
        message: "This is the beginning of something beautiful. Every journey starts with a single step."
      }
    }
    
    if (streakCount === 1) {
      return {
        title: "🔥 Great start!",
        subtitle: "Day 1 of your streak!",
        message: "Consistency is the key to transformation. Keep this momentum going!"
      }
    }
    
    if (streakCount <= 7) {
      return {
        title: "💪 You're building momentum!",
        subtitle: `${streakCount} days in a row!`,
        message: "Each day you're proving to yourself that change is possible. Keep going!"
      }
    }
    
    if (streakCount <= 30) {
      return {
        title: "⚡ You're unstoppable!",
        subtitle: `${streakCount}-day streak!`,
        message: "This is incredible! You're developing a powerful habit that will serve you for life."
      }
    }
    
    return {
      title: "👑 Legendary achievement!",
      subtitle: `${streakCount} days of excellence!`,
      message: "You've mastered the art of consistency. You're an inspiration!"
    }
  }

  const celebration = getCelebrationMessage()

  return (
    <div className={`fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 transition-all duration-500 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      <div className={`bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full transform transition-all duration-500 ${isVisible ? 'scale-100 translate-y-0' : 'scale-95 translate-y-4'}`}>
        {/* Animated Success Icon */}
        <div className="text-center mb-6">
          <div className="relative inline-block">
            <div className={`w-24 h-24 bg-gradient-to-br from-emerald-500 to-green-600 rounded-full flex items-center justify-center shadow-2xl transition-all duration-1000 ${isVisible ? 'scale-100 rotate-0' : 'scale-0 rotate-180'}`}>
              <CheckCircle className="w-12 h-12 text-white" />
            </div>
            
            {/* Floating particles */}
            <div className="absolute inset-0 pointer-events-none">
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`absolute w-2 h-2 bg-yellow-400 rounded-full transition-all duration-1000 delay-${i * 100} ${
                    showConfetti ? 'animate-ping' : 'opacity-0'
                  }`}
                  style={{
                    top: `${20 + Math.random() * 60}%`,
                    left: `${20 + Math.random() * 60}%`,
                    animationDelay: `${i * 200}ms`
                  }}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Celebration Text */}
        <div className="text-center space-y-4">
          <h3 className={`text-2xl font-bold text-gray-900 transition-all duration-700 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            {celebration.title}
          </h3>
          
          <p className={`text-lg font-semibold text-blue-600 transition-all duration-700 delay-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            {celebration.subtitle}
          </p>
          
          <p className={`text-gray-600 leading-relaxed transition-all duration-700 delay-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            {celebration.message}
          </p>
        </div>

        {/* Stats Display */}
        <div className={`mt-8 grid grid-cols-2 gap-4 transition-all duration-700 delay-900 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Target className="w-5 h-5 text-blue-600" />
              <span className="font-semibold text-blue-900">Today</span>
            </div>
            <div className="text-2xl font-bold text-blue-600">✓</div>
            <div className="text-xs text-blue-600">Completed</div>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl border border-orange-100">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-orange-600" />
              <span className="font-semibold text-orange-900">Streak</span>
            </div>
            <div className="text-2xl font-bold text-orange-600">{streakCount}</div>
            <div className="text-xs text-orange-600">{streakCount === 1 ? 'day' : 'days'}</div>
          </div>
        </div>

        {/* Motivational Quote */}
        <div className={`mt-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl border border-purple-100 transition-all duration-700 delay-1100 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="text-center">
            <Star className="w-5 h-5 text-purple-600 mx-auto mb-2" />
            <p className="text-sm text-purple-700 italic">
              "Success is the sum of small efforts repeated day in and day out."
            </p>
            <p className="text-xs text-purple-600 mt-1">— Robert Collier</p>
          </div>
        </div>

        {/* Auto-close indicator */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 text-xs text-gray-500">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
            <span>Celebrating your success...</span>
          </div>
        </div>
      </div>
    </div>
  )
}