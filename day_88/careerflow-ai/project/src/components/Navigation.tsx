import React from 'react';
import { Heart, MessageSquare, Compass, Upload, AlertCircle, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ExportModal } from './ExportModal';
import { useAppContext } from '@/contexts/AppContext';

export const Navigation: React.FC = () => {
  const { state, dispatch } = useAppContext();
  const [showExportModal, setShowExportModal] = React.useState(false);

  const tabs = [
    {
      id: 'upload',
      name: 'Upload',
      icon: Upload,
      color: 'text-gray-600',
      description: 'Upload Resume',
    },
    {
      id: 'empathy',
      name: 'Empathy Mirror',
      icon: Heart,
      color: 'text-red-500',
      description: 'Tone Analysis',
      disabled: !state.resumeData,
    },
    {
      id: 'feedback',
      name: 'RealTalk',
      icon: MessageSquare,
      color: 'text-blue-500',
      description: 'Recruiter Feedback',
      disabled: !state.resumeData,
    },
    {
      id: 'growth',
      name: 'Growth Compass',
      icon: Compass,
      color: 'text-green-500',
      description: 'Career Planning',
      disabled: !state.resumeData,
    },
  ];

  const getCompletionStatus = (tabId: string) => {
    switch (tabId) {
      case 'upload':
        return state.resumeData ? 'complete' : 'incomplete';
      case 'empathy':
        return state.empathyAnalysis ? 'complete' : state.resumeData ? 'available' : 'disabled';
      case 'feedback':
        return state.recruiterFeedback ? 'complete' : state.resumeData ? 'available' : 'disabled';
      case 'growth':
        return state.growthPlan ? 'complete' : state.resumeData ? 'available' : 'disabled';
      default:
        return 'disabled';
    }
  };

  return (
    <div className="bg-white/95 backdrop-blur-sm border-b border-gray-200 sticky top-16 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-4 animate-fade-in">
          <div className="flex items-center space-x-1 overflow-x-auto animate-slide-in-left">
            {tabs.map((tab) => {
              const status = getCompletionStatus(tab.id);
              const isActive = state.activeTab === tab.id;
              const isDisabled = status === 'disabled';
              
              return (
                <Button
                  key={tab.id}
                  variant={isActive ? 'default' : 'ghost'}
                  size="sm"
                  disabled={isDisabled || state.isProcessing}
                  onClick={() => dispatch({ type: 'SET_ACTIVE_TAB', payload: tab.id })}
                  className={`flex items-center gap-2 min-w-0 whitespace-nowrap transition-all-smooth hover-lift ${
                    isDisabled ? 'opacity-50' : ''
                  } ${isActive ? 'shadow-lg bg-gradient-to-r from-blue-600 to-blue-700' : 'hover:bg-gray-50'}`}
                >
                  <tab.icon className={`w-4 h-4 transition-all duration-300 ${
                    isActive ? 'text-white animate-pulse-soft' : tab.color
                  } ${!isDisabled && !isActive ? 'group-hover:scale-110' : ''}`} />
                  <span className="hidden sm:inline">{tab.name}</span>
                  <span className="sm:hidden">{tab.description}</span>
                  {status === 'complete' && (
                    <Badge variant="secondary" className="ml-1 text-xs px-1 animate-scale-in">
                      ✓
                    </Badge>
                  )}
                </Button>
              );
            })}
          </div>

          {state.error && (
            <div className="flex items-center gap-2 text-red-600 animate-slide-in-right">
              <AlertCircle className="w-4 h-4 animate-pulse" />
              <span className="text-sm">Analysis error</span>
            </div>
          )}

          {state.isProcessing && (
            <div className="flex items-center gap-2 text-blue-600 animate-slide-in-right">
              <div className="animate-spin w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full" />
              <span className="text-sm">Processing...</span>
            </div>
          )}

          {/* Export Button */}
          {(state.empathyAnalysis || state.recruiterFeedback || state.growthPlan) && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowExportModal(true)}
              className="flex items-center gap-2 hover-lift transition-all-smooth animate-slide-in-right"
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">Export</span>
            </Button>
          )}
        </div>

        <ExportModal 
          isOpen={showExportModal} 
          onClose={() => setShowExportModal(false)} 
        />
      </div>
    </div>
  );
};