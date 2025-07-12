import React, { useCallback, useState } from 'react';
import { Upload, File, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAppContext } from '@/contexts/AppContext';

export const FileUpload: React.FC = () => {
  const { dispatch } = useAppContext();
  const [dragActive, setDragActive] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle');

  const extractTextFromFile = async (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        const text = e.target?.result as string;
        if (text && text.trim()) {
          resolve(text);
        } else {
          reject(new Error('Could not extract text from file'));
        }
      };
      
      reader.onerror = () => reject(new Error('Error reading file'));
      
      if (file.type === 'text/plain') {
        reader.readAsText(file);
      } else {
        // For now, we'll handle PDF as text. In production, you'd use a PDF parser
        reader.readAsText(file);
      }
    });
  };

  const handleFile = useCallback(async (file: File) => {
    if (!file) return;

    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      setUploadStatus('error');
      dispatch({ type: 'SET_ERROR', payload: 'File size must be less than 5MB' });
      return;
    }

    const allowedTypes = ['text/plain', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
      setUploadStatus('error');
      dispatch({ type: 'SET_ERROR', payload: 'Only PDF and TXT files are supported' });
      return;
    }

    setUploadStatus('processing');
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      const text = await extractTextFromFile(file);
      
      if (text.length < 100) {
        throw new Error('Resume appears to be too short. Please ensure it contains sufficient content.');
      }

      const resumeData = {
        text,
        fileName: file.name,
        uploadedAt: new Date(),
      };

      // Reset all previous analysis state before setting new resume
      dispatch({ type: 'RESET_ANALYSIS' });
      dispatch({ type: 'SET_RESUME_DATA', payload: resumeData });
      setUploadStatus('success');
      
      // Auto-switch to empathy tab after successful upload
      setTimeout(() => {
        dispatch({ type: 'SET_ACTIVE_TAB', payload: 'empathy' });
      }, 1500);

    } catch (error) {
      setUploadStatus('error');
      dispatch({ 
        type: 'SET_ERROR', 
        payload: error instanceof Error ? error.message : 'Failed to process file' 
      });
    }
  }, [dispatch]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files?.[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, [handleFile]);

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      handleFile(e.target.files[0]);
    }
  }, [handleFile]);

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'processing':
        return <div className="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full" />;
      case 'success':
        return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-6 h-6 text-red-500" />;
      default:
        return <Upload className="w-8 h-8 text-gray-400" />;
    }
  };

  const getStatusMessage = () => {
    switch (uploadStatus) {
      case 'processing':
        return 'Processing your resume...';
      case 'success':
        return 'Resume uploaded successfully! Redirecting to analysis...';
      case 'error':
        return 'Upload failed. Please try again.';
      default:
        return 'Upload your resume to get started';
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center space-y-4 animate-scale-in">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-gray-900 bg-clip-text text-transparent">
          Welcome to CareerMirror.ai
        </h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Get emotionally intelligent insights about your resume from AI-powered career coaching
        </p>
      </div>

      <Card className="max-w-2xl mx-auto hover-lift transition-all-smooth animate-slide-in-left">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="w-5 h-5 text-blue-600" />
            Upload Your Resume
          </CardTitle>
          <CardDescription className="text-gray-600">
            Upload your resume in PDF or TXT format to receive comprehensive AI-powered feedback
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all-smooth hover-scale ${
              dragActive
                ? 'border-blue-500 bg-blue-50 shadow-lg'
                : uploadStatus === 'error'
                ? 'border-red-300 bg-red-50 shadow-lg'
                : uploadStatus === 'success'
                ? 'border-green-300 bg-green-50 shadow-lg'
                : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/30'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={handleInputChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              disabled={uploadStatus === 'processing'}
            />
            
            <div className="space-y-4 animate-fade-in">
              <div className="flex justify-center">
                {getStatusIcon()}
              </div>
              
              <div>
                <p className="text-lg font-medium text-gray-900 transition-colors duration-300">
                  {getStatusMessage()}
                </p>
                <p className="text-sm text-gray-500 mt-2 transition-colors duration-300">
                  Drag and drop your file here, or click to browse
                </p>
              </div>

              {uploadStatus === 'idle' && (
                <div className="flex justify-center animate-scale-in">
                  <Button variant="outline" className="mt-2 hover-lift transition-all-smooth">
                    <File className="w-4 h-4 mr-2" />
                    Choose File
                  </Button>
                </div>
              )}
            </div>
          </div>

          <div className="mt-4 text-xs text-gray-500 space-y-1 animate-slide-in-right">
            <p>• Supported formats: PDF, TXT</p>
            <p>• Maximum file size: 5MB</p>
            <p>• Your data is processed securely and not stored permanently</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};