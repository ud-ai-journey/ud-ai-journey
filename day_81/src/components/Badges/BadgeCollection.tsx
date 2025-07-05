import React from 'react'
import { Trophy, Lock, Star, Target, Award, Crown } from 'lucide-react'
import { useBadges } from '../../hooks/useBadges'

export function BadgeCollection() {
  const { earnedBadges, availableBadges, loading } = useBadges()

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4">
        <div className="max-w-4xl mx-auto pt-8">
          <div className="animate-pulse space-y-6">
            <div className="h-32 bg-gray-200 rounded-2xl"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="h-40 bg-gray-200 rounded-2xl"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  const totalBadges = earnedBadges.length + availableBadges.length

  const getBadgeIcon = (badgeId: string) => {
    switch (badgeId) {
      case 'first_step': return <Star className="w-6 h-6" />
      case 'consistent': return <Target className="w-6 h-6" />
      case 'dedicated': return <Trophy className="w-6 h-6" />
      case 'champion': return <Crown className="w-6 h-6" />
      case 'streak_3': case 'streak_7': case 'streak_30': return <Award className="w-6 h-6" />
      default: return <Trophy className="w-6 h-6" />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4">
      <div className="max-w-4xl mx-auto pt-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
            <div className="p-2 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg">
              <Trophy className="w-8 h-8 text-white" />
            </div>
            Badge Collection
          </h1>
          <p className="text-gray-600">
            Earn badges by completing rituals and building streaks
          </p>
        </div>

        {/* Progress Overview */}
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg p-6 mb-8 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Your Progress</h2>
              <p className="text-gray-600">
                {earnedBadges.length} of {totalBadges} badges earned
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold bg-gradient-to-r from-purple-500 to-blue-500 bg-clip-text text-transparent">
                {totalBadges > 0 ? Math.round((earnedBadges.length / totalBadges) * 100) : 0}%
              </div>
              <div className="text-sm text-gray-600">Complete</div>
            </div>
          </div>
          <div className="bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-purple-500 via-blue-500 to-green-500 h-3 rounded-full transition-all duration-1000 ease-out relative"
              style={{ width: `${totalBadges > 0 ? (earnedBadges.length / totalBadges) * 100 : 0}%` }}
            >
              <div className="absolute inset-0 bg-white opacity-30 animate-pulse"></div>
            </div>
          </div>
        </div>

        {/* Earned Badges */}
        {earnedBadges.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                <Trophy className="w-5 h-5 text-white" />
              </div>
              Earned Badges ({earnedBadges.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {earnedBadges.map((badge) => (
                <div key={badge.id} className="bg-gradient-to-br from-white to-green-50 rounded-2xl shadow-lg p-6 transition-all duration-300 hover:shadow-xl hover:scale-105 border border-green-200">
                  <div className="text-center">
                    <div className="relative mb-4">
                      <div className="text-5xl mb-2">{badge.icon}</div>
                      <div className="absolute -top-2 -right-2 bg-green-500 text-white rounded-full p-1">
                        <Trophy className="w-4 h-4" />
                      </div>
                    </div>
                    <h3 className="font-bold text-gray-900 mb-2 text-lg">{badge.name}</h3>
                    <p className="text-sm text-gray-600 mb-4">{badge.description}</p>
                    <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded-full text-sm font-semibold flex items-center justify-center gap-2">
                      <Trophy className="w-4 h-4" />
                      Earned ✓
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Locked Badges */}
        {availableBadges.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-r from-gray-400 to-gray-500 rounded-lg flex items-center justify-center">
                <Lock className="w-5 h-5 text-white" />
              </div>
              Available Badges ({availableBadges.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {availableBadges.map((badge) => {
                return (
                  <div key={badge.id} className="bg-white rounded-2xl shadow-lg p-6 transition-all duration-300 hover:shadow-xl border border-gray-200">
                    <div className="text-center">
                      <div className="relative mb-4">
                        <div className="text-5xl mb-2 filter grayscale opacity-60">{badge.icon}</div>
                        <div className="absolute -top-2 -right-2 bg-gray-400 text-white rounded-full p-1">
                          <Lock className="w-4 h-4" />
                        </div>
                      </div>
                      <h3 className="font-bold text-gray-900 mb-2 text-lg">{badge.name}</h3>
                      <p className="text-sm text-gray-600 mb-4">{badge.description}</p>
                      
                      {/* Progress Bar */}
                      <div className="mb-4">
                        <div className="flex justify-between text-xs text-gray-500 mb-1">
                          <span>Progress</span>
                          <span>{badge.currentValue || 0}/{badge.requirement}</span>
                        </div>
                        <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
                          <div 
                            className="bg-gradient-to-r from-purple-400 to-blue-400 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${badge.progress || 0}%` }}
                          />
                        </div>
                      </div>

                      {/* Criteria */}
                      <div className="bg-gray-50 rounded-lg p-3 mb-4">
                        <div className="text-xs text-gray-500 mb-1">Criteria to unlock:</div>
                        <div className="text-sm font-medium text-gray-700">
                          {badge.type === 'streak' && `Maintain a ${badge.requirement}-day streak`}
                          {badge.type === 'completion' && `Complete ${badge.requirement} rituals`}
                          {badge.type === 'special' && badge.description}
                        </div>
                      </div>

                      <div className="bg-gray-400 text-white px-4 py-2 rounded-full text-sm font-semibold flex items-center justify-center gap-2">
                        <Lock className="w-4 h-4" />
                        {(badge.progress || 0) >= 100 ? 'Almost there!' : 'Locked'}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Surprise Badge Notification Placeholder */}
        <div className="mt-8 bg-gradient-to-r from-purple-100 to-pink-100 rounded-2xl p-6 border-2 border-dashed border-purple-300">
          <div className="text-center">
            <div className="text-4xl mb-3">🎁</div>
            <h3 className="font-bold text-gray-900 mb-2">Surprise Badges Coming Soon!</h3>
            <p className="text-gray-600 text-sm">
              Keep completing your daily rituals to unlock special surprise badges with unique rewards and achievements.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}