import React, { useState } from 'react';
import { AppProvider, useAppContext } from './contexts/AppContext';
import { Header } from './components/Header';
import { Navigation } from './components/Navigation';
import { FileUpload } from './components/FileUpload';
import { EmpathyMirror } from './components/EmpathyMirror';
import { RealTalkFeedback } from './components/RealTalkFeedback';
import { GrowthCompass } from './components/GrowthCompass';
import { LandingPage } from './components/LandingPage';
import { APIStatus } from './components/APIStatus';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

const AppContent: React.FC = () => {
  const { state } = useAppContext();
  const [showLanding, setShowLanding] = useState(true);

  const handleGetStarted = () => {
    setShowLanding(false);
  };

  const renderActiveTab = () => {
    switch (state.activeTab) {
      case 'upload':
        return <FileUpload />;
      case 'empathy':
        return <EmpathyMirror />;
      case 'feedback':
        return <RealTalkFeedback />;
      case 'growth':
        return <GrowthCompass />;
      default:
        return <FileUpload />;
    }
  };

  if (showLanding) {
    return <LandingPage onGetStarted={handleGetStarted} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <Header />
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        {state.error && (
          <Alert className="mb-6 border-red-200 bg-red-50 hover-lift transition-all-smooth animate-slide-in-left">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-700">
              {state.error}
            </AlertDescription>
          </Alert>
        )}
        {renderActiveTab()}
      </main>
      <APIStatus />
      <footer className="bg-white/95 backdrop-blur-sm border-t border-gray-200 py-8 mt-16 animate-fade-in">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-gray-500 space-y-2">
            <p>CareerFlow.ai - Emotionally Intelligent Career Coaching</p>
            <p className="flex items-center justify-center gap-2">
              <span>Powered by AI</span>
              <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
              <span>Built with empathy</span>
              <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
              <span>Designed for growth</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;