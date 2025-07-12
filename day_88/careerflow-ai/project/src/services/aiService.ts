interface GroqResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

interface GeminiResponse {
  candidates: Array<{
    content: {
      parts: Array<{
        text: string;
      }>;
    };
  }>;
}

interface APIConfig {
  name: string;
  baseURL: string;
  apiKey: string;
  model: string;
  available: boolean;
  lastError?: string;
  errorCount: number;
  lastSuccess?: Date;
  disabledUntil?: number;
}

class AIService {
  private apis: APIConfig[] = [
    {
      name: 'groq',
      baseURL: 'https://api.groq.com/openai/v1/chat/completions',
      apiKey: import.meta.env.VITE_GROQ_API_KEY || '',
      model: 'llama-3.3-70b-versatile',
      available: true,
      errorCount: 0,
    },
    {
      name: 'gemini',
      baseURL: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent',
      apiKey: import.meta.env.VITE_GEMINI_API_KEY || '',
      model: 'gemini-2.0-flash-exp',
      available: true,
      errorCount: 0,
    },
  ];

  private timeout = parseInt(import.meta.env.VITE_API_TIMEOUT || '30000');
  private maxRetries = parseInt(import.meta.env.VITE_RETRY_ATTEMPTS || '3');
  private requestQueue: Array<() => Promise<any>> = [];
  private isProcessingQueue = false;

  constructor() {
    // Filter out APIs without keys and log configuration status
    this.apis = this.apis.filter(api => {
      if (!api.apiKey) {
        console.warn(`${api.name} API key not configured`);
        return false;
      }
      console.log(`${api.name} API configured successfully`);
      return true;
    });
    
    if (this.apis.length === 0) {
      console.error('❌ No API keys configured. Please check your environment variables:');
      console.error('- VITE_GROQ_API_KEY');
      console.error('- VITE_GEMINI_API_KEY');
      console.error('At least one API key must be provided.');
    }
  }

  private async makeGroqRequest(prompt: string, systemPrompt: string, config: APIConfig): Promise<string> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(config.baseURL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${config.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: config.model,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: prompt },
          ],
          temperature: 0.1,
          max_tokens: 2048,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = `API request failed: ${response.status} ${response.statusText}`;
        
        try {
          const errorData = JSON.parse(errorText);
          if (errorData.error?.message) {
            errorMessage = errorData.error.message;
          }
        } catch (parseError) {
          // Use default error message if JSON parsing fails
        }
        
        throw new Error(errorMessage);
      }

      const data: GroqResponse = await response.json();
      
      if (!data.choices?.[0]?.message?.content) {
        throw new Error('Invalid response format from Groq API');
      }

      return data.choices[0].message.content;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private async makeGeminiRequest(prompt: string, systemPrompt: string, config: APIConfig): Promise<string> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${config.baseURL}?key=${config.apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `${systemPrompt}\n\nUser Request: ${prompt}`
            }]
          }],
          generationConfig: {
            temperature: 0.1,
            maxOutputTokens: 2048,
          },
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = `API request failed: ${response.status} ${response.statusText}`;
        
        try {
          const errorData = JSON.parse(errorText);
          if (errorData.error?.message) {
            errorMessage = errorData.error.message;
          }
        } catch (parseError) {
          // Use default error message if JSON parsing fails
        }
        
        throw new Error(errorMessage);
      }

      const data: GeminiResponse = await response.json();
      
      if (!data.candidates?.[0]?.content?.parts?.[0]?.text) {
        throw new Error('Invalid response format from Gemini API');
      }

      return data.candidates[0].content.parts[0].text;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private async makeRequestWithAPI(prompt: string, systemPrompt: string, config: APIConfig): Promise<string> {
    try {
      let response: string;
      
      if (config.name === 'groq') {
        response = await this.makeGroqRequest(prompt, systemPrompt, config);
      } else if (config.name === 'gemini') {
        response = await this.makeGeminiRequest(prompt, systemPrompt, config);
      } else {
        throw new Error(`Unknown API: ${config.name}`);
      }

      // Mark API as successful
      config.available = true;
      config.errorCount = 0;
      config.lastSuccess = new Date();
      config.lastError = undefined;

      return response;
    } catch (error) {
      // Mark API as having issues
      config.errorCount++;
      config.lastError = error instanceof Error ? error.message : 'Unknown error';
      
      // Check for quota/billing errors and disable API immediately
      const errorMessage = error instanceof Error ? error.message.toLowerCase() : '';
      const isQuotaError = errorMessage.includes('quota') || 
                          errorMessage.includes('billing') || 
                          errorMessage.includes('exceeded') ||
                          errorMessage.includes('limit');
      
      const isRateLimit = errorMessage.includes('rate limit') || 
                         errorMessage.includes('429') ||
                         errorMessage.includes('too many requests');
      
      // Temporarily disable API based on error type
      if (config.errorCount >= 2 || isQuotaError || isRateLimit) {
        config.available = false;
        // Re-enable after 2 minutes for quota errors, 1 minute for rate limits, 30 seconds for other errors
        let retryDelay = 30 * 1000; // 30 seconds default
        if (isQuotaError) {
          retryDelay = 2 * 60 * 1000; // 2 minutes for quota
        } else if (isRateLimit) {
          retryDelay = 1 * 60 * 1000; // 1 minute for rate limits
        }
        
        config.disabledUntil = Date.now() + retryDelay;
      }

      throw error;
    }
  }

  private isRateLimitError(error: Error): boolean {
    const message = error.message.toLowerCase();
    return message.includes('rate limit') || 
           message.includes('429') || 
           message.includes('quota') ||
           message.includes('too many requests');
  }

  private async makeRequest(prompt: string, systemPrompt: string): Promise<string> {
    const availableAPIs = this.apis.filter(api => api.available);
    
    if (availableAPIs.length === 0) {
      const configuredAPIs = this.apis.filter(api => api.apiKey);
      if (configuredAPIs.length === 0) {
        throw new Error('No API keys configured. Please add VITE_GROQ_API_KEY or VITE_GEMINI_API_KEY to your environment variables.');
      } else {
        // Check if any APIs can be re-enabled (reset error counts for APIs that have been disabled for a while)
        const now = new Date();
        configuredAPIs.forEach(api => {
          if (!api.available && api.disabledUntil) {
            if (now.getTime() > api.disabledUntil) {
              api.available = true;
              api.errorCount = 0;
              api.lastError = undefined;
              api.disabledUntil = undefined;
            }
          }
        });
        
        // Check again for available APIs
        const retryAvailableAPIs = this.apis.filter(api => api.available);
        if (retryAvailableAPIs.length === 0) {
          throw new Error('All AI services are currently unavailable due to quota limits or errors. Please check your API billing status and try again in a few minutes.');
        }
        
        // Continue with retry logic
        return this.makeRequest(prompt, systemPrompt);
      }
    }

    let lastError: Error | null = null;

    // Try each available API
    for (const api of availableAPIs) {
      try {
        console.log(`Attempting request with ${api.name} API...`);
        const response = await this.makeRequestWithAPI(prompt, systemPrompt, api);
        console.log(`✅ Success with ${api.name} API`);
        return response;
      } catch (error) {
        console.warn(`❌ ${api.name} API failed:`, error instanceof Error ? error.message : error);
        lastError = error instanceof Error ? error : new Error('Unknown error');
        
        // If it's a rate limit error, try the next API immediately
        if (this.isRateLimitError(lastError)) {
          console.log(`Rate limit detected for ${api.name}, trying next API...`);
          continue;
        }
        
        // For other errors, still try the next API but with a small delay
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    // If all APIs failed, provide a more helpful error message
    const errorMessage = lastError?.message || 'Unknown error';
    if (errorMessage.toLowerCase().includes('quota') || errorMessage.toLowerCase().includes('billing')) {
      throw new Error('API quota exceeded. Please check your API billing and usage limits, or try again later.');
    } else if (this.isRateLimitError(lastError!)) {
      throw new Error('Rate limit exceeded on all APIs. Please wait a few minutes before trying again.');
    } else {
      throw new Error(`All APIs failed. Last error: ${errorMessage}`);
    }
  }

  private truncateText(text: string, maxChars: number = 8000): string {
    if (text.length <= maxChars) {
      return text;
    }
    
    return text.substring(0, maxChars) + '\n\n[Note: Resume text was truncated to fit within processing limits]';
  }

  private removeComments(jsonString: string): string {
    let cleaned = jsonString.replace(/\/\/.*$/gm, '');
    cleaned = cleaned.replace(/\/\*[\s\S]*?\*\//g, '');
    cleaned = cleaned.replace(/,(\s*[}\]])/g, '$1');
    return cleaned;
  }

  private extractJSON(response: string): string | null {
    const trimmedResponse = response.trim();
    
    const cleanJSONString = (jsonStr: string): string => {
      let cleaned = jsonStr;
      cleaned = cleaned.replace(/("(?:[^"\\]|\\.)*?")/g, (match) => {
        return match.replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t');
      });
      return cleaned;
    };
    
    const cleanedResponse = cleanJSONString(this.removeComments(trimmedResponse));
    if (cleanedResponse.trim().startsWith('{') && cleanedResponse.trim().endsWith('}')) {
      return cleanedResponse;
    }

    const jsonCodeBlockRegex = /```(?:json)?\s*(\{[\s\S]*?\})\s*```/i;
    const codeBlockMatch = trimmedResponse.match(jsonCodeBlockRegex);
    
    if (codeBlockMatch && codeBlockMatch[1]) {
      const extracted = cleanJSONString(this.removeComments(codeBlockMatch[1].trim()));
      return extracted;
    }
    
    const firstBrace = trimmedResponse.indexOf('{');
    const lastBrace = trimmedResponse.lastIndexOf('}');
    
    if (firstBrace === -1 || lastBrace === -1 || firstBrace >= lastBrace) {
      return null;
    }
    
    const extracted = cleanJSONString(this.removeComments(trimmedResponse.substring(firstBrace, lastBrace + 1)));
    return extracted;
  }

  // Public method to get API status
  getAPIStatus() {
    return this.apis.map(api => ({
      name: api.name,
      available: api.available,
      errorCount: api.errorCount,
      lastError: api.lastError,
      lastSuccess: api.lastSuccess,
      configured: !!api.apiKey,
    }));
  }

  async analyzeEmpathy(resumeText: string) {
    const systemPrompt = `You are an empathetic career coach analyzing resume tone and emotional positioning. 

CRITICAL: Your response must be ONLY a single valid JSON object. Do not include any text before or after the JSON. Do not use markdown code blocks. Start your response with '{' and end with '}'. Ensure all strings are properly escaped and there are no trailing commas.

Analyze the resume and provide a response in this exact JSON structure:
{
  "confidenceScore": [number between 1-10],
  "toneAnalysis": "[detailed tone analysis in 2-3 sentences]",
  "strongPoints": ["[specific strong language example 1]", "[specific strong language example 2]", "[specific strong language example 3]"],
  "weakPoints": ["[specific weak language example 1]", "[specific weak language example 2]", "[specific weak language example 3]"],
  "improvements": ["[specific improvement suggestion 1]", "[specific improvement suggestion 2]", "[specific improvement suggestion 3]"]
}`;

    const truncatedResumeText = this.truncateText(resumeText);
    const prompt = `Analyze this resume for emotional tone, confidence level, and language strength:\n\n${truncatedResumeText}`;
    
    try {
      const response = await this.makeRequest(prompt, systemPrompt);
      
      const jsonString = this.extractJSON(response);
      
      if (!jsonString) {
        throw new Error('AI response did not contain a valid JSON structure.');
      }
      
      return JSON.parse(jsonString);
    } catch (error) {
      console.error('Empathy analysis error:', error);
      throw new Error('Failed to analyze resume tone. Please try again.');
    }
  }

  async getRecruiterFeedback(resumeText: string) {
    const systemPrompt = `You are three different types of recruiters providing honest feedback. 

CRITICAL: Your response must be ONLY a single valid JSON object. Do not include any text before or after the JSON. Do not use markdown code blocks. Start your response with '{' and end with '}'. Ensure all strings are properly escaped and there are no trailing commas.

Respond in this exact JSON format:
{
  "startup": {
    "assessment": "[startup recruiter's detailed perspective in 2-3 sentences]",
    "likelihood": [number 1-10],
    "feedback": ["[specific actionable point 1]", "[specific actionable point 2]", "[specific actionable point 3]"]
  },
  "faang": {
    "assessment": "[FAANG recruiter's detailed perspective in 2-3 sentences]", 
    "likelihood": [number 1-10],
    "feedback": ["[specific actionable point 1]", "[specific actionable point 2]", "[specific actionable point 3]"]
  },
  "consulting": {
    "assessment": "[consulting recruiter's detailed perspective in 2-3 sentences]",
    "likelihood": [number 1-10],
    "feedback": ["[specific actionable point 1]", "[specific actionable point 2]", "[specific actionable point 3]"]
  }
}`;

    const truncatedResumeText = this.truncateText(resumeText);
    const prompt = `Provide recruiter feedback for this resume from three perspectives - startup, FAANG, and consulting:\n\n${truncatedResumeText}`;
    
    try {
      const response = await this.makeRequest(prompt, systemPrompt);
      
      const jsonString = this.extractJSON(response);
      
      if (!jsonString) {
        throw new Error('AI response did not contain a valid JSON structure.');
      }
      
      return JSON.parse(jsonString);
    } catch (error) {
      console.error('Recruiter feedback error:', error);
      throw new Error('Failed to get recruiter feedback. Please try again.');
    }
  }

  async createGrowthPlan(resumeText: string) {
    const systemPrompt = `You are a strategic career advisor creating a comprehensive growth plan.

CRITICAL: Your response must be ONLY a single valid JSON object. Do not include any text before or after the JSON. Do not use markdown code blocks. Start your response with '{' and end with '}'. Ensure all strings are properly escaped and there are no trailing commas.

Respond in this exact JSON format:
{
  "skillsGap": ["[specific skill 1]", "[specific skill 2]", "[specific skill 3]", "[specific skill 4]"],
  "careerPaths": {
    "conventional": "[traditional next step description]",
    "unconventional": ["[unique alternative path 1]", "[unique alternative path 2]"]
  },
  "roadmap": {
    "thirtyDays": ["[specific 30-day action 1]", "[specific 30-day action 2]", "[specific 30-day action 3]"],
    "sixtyDays": ["[specific 60-day action 1]", "[specific 60-day action 2]", "[specific 60-day action 3]"],
    "ninetyDays": ["[specific 90-day action 1]", "[specific 90-day action 2]", "[specific 90-day action 3]"]
  },
  "coldEmailTemplate": "[personalized networking email template with placeholders]",
  "resources": ["[specific learning resource 1]", "[specific learning resource 2]", "[specific learning resource 3]", "[specific learning resource 4]"]
}`;

    const truncatedResumeText = this.truncateText(resumeText);
    const prompt = `Create a comprehensive career growth plan based on this resume:\n\n${truncatedResumeText}`;
    
    try {
      const response = await this.makeRequest(prompt, systemPrompt);
      
      const jsonString = this.extractJSON(response);
      
      if (!jsonString) {
        throw new Error('AI response did not contain a valid JSON structure.');
      }
      
      return JSON.parse(jsonString);
    } catch (error) {
      console.error('Growth plan error:', error);
      throw new Error('Failed to create growth plan. Please try again.');
    }
  }
}

export const aiService = new AIService();