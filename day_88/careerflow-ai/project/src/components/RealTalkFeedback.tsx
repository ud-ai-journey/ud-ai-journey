import React, { useEffect, useState } from 'react';
import { MessageSquare, Zap, Building2, Briefcase, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAppContext } from '@/contexts/AppContext';
import { aiService } from '@/services/aiService';

export const RealTalkFeedback: React.FC = () => {
  const { state, dispatch } = useAppContext();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const runAnalysis = async () => {
    if (!state.resumeData) return;

    setIsAnalyzing(true);
    dispatch({ type: 'SET_PROCESSING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      const feedback = await aiService.getRecruiterFeedback(state.resumeData.text);
      dispatch({ type: 'SET_RECRUITER_FEEDBACK', payload: feedback });
    } catch (error) {
      console.error('Recruiter feedback failed:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: error instanceof Error ? error.message : 'Analysis failed' 
      });
    } finally {
      setIsAnalyzing(false);
      dispatch({ type: 'SET_PROCESSING', payload: false });
    }
  };

  useEffect(() => {
    if (state.resumeData && !state.recruiterFeedback && !isAnalyzing) {
      runAnalysis();
    }
  }, [state.resumeData]);

  const getLikelihoodColor = (score: number) => {
    if (score >= 8) return 'bg-green-500';
    if (score >= 6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getLikelihoodText = (score: number) => {
    if (score >= 8) return 'High';
    if (score >= 6) return 'Medium';
    return 'Low';
  };

  const recruiterTypes = [
    {
      id: 'startup',
      name: 'Startup Recruiter',
      icon: Zap,
      description: 'Fast-paced, innovation-focused',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      id: 'faang',
      name: 'FAANG Recruiter',
      icon: Building2,
      description: 'Technical excellence, scalability',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      id: 'consulting',
      name: 'Consulting Recruiter',
      icon: Briefcase,
      description: 'Problem-solving, strategic thinking',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
  ];

  if (!state.resumeData) {
    return (
      <div className="text-center py-12">
        <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">Please upload your resume first to see recruiter feedback</p>
      </div>
    );
  }

  if (isAnalyzing) {
    return (
      <div className="space-y-6 animate-fade-in">
        <div className="text-center py-12 animate-scale-in">
          <div className="space-y-4">
            <div className="relative">
              <MessageSquare className="w-12 h-12 text-blue-400 mx-auto animate-bounce" />
              <div className="absolute inset-0 w-12 h-12 mx-auto rounded-full bg-blue-100 animate-ping opacity-75"></div>
            </div>
            <p className="text-lg font-medium text-gray-700 animate-pulse-soft">Getting recruiter perspectives...</p>
            <p className="text-sm text-gray-500">Analyzing from 3 different viewpoints</p>
            <div className="w-32 h-1 bg-gray-200 rounded-full mx-auto overflow-hidden">
              <div className="h-full bg-gradient-to-r from-blue-400 to-blue-600 animate-shimmer"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!state.recruiterFeedback) {
    return (
      <div className="text-center py-12 animate-fade-in">
        <Button onClick={runAnalysis} className="bg-blue-500 hover:bg-blue-600 hover-lift transition-all-smooth">
          <MessageSquare className="w-4 h-4 mr-2" />
          Get Recruiter Feedback
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center space-y-2 animate-scale-in">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent flex items-center justify-center gap-2">
          <MessageSquare className="w-6 h-6 text-blue-500" />
          RealTalk Recruiter Feedback
        </h2>
        <p className="text-gray-600">Brutally honest insights from three recruiter perspectives</p>
      </div>

      <Tabs defaultValue="startup" className="w-full animate-slide-in-left">
        <TabsList className="grid w-full grid-cols-3 bg-gray-100 p-1 rounded-lg">
          {recruiterTypes.map((type) => (
            <TabsTrigger key={type.id} value={type.id} className="flex items-center gap-2 transition-all-smooth hover-scale data-[state=active]:bg-white data-[state=active]:shadow-sm">
              <type.icon className="w-4 h-4 transition-transform duration-300" />
              <span className="hidden sm:inline">{type.name}</span>
              <span className="sm:hidden">{type.name.split(' ')[0]}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {recruiterTypes.map((type) => {
          const feedback = state.recruiterFeedback![type.id as keyof typeof state.recruiterFeedback];
          
          return (
            <TabsContent key={type.id} value={type.id} className="space-y-4 animate-fade-in">
              <Card className={`${type.bgColor} hover-lift transition-all-smooth`}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <type.icon className={`w-6 h-6 ${type.color} animate-pulse-soft`} />
                    <div>
                      <h3 className="text-lg font-bold">{type.name}</h3>
                      <p className="text-sm text-gray-600 font-normal">{type.description}</p>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4 animate-fade-in">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Interview Likelihood</span>
                      <div className="flex items-center gap-2">
                        <Badge className={`${getLikelihoodColor(feedback.likelihood)} text-white animate-scale-in`}>
                          {getLikelihoodText(feedback.likelihood)}
                        </Badge>
                        <span className="text-lg font-bold">{feedback.likelihood}/10</span>
                      </div>
                    </div>
                    <Progress value={feedback.likelihood * 10} className="h-2 transition-all duration-1000 ease-out" />
                  </div>
                </CardContent>
              </Card>

              <Card className="hover-lift transition-all-smooth animate-slide-in-left">
                <CardHeader>
                  <CardTitle>Assessment</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed animate-fade-in">{feedback.assessment}</p>
                </CardContent>
              </Card>

              <Card className="hover-lift transition-all-smooth animate-slide-in-right">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5 text-orange-500" />
                    Specific Feedback Points
                  </CardTitle>
                  <CardDescription>
                    Actionable insights to improve your chances
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {feedback.feedback.map((point, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                        <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-sm text-gray-700">{point}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          );
        })}
      </Tabs>
    </div>
  );
};