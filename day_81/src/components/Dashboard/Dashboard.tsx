import React, { useState } from 'react'
import { useRituals } from '../../hooks/useRituals'
import { useCompletions } from '../../hooks/useCompletions'
import { useOnboarding } from '../../hooks/useOnboarding'
import { RitualCard } from './RitualCard'
import { CompletionButton } from './CompletionButton'
import { StreakCounter } from './StreakCounter'
import { OnboardingFlow } from '../Onboarding/OnboardingFlow'
import { Calendar, Clock, Sparkles, ArrowRight } from 'lucide-react'
import type { Badge } from '../../types'

export function Dashboard() {
  const { getTodayRitual, loading } = useRituals()
  const { refetch: refetchCompletions } = useCompletions()
  const { hasCompletedOnboarding, completeOnboarding, loading: onboardingLoading } = useOnboarding()

  const todayRitual = getTodayRitual()
  const today = new Date()

  const handleComplete = (badges: Badge[]) => {
    refetchCompletions()
  }

  // Show onboarding if user hasn't completed it
  if (onboardingLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-4">
        <div className="max-w-2xl mx-auto pt-8">
          <div className="animate-pulse space-y-6">
            <div className="h-32 bg-slate-200 rounded-3xl"></div>
            <div className="h-64 bg-slate-200 rounded-3xl"></div>
            <div className="h-16 bg-slate-200 rounded-3xl"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!hasCompletedOnboarding) {
    return <OnboardingFlow onComplete={completeOnboarding} />
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-4">
        <div className="max-w-2xl mx-auto pt-8">
          <div className="animate-pulse space-y-6">
            <div className="h-32 bg-slate-200 rounded-3xl"></div>
            <div className="h-64 bg-slate-200 rounded-3xl"></div>
            <div className="h-16 bg-slate-200 rounded-3xl"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!todayRitual) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-4 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-slate-200 to-slate-300 rounded-3xl mb-6">
            <Sparkles className="w-10 h-10 text-slate-500" />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-4">Preparing your ritual</h1>
          <p className="text-slate-600 mb-6 leading-relaxed">
            We're crafting the perfect one-minute experience for you. Check back in a moment for today's ritual.
          </p>
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-4 border border-white/20">
            <p className="text-sm text-slate-500">
              New rituals are available daily at midnight
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-4">
      <div className="max-w-2xl mx-auto pt-8 space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl mb-6 shadow-lg">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-slate-900 mb-3">
            Today's One-Minute Win
          </h1>
          <p className="text-slate-600 text-lg leading-relaxed max-w-md mx-auto">
            Small actions create lasting change. Take just 60 seconds to move forward.
          </p>
          
          {/* Date and Time Info */}
          <div className="flex items-center justify-center gap-6 mt-6 text-sm text-slate-500">
            <div className="flex items-center gap-2 bg-white/60 backdrop-blur-sm px-3 py-2 rounded-xl border border-white/20">
              <Calendar className="w-4 h-4" />
              <span>{today.toLocaleDateString('en-US', { 
                weekday: 'long', 
                month: 'short', 
                day: 'numeric' 
              })}</span>
            </div>
            <div className="flex items-center gap-2 bg-white/60 backdrop-blur-sm px-3 py-2 rounded-xl border border-white/20">
              <Clock className="w-4 h-4" />
              <span>~1 minute</span>
            </div>
          </div>
        </div>

        {/* Streak Counter */}
        <StreakCounter />

        {/* Ritual Card */}
        <div className="relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-3xl blur opacity-20"></div>
          <div className="relative">
            <RitualCard ritual={todayRitual} />
          </div>
        </div>

        {/* Completion Button */}
        <CompletionButton ritual={todayRitual} onComplete={handleComplete} />

        {/* What's Next Section */}
        <div className="bg-white/60 backdrop-blur-sm rounded-3xl p-6 border border-white/20">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-xl flex items-center justify-center">
              <ArrowRight className="w-4 h-4 text-white" />
            </div>
            <h3 className="font-bold text-slate-900 text-lg">What's next?</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-slate-600">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">New ritual available every day</span>
              </div>
              <div className="flex items-center gap-3 text-slate-600">
                <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                <span className="text-sm">Build your streak with consistency</span>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-slate-600">
                <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                <span className="text-sm">Earn badges for milestones</span>
              </div>
              <div className="flex items-center gap-3 text-slate-600">
                <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                <span className="text-sm">Track your progress over time</span>
              </div>
            </div>
          </div>
          
          {/* Quick Stats */}
          <div className="pt-4 border-t border-slate-200/50">
            <div className="flex items-center justify-between">
              <span className="text-slate-500 text-sm">Today's ritual type</span>
              <span className="font-medium text-slate-700 capitalize bg-slate-100/80 px-3 py-1 rounded-lg text-sm">
                {todayRitual.type}
              </span>
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}