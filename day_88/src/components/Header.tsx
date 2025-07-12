import React, { useState } from 'react';
import { Brain, Heart, TrendingUp, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { SettingsPanel } from './SettingsPanel';

export const Header: React.FC = () => {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <>
      <header className="bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm sticky top-0 z-50 transition-all-smooth">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16 animate-fade-in">
            <div className="flex items-center space-x-3 hover-scale transition-transform-smooth">
              <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg shadow-lg hover-glow transition-all-smooth">
                <Brain className="w-6 h-6 text-white animate-pulse-soft" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  CareerFlow.ai
                </h1>
                <p className="text-xs text-gray-500 transition-colors duration-300">
                  Emotionally Intelligent Career Coaching
                </p>
              </div>
            </div>
            
            <div className="hidden md:flex items-center space-x-8 animate-slide-in-right">
              <div className="flex items-center space-x-2 text-sm text-gray-600 hover:text-red-600 transition-colors duration-300 cursor-pointer group">
                <Heart className="w-4 h-4 text-red-500 group-hover:scale-110 transition-transform duration-300" />
                <span>Empathy Analysis</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600 hover:text-blue-600 transition-colors duration-300 cursor-pointer group">
                <Brain className="w-4 h-4 text-blue-500 group-hover:scale-110 transition-transform duration-300" />
                <span>Recruiter Insights</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600 hover:text-green-600 transition-colors duration-300 cursor-pointer group">
                <TrendingUp className="w-4 h-4 text-green-500 group-hover:scale-110 transition-transform duration-300" />
                <span>Growth Planning</span>
              </div>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSettings(true)}
                className="text-gray-600 hover:text-gray-900 transition-colors duration-300"
              >
                <Settings className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>
      
      {showSettings && (
        <SettingsPanel onClose={() => setShowSettings(false)} />
      )}
    </>
  );
};