# Title optimization prompt template
TITLE_OPTIMIZATION_PROMPT = """
You are a world-class YouTube optimization expert with deep knowledge of viral content, SEO, and viewer psychology.

TASK: Transform this YouTube title into a high-performing, clickable masterpiece.

ORIGINAL TITLE: "{original_title}"
DESCRIPTION: "{description}"
CATEGORY: {category}
TARGET EMOTION: {target_emotion}
CONTENT TYPE: {content_type}
OPTIMIZATION STRENGTH: {optimization_strength}/10

REQUIREMENTS:
- Keep titles under 60 characters for mobile optimization
- Use power words and emotional triggers
- Include numbers, brackets, or symbols when appropriate
- Optimize for {target_emotion} emotion
- Make it {category} category appropriate
- Ensure it's {content_type} content type suitable
- Apply optimization strength of {optimization_strength}/10 (higher = more aggressive optimization)

RESPOND IN THIS EXACT JSON FORMAT:
{{
  "improved_title": "Your best optimized title here",
  "alternates": [
    "Alternative title 1",
    "Alternative title 2", 
    "Alternative title 3"
  ],
  "reason": "Detailed explanation of why this title works better, including psychological triggers used",
  "seo_score": 85,
  "emotional_hooks": ["Hook1", "Hook2", "Hook3"],
  "metrics": {{
    "predicted_ctr": 8.7,
    "keyword_density": 4.2,
    "readability_score": 82,
    "emotional_impact": 76,
    "trend_alignment": 92
  }},
  "keyword_analysis": {{
    "primary_keywords": ["keyword1", "keyword2", "keyword3"],
    "secondary_keywords": ["keyword4", "keyword5", "keyword6"],
    "missing_opportunities": ["keyword7", "keyword8", "keyword9"]
  }},
  "competitor_analysis": {{
    "similar_videos": [
      {{"title": "Competitor Title 1", "views": "1.2M", "ctr": "6.8%"}},
      {{"title": "Competitor Title 2", "views": "892K", "ctr": "7.2%"}},
      {{"title": "Competitor Title 3", "views": "504K", "ctr": "5.9%"}}
    ],
    "trending_patterns": ["pattern1", "pattern2", "pattern3"]
  }},
  "thumbnail_suggestions": [
    "Thumbnail suggestion 1",
    "Thumbnail suggestion 2",
    "Thumbnail suggestion 3"
  ],
  "a_b_test_recommendation": {{
    "test_a": "A/B test title A",
    "test_b": "A/B test title B",
    "estimated_difference": "12% CTR improvement potential"
  }}
}}

Focus on creating titles that would genuinely perform well on YouTube's algorithm while maintaining authenticity.
Include advanced analysis: {advanced_analysis}
"""

# Batch optimization prompt template
BATCH_OPTIMIZATION_PROMPT = """
You are a world-class YouTube optimization expert with deep knowledge of viral content, SEO, and viewer psychology.

TASK: Transform these YouTube titles into high-performing, clickable masterpieces.

TITLES:
{titles}

CATEGORY: {category}
TARGET EMOTION: {target_emotion}
CONTENT TYPE: {content_type}

REQUIREMENTS:
- Keep titles under 60 characters for mobile optimization
- Use power words and emotional triggers
- Include numbers, brackets, or symbols when appropriate
- Optimize for {target_emotion} emotion
- Make them {category} category appropriate
- Ensure they're {content_type} content type suitable

RESPOND IN THIS EXACT JSON FORMAT:
{{
  "optimized_titles": [
    {{
      "original": "Original title 1",
      "optimized": "Optimized title 1",
      "seo_score": 85
    }},
    {{
      "original": "Original title 2",
      "optimized": "Optimized title 2",
      "seo_score": 78
    }}
    // ... and so on for all titles
  ]
}}

Focus on creating titles that would genuinely perform well on YouTube's algorithm while maintaining authenticity.
"""

# Competitor analysis prompt template
COMPETITOR_ANALYSIS_PROMPT = """
You are a YouTube analytics expert specializing in competitive analysis and trend identification.

TASK: Analyze these competitor video titles and provide strategic insights.

MY TITLE: "{my_title}"
MY NICHE: {my_niche}

COMPETITOR TITLES:
{competitor_titles}

RESPOND IN THIS EXACT JSON FORMAT:
{{
  "trend_analysis": {{
    "common_patterns": ["pattern1", "pattern2", "pattern3"],
    "emotional_triggers": ["trigger1", "trigger2", "trigger3"],
    "keyword_frequency": {{"keyword1": 5, "keyword2": 3, "keyword3": 2}}
  }},
  "gap_analysis": {{
    "underutilized_hooks": ["hook1", "hook2", "hook3"],
    "missing_keywords": ["keyword1", "keyword2", "keyword3"],
    "differentiation_opportunities": ["opportunity1", "opportunity2", "opportunity3"]
  }},
  "recommendations": [
    "Strategic recommendation 1",
    "Strategic recommendation 2",
    "Strategic recommendation 3"
  ],
  "title_improvement": "Suggested improved title based on competitive analysis"
}}

Provide actionable insights that can be used to outperform competitors in the same niche.
"""

# Title A/B testing prompt template
AB_TESTING_PROMPT = """
You are a YouTube A/B testing expert who specializes in creating variant titles for maximum performance.

TASK: Create A/B test variants for this YouTube title.

ORIGINAL TITLE: "{original_title}"
DESCRIPTION: "{description}"
CATEGORY: {category}
TARGET AUDIENCE: {target_audience}

RESPOND IN THIS EXACT JSON FORMAT:
{{
  "variant_a": {{
    "title": "Variant A title",
    "hypothesis": "Why this variant might perform better",
    "target_metric": "CTR"
  }},
  "variant_b": {{
    "title": "Variant B title",
    "hypothesis": "Why this variant might perform better",
    "target_metric": "Watch time"
  }},
  "variant_c": {{
    "title": "Variant C title",
    "hypothesis": "Why this variant might perform better",
    "target_metric": "Subscriber conversion"
  }},
  "testing_recommendation": "Recommendation for how to run the test effectively",
  "success_metrics": ["Primary metric", "Secondary metric", "Tertiary metric"]
}}

Create variants that test different hypotheses about what drives engagement for this type of content.
"""
