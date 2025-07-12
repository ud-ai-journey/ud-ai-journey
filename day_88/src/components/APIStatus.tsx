import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle, CheckCircle, Clock, Zap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { aiService } from '@/services/aiService';

export const APIStatus: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<any[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const updateStatus = () => {
      setApiStatus(aiService.getAPIStatus());
    };

    updateStatus();
    const interval = setInterval(updateStatus, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (api: any) => {
    if (!api.configured) return <AlertCircle className="w-4 h-4 text-gray-400" />;
    if (api.available && api.errorCount === 0) return <CheckCircle className="w-4 h-4 text-green-500" />;
    if (api.available && api.errorCount > 0) return <Clock className="w-4 h-4 text-yellow-500" />;
    return <AlertCircle className="w-4 h-4 text-red-500" />;
  };

  const getStatusText = (api: any) => {
    if (!api.configured) return 'Not Configured';
    if (!api.available && api.lastError?.toLowerCase().includes('quota')) return 'Quota Exceeded';
    if (!api.available && api.lastError?.toLowerCase().includes('rate limit')) return 'Rate Limited';
    if (api.available && api.errorCount === 0) return 'Healthy';
    if (api.available && api.errorCount > 0) return 'Recovering';
    return 'Unavailable';
  };

  const getStatusColor = (api: any) => {
    if (!api.configured) return 'bg-gray-100 text-gray-600';
    if (!api.available && api.lastError?.toLowerCase().includes('quota')) return 'bg-orange-100 text-orange-700';
    if (!api.available && api.lastError?.toLowerCase().includes('rate limit')) return 'bg-yellow-100 text-yellow-700';
    if (api.available && api.errorCount === 0) return 'bg-green-100 text-green-700';
    if (api.available && api.errorCount > 0) return 'bg-yellow-100 text-yellow-700';
    return 'bg-red-100 text-red-700';
  };

  if (!isVisible) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsVisible(true)}
          className="flex items-center gap-2 bg-white shadow-lg hover:shadow-xl transition-all duration-300"
        >
          <Activity className="w-4 h-4" />
          API Status
        </Button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 w-80">
      <Card className="shadow-xl border-2 animate-scale-in">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Activity className="w-4 h-4 text-blue-500" />
              API Status Monitor
            </CardTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsVisible(false)}
              className="h-6 w-6 p-0"
            >
              ×
            </Button>
          </div>
          <CardDescription className="text-xs">
            Real-time monitoring of AI service health
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {apiStatus.map((api) => (
            <div key={api.name} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2">
                {getStatusIcon(api)}
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm capitalize">{api.name}</span>
                    {api.name === 'groq' && <Zap className="w-3 h-3 text-purple-500" />}
                  </div>
                  {api.lastError && (
                    <p className="text-xs text-gray-500 truncate max-w-40" title={api.lastError}>
                      {api.lastError}
                    </p>
                  )}
                </div>
              </div>
              <div className="text-right">
                <Badge variant="secondary" className={`text-xs ${getStatusColor(api)}`}>
                  {getStatusText(api)}
                </Badge>
                {api.errorCount > 0 && (
                  <p className="text-xs text-gray-500 mt-1">
                    Errors: {api.errorCount}
                  </p>
                )}
              </div>
            </div>
          ))}
          
          <div className="pt-2 border-t text-xs text-gray-500">
            <div className="flex items-center justify-between">
              <span>Auto-refresh: 5s</span>
              <span>Fallback: Enabled</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};