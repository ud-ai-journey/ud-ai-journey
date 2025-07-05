import React from 'react'
import { User, Calendar, Trophy, TrendingUp, LogOut, Target, Award, BarChart3, Clock, Sparkles } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'
import { useStreaks } from '../../hooks/useStreaks'
import { useCompletions } from '../../hooks/useCompletions'
import { useBadges } from '../../hooks/useBadges'
import { useOnboarding } from '../../hooks/useOnboarding'

export function Profile() {
  const { user, signOut } = useAuth()
  const { streak } = useStreaks()
  const { totalCompletions } = useCompletions()
  const { earnedBadges } = useBadges()
  const { resetOnboarding } = useOnboarding()

  const joinDate = user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4">
      <div className="max-w-4xl mx-auto pt-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg">
              <User className="w-8 h-8 text-white" />
            </div>
            Your Profile
          </h1>
          <p className="text-gray-600">Track your habit-building journey and achievements</p>
        </div>

        {/* Account Info Card */}
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg p-6 mb-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Account Information</h2>
                <p className="text-gray-600">{user?.email}</p>
              </div>
            </div>
            <button
              onClick={signOut}
              className="flex items-center gap-2 text-red-600 hover:text-red-700 transition-colors px-4 py-2 rounded-lg hover:bg-red-50"
            >
              <LogOut className="w-5 h-5" />
              Sign Out
            </button>
            <button
              onClick={resetOnboarding}
              className="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors px-4 py-2 rounded-lg hover:bg-blue-50"
            >
              <Sparkles className="w-5 h-5" />
              View Tutorial
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
              <Calendar className="w-5 h-5 text-gray-500" />
              <div>
                <p className="text-sm text-gray-600">Member since</p>
                <p className="font-semibold text-gray-900">{joinDate}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
              <Clock className="w-5 h-5 text-gray-500" />
              <div>
                <p className="text-sm text-gray-600">Total time invested</p>
                <p className="font-semibold text-gray-900">{totalCompletions} minutes</p>
              </div>
            </div>
          </div>
        </div>

        {/* Key Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl shadow-lg p-6 border border-orange-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-lg">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Current Streak</h3>
                <p className="text-2xl font-bold text-orange-600">
                  {streak?.current_streak || 0}
                </p>
              </div>
            </div>
            <div className="text-sm text-gray-600">
              🔥 {streak?.current_streak === 1 ? 'day' : 'days'} in a row
            </div>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl shadow-lg p-6 border border-yellow-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg">
                <Trophy className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Best Streak</h3>
                <p className="text-2xl font-bold text-yellow-600">
                  {streak?.longest_streak || 0}
                </p>
              </div>
            </div>
            <div className="text-sm text-gray-600">
              🏆 Personal record
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl shadow-lg p-6 border border-blue-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Total Rituals</h3>
                <p className="text-2xl font-bold text-blue-600">
                  {totalCompletions}
                </p>
              </div>
            </div>
            <div className="text-sm text-gray-600">
              ⭐ Completed successfully
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl shadow-lg p-6 border border-green-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
                <Award className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Badges Earned</h3>
                <p className="text-2xl font-bold text-green-600">
                  {earnedBadges.length}
                </p>
              </div>
            </div>
            <div className="text-sm text-gray-600">
              🎖️ Achievements unlocked
            </div>
          </div>
        </div>

        {/* Detailed Statistics */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h3 className="font-bold text-gray-900 mb-6 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-purple-500" />
            Detailed Statistics
          </h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600 flex items-center gap-2">
                <Target className="w-4 h-4" />
                Total Rituals Completed
              </span>
              <span className="font-semibold text-gray-900">{totalCompletions}</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600 flex items-center gap-2">
                <TrendingUp className="w-4 h-4" />
                Current Streak
              </span>
              <span className="font-semibold text-gray-900">{streak?.current_streak || 0} days</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600 flex items-center gap-2">
                <Trophy className="w-4 h-4" />
                Longest Streak
              </span>
              <span className="font-semibold text-gray-900">{streak?.longest_streak || 0} days</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600 flex items-center gap-2">
                <Award className="w-4 h-4" />
                Badges Earned
              </span>
              <span className="font-semibold text-gray-900">{earnedBadges.length}</span>
            </div>
            <div className="flex justify-between items-center py-3">
              <span className="text-gray-600 flex items-center gap-2">
                <Clock className="w-4 h-4" />
                Time Invested
              </span>
              <span className="font-semibold text-gray-900">{totalCompletions} minutes</span>
            </div>
          </div>
        </div>

        {/* Earned Badges Preview */}
        {earnedBadges.length > 0 && (
          <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl shadow-lg p-6 border border-yellow-200">
            <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Trophy className="w-6 h-6 text-yellow-500" />
              Your Badges ({earnedBadges.length})
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {earnedBadges.slice(0, 6).map((badge) => (
                <div key={badge.id} className="text-center p-3 bg-white rounded-lg shadow-sm">
                  <div className="text-2xl mb-1">🏆</div>
                  <div className="text-xs font-medium text-gray-700 truncate">
                    {badge.name}
                  </div>
                </div>
              ))}
            </div>
            {earnedBadges.length > 6 && (
              <div className="text-center mt-4">
                <p className="text-sm text-gray-600">
                  +{earnedBadges.length - 6} more badges earned
                </p>
              </div>
            )}
          </div>
        )}

        {/* Future Features Placeholder */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <div className="bg-gradient-to-br from-purple-100 to-blue-100 rounded-2xl p-6 border-2 border-dashed border-purple-300">
            <div className="text-center">
              <BarChart3 className="w-12 h-12 text-purple-500 mx-auto mb-3" />
              <h3 className="font-bold text-gray-900 mb-2">Streak History Graph</h3>
              <p className="text-gray-600 text-sm">
                Visual timeline of your streak progress coming soon
              </p>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-green-100 to-emerald-100 rounded-2xl p-6 border-2 border-dashed border-green-300">
            <div className="text-center">
              <Calendar className="w-12 h-12 text-green-500 mx-auto mb-3" />
              <h3 className="font-bold text-gray-900 mb-2">Completion Calendar</h3>
              <p className="text-gray-600 text-sm">
                Monthly view of your ritual completions coming soon
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}