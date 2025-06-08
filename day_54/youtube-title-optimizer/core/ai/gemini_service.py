import os
import time
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable

# Local imports
from core.ai.prompt_templates import TITLE_OPTIMIZATION_PROMPT
from core.analytics.metrics import calculate_seo_score

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google's Gemini AI models"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini service with API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Available models
        self.models = {
            "gemini-pro": "gemini-1.5-pro",
            "gemini-flash": "gemini-1.5-flash"
        }
        
        # Cache for rate limiting
        self._last_request_time = 0
        self._min_request_interval = 1.0  # seconds
    
    def _rate_limit(self) -> None:
        """Implement rate limiting to avoid API quota issues"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        
        if time_since_last_request < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ResourceExhausted, ServiceUnavailable)),
        reraise=True
    )
    async def optimize_title(
        self,
        original_title: str,
        description: str,
        category: str = "General",
        target_emotion: str = "Curiosity",
        content_type: str = "General",
        model_name: str = "gemini-pro",
        optimization_strength: int = 7,
        advanced_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize a YouTube title using Gemini AI
        
        Args:
            original_title: The original video title
            description: The video description
            category: Content category (e.g., Tech, Gaming)
            target_emotion: Target emotion to evoke (e.g., Curiosity, Urgency)
            content_type: Type of content (e.g., Tutorial, Vlog)
            model_name: Gemini model to use
            optimization_strength: How aggressive the optimization should be (1-10)
            advanced_analysis: Whether to include advanced analysis
            
        Returns:
            Dictionary containing optimization results
        """
        # Apply rate limiting
        self._rate_limit()
        
        # Select the appropriate model
        model_id = self.models.get(model_name, "gemini-1.5-pro")
        model = genai.GenerativeModel(model_id)
        
        # Format the prompt with user inputs
        prompt = TITLE_OPTIMIZATION_PROMPT.format(
            original_title=original_title,
            description=description,
            category=category,
            target_emotion=target_emotion,
            content_type=content_type,
            optimization_strength=optimization_strength,
            advanced_analysis=str(advanced_analysis).lower()
        )
        
        try:
            # Generate content with Gemini
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            # Extract and parse the JSON response
            result_text = response.text
            json_match = self._extract_json(result_text)
            
            if not json_match:
                logger.error(f"Failed to extract JSON from response: {result_text}")
                raise ValueError("Invalid response format from Gemini API")
            
            # Parse the JSON response
            result = json.loads(json_match)
            
            # Validate the response structure
            self._validate_response(result)
            
            # Calculate SEO score if not provided
            if "seo_score" not in result:
                result["seo_score"] = calculate_seo_score(
                    result["improved_title"], 
                    original_title,
                    category
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    def _extract_json(self, text: str) -> Optional[str]:
        """Extract JSON from the response text"""
        import re
        json_pattern = r'\{[\s\S]*\}'
        match = re.search(json_pattern, text)
        return match.group(0) if match else None
    
    def _validate_response(self, result: Dict[str, Any]) -> None:
        """Validate that the response has the required fields"""
        required_fields = ["improved_title", "alternates", "reason"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field in response: {field}")
        
        # Ensure alternates is a list with at least one item
        if not isinstance(result["alternates"], list) or len(result["alternates"]) == 0:
            raise ValueError("Response must include at least one alternate title")

    def get_model_info(self, model_name: str = "gemini-pro") -> Dict[str, Any]:
        """Get information about a specific model"""
        model_id = self.models.get(model_name, "gemini-1.5-pro")
        
        try:
            model_info = genai.get_model(model_id)
            return {
                "name": model_info.name,
                "display_name": model_info.display_name,
                "description": model_info.description,
                "input_token_limit": model_info.input_token_limit,
                "output_token_limit": model_info.output_token_limit,
                "supported_generation_methods": model_info.supported_generation_methods,
            }
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return {"error": str(e)}
