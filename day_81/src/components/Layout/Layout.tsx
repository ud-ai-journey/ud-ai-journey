import React, { useState } from 'react'
import { Navigation } from './Navigation'
import { Dashboard } from '../Dashboard/Dashboard'
import { BadgeCollection } from '../Badges/BadgeCollection'
import { Profile } from '../Profile/Profile'
import { Sparkles } from 'lucide-react'

export function Layout() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />
      case 'badges':
        return <BadgeCollection />
      case 'profile':
        return <Profile />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Mobile Layout */}
      <div className="md:hidden">
        {renderContent()}
        <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
      </div>
      
      {/* Desktop Layout */}
      <div className="hidden md:block">
        <div className="max-w-7xl mx-auto p-6">
          <div className="flex gap-8">
            {/* Sidebar */}
            <div className="w-72 flex-shrink-0">
              <div className="sticky top-6">
                <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl p-8 border border-white/20">
                  {/* Logo */}
                  <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl mb-4 shadow-lg">
                      <Sparkles className="w-8 h-8 text-white" />
                    </div>
                    <h1 className="text-2xl font-bold text-slate-900 mb-1">One-Minute Wins</h1>
                    <p className="text-slate-600 text-sm">Small steps, big changes</p>
                  </div>
                  
                  {/* Navigation */}
                  <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
                  
                  {/* Motivational Quote */}
                  <div className="mt-8 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100/50">
                    <p className="text-sm text-slate-600 italic text-center leading-relaxed">
                      "The journey of a thousand miles begins with one step."
                    </p>
                    <p className="text-xs text-slate-500 text-center mt-2">— Lao Tzu</p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Main Content */}
            <div className="flex-1 min-w-0">
              {renderContent()}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}