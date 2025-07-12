import React, { useEffect, useState } from 'react';
import { Compass, Target, TrendingUp, Mail, BookOpen, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import { useAppContext } from '@/contexts/AppContext';
import { aiService } from '@/services/aiService';

export const GrowthCompass: React.FC = () => {
  const { state, dispatch } = useAppContext();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const runAnalysis = async () => {
    if (!state.resumeData) return;

    setIsAnalyzing(true);
    dispatch({ type: 'SET_PROCESSING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      const plan = await aiService.createGrowthPlan(state.resumeData.text);
      dispatch({ type: 'SET_GROWTH_PLAN', payload: plan });
    } catch (error) {
      console.error('Growth plan failed:', error);
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
    if (state.resumeData && !state.growthPlan && !isAnalyzing) {
      runAnalysis();
    }
  }, [state.resumeData]);

  if (!state.resumeData) {
    return (
      <div className="text-center py-12">
        <Compass className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">Please upload your resume first to see your growth plan</p>
      </div>
    );
  }

  if (isAnalyzing) {
    return (
      <div className="space-y-6 animate-fade-in">
        <div className="text-center py-12 animate-scale-in">
          <div className="space-y-4">
            <div className="relative">
              <Compass className="w-12 h-12 text-green-400 mx-auto animate-spin" />
              <div className="absolute inset-0 w-12 h-12 mx-auto rounded-full bg-green-100 animate-ping opacity-75"></div>
            </div>
            <p className="text-lg font-medium text-gray-700 animate-pulse-soft">Creating your growth plan...</p>
            <p className="text-sm text-gray-500">Mapping out your career journey</p>
            <div className="w-32 h-1 bg-gray-200 rounded-full mx-auto overflow-hidden">
              <div className="h-full bg-gradient-to-r from-green-400 to-green-600 animate-shimmer"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!state.growthPlan) {
    return (
      <div className="text-center py-12 animate-fade-in">
        <Button onClick={runAnalysis} className="bg-green-500 hover:bg-green-600 hover-lift transition-all-smooth">
          <Compass className="w-4 h-4 mr-2" />
          Create Growth Plan
        </Button>
      </div>
    );
  }

  const { skillsGap, careerPaths, roadmap, coldEmailTemplate, resources } = state.growthPlan;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center space-y-2 animate-scale-in">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent flex items-center justify-center gap-2">
          <Compass className="w-6 h-6 text-green-500" />
          Growth Compass
        </h2>
        <p className="text-gray-600">Your personalized roadmap to career advancement</p>
      </div>

      <Tabs defaultValue="skills" className="w-full animate-slide-in-left">
        <TabsList className="grid w-full grid-cols-4 bg-gray-100 p-1 rounded-lg">
          <TabsTrigger value="skills" className="transition-all-smooth hover-scale data-[state=active]:bg-white data-[state=active]:shadow-sm">Skills Gap</TabsTrigger>
          <TabsTrigger value="paths" className="transition-all-smooth hover-scale data-[state=active]:bg-white data-[state=active]:shadow-sm">Career Paths</TabsTrigger>
          <TabsTrigger value="roadmap" className="transition-all-smooth hover-scale data-[state=active]:bg-white data-[state=active]:shadow-sm">90-Day Plan</TabsTrigger>
          <TabsTrigger value="network" className="transition-all-smooth hover-scale data-[state=active]:bg-white data-[state=active]:shadow-sm">Networking</TabsTrigger>
        </TabsList>

        <TabsContent value="skills" className="space-y-4 animate-fade-in">
          <Card className="hover-lift transition-all-smooth">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5 text-red-500" />
                Skills Gap Analysis
              </CardTitle>
              <CardDescription>
                Key skills to develop for your next career move
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 sm:grid-cols-2">
                {skillsGap.map((skill, index) => (
                  <div key={index} className="flex items-center gap-2 p-3 bg-red-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                    <div className="w-2 h-2 bg-red-500 rounded-full" />
                    <span className="text-sm font-medium text-gray-700">{skill}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="hover-lift transition-all-smooth">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-500" />
                Learning Resources
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {resources.map((resource, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                    <BookOpen className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-700">{resource}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="paths" className="space-y-4 animate-fade-in">
          <Card className="hover-lift transition-all-smooth">
            <CardHeader>
              <CardTitle>Conventional Path</CardTitle>
              <CardDescription>The traditional next step in your career</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed animate-fade-in">{careerPaths.conventional}</p>
            </CardContent>
          </Card>

          <Card className="hover-lift transition-all-smooth">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-purple-500" />
                Unconventional Paths
              </CardTitle>
              <CardDescription>
                Alternative routes that could set you apart
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {careerPaths.unconventional.map((path, index) => (
                  <div key={index} className="p-4 bg-purple-50 rounded-lg hover-scale transition-all-smooth animate-fade-in" style={{ animationDelay: `${index * 0.2}s` }}>
                    <h4 className="font-medium text-gray-900 mb-2">Alternative Path {index + 1}</h4>
                    <p className="text-sm text-gray-700">{path}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="roadmap" className="space-y-4 animate-fade-in">
          <div className="grid gap-4 md:grid-cols-3 animate-slide-in-left">
            <Card className="hover-lift transition-all-smooth">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-green-500" />
                  30 Days
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {roadmap.thirtyDays.map((action, index) => (
                    <div key={index} className="flex items-start gap-2 animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                      <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                      <p className="text-sm text-gray-700">{action}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="hover-lift transition-all-smooth">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-yellow-500" />
                  60 Days
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {roadmap.sixtyDays.map((action, index) => (
                    <div key={index} className="flex items-start gap-2 animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                      <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0" />
                      <p className="text-sm text-gray-700">{action}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="hover-lift transition-all-smooth">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-red-500" />
                  90 Days
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {roadmap.ninetyDays.map((action, index) => (
                    <div key={index} className="flex items-start gap-2 animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                      <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0" />
                      <p className="text-sm text-gray-700">{action}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="network" className="space-y-4 animate-fade-in">
          <Card className="hover-lift transition-all-smooth">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mail className="w-5 h-5 text-blue-500" />
                Cold Email Template
              </CardTitle>
              <CardDescription>
                Personalized template for networking outreach
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={coldEmailTemplate}
                readOnly
                className="min-h-[200px] text-sm transition-all-smooth focus:ring-2 focus:ring-blue-500"
                placeholder="Your personalized cold email template will appear here..."
              />
              <div className="mt-4 flex gap-2 animate-slide-in-right">
                <Button 
                  size="sm"
                  className="hover-lift transition-all-smooth"
                  onClick={() => navigator.clipboard.writeText(coldEmailTemplate)}
                >
                  Copy Template
                </Button>
                <Badge variant="secondary" className="animate-scale-in">Ready to customize and send</Badge>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};