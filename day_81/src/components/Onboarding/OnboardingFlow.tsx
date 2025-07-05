import React, { useState } from 'react'
import { Sparkles, Target, Trophy, Calendar, ArrowRight, ArrowLeft, CheckCircle } from 'lucide-react'

interface OnboardingFlowProps {
  onComplete: () => void
}

const steps = [
  {
    id: 'welcome',
    title: 'Welcome to One-Minute Wins! 🎉',
    description: 'Transform your life with tiny daily actions that create lasting change.',
    content: (
      <div className="text-center space-y-6">
        <div className="relative">
          <div className="w-32 h-32 mx-auto bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center shadow-2xl">
            <Sparkles className="w-16 h-16 text-white" />
          </div>
          <div className="absolute -top-2 -right-2 w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce">
            ✨
          </div>
        </div>
        <div className="space-y-4">
          <p className="text-lg text-slate-600 leading-relaxed">
            Small steps lead to big changes. Just one minute a day can transform your habits and mindset.
          </p>
          <div className="grid grid-cols-3 gap-4 mt-8">
            <div className="text-center p-4 bg-blue-50 rounded-xl">
              <div className="text-2xl mb-2">⏱️</div>
              <div className="text-sm font-medium text-slate-700">Just 1 minute</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-xl">
              <div className="text-2xl mb-2">🎯</div>
              <div className="text-sm font-medium text-slate-700">Daily rituals</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-xl">
              <div className="text-2xl mb-2">🏆</div>
              <div className="text-sm font-medium text-slate-700">Build streaks</div>
            </div>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'how-it-works',
    title: 'How it works',
    description: 'Simple, effective, and designed for busy lives.',
    content: (
      <div className="space-y-8">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white font-bold text-lg">
            1
          </div>
          <div>
            <h4 className="font-semibold text-slate-900 mb-2">Get your daily ritual</h4>
            <p className="text-slate-600">Each day, discover a new one-minute activity designed to improve your mindset, productivity, or well-being.</p>
          </div>
        </div>
        
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-500 rounded-xl flex items-center justify-center text-white font-bold text-lg">
            2
          </div>
          <div>
            <h4 className="font-semibold text-slate-900 mb-2">Complete in 60 seconds</h4>
            <p className="text-slate-600">Whether it's reflection, a quick task, meditation, or a knowledge quiz - it only takes a minute.</p>
          </div>
        </div>
        
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center text-white font-bold text-lg">
            3
          </div>
          <div>
            <h4 className="font-semibold text-slate-900 mb-2">Build your streak</h4>
            <p className="text-slate-600">Track your consistency, earn badges, and watch as small daily wins compound into meaningful change.</p>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'ritual-types',
    title: 'Types of rituals',
    description: 'Discover the variety of one-minute experiences waiting for you.',
    content: (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl p-6 border border-purple-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <Target className="w-5 h-5 text-white" />
            </div>
            <h4 className="font-semibold text-slate-900">Reflection</h4>
          </div>
          <p className="text-sm text-slate-600 mb-3">Thoughtful prompts to help you gain clarity and self-awareness.</p>
          <div className="text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded-lg inline-block">
            Example: "What's one thing you're grateful for today?"
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl p-6 border border-blue-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center">
              <CheckCircle className="w-5 h-5 text-white" />
            </div>
            <h4 className="font-semibold text-slate-900">Quick Tasks</h4>
          </div>
          <p className="text-sm text-slate-600 mb-3">Simple actions that create immediate positive impact.</p>
          <div className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-lg inline-block">
            Example: "Send a thank you message to someone"
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-6 border border-emerald-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <h4 className="font-semibold text-slate-900">Knowledge Quiz</h4>
          </div>
          <p className="text-sm text-slate-600 mb-3">Fun questions to expand your knowledge and spark curiosity.</p>
          <div className="text-xs text-emerald-600 bg-emerald-100 px-2 py-1 rounded-lg inline-block">
            Example: "Which habit takes 21 days to form?"
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-rose-50 to-pink-50 rounded-2xl p-6 border border-rose-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-rose-500 to-pink-600 rounded-xl flex items-center justify-center">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <h4 className="font-semibold text-slate-900">Meditation</h4>
          </div>
          <p className="text-sm text-slate-600 mb-3">Brief mindfulness exercises to center yourself.</p>
          <div className="text-xs text-rose-600 bg-rose-100 px-2 py-1 rounded-lg inline-block">
            Example: "Take 5 deep breaths and notice your surroundings"
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'badges-streaks',
    title: 'Earn badges & build streaks',
    description: 'Celebrate your progress and stay motivated.',
    content: (
      <div className="space-y-8">
        <div className="text-center">
          <div className="flex justify-center gap-4 mb-6">
            <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg transform rotate-3">
              <Trophy className="w-8 h-8 text-white" />
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-400 to-green-500 rounded-2xl flex items-center justify-center shadow-lg transform -rotate-2">
              <span className="text-2xl">🔥</span>
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg transform rotate-1">
              <span className="text-2xl">⭐</span>
            </div>
          </div>
          <h4 className="font-bold text-slate-900 mb-3">Unlock achievements as you grow</h4>
          <p className="text-slate-600 mb-6">Every ritual completed and streak maintained earns you beautiful badges that celebrate your journey.</p>
        </div>
        
        <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-2xl p-6 border border-orange-100">
          <div className="flex items-center gap-4">
            <div className="text-4xl">🔥</div>
            <div>
              <h5 className="font-semibold text-slate-900 mb-1">Streak Counter</h5>
              <p className="text-sm text-slate-600">Build momentum by completing rituals daily. Watch your streak grow and feel the satisfaction of consistency!</p>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
            <div className="text-2xl mb-2">🌟</div>
            <div className="text-xs font-medium text-slate-700">First Step</div>
            <div className="text-xs text-slate-500">Complete 1 ritual</div>
          </div>
          <div className="text-center p-4 bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl border border-emerald-100">
            <div className="text-2xl mb-2">💪</div>
            <div className="text-xs font-medium text-slate-700">Consistent</div>
            <div className="text-xs text-slate-500">3-day streak</div>
          </div>
          <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-100">
            <div className="text-2xl mb-2">👑</div>
            <div className="text-xs font-medium text-slate-700">Champion</div>
            <div className="text-xs text-slate-500">30 rituals</div>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'ready',
    title: 'You\'re all set! 🚀',
    description: 'Ready to start your journey of small wins and big changes?',
    content: (
      <div className="text-center space-y-8">
        <div className="relative">
          <div className="w-24 h-24 mx-auto bg-gradient-to-br from-emerald-500 to-green-600 rounded-full flex items-center justify-center shadow-2xl">
            <CheckCircle className="w-12 h-12 text-white" />
          </div>
          <div className="absolute -top-2 -right-2 w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center animate-pulse">
            ✨
          </div>
        </div>
        
        <div className="space-y-4">
          <h4 className="text-xl font-bold text-slate-900">Your first ritual is waiting!</h4>
          <p className="text-slate-600 leading-relaxed">
            Remember: consistency beats perfection. Just one minute a day can create remarkable change over time.
          </p>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Target className="w-5 h-5 text-blue-600" />
            <span className="font-semibold text-slate-900">Pro tip</span>
          </div>
          <p className="text-sm text-slate-600">
            Set a daily reminder and choose a consistent time that works for you. Many users find success with morning rituals!
          </p>
        </div>
      </div>
    )
  }
]

export function OnboardingFlow({ onComplete }: OnboardingFlowProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isAnimating, setIsAnimating] = useState(false)

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setIsAnimating(true)
      setTimeout(() => {
        setCurrentStep(currentStep + 1)
        setIsAnimating(false)
      }, 150)
    } else {
      onComplete()
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setIsAnimating(true)
      setTimeout(() => {
        setCurrentStep(currentStep - 1)
        setIsAnimating(false)
      }, 150)
    }
  }

  const currentStepData = steps[currentStep]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-slate-600">
              Step {currentStep + 1} of {steps.length}
            </span>
            <span className="text-sm text-slate-500">
              {Math.round(((currentStep + 1) / steps.length) * 100)}% complete
            </span>
          </div>
          <div className="bg-slate-200 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-blue-500 to-indigo-600 h-2 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Content Card */}
        <div className={`bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/20 p-8 md:p-12 transition-all duration-300 ${isAnimating ? 'opacity-50 scale-95' : 'opacity-100 scale-100'}`}>
          {/* Header */}
          <div className="text-center mb-8">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              {currentStepData.title}
            </h2>
            <p className="text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto">
              {currentStepData.description}
            </p>
          </div>

          {/* Step Content */}
          <div className="mb-12">
            {currentStepData.content}
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between">
            <button
              onClick={handlePrevious}
              disabled={currentStep === 0}
              className={`flex items-center gap-2 px-6 py-3 rounded-2xl font-semibold transition-all duration-200 ${
                currentStep === 0
                  ? 'text-slate-400 cursor-not-allowed'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <ArrowLeft className="w-5 h-5" />
              Previous
            </button>

            <div className="flex gap-2">
              {steps.map((_, index) => (
                <div
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentStep
                      ? 'bg-blue-500 scale-125'
                      : index < currentStep
                      ? 'bg-blue-300'
                      : 'bg-slate-300'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={handleNext}
              className="flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-2xl font-semibold hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >
              {currentStep === steps.length - 1 ? 'Start my journey' : 'Next'}
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Skip Option */}
        <div className="text-center mt-6">
          <button
            onClick={onComplete}
            className="text-slate-500 hover:text-slate-700 text-sm transition-colors"
          >
            Skip tutorial
          </button>
        </div>
      </div>
    </div>
  )
}