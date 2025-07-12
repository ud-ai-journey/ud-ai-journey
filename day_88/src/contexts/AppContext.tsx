import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface ResumeData {
  text: string;
  fileName: string;
  uploadedAt: Date;
}

interface EmpathyAnalysis {
  confidenceScore: number;
  toneAnalysis: string;
  strongPoints: string[];
  weakPoints: string[];
  improvements: string[];
}

interface RecruiterFeedback {
  startup: {
    assessment: string;
    likelihood: number;
    feedback: string[];
  };
  faang: {
    assessment: string;
    likelihood: number;
    feedback: string[];
  };
  consulting: {
    assessment: string;
    likelihood: number;
    feedback: string[];
  };
}

interface GrowthPlan {
  skillsGap: string[];
  careerPaths: {
    conventional: string;
    unconventional: string[];
  };
  roadmap: {
    thirtyDays: string[];
    sixtyDays: string[];
    ninetyDays: string[];
  };
  coldEmailTemplate: string;
  resources: string[];
}

interface AppState {
  resumeData: ResumeData | null;
  empathyAnalysis: EmpathyAnalysis | null;
  recruiterFeedback: RecruiterFeedback | null;
  growthPlan: GrowthPlan | null;
  activeTab: string;
  isProcessing: boolean;
  error: string | null;
}

type AppAction =
  | { type: 'SET_RESUME_DATA'; payload: ResumeData }
  | { type: 'SET_EMPATHY_ANALYSIS'; payload: EmpathyAnalysis }
  | { type: 'SET_RECRUITER_FEEDBACK'; payload: RecruiterFeedback }
  | { type: 'SET_GROWTH_PLAN'; payload: GrowthPlan }
  | { type: 'SET_ACTIVE_TAB'; payload: string }
  | { type: 'SET_PROCESSING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'RESET_ANALYSIS' };

const initialState: AppState = {
  resumeData: null,
  empathyAnalysis: null,
  recruiterFeedback: null,
  growthPlan: null,
  activeTab: 'upload',
  isProcessing: false,
  error: null,
};

const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'SET_RESUME_DATA':
      return { ...state, resumeData: action.payload, error: null };
    case 'SET_EMPATHY_ANALYSIS':
      return { ...state, empathyAnalysis: action.payload };
    case 'SET_RECRUITER_FEEDBACK':
      return { ...state, recruiterFeedback: action.payload };
    case 'SET_GROWTH_PLAN':
      return { ...state, growthPlan: action.payload };
    case 'SET_ACTIVE_TAB':
      return { ...state, activeTab: action.payload };
    case 'SET_PROCESSING':
      return { ...state, isProcessing: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, isProcessing: false };
    case 'RESET_ANALYSIS':
      return {
        ...state,
        empathyAnalysis: null,
        recruiterFeedback: null,
        growthPlan: null,
        activeTab: 'upload',
        error: null,
      };
    default:
      return state;
  }
};

const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};