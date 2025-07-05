import React from 'react'
import { Home, Trophy, User } from 'lucide-react'

interface NavigationProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

export function Navigation({ activeTab, onTabChange }: NavigationProps) {
  const tabs = [
    { id: 'dashboard', label: 'Today', icon: Home },
    { id: 'badges', label: 'Badges', icon: Trophy },
    { id: 'profile', label: 'Profile', icon: User },
  ]

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-sm border-t border-slate-200/50 px-4 py-3 md:static md:border-0 md:bg-transparent md:px-0 md:py-0">
      <div className="flex justify-around md:justify-start md:flex-col md:gap-2">
        {tabs.map((tab) => {
          const Icon = tab.icon
          const isActive = activeTab === tab.id
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex flex-col md:flex-row items-center gap-1 md:gap-3 px-3 py-2 md:px-4 md:py-3 rounded-xl md:rounded-2xl transition-all duration-200 ${
                isActive
                  ? 'bg-blue-100 text-blue-600 md:bg-gradient-to-r md:from-blue-500 md:to-indigo-600 md:text-white md:shadow-lg'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 md:hover:bg-slate-50'
              }`}
            >
              <Icon className="w-6 h-6" />
              <span className="text-xs md:text-sm font-medium">{tab.label}</span>
            </button>
          )
        })}
      </div>
    </nav>
  )
}