export interface DemoData {
  empathyAnalysis: {
    confidenceScore: number;
    emotionalTone: string;
    strengths: string[];
    weaknesses: string[];
    suggestions: string[];
  };
  recruiterFeedback: {
    startup: {
      feedback: string;
      score: number;
      improvements: string[];
    };
    faang: {
      feedback: string;
      score: number;
      improvements: string[];
    };
    consulting: {
      feedback: string;
      score: number;
      improvements: string[];
    };
  };
  growthPlan: {
    skillsGap: string[];
    careerPaths: string[];
    roadmap: {
      '30': string[];
      '60': string[];
      '90': string[];
    };
    resources: string[];
  };
}

export const demoData: DemoData = {
  empathyAnalysis: {
    confidenceScore: 7.5,
    emotionalTone: "Confident and professional with room for improvement",
    strengths: [
      "Strong action verbs in achievements",
      "Clear progression in career history",
      "Quantified results demonstrate impact"
    ],
    weaknesses: [
      "Some passive language in descriptions",
      "Could be more specific about leadership impact",
      "Missing emotional connection to company values"
    ],
    suggestions: [
      "Replace 'was responsible for' with 'led' or 'drove'",
      "Add specific metrics for team leadership",
      "Include company mission alignment in summary"
    ]
  },
  recruiterFeedback: {
    startup: {
      feedback: "Shows good technical skills but needs more emphasis on adaptability and growth mindset. The resume demonstrates solid execution but could better highlight innovation and risk-taking.",
      score: 7.2,
      improvements: [
        "Add examples of rapid learning and adaptation",
        "Highlight innovative solutions to problems",
        "Include metrics on time-to-market or efficiency gains"
      ]
    },
    faang: {
      feedback: "Strong technical foundation with good system design thinking. However, needs more emphasis on scale, complexity, and cross-functional collaboration. Good candidate for mid-level positions.",
      score: 8.1,
      improvements: [
        "Quantify system scale and complexity",
        "Add cross-functional project examples",
        "Include performance optimization metrics"
      ]
    },
    consulting: {
      feedback: "Demonstrates good problem-solving skills but needs more strategic thinking examples. The resume shows execution capability but could better highlight strategic impact and client-facing experience.",
      score: 6.8,
      improvements: [
        "Add strategic planning examples",
        "Include stakeholder management experience",
        "Highlight business impact beyond technical metrics"
      ]
    }
  },
  growthPlan: {
    skillsGap: [
      "Advanced system design and architecture",
      "Cross-functional leadership",
      "Strategic thinking and business acumen",
      "Public speaking and presentation skills"
    ],
    careerPaths: [
      "Senior Software Engineer → Tech Lead",
      "Technical Architect → Engineering Manager",
      "Product Manager → Director of Product",
      "Startup CTO → Technical Consultant",
      "AI/ML Specialist → Research Scientist"
    ],
    roadmap: {
      '30': [
        "Complete advanced system design course",
        "Lead a cross-functional project",
        "Present technical findings to stakeholders",
        "Mentor junior developers"
      ],
      '60': [
        "Design and implement a scalable system",
        "Collaborate with product and design teams",
        "Contribute to technical strategy",
        "Build a personal brand through content creation"
      ],
      '90': [
        "Lead a major technical initiative",
        "Develop team leadership skills",
        "Create technical vision and roadmap",
        "Network with industry leaders"
      ]
    },
    resources: [
      "System Design Interview course",
      "Leadership books: 'The Manager's Path'",
      "Technical blogs and podcasts",
      "Industry conferences and meetups",
      "Mentorship programs"
    ]
  }
};

export const getDemoAnalysis = async (resumeText: string): Promise<DemoData> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Return demo data with slight variations based on resume content
  const wordCount = resumeText.split(' ').length;
  const hasLeadership = resumeText.toLowerCase().includes('lead') || resumeText.toLowerCase().includes('manage');
  const hasMetrics = /\d+%|\d+x|\$\d+/.test(resumeText);
  
  let adjustedData = { ...demoData };
  
  if (hasLeadership) {
    adjustedData.empathyAnalysis.confidenceScore = Math.min(9, adjustedData.empathyAnalysis.confidenceScore + 0.5);
  }
  
  if (hasMetrics) {
    adjustedData.recruiterFeedback.faang.score = Math.min(9, adjustedData.recruiterFeedback.faang.score + 0.3);
  }
  
  if (wordCount > 500) {
    adjustedData.empathyAnalysis.suggestions.push("Consider condensing some sections for better readability");
  }
  
  return adjustedData;
};

export const getDemoProgressSteps = () => [
  {
    id: 'upload',
    title: 'Resume Upload',
    description: 'Processing your resume file',
    status: 'completed' as const,
    icon: () => null,
    color: 'text-green-500'
  },
  {
    id: 'empathy',
    title: 'Empathy Analysis',
    description: 'Analyzing emotional tone and confidence',
    status: 'completed' as const,
    icon: () => null,
    color: 'text-green-500'
  },
  {
    id: 'feedback',
    title: 'Recruiter Feedback',
    description: 'Generating feedback from different perspectives',
    status: 'completed' as const,
    icon: () => null,
    color: 'text-green-500'
  },
  {
    id: 'growth',
    title: 'Growth Planning',
    description: 'Creating personalized career roadmap',
    status: 'completed' as const,
    icon: () => null,
    color: 'text-green-500'
  }
]; 