import React from 'react'
import { useAuth } from './hooks/useAuth'
import { AuthWrapper } from './components/Auth/AuthWrapper'
import { Layout } from './components/Layout/Layout'
import { Sparkles } from 'lucide-react'

function App() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-3xl mb-6 shadow-xl animate-pulse">
            <Sparkles className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-slate-900 mb-3">One-Minute Wins</h1>
          <p className="text-slate-600 text-lg">Loading your journey...</p>
          <div className="mt-6 flex items-center justify-center">
            <div className="w-8 h-8 border-3 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
    )
  }

  return user ? <Layout /> : <AuthWrapper />
}

export default App