import React, { useEffect, useState } from 'react'
import { Trophy, Star, Sparkles, Crown, Target } from 'lucide-react'
import confetti from 'canvas-confetti'
import type { Badge } from '../../types'

interface BadgeCelebrationProps {
  badges: Badge[]
  onComplete: () => void
}

export function BadgeCelebration({ badges, onComplete }: BadgeCelebrationProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [currentBadgeIndex, setCurrentBadgeIndex] = useState(0)

  useEffect(() => {
    // Trigger special confetti for badge earning
    if (typeof window !== 'undefined') {
      const duration = 4000
      const end = Date.now() + duration

      const colors = ['#FFD700', '#FFA500', '#FF6B6B', '#4ECDC4', '#45B7D1']

      // Create a burst effect
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: colors
      })

      // Continuous smaller bursts
      const frame = () => {
        confetti({
          particleCount: 2,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: colors
        })
        confetti({
          particleCount: 2,
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

    // If multiple badges, cycle through them
    if (badges.length > 1) {
      const interval = setInterval(() => {
        setCurrentBadgeIndex((prev) => {
          if (prev < badges.length - 1) {
            return prev + 1
          } else {
            clearInterval(interval)
            setTimeout(() => {
              setIsVisible(false)
              setTimeout(onComplete, 500)
            }, 2000)
            return prev
          }
        })
      }, 2500)

      return () => clearInterval(interval)
    } else {
      const timer = setTimeout(() => {
        setIsVisible(false)
        setTimeout(onComplete, 500)
      }, 5000)

      return () => clearTimeout(timer)
    }
  }, [badges.length, onComplete])

  const currentBadge = badges[currentBadgeIndex]

  const getBadgeIcon = (badgeId: string) => {
    switch (badgeId) {
      case 'first_step': return <Star className="w-8 h-8 text-white" />
      case 'consistent': return <Target className="w-8 h-8 text-white" />
      case 'dedicated': return <Trophy className="w-8 h-8 text-white" />
      case 'champion': return <Crown className="w-8 h-8 text-white" />
      default: return <Trophy className="w-8 h-8 text-white" />
    }
  }

  const getBadgeGradient = (badgeId: string) => {
    switch (badgeId) {
      case 'first_step': return 'from-yellow-400 to-orange-500'
      case 'consistent': return 'from-blue-400 to-purple-500'
      case 'dedicated': return 'from-emerald-400 to-teal-500'
      case 'champion': return 'from-purple-400 to-pink-500'
      default: return 'from-yellow-400 to-orange-500'
    }
  }

  const getCelebrationMessage = (badge: Badge) => {
    switch (badge.id) {
      case 'first_step':
        return {
          title: "🌟 First Badge Earned!",
          message: "You've taken your first step on this incredible journey!"
        }
      case 'consistent':
        return {
          title: "💪 Consistency Champion!",
          message: "You're proving that small actions lead to big results!"
        }
      case 'dedicated':
        return {
          title: "🏆 Dedication Master!",
          message: "Your commitment is truly inspiring!"
        }
      case 'champion':
        return {
          title: "👑 Ultimate Champion!",
          message: "You've reached legendary status!"
        }
      default:
        return {
          title: "🎉 Badge Earned!",
          message: "Another milestone achieved!"
        }
    }
  }

  const celebration = getCelebrationMessage(currentBadge)

  return (
    <div className={`fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 transition-all duration-500 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      <div className={`bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full transform transition-all duration-700 ${isVisible ? 'scale-100 translate-y-0' : 'scale-95 translate-y-8'}`}>
        {/* Badge Display */}
        <div className="text-center mb-6">
          <div className="relative inline-block">
            {/* Main badge */}
            <div className={`w-32 h-32 bg-gradient-to-br ${getBadgeGradient(currentBadge.id)} rounded-full flex items-center justify-center shadow-2xl transition-all duration-1000 ${isVisible ? 'scale-100 rotate-0' : 'scale-0 rotate-180'}`}>
              {getBadgeIcon(currentBadge.id)}
            </div>
            
            {/* Glow effect */}
            <div className={`absolute inset-0 bg-gradient-to-br ${getBadgeGradient(currentBadge.id)} rounded-full opacity-30 animate-pulse scale-110`}></div>
            
            {/* Sparkle effects */}
            <div className="absolute inset-0 pointer-events-none">
              {[...Array(8)].map((_, i) => (
                <div
                  key={i}
                  className={`absolute transition-all duration-1000 delay-${i * 100} ${
                    isVisible ? 'animate-ping opacity-100' : 'opacity-0'
                  }`}
                  style={{
                    top: `${10 + Math.random() * 80}%`,
                    left: `${10 + Math.random() * 80}%`,
                    animationDelay: `${i * 150}ms`
                  }}
                >
                  <Sparkles className="w-4 h-4 text-yellow-400" />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Badge Info */}
        <div className="text-center space-y-4">
          <h3 className={`text-2xl font-bold text-gray-900 transition-all duration-700 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            {celebration.title}
          </h3>
          
          <div className={`transition-all duration-700 delay-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            <h4 className="text-xl font-semibold text-gray-800 mb-2">{currentBadge.name}</h4>
            <p className="text-gray-600">{currentBadge.description}</p>
          </div>
          
          <p className={`text-gray-600 leading-relaxed transition-all duration-700 delay-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            {celebration.message}
          </p>
        </div>

        {/* Badge Progress */}
        <div className={`mt-8 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-2xl border border-yellow-200 transition-all duration-700 delay-900 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="flex items-center justify-center gap-3">
            <Trophy className="w-5 h-5 text-yellow-600" />
            <span className="font-semibold text-yellow-800">Badge Unlocked!</span>
            <div className="text-2xl">🎉</div>
          </div>
        </div>

        {/* Multiple badges indicator */}
        {badges.length > 1 && (
          <div className={`mt-6 text-center transition-all duration-700 delay-1100 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            <div className="flex justify-center gap-2 mb-2">
              {badges.map((_, index) => (
                <div
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentBadgeIndex
                      ? 'bg-yellow-500 scale-125'
                      : index < currentBadgeIndex
                      ? 'bg-yellow-400'
                      : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
            <p className="text-sm text-gray-600">
              {currentBadgeIndex + 1} of {badges.length} new badges
            </p>
          </div>
        )}

        {/* Auto-close indicator */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 text-xs text-gray-500">
            <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
            <span>Celebrating your achievement...</span>
          </div>
        </div>
      </div>
    </div>
  )
}