import React, { useEffect, useState } from 'react';
import { Heart, TrendingUp, TrendingDown, Lightbulb, Target } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { useAppContext } from '@/contexts/AppContext';
import { aiService } from '@/services/aiService';

export const EmpathyMirror: React.FC = () => {
  const { state, dispatch } = useAppContext();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const runAnalysis = async () => {
    if (!state.resumeData) return;

    setIsAnalyzing(true);
    dispatch({ type: 'SET_PROCESSING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      const analysis = await aiService.analyzeEmpathy(state.resumeData.text);
      dispatch({ type: 'SET_EMPATHY_ANALYSIS', payload: analysis });
    } catch (error) {
      console.error('Empathy analysis failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Analysis failed';
      
      // Provide more specific error messages based on the error type
      let userMessage = errorMessage;
      if (errorMessage.includes('quota') || errorMessage.includes('billing')) {
        userMessage = 'API quota exceeded. Please check your billing status at console.groq.com or aistudio.google.com, ensure your account is active with sufficient quota, then restart the dev server and try again.';
      } else if (errorMessage.includes('rate limit')) {
        userMessage = 'Rate limit exceeded. Please wait 1-2 minutes before trying again.';
      } else if (errorMessage.includes('No API keys configured')) {
        userMessage = 'No AI services configured. Please add VITE_GROQ_API_KEY or VITE_GEMINI_API_KEY to your .env file, then restart the dev server with "npm run dev".';
      } else if (errorMessage.includes('unavailable') || errorMessage.includes('All AI services')) {
        userMessage = 'All AI services are temporarily unavailable. Please check your API billing status and try again in 2-3 minutes.';
      } else {
        userMessage = 'Analysis failed due to a temporary issue. Please check your internet connection and try again.';
      }
      
      dispatch({ 
        type: 'SET_ERROR', 
        payload: userMessage
      });
    } finally {
      setIsAnalyzing(false);
      dispatch({ type: 'SET_PROCESSING', payload: false });
    }
  };

  useEffect(() => {
    if (state.resumeData && !state.empathyAnalysis && !isAnalyzing) {
      runAnalysis();
    }
  }, [state.resumeData]);

  const getConfidenceColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceDescription = (score: number) => {
    if (score >= 8) return 'Strong confidence level';
    if (score >= 6) return 'Moderate confidence level';
    return 'Needs confidence boost';
  };

  if (!state.resumeData) {
    return (
      <div className="text-center py-12">
        <Heart className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">Please upload your resume first to see empathy analysis</p>
      </div>
    );
  }

  if (isAnalyzing) {
    return (
      <div className="space-y-6 animate-fade-in">
        <div className="text-center py-12 animate-scale-in">
          <div className="space-y-4">
            <div className="relative">
              <Heart className="w-12 h-12 text-red-400 mx-auto animate-bounce" />
              <div className="absolute inset-0 w-12 h-12 mx-auto rounded-full bg-red-100 animate-ping opacity-75"></div>
            </div>
            <p className="text-lg font-medium text-gray-700 animate-pulse-soft">Analyzing emotional tone...</p>
            <p className="text-sm text-gray-500">This may take 10-15 seconds</p>
            <div className="w-32 h-1 bg-gray-200 rounded-full mx-auto overflow-hidden">
              <div className="h-full bg-gradient-to-r from-red-400 to-red-600 animate-shimmer"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!state.empathyAnalysis) {
    return (
      <div className="text-center py-12 animate-fade-in">
        <Button onClick={runAnalysis} className="bg-red-500 hover:bg-red-600 hover-lift transition-all-smooth">
          <Heart className="w-4 h-4 mr-2" />
          Start Empathy Analysis
        </Button>
      </div>
    );
  }

  const { confidenceScore, toneAnalysis, strongPoints, weakPoints, improvements } = state.empathyAnalysis;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center space-y-2 animate-scale-in">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-red-600 to-pink-600 bg-clip-text text-transparent flex items-center justify-center gap-2">
          <Heart className="w-6 h-6 text-red-500" />
          Empathy Mirror Analysis
        </h2>
        <p className="text-gray-600">Understanding the emotional resonance of your resume</p>
      </div>

      {/* Confidence Score */}
      <Card className="hover-lift transition-all-smooth animate-slide-in-left">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="w-5 h-5 text-blue-500" />
            Confidence Level
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Confidence Score</span>
              <span className={`text-2xl font-bold ${getConfidenceColor(confidenceScore)}`}>
                {confidenceScore}/10
              </span>
            </div>
            <Progress value={confidenceScore * 10} className="h-3 transition-all duration-1000 ease-out" />
            <p className="text-sm text-gray-600">{getConfidenceDescription(confidenceScore)}</p>
          </div>
        </CardContent>
      </Card>

      {/* Tone Analysis */}
      <Card className="hover-lift transition-all-smooth animate-slide-in-right">
        <CardHeader>
          <CardTitle>Overall Tone Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 leading-relaxed animate-fade-in">{toneAnalysis}</p>
        </CardContent>
      </Card>

      {/* Strong Points */}
      <Card className="hover-lift transition-all-smooth animate-slide-in-left">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-500" />
            Strong Language Examples
          </CardTitle>
          <CardDescription>
            These phrases demonstrate confidence and impact
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {strongPoints.map((point, index) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <TrendingUp className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{point}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Weak Points */}
      <Card className="hover-lift transition-all-smooth animate-slide-in-right">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-red-500" />
            Areas for Improvement
          </CardTitle>
          <CardDescription>
            Language that could be strengthened for better impact
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {weakPoints.map((point, index) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-red-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <TrendingDown className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{point}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Improvements */}
      <Card className="hover-lift transition-all-smooth animate-slide-in-left">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-yellow-500" />
            Empathetic Improvement Suggestions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {improvements.map((improvement, index) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <Lightbulb className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{improvement}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};