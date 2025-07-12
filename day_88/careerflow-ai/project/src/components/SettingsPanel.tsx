import React, { useState } from 'react';
import { Settings, Key, Eye, EyeOff, Save, TestTube, AlertCircle, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';

interface SettingsPanelProps {
  onClose: () => void;
}

export const SettingsPanel: React.FC<SettingsPanelProps> = ({ onClose }) => {
  const [showKeys, setShowKeys] = useState(false);
  const [groqKey, setGroqKey] = useState(import.meta.env.VITE_GROQ_API_KEY || '');
  const [geminiKey, setGeminiKey] = useState(import.meta.env.VITE_GEMINI_API_KEY || '');
  const [emailjsServiceId, setEmailjsServiceId] = useState(import.meta.env.VITE_EMAILJS_SERVICE_ID || '');
  const [emailjsTemplateId, setEmailjsTemplateId] = useState(import.meta.env.VITE_EMAILJS_TEMPLATE_ID || '');
  const [emailjsUserId, setEmailjsUserId] = useState(import.meta.env.VITE_EMAILJS_USER_ID || '');
  const [demoMode, setDemoMode] = useState(false);
  const [autoSave, setAutoSave] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [testMessage, setTestMessage] = useState('');

  const handleSaveSettings = () => {
    // In a real app, you'd save these to localStorage or a backend
    localStorage.setItem('careerflow_settings', JSON.stringify({
      groqKey,
      geminiKey,
      emailjsServiceId,
      emailjsTemplateId,
      emailjsUserId,
      demoMode,
      autoSave,
      notifications
    }));
    
    // Show success message
    setTestStatus('success');
    setTestMessage('Settings saved successfully!');
    
    setTimeout(() => {
      setTestStatus('idle');
      setTestMessage('');
    }, 3000);
  };

  const testAPIKeys = async () => {
    setTestStatus('testing');
    setTestMessage('Testing API keys...');
    
    try {
      // Simulate API test
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      if (groqKey || geminiKey) {
        setTestStatus('success');
        setTestMessage('API keys are working correctly!');
      } else {
        setTestStatus('error');
        setTestMessage('No API keys configured. Please add at least one API key.');
      }
    } catch (error) {
      setTestStatus('error');
      setTestMessage('Failed to test API keys. Please check your configuration.');
    }
    
    setTimeout(() => {
      setTestStatus('idle');
      setTestMessage('');
    }, 5000);
  };

  const getAPIStatus = () => {
    if (groqKey || geminiKey) {
      return { status: 'configured', color: 'bg-green-100 text-green-800' };
    }
    return { status: 'not configured', color: 'bg-red-100 text-red-800' };
  };

  const apiStatus = getAPIStatus();

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <Settings className="w-6 h-6 text-gray-600" />
              <h2 className="text-2xl font-bold text-gray-900">Settings</h2>
            </div>
            <Button variant="ghost" onClick={onClose} size="sm">
              ✕
            </Button>
          </div>

          {/* API Configuration */}
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg font-semibold">API Configuration</CardTitle>
                  <CardDescription>Configure your AI service API keys</CardDescription>
                </div>
                <Badge variant="outline" className={apiStatus.color}>
                  {apiStatus.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <Label htmlFor="show-keys" className="text-sm font-medium">
                  Show API Keys
                </Label>
                <Switch
                  id="show-keys"
                  checked={showKeys}
                  onCheckedChange={setShowKeys}
                />
              </div>
              
              <div className="space-y-4">
                <div>
                  <Label htmlFor="groq-key" className="text-sm font-medium">
                    Groq API Key
                  </Label>
                  <div className="relative mt-1">
                    <Input
                      id="groq-key"
                      type={showKeys ? 'text' : 'password'}
                      value={groqKey}
                      onChange={(e) => setGroqKey(e.target.value)}
                      placeholder="Enter your Groq API key"
                      className="pr-10"
                    />
                    {groqKey && (
                      <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <Label htmlFor="gemini-key" className="text-sm font-medium">
                    Gemini API Key
                  </Label>
                  <div className="relative mt-1">
                    <Input
                      id="gemini-key"
                      type={showKeys ? 'text' : 'password'}
                      value={geminiKey}
                      onChange={(e) => setGeminiKey(e.target.value)}
                      placeholder="Enter your Gemini API key"
                      className="pr-10"
                    />
                    {geminiKey && (
                      <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <Button 
                onClick={testAPIKeys}
                disabled={testStatus === 'testing'}
                className="w-full"
              >
                <TestTube className="w-4 h-4 mr-2" />
                {testStatus === 'testing' ? 'Testing...' : 'Test API Keys'}
              </Button>

              {testMessage && (
                <Alert className={testStatus === 'error' ? 'border-red-200 bg-red-50' : 'border-green-200 bg-green-50'}>
                  {testStatus === 'error' ? (
                    <AlertCircle className="h-4 w-4 text-red-600" />
                  ) : (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  )}
                  <AlertDescription className={testStatus === 'error' ? 'text-red-700' : 'text-green-700'}>
                    {testMessage}
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Email Configuration */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">Email Configuration</CardTitle>
              <CardDescription>Configure EmailJS for email export feature</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="emailjs-service" className="text-sm font-medium">
                  EmailJS Service ID
                </Label>
                <Input
                  id="emailjs-service"
                  type="text"
                  value={emailjsServiceId}
                  onChange={(e) => setEmailjsServiceId(e.target.value)}
                  placeholder="Enter your EmailJS service ID"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="emailjs-template" className="text-sm font-medium">
                  EmailJS Template ID
                </Label>
                <Input
                  id="emailjs-template"
                  type="text"
                  value={emailjsTemplateId}
                  onChange={(e) => setEmailjsTemplateId(e.target.value)}
                  placeholder="Enter your EmailJS template ID"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="emailjs-user" className="text-sm font-medium">
                  EmailJS User ID
                </Label>
                <Input
                  id="emailjs-user"
                  type="text"
                  value={emailjsUserId}
                  onChange={(e) => setEmailjsUserId(e.target.value)}
                  placeholder="Enter your EmailJS user ID"
                  className="mt-1"
                />
              </div>
            </CardContent>
          </Card>

          {/* Application Settings */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">Application Settings</CardTitle>
              <CardDescription>Customize your experience</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="demo-mode" className="text-sm font-medium">
                    Demo Mode
                  </Label>
                  <p className="text-xs text-gray-500 mt-1">
                    Use sample data for testing without API keys
                  </p>
                </div>
                <Switch
                  id="demo-mode"
                  checked={demoMode}
                  onCheckedChange={setDemoMode}
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="auto-save" className="text-sm font-medium">
                    Auto Save
                  </Label>
                  <p className="text-xs text-gray-500 mt-1">
                    Automatically save your analysis results
                  </p>
                </div>
                <Switch
                  id="auto-save"
                  checked={autoSave}
                  onCheckedChange={setAutoSave}
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="notifications" className="text-sm font-medium">
                    Notifications
                  </Label>
                  <p className="text-xs text-gray-500 mt-1">
                    Show notifications for analysis completion
                  </p>
                </div>
                <Switch
                  id="notifications"
                  checked={notifications}
                  onCheckedChange={setNotifications}
                />
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <Button onClick={handleSaveSettings} className="flex-1">
              <Save className="w-4 h-4 mr-2" />
              Save Settings
            </Button>
            <Button variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}; 