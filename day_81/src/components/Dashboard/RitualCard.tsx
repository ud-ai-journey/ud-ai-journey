import React, { useState } from 'react'
import { Brain, CheckSquare, HelpCircle, Heart, Clock, Lightbulb, ArrowRight } from 'lucide-react'
import type { Ritual } from '../../types'

interface RitualCardProps {
  ritual: Ritual
}

const getRitualIcon = (type: string) => {
  switch (type) {
    case 'reflection':
      return <Brain className="w-7 h-7 text-white" />
    case 'task':
      return <CheckSquare className="w-7 h-7 text-white" />
    case 'quiz':
      return <HelpCircle className="w-7 h-7 text-white" />
    case 'meditation':
      return <Heart className="w-7 h-7 text-white" />
    default:
      return <Brain className="w-7 h-7 text-white" />
  }
}

const getRitualGradient = (type: string) => {
  switch (type) {
    case 'reflection':
      return 'from-purple-500 to-indigo-600'
    case 'task':
      return 'from-blue-500 to-cyan-600'
    case 'quiz':
      return 'from-emerald-500 to-teal-600'
    case 'meditation':
      return 'from-rose-500 to-pink-600'
    default:
      return 'from-purple-500 to-indigo-600'
  }
}

const getRitualBgGradient = (type: string) => {
  switch (type) {
    case 'reflection':
      return 'from-purple-50 to-indigo-50'
    case 'task':
      return 'from-blue-50 to-cyan-50'
    case 'quiz':
      return 'from-emerald-50 to-teal-50'
    case 'meditation':
      return 'from-rose-50 to-pink-50'
    default:
      return 'from-purple-50 to-indigo-50'
  }
}

export function RitualCard({ ritual }: RitualCardProps) {
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({})
  const [showResults, setShowResults] = useState<{ [key: number]: boolean }>({})
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)

  const handleAnswerSelect = (questionIndex: number, optionIndex: number) => {
    setSelectedAnswers(prev => ({ ...prev, [questionIndex]: optionIndex }))
    setShowResults(prev => ({ ...prev, [questionIndex]: true }))
    
    if (ritual.content.questions && questionIndex < ritual.content.questions.length - 1) {
      setTimeout(() => {
        setCurrentQuestionIndex(questionIndex + 1)
      }, 2000)
    }
  }

  const resetQuiz = () => {
    setSelectedAnswers({})
    setShowResults({})
    setCurrentQuestionIndex(0)
  }

  const renderContent = () => {
    switch (ritual.type) {
      case 'reflection':
        return (
          <div className="space-y-5">
            <div className="flex items-center gap-3 mb-5">
              <Lightbulb className="w-5 h-5 text-purple-600" />
              <h4 className="font-semibold text-slate-800 text-lg">Reflection prompts</h4>
            </div>
            <div className="space-y-4">
              {ritual.content.prompts?.map((prompt: string, index: number) => (
                <div key={index} className="group">
                  <div className="flex items-start gap-4 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl border border-purple-100/50 hover:border-purple-200 transition-all duration-200">
                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-semibold text-sm">
                      {index + 1}
                    </div>
                    <p className="text-slate-700 leading-relaxed pt-1">{prompt}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 p-4 bg-gradient-to-r from-purple-100 to-indigo-100 rounded-2xl border border-purple-200/50">
              <div className="flex items-center gap-2 mb-2">
                <Lightbulb className="w-4 h-4 text-purple-600" />
                <span className="text-sm font-medium text-purple-800">Reflection tip</span>
              </div>
              <p className="text-sm text-purple-700">
                Take your time with each prompt. There are no right or wrong answers—just honest reflection.
              </p>
            </div>
          </div>
        )
      case 'task':
        return (
          <div className="space-y-5">
            <div className="flex items-center gap-3 mb-5">
              <ArrowRight className="w-5 h-5 text-blue-600" />
              <h4 className="font-semibold text-slate-800 text-lg">Simple steps</h4>
            </div>
            <div className="space-y-4">
              {ritual.content.steps?.map((step: string, index: number) => (
                <div key={index} className="group">
                  <div className="flex items-start gap-4 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-2xl border border-blue-100/50 hover:border-blue-200 transition-all duration-200">
                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center text-white font-semibold text-sm">
                      {index + 1}
                    </div>
                    <p className="text-slate-700 leading-relaxed pt-1">{step}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 p-4 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-2xl border border-blue-200/50">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">Time estimate</span>
              </div>
              <p className="text-sm text-blue-700">
                This should take about 60 seconds to complete. Take it at your own pace.
              </p>
            </div>
          </div>
        )
      case 'quiz':
        return (
          <div className="space-y-6">
            <div className="flex items-center gap-3 mb-5">
              <HelpCircle className="w-5 h-5 text-emerald-600" />
              <h4 className="font-semibold text-slate-800 text-lg">Knowledge check</h4>
            </div>
            
            {ritual.content.questions && ritual.content.questions.length > 1 && (
              <div className="flex items-center justify-between p-4 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-2xl border border-emerald-100/50">
                <div className="flex gap-2">
                  {ritual.content.questions.map((_: any, index: number) => (
                    <div
                      key={index}
                      className={`w-3 h-3 rounded-full transition-all duration-300 ${
                        index === currentQuestionIndex
                          ? 'bg-emerald-500 scale-125'
                          : index < currentQuestionIndex || showResults[index]
                          ? 'bg-emerald-400'
                          : 'bg-slate-300'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm font-medium text-emerald-700">
                  Question {currentQuestionIndex + 1} of {ritual.content.questions.length}
                </span>
              </div>
            )}

            {ritual.content.questions?.map((question: any, questionIndex: number) => {
              if (questionIndex !== currentQuestionIndex && !showResults[questionIndex]) return null
              
              const selectedAnswer = selectedAnswers[questionIndex]
              const showResult = showResults[questionIndex]
              
              return (
                <div key={questionIndex} className="space-y-4">
                  <div className="p-5 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-2xl border border-emerald-100/50">
                    <p className="text-slate-800 font-medium text-lg leading-relaxed">{question.q}</p>
                  </div>
                  <div className="space-y-3">
                    {question.options?.map((option: string, optIndex: number) => {
                      const isSelected = selectedAnswer === optIndex
                      const isCorrect = optIndex === question.correct
                      const showCorrectAnswer = showResult && isCorrect
                      const showWrongAnswer = showResult && isSelected && !isCorrect
                      
                      return (
                        <button
                          key={optIndex}
                          onClick={() => handleAnswerSelect(questionIndex, optIndex)}
                          disabled={showResult}
                          className={`w-full p-4 rounded-2xl border-2 transition-all duration-300 text-left font-medium transform ${
                            showCorrectAnswer
                              ? 'border-emerald-500 bg-emerald-100 text-emerald-800 scale-[1.02]'
                              : showWrongAnswer
                              ? 'border-red-500 bg-red-100 text-red-800'
                              : isSelected
                              ? 'border-emerald-500 bg-emerald-50 text-emerald-700'
                              : 'border-slate-200 hover:border-emerald-300 hover:bg-emerald-50 cursor-pointer'
                          } ${showResult ? 'cursor-not-allowed' : 'cursor-pointer hover:scale-[1.01]'}`}
                        >
                          <div className="flex items-center justify-between">
                            <span className="leading-relaxed">{option}</span>
                            {showResult && (
                              <span className="text-xl ml-3">
                                {isCorrect ? '✅' : isSelected ? '❌' : ''}
                              </span>
                            )}
                          </div>
                        </button>
                      )
                    })}
                  </div>
                  {showResult && (
                    <div className="p-5 bg-gradient-to-r from-emerald-100 to-teal-100 border border-emerald-200 rounded-2xl">
                      <p className="text-emerald-800 font-medium mb-3">
                        {selectedAnswer === question.correct 
                          ? '🎉 Excellent! You got it right!' 
                          : `💡 The correct answer is: ${question.options[question.correct]}`
                        }
                      </p>
                      {questionIndex === ritual.content.questions.length - 1 && (
                        <button
                          onClick={resetQuiz}
                          className="px-4 py-2 bg-emerald-500 text-white rounded-xl hover:bg-emerald-600 transition-colors font-medium"
                        >
                          🔄 Try again
                        </button>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )
      case 'meditation':
        return (
          <div className="space-y-5">
            <div className="flex items-center gap-3 mb-5">
              <Heart className="w-5 h-5 text-rose-600" />
              <h4 className="font-semibold text-slate-800 text-lg">Meditation guide</h4>
            </div>
            <div className="space-y-4">
              {ritual.content.instructions?.map((instruction: string, index: number) => (
                <div key={index} className="group">
                  <div className="flex items-start gap-4 p-4 bg-gradient-to-r from-rose-50 to-pink-50 rounded-2xl border border-rose-100/50 hover:border-rose-200 transition-all duration-200">
                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-rose-500 to-pink-600 rounded-xl flex items-center justify-center text-white font-semibold text-sm">
                      {index + 1}
                    </div>
                    <p className="text-slate-700 leading-relaxed pt-1">{instruction}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 p-4 bg-gradient-to-r from-rose-100 to-pink-100 rounded-2xl border border-rose-200/50">
              <div className="flex items-center gap-2 mb-2">
                <Heart className="w-4 h-4 text-rose-600" />
                <span className="text-sm font-medium text-rose-800">Meditation tip</span>
              </div>
              <p className="text-sm text-rose-700">
                Find a quiet space and take your time with each step. Focus on your breath and be present.
              </p>
            </div>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className={`bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 p-8 transition-all duration-300 hover:shadow-2xl`}>
      {/* Header */}
      <div className="flex items-center gap-5 mb-8">
        <div className={`p-4 rounded-2xl bg-gradient-to-br ${getRitualGradient(ritual.type)} shadow-lg`}>
          {getRitualIcon(ritual.type)}
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-2xl font-bold text-slate-900">{ritual.title}</h3>
            <div className="flex items-center gap-1 text-xs text-slate-500 bg-slate-100 px-2 py-1 rounded-lg">
              <Clock className="w-3 h-3" />
              <span>1 min</span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-slate-600 capitalize font-medium bg-slate-100 px-3 py-1 rounded-lg text-sm">
              {ritual.type}
            </span>
            <span className="text-slate-400">•</span>
            <span className="text-sm text-slate-500">Daily ritual</span>
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="mb-8 p-5 bg-slate-50/80 rounded-2xl border border-slate-100">
        <p className="text-slate-700 leading-relaxed text-lg">{ritual.description}</p>
      </div>

      {/* Content */}
      <div className="bg-slate-50/50 rounded-2xl p-6 border border-slate-100">
        {renderContent()}
      </div>
    </div>
  )
}