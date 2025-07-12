# CareerFlow.ai - Day 88

> **Security Note:** Never commit your `.env` file or any API keys, secrets, or credentials to GitHub. Always use environment variables for sensitive information.

## Day 88 Journey & Reflections

Today was a full-stack, full-soul Saturday! 🌟

- **Validated my idea** using ChatGPT (in my own persona, thinking like a supportive son and a hackathon winner!)
- **Researched** the landscape with Perplexity and Claude to make sure the concept was unique and valuable
- **Built the MVP** in Bolt, getting the core features up and running fast
- **Moved to Cursor** for deeper enhancements and a smoother dev experience
- **Designed and enhanced the landing page** to make a great first impression
- **Integrated EmailJS** for seamless email delivery
- **Added export functionality** for PDF and Notion templates
- **Implemented Google Drive integration** for secure, scalable report sharing via email
- **Tested the full flow**—from upload to analysis to export to email, all in one day!

> I started this morning with a decision to build CareerFlow.ai today—and I made it happen. The attached mail report is proof that with focus, the right tools, and a bit of AI magic, you can turn an idea into a working product in a single day.

---

An emotionally intelligent AI career coach that combines empathy analysis, recruiter feedback simulation, and personalized growth planning.

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# EmailJS
VITE_EMAILJS_SERVICE_ID=your_emailjs_service_id
VITE_EMAILJS_TEMPLATE_ID=your_emailjs_template_id
VITE_EMAILJS_USER_ID=your_emailjs_user_id

# Google OAuth
VITE_GOOGLE_CLIENT_ID=your_google_client_id

# Groq API
VITE_GROQ_API_KEY=your_groq_api_key

# Gemini API
VITE_GEMINI_API_KEY=your_gemini_api_key
```

**Never share or commit your .env file!**

## Features

### 🔍 Empathy Mirror Module
- Resume tone analysis using advanced sentiment analysis
- Confidence level scoring (1-10 scale)  
- Emotional positioning feedback
- Specific examples of strong/weak language
- Improvement suggestions with empathetic tone

### 💬 RealTalk Feedback Module
- Three distinct recruiter personas:
  - **Startup Recruiter**: Fast-paced, innovation-focused
  - **FAANG Recruiter**: Technical excellence, scalability focus
  - **Consulting Recruiter**: Problem-solving, strategic thinking
- Brutally honest, constructive feedback
- Specific, actionable improvement points
- Interview likelihood assessment

### 🧭 Growth Compass Module
- Comprehensive skills gap analysis
- Career path recommendations (including 2 unconventional routes)
- 30/60/90-day actionable roadmap
- Cold email templates for networking
- Personalized learning resources

### 📄 Export & Sharing
- **Professional PDF Reports**: Beautifully formatted analysis reports
- **Notion Templates**: Markdown-ready templates for Notion workspace
- **Email Delivery**: Direct email delivery with EmailJS integration
- **Multiple Formats**: PDF, Markdown, and copyable text formats

## Technology Stack

- **Frontend**: React with TypeScript, Tailwind CSS, ShadCN UI
- **AI Integration**: Groq API for blazing-fast LLM processing
- **Export**: jsPDF for PDF generation, EmailJS for email delivery
- **State Management**: React Context
- **File Processing**: PDF and text resume uploads
- **Styling**: Modern, professional design with responsive layout

## Setup Instructions

1. **Clone and Install**
   ```bash
   npm install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   ```

3. **Configure API Keys**
   
   **Get Groq API Key (Primary - Recommended):**
   - Visit [Groq Console](https://console.groq.com/)
   - Create an account and generate an API key
   - Copy your API key
   
   **Get Gemini API Key (Secondary - Optional but Recommended):**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create an account and generate an API key
   - Copy your API key
   
   **Add your API keys to `.env`:**
     ```
     VITE_GROQ_API_KEY=your_actual_api_key_here
     VITE_GEMINI_API_KEY=your_gemini_api_key_here
     ```
   
   **Important Notes:**
   - At least one API key is required for the app to function
   - Both keys provide redundancy and better reliability
   - Groq offers faster responses, Gemini provides reliable fallback
   - Never commit your `.env` file to version control

4. **Optional: Setup EmailJS for Email Export**
   - Visit [EmailJS](https://www.emailjs.com/)
   - Create an account and set up a service
   - Add your EmailJS credentials to `.env`:
     ```
     VITE_EMAILJS_SERVICE_ID=your_service_id
     VITE_EMAILJS_TEMPLATE_ID=your_template_id
     VITE_EMAILJS_USER_ID=your_user_id
     ```

5. **Start Development Server**
   ```bash
   npm run dev
   ```

## Usage

1. **Upload Resume**: Start by uploading your resume (PDF or TXT format)
2. **Empathy Analysis**: Get insights into your resume's emotional tone and confidence level
3. **Recruiter Feedback**: Receive honest feedback from three different recruiter perspectives
4. **Growth Planning**: Access your personalized 90-day career development roadmap
5. **Export Results**: Download PDF reports, copy Notion templates, or email results

## Project Structure

```
src/
├── components/          # React components
├── contexts/           # React Context for state management
├── services/           # API services and utilities
├── lib/               # Utility functions
└── hooks/             # Custom React hooks
```

## Key Features

- **Real-time AI Processing**: Fast responses powered by Groq
- **Professional Export**: PDF generation with professional formatting
- **Notion Integration**: Ready-to-use Notion templates
- **Email Delivery**: Direct email sharing with EmailJS
- **Professional Design**: Premium UI/UX that feels worth paying for
- **Mobile Responsive**: Optimized for all devices
- **Error Handling**: Robust error boundaries and user feedback
- **Secure**: Client-side processing with secure API integration

## Deployment

Ready for deployment to Netlify:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## License

MIT License - feel free to use for personal or commercial projects.