import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { emailService } from './emailService';

interface ExportData {
  resumeData: {
    fileName: string;
    uploadedAt: Date;
  };
  empathyAnalysis?: {
    confidenceScore: number;
    toneAnalysis: string;
    strongPoints: string[];
    weakPoints: string[];
    improvements: string[];
  };
  recruiterFeedback?: {
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
  };
  growthPlan?: {
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
  };
}

class ExportService {

  // Generate PDF Report
  async generatePDF(data: ExportData): Promise<Blob> {
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 20;
    let yPosition = margin;

    // Helper function to add text with word wrapping
    const addWrappedText = (text: string, x: number, y: number, maxWidth: number, fontSize: number = 10): number => {
      pdf.setFontSize(fontSize);
      const lines = pdf.splitTextToSize(text, maxWidth);
      pdf.text(lines, x, y);
      return y + (lines.length * fontSize * 0.35);
    };

    // Helper function to check if we need a new page
    const checkNewPage = (requiredHeight: number): number => {
      if (yPosition + requiredHeight > pageHeight - margin) {
        pdf.addPage();
        return margin;
      }
      return yPosition;
    };

    // Header
    pdf.setFontSize(24);
    pdf.setFont('helvetica', 'bold');
    pdf.setTextColor(59, 130, 246); // Blue color
    pdf.text('CareerFlow.ai Analysis Report', margin, yPosition);
    yPosition += 15;

    pdf.setFontSize(12);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(100, 100, 100);
    pdf.text(`Generated on: ${new Date().toLocaleDateString()}`, margin, yPosition);
    pdf.text(`Resume: ${data.resumeData.fileName}`, margin, yPosition + 5);
    yPosition += 20;

    // Empathy Analysis Section
    if (data.empathyAnalysis) {
      yPosition = checkNewPage(40);
      
      pdf.setFontSize(18);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(220, 38, 127); // Pink color
      pdf.text('🔍 Empathy Mirror Analysis', margin, yPosition);
      yPosition += 10;

      pdf.setFontSize(12);
      pdf.setFont('helvetica', 'normal');
      pdf.setTextColor(0, 0, 0);
      
      // Confidence Score
      pdf.text(`Confidence Score: ${data.empathyAnalysis.confidenceScore}/10`, margin, yPosition);
      yPosition += 8;

      // Tone Analysis
      pdf.setFont('helvetica', 'bold');
      pdf.text('Tone Analysis:', margin, yPosition);
      yPosition += 5;
      pdf.setFont('helvetica', 'normal');
      yPosition = addWrappedText(data.empathyAnalysis.toneAnalysis, margin, yPosition, pageWidth - 2 * margin);
      yPosition += 5;

      // Strong Points
      pdf.setFont('helvetica', 'bold');
      pdf.text('Strong Points:', margin, yPosition);
      yPosition += 5;
      pdf.setFont('helvetica', 'normal');
      data.empathyAnalysis.strongPoints.forEach((point, index) => {
        yPosition = checkNewPage(8);
        yPosition = addWrappedText(`• ${point}`, margin + 5, yPosition, pageWidth - 2 * margin - 5);
        yPosition += 2;
      });
      yPosition += 5;

      // Weak Points
      pdf.setFont('helvetica', 'bold');
      pdf.text('Areas for Improvement:', margin, yPosition);
      yPosition += 5;
      pdf.setFont('helvetica', 'normal');
      data.empathyAnalysis.weakPoints.forEach((point, index) => {
        yPosition = checkNewPage(8);
        yPosition = addWrappedText(`• ${point}`, margin + 5, yPosition, pageWidth - 2 * margin - 5);
        yPosition += 2;
      });
      yPosition += 5;

      // Improvements
      pdf.setFont('helvetica', 'bold');
      pdf.text('Improvement Suggestions:', margin, yPosition);
      yPosition += 5;
      pdf.setFont('helvetica', 'normal');
      data.empathyAnalysis.improvements.forEach((improvement, index) => {
        yPosition = checkNewPage(8);
        yPosition = addWrappedText(`• ${improvement}`, margin + 5, yPosition, pageWidth - 2 * margin - 5);
        yPosition += 2;
      });
      yPosition += 10;
    }

    // Recruiter Feedback Section
    if (data.recruiterFeedback) {
      yPosition = checkNewPage(40);
      
      pdf.setFontSize(18);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(59, 130, 246); // Blue color
      pdf.text('💬 RealTalk Recruiter Feedback', margin, yPosition);
      yPosition += 10;

      const recruiters = [
        { key: 'startup', name: 'Startup Recruiter', icon: '⚡' },
        { key: 'faang', name: 'FAANG Recruiter', icon: '🏢' },
        { key: 'consulting', name: 'Consulting Recruiter', icon: '💼' }
      ];

      recruiters.forEach((recruiter) => {
        const feedback = data.recruiterFeedback![recruiter.key as keyof typeof data.recruiterFeedback];
        
        yPosition = checkNewPage(30);
        
        pdf.setFontSize(14);
        pdf.setFont('helvetica', 'bold');
        pdf.setTextColor(0, 0, 0);
        pdf.text(`${recruiter.icon} ${recruiter.name}`, margin, yPosition);
        yPosition += 8;

        pdf.setFontSize(12);
        pdf.text(`Interview Likelihood: ${feedback.likelihood}/10`, margin, yPosition);
        yPosition += 8;

        pdf.setFont('helvetica', 'bold');
        pdf.text('Assessment:', margin, yPosition);
        yPosition += 5;
        pdf.setFont('helvetica', 'normal');
        yPosition = addWrappedText(feedback.assessment, margin, yPosition, pageWidth - 2 * margin);
        yPosition += 5;

        pdf.setFont('helvetica', 'bold');
        pdf.text('Feedback Points:', margin, yPosition);
        yPosition += 5;
        pdf.setFont('helvetica', 'normal');
        feedback.feedback.forEach((point) => {
          yPosition = checkNewPage(8);
          yPosition = addWrappedText(`• ${point}`, margin + 5, yPosition, pageWidth - 2 * margin - 5);
          yPosition += 2;
        });
        yPosition += 8;
      });
    }

    // Growth Plan Section
    if (data.growthPlan) {
      yPosition = checkNewPage(40);
      
      pdf.setFontSize(18);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(34, 197, 94); // Green color
      pdf.text('🧭 Growth Compass Plan', margin, yPosition);
      yPosition += 10;

      // Skills Gap
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(0, 0, 0);
      pdf.text('Skills Gap Analysis:', margin, yPosition);
      yPosition += 8;
      pdf.setFontSize(12);
      pdf.setFont('helvetica', 'normal');
      data.growthPlan.skillsGap.forEach((skill) => {
        yPosition = checkNewPage(6);
        pdf.text(`• ${skill}`, margin + 5, yPosition);
        yPosition += 6;
      });
      yPosition += 5;

      // Career Paths
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.text('Career Paths:', margin, yPosition);
      yPosition += 8;
      
      pdf.setFontSize(12);
      pdf.text('Conventional Path:', margin, yPosition);
      yPosition += 5;
      pdf.setFont('helvetica', 'normal');
      yPosition = addWrappedText(data.growthPlan.careerPaths.conventional, margin + 5, yPosition, pageWidth - 2 * margin - 5);
      yPosition += 8;

      pdf.setFont('helvetica', 'bold');
      pdf.text('Unconventional Paths:', margin, yPosition);
      yPosition += 5;
      pdf.setFont('helvetica', 'normal');
      data.growthPlan.careerPaths.unconventional.forEach((path, index) => {
        yPosition = checkNewPage(15);
        yPosition = addWrappedText(`${index + 1}. ${path}`, margin + 5, yPosition, pageWidth - 2 * margin - 5);
        yPosition += 5;
      });
      yPosition += 5;

      // 90-Day Roadmap
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.text('90-Day Roadmap:', margin, yPosition);
      yPosition += 8;

      const roadmapSections = [
        { title: '30 Days', items: data.growthPlan.roadmap.thirtyDays },
        { title: '60 Days', items: data.growthPlan.roadmap.sixtyDays },
        { title: '90 Days', items: data.growthPlan.roadmap.ninetyDays }
      ];

      roadmapSections.forEach((section) => {
        yPosition = checkNewPage(20);
        pdf.setFontSize(12);
        pdf.setFont('helvetica', 'bold');
        pdf.text(section.title + ':', margin, yPosition);
        yPosition += 5;
        pdf.setFont('helvetica', 'normal');
        section.items.forEach((item) => {
          yPosition = checkNewPage(6);
          yPosition = addWrappedText(`• ${item}`, margin + 5, yPosition, pageWidth - 2 * margin - 5);
          yPosition += 2;
        });
        yPosition += 5;
      });
    }

    // Footer
    const totalPages = pdf.getNumberOfPages();
    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i);
      pdf.setFontSize(8);
      pdf.setTextColor(150, 150, 150);
      pdf.text(`Page ${i} of ${totalPages}`, pageWidth - margin - 20, pageHeight - 10);
      pdf.text('Generated by CareerFlow.ai', margin, pageHeight - 10);
    }

    return pdf.output('blob');
  }

  // Generate Notion Template
  generateNotionTemplate(data: ExportData): string {
    let template = `# 🎯 CareerFlow.ai Analysis Report

**Generated:** ${new Date().toLocaleDateString()}
**Resume:** ${data.resumeData.fileName}

---

`;

    if (data.empathyAnalysis) {
      template += `## 🔍 Empathy Mirror Analysis

### Confidence Score
**${data.empathyAnalysis.confidenceScore}/10**

### Tone Analysis
${data.empathyAnalysis.toneAnalysis}

### ✅ Strong Points
${data.empathyAnalysis.strongPoints.map(point => `- ${point}`).join('\n')}

### ⚠️ Areas for Improvement
${data.empathyAnalysis.weakPoints.map(point => `- ${point}`).join('\n')}

### 💡 Improvement Suggestions
${data.empathyAnalysis.improvements.map(improvement => `- ${improvement}`).join('\n')}

---

`;
    }

    if (data.recruiterFeedback) {
      template += `## 💬 RealTalk Recruiter Feedback

### ⚡ Startup Recruiter
**Interview Likelihood:** ${data.recruiterFeedback.startup.likelihood}/10

**Assessment:**
${data.recruiterFeedback.startup.assessment}

**Feedback:**
${data.recruiterFeedback.startup.feedback.map(point => `- ${point}`).join('\n')}

### 🏢 FAANG Recruiter
**Interview Likelihood:** ${data.recruiterFeedback.faang.likelihood}/10

**Assessment:**
${data.recruiterFeedback.faang.assessment}

**Feedback:**
${data.recruiterFeedback.faang.feedback.map(point => `- ${point}`).join('\n')}

### 💼 Consulting Recruiter
**Interview Likelihood:** ${data.recruiterFeedback.consulting.likelihood}/10

**Assessment:**
${data.recruiterFeedback.consulting.assessment}

**Feedback:**
${data.recruiterFeedback.consulting.feedback.map(point => `- ${point}`).join('\n')}

---

`;
    }

    if (data.growthPlan) {
      template += `## 🧭 Growth Compass Plan

### 🎯 Skills Gap Analysis
${data.growthPlan.skillsGap.map(skill => `- [ ] ${skill}`).join('\n')}

### 🛤️ Career Paths

**Conventional Path:**
${data.growthPlan.careerPaths.conventional}

**Unconventional Paths:**
${data.growthPlan.careerPaths.unconventional.map((path, index) => `${index + 1}. ${path}`).join('\n')}

### 📅 90-Day Roadmap

**30 Days:**
${data.growthPlan.roadmap.thirtyDays.map(item => `- [ ] ${item}`).join('\n')}

**60 Days:**
${data.growthPlan.roadmap.sixtyDays.map(item => `- [ ] ${item}`).join('\n')}

**90 Days:**
${data.growthPlan.roadmap.ninetyDays.map(item => `- [ ] ${item}`).join('\n')}

### 📧 Cold Email Template
\`\`\`
${data.growthPlan.coldEmailTemplate}
\`\`\`

### 📚 Learning Resources
${data.growthPlan.resources.map(resource => `- ${resource}`).join('\n')}

---

*Generated by CareerFlow.ai - Emotionally Intelligent Career Coaching*`;
    }

    return template;
  }

  // Send Email with Report
  async sendEmailReport(
    recipientEmail: string, 
    recipientName: string, 
    data: ExportData,
    format: 'pdf' | 'notion' = 'pdf'
  ): Promise<boolean> {

    // This method is deprecated - use emailService.sendEmail directly
    throw new Error('This method has been deprecated. Use emailService.sendEmail directly.');
  }


  // Download file directly
  downloadFile(content: string | Blob, filename: string, type: string = 'text/plain') {
    const blob = content instanceof Blob ? content : new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}

export const exportService = new ExportService();