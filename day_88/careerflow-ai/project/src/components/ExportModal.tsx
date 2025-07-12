import React, { useState, useEffect } from 'react';
import { Download, Mail, FileText, Send, Copy, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { exportService } from '@/services/exportService';
import { emailService } from '@/services/emailService';
import { useAppContext } from '@/contexts/AppContext';
import { initGoogleIdentity, uploadPdfToDriveWithGIS } from '@/services/googleDriveService';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ExportModal: React.FC<ExportModalProps> = ({ isOpen, onClose }) => {
  const { state } = useAppContext();
  const { toast } = useToast();
  const [isExporting, setIsExporting] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [emailData, setEmailData] = useState({
    name: '',
    email: '',
  });
  const [notionTemplate, setNotionTemplate] = useState('');
  const [copied, setCopied] = useState(false);

  const exportData = {
    resumeData: state.resumeData!,
    empathyAnalysis: state.empathyAnalysis || undefined,
    recruiterFeedback: state.recruiterFeedback || undefined,
    growthPlan: state.growthPlan || undefined,
  };

  useEffect(() => {
    initGoogleIdentity();
  }, []);

  const handleDownloadPDF = async () => {
    setIsExporting(true);
    try {
      const pdfBlob = await exportService.generatePDF(exportData);
      const filename = `CareerMirror_Analysis_${new Date().toISOString().split('T')[0]}.pdf`;
      exportService.downloadFile(pdfBlob, filename);
      
      toast({
        title: "PDF Downloaded",
        description: "Your analysis report has been downloaded successfully.",
      });
    } catch (error) {
      toast({
        title: "Export Failed",
        description: "Failed to generate PDF. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsExporting(false);
    }
  };

  const handleGenerateNotion = () => {
    try {
      const template = exportService.generateNotionTemplate(exportData);
      setNotionTemplate(template);
      
      toast({
        title: "Notion Template Generated",
        description: "Your Notion-ready template is ready to copy.",
      });
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: "Failed to generate Notion template. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleCopyNotion = async () => {
    try {
      await navigator.clipboard.writeText(notionTemplate);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      
      toast({
        title: "Copied to Clipboard",
        description: "Notion template copied successfully.",
      });
    } catch (error) {
      toast({
        title: "Copy Failed",
        description: "Failed to copy to clipboard. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleDownloadNotion = () => {
    if (!notionTemplate) {
      handleGenerateNotion();
      return;
    }
    
    const filename = `CareerMirror_Analysis_${new Date().toISOString().split('T')[0]}.md`;
    exportService.downloadFile(notionTemplate, filename, 'text/markdown');
    
    toast({
      title: "Markdown Downloaded",
      description: "Your Notion template has been downloaded as a markdown file.",
    });
  };

  const handleSendEmail = async (format: 'pdf' | 'notion') => {
    const trimmedName = emailData.name.trim();
    const trimmedEmail = emailData.email.trim();
    
    if (!trimmedName || !trimmedEmail) {
      console.log('Missing name or email:', { trimmedName, trimmedEmail });
      toast({
        title: "Missing Information",
        description: "Please enter both name and email address.",
        variant: "destructive",
      });
      return;
    }

    // Basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(trimmedEmail)) {
      console.log('Invalid email format:', trimmedEmail);
      toast({
        title: "Invalid Email",
        description: "Please enter a valid email address.",
        variant: "destructive",
      });
      return;
    }

    if (!emailService.isEmailConfigured()) {
      console.log('Email service not configured. Check your .env for VITE_EMAILJS_SERVICE_ID, VITE_EMAILJS_TEMPLATE_ID, VITE_EMAILJS_USER_ID');
      toast({
        title: "Email Not Configured",
        description: "EmailJS environment variables are not set up. Please configure EmailJS to use email functionality.",
        variant: "destructive",
      });
      return;
    }

    setIsSending(true);
    try {
      let emailContent = '';
      let reportLink = '';
      
      if (format === 'pdf') {
        const pdfBlob = await exportService.generatePDF(exportData);
        const fileName = `CareerFlow_Report_${new Date().toISOString().split('T')[0]}.pdf`;
        reportLink = await uploadPdfToDriveWithGIS(pdfBlob, fileName);
        emailContent = `Your PDF report is ready! <a href="${reportLink}">Download it here</a>.`;
      } else if (format === 'notion') {
        const notionTemplate = exportService.generateNotionTemplate(exportData);
        const fileName = `CareerFlow_Notion_Template_${new Date().toISOString().split('T')[0]}.md`;
        const notionBlob = new Blob([notionTemplate], { type: 'text/markdown' });
        reportLink = await uploadPdfToDriveWithGIS(notionBlob, fileName);
        emailContent = `Your Notion template is ready! <a href="${reportLink}">Download it here</a>.`;
      }
      
      await emailService.sendEmail({
        to: trimmedEmail,
        name: trimmedName,
        subject: 'Your CareerFlow.ai Report Is Ready',
        content: emailContent,
        reportLink: reportLink,
      });
      
      toast({
        title: "Email Sent",
        description: `Your ${format.toUpperCase()} report link has been sent successfully.`,
      });
      
      setEmailData({ name: '', email: '' });
    } catch (error) {
      console.log('Error sending email:', error);
      toast({
        title: "Email Failed",
        description: error instanceof Error ? error.message : "Failed to send email. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSending(false);
    }
  };

  // Helper function to convert Blob to base64
  function blobToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  const getAvailableAnalyses = () => {
    const analyses = [];
    if (state.empathyAnalysis) analyses.push('Empathy Analysis');
    if (state.recruiterFeedback) analyses.push('Recruiter Feedback');
    if (state.growthPlan) analyses.push('Growth Plan');
    return analyses;
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto animate-scale-in">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Download className="w-5 h-5 text-blue-600" />
            Export Your Analysis
          </DialogTitle>
          <DialogDescription>
            Download or share your comprehensive career analysis report
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Available Analyses */}
          <Card className="animate-fade-in">
            <CardHeader>
              <CardTitle className="text-sm">Report Contents</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {getAvailableAnalyses().map((analysis) => (
                  <Badge key={analysis} variant="secondary" className="animate-scale-in">
                    {analysis}
                  </Badge>
                ))}
                {getAvailableAnalyses().length === 0 && (
                  <p className="text-sm text-gray-500">No analyses completed yet</p>
                )}
              </div>
            </CardContent>
          </Card>

          <Tabs defaultValue="download" className="w-full animate-slide-in-left">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="download" className="transition-all-smooth">Download</TabsTrigger>
              <TabsTrigger value="notion" className="transition-all-smooth">Notion</TabsTrigger>
              <TabsTrigger value="email" className="transition-all-smooth">Email</TabsTrigger>
            </TabsList>

            <TabsContent value="download" className="space-y-4 animate-fade-in">
              <Card className="hover-lift transition-all-smooth">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-red-500" />
                    PDF Report
                  </CardTitle>
                  <CardDescription>
                    Professional PDF report with all your analyses
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button 
                    onClick={handleDownloadPDF}
                    disabled={isExporting || getAvailableAnalyses().length === 0}
                    className="w-full hover-lift transition-all-smooth"
                  >
                    {isExporting ? (
                      <>
                        <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                        Generating PDF...
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4 mr-2" />
                        Download PDF Report
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="notion" className="space-y-4 animate-fade-in">
              <Card className="hover-lift transition-all-smooth">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-purple-500" />
                    Notion Template
                  </CardTitle>
                  <CardDescription>
                    Markdown-formatted template ready for Notion
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <Button 
                      onClick={handleGenerateNotion}
                      disabled={getAvailableAnalyses().length === 0}
                      variant="outline"
                      className="hover-lift transition-all-smooth"
                    >
                      <FileText className="w-4 h-4 mr-2" />
                      Generate Template
                    </Button>
                    <Button 
                      onClick={handleDownloadNotion}
                      disabled={getAvailableAnalyses().length === 0}
                      className="hover-lift transition-all-smooth"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download Markdown
                    </Button>
                  </div>

                  {notionTemplate && (
                    <div className="space-y-2 animate-slide-in-left">
                      <div className="flex items-center justify-between">
                        <Label>Template Preview</Label>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={handleCopyNotion}
                          className="hover-lift transition-all-smooth"
                        >
                          {copied ? (
                            <>
                              <Check className="w-4 h-4 mr-2 text-green-500" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="w-4 h-4 mr-2" />
                              Copy
                            </>
                          )}
                        </Button>
                      </div>
                      <Textarea
                        value={notionTemplate}
                        readOnly
                        className="min-h-[200px] text-xs font-mono transition-all-smooth"
                        placeholder="Your Notion template will appear here..."
                      />
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="email" className="space-y-4 animate-fade-in">
              <Card className="hover-lift transition-all-smooth">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Mail className="w-5 h-5 text-blue-500" />
                    Email Delivery
                  </CardTitle>
                  <CardDescription>
                    Send your report directly to your email
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Your Name</Label>
                      <Input
                        id="name"
                        value={emailData.name}
                        onChange={(e) => setEmailData(prev => ({ ...prev, name: e.target.value }))}
                        placeholder="Enter your name"
                        className="transition-all-smooth focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email Address</Label>
                      <Input
                        id="email"
                        type="email"
                        value={emailData.email}
                        onChange={(e) => setEmailData(prev => ({ ...prev, email: e.target.value }))}
                        placeholder="Enter your email"
                        className="transition-all-smooth focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <Button
                      onClick={() => handleSendEmail('pdf')}
                      disabled={isSending || getAvailableAnalyses().length === 0}
                      className="hover-lift transition-all-smooth"
                    >
                      {isSending ? (
                        <>
                          <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                          Sending...
                        </>
                      ) : (
                        <>
                          <Send className="w-4 h-4 mr-2" />
                          Send PDF
                        </>
                      )}
                    </Button>
                    <Button
                      onClick={() => handleSendEmail('notion')}
                      disabled={isSending || getAvailableAnalyses().length === 0}
                      variant="outline"
                      className="hover-lift transition-all-smooth"
                    >
                      {isSending ? (
                        <>
                          <div className="animate-spin w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full mr-2" />
                          Sending...
                        </>
                      ) : (
                        <>
                          <Send className="w-4 h-4 mr-2" />
                          Send Markdown
                        </>
                      )}
                    </Button>
                  </div>

                  <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded-lg animate-fade-in">
                    <p className="font-medium mb-1">📧 Email Powered by SendGrid:</p>
                    <p>Email delivery is configured and ready to use with your SendGrid API key.</p>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>Professional HTML email templates</li>
                      <li>Secure attachment delivery</li>
                      <li>Reliable SendGrid infrastructure</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        <div className="flex justify-end pt-4 border-t animate-slide-in-right">
          <Button variant="outline" onClick={onClose} className="hover-lift transition-all-smooth">
            <X className="w-4 h-4 mr-2" />
            Close
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};