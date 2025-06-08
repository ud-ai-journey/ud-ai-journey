from typing import Dict, Any, Optional
import os
import logging

# Local imports
from core.ai.gemini_service import GeminiService
from core.ai.openai_service import OpenAIService
from core.ai.anthropic_service import AnthropicService

# Configure logging
logger = logging.getLogger(__name__)

class ModelFactory:
    """Factory for creating AI model service instances"""
    
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None
    ):
        """Initialize the model factory with API keys"""
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        
        # Initialize services lazily
        self._services = {}
    
    def get_service(self, model_name: str) -> Any:
        """
        Get an AI service instance based on the model name
        
        Args:
            model_name: Name of the model/service (gemini, openai, anthropic, ensemble)
            
        Returns:
            An instance of the appropriate AI service
        """
        model_name = model_name.lower()
        
        # Check if service is already initialized
        if model_name in self._services:
            return self._services[model_name]
        
        # Initialize the appropriate service
        if model_name in ["gemini", "gemini-pro", "gemini-flash"]:
            if not self.gemini_api_key:
                raise ValueError("Gemini API key is required for Gemini service")
            
            service = GeminiService(api_key=self.gemini_api_key)
            self._services[model_name] = service
            return service
            
        elif model_name in ["openai", "gpt", "gpt-4", "gpt-4o"]:
            if not self.openai_api_key:
                raise ValueError("OpenAI API key is required for OpenAI service")
            
            service = OpenAIService(api_key=self.openai_api_key)
            self._services[model_name] = service
            return service
            
        elif model_name in ["anthropic", "claude", "claude-3"]:
            if not self.anthropic_api_key:
                raise ValueError("Anthropic API key is required for Claude service")
            
            service = AnthropicService(api_key=self.anthropic_api_key)
            self._services[model_name] = service
            return service
            
        elif model_name == "ensemble":
            # Ensemble requires all services to be available
            services = []
            
            if self.gemini_api_key:
                services.append(self.get_service("gemini"))
            
            if self.openai_api_key:
                services.append(self.get_service("openai"))
            
            if self.anthropic_api_key:
                services.append(self.get_service("anthropic"))
            
            if not services:
                raise ValueError("At least one AI service is required for ensemble")
            
            # In a real implementation, this would be an EnsembleService class
            # For now, just return the first available service
            return services[0]
        
        else:
            # Default to Gemini if available
            if self.gemini_api_key:
                return self.get_service("gemini")
            
            # Otherwise, use any available service
            if self.openai_api_key:
                return self.get_service("openai")
            
            if self.anthropic_api_key:
                return self.get_service("anthropic")
            
            raise ValueError(f"Unknown model name: {model_name} and no default services available")
    
    def available_models(self) -> Dict[str, bool]:
        """Get a dictionary of available models"""
        return {
            "gemini": bool(self.gemini_api_key),
            "openai": bool(self.openai_api_key),
            "anthropic": bool(self.anthropic_api_key),
            "ensemble": bool(self.gemini_api_key or self.openai_api_key or self.anthropic_api_key)
        }

# Dependency for FastAPI
def get_model_factory() -> ModelFactory:
    """Dependency to get the model factory instance"""
    return ModelFactory(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
