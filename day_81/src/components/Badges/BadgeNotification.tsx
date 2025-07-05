import React, { useEffect, useState } from 'react'
import { X, Sparkles } from 'lucide-react'
import type { Badge } from '../../types'

interface BadgeNotificationProps {
  badges: Badge[]
  onDismiss: () => void
}

export function BadgeNotification({ badges, onDismiss }: BadgeNotificationProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(onDismiss, 300)
    }, 4000)

    return () => clearTimeout(timer)
  }, [onDismiss])

  return (
    <div className={`fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 transition-opacity duration-300 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      <div className={`bg-white rounded-2xl shadow-2xl p-6 max-w-sm w-full transform transition-all duration-300 ${isVisible ? 'scale-100' : 'scale-95'}`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-yellow-500" />
            <h3 className="text-xl font-bold text-gray-900">Badge Earned!</h3>
          </div>
          <button
            onClick={onDismiss}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="space-y-4">
          {badges.map((badge) => (
            <div key={badge.id} className="flex items-center gap-3 p-3 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg">
              <div className="text-3xl">{badge.icon}</div>
              <div>
                <h4 className="font-semibold text-gray-900">{badge.name}</h4>
                <p className="text-sm text-gray-600">{badge.description}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Keep up the great work! 🎉
          </p>
        </div>
      </div>
    </div>
  )
}