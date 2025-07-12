import emailjs from '@emailjs/browser';

interface EmailData {
  to: string;
  name: string;
  subject: string;
  content: string;
  attachment?: string; // base64 string for PDF
  reportLink?: string; // Google Drive link for the report
}

class EmailService {
  private serviceId = import.meta.env.VITE_EMAILJS_SERVICE_ID!;
  private templateId = import.meta.env.VITE_EMAILJS_TEMPLATE_ID!;
  private userId = import.meta.env.VITE_EMAILJS_USER_ID!;
  private isConfigured: boolean;

  constructor() {
    this.isConfigured = !!(this.serviceId && this.templateId && this.userId);
    if (!this.isConfigured) {
      console.warn('EmailJS environment variables not configured. Email functionality will be disabled.');
    }
  }

  isEmailConfigured(): boolean {
    return this.isConfigured;
  }

  async sendEmail(emailData: EmailData): Promise<void> {
    if (!this.isConfigured) {
      throw new Error('EmailJS is not configured. Please set up your EmailJS environment variables.');
    }

    const templateParams: any = {
      to_name: emailData.name,
      to_email: emailData.to,
      from_name: 'CareerFlow.ai',
      message: emailData.content,
      subject: emailData.subject,
      report_link: emailData.reportLink || 'https://careerflow.ai/reports',
      unsubscribe_link: 'https://careerflow.ai/unsubscribe',
    };
    if (emailData.attachment) {
      templateParams.attachment = emailData.attachment;
    }

    try {
      const response = await emailjs.send(
        this.serviceId,
        this.templateId,
        templateParams,
        this.userId
      );
      if (response.status !== 200) {
        throw new Error(`EmailJS send error: ${response.status}`);
      }
      console.log('Email sent successfully');
    } catch (err) {
      console.error('Failed to send email:', err);
      throw err;
    }
  }
}

export const emailService = new EmailService();
