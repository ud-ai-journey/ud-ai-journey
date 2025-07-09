"""
Guru Sahayam Configuration
Google Cloud Integration and System Settings
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import json

@dataclass
class GoogleCloudConfig:
    """Google Cloud Platform configuration"""
    project_id: str = "guru-sahayam-ai"
    region: str = "us-central1"
    vertex_ai_location: str = "us-central1"
    
    # AI Model configurations
    gemini_model: str = "gemini-2.0-flash-exp"
    text_model: str = "text-bison@001"
    
    # Translation API
    translation_service: str = "translate.googleapis.com"
    
    # Storage
    bucket_name: str = "guru-sahayam-content"
    
    # Authentication
    service_account_key: str = ""

@dataclass
class AgentConfig:
    """Agent-specific configurations"""
    content_creation: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.8,
        "max_tokens": 2048,
        "top_p": 0.9
    })
    differentiation: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.6,
        "max_tokens": 1024,
        "top_p": 0.8
    })
    localization: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.7,
        "max_tokens": 1536,
        "top_p": 0.85
    })
    assessment: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.6,
        "max_tokens": 1024,
        "top_p": 0.8
    })
    teaching_support: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.85
    })

@dataclass
class UIConfig:
    """User interface configuration"""
    theme: str = "light"
    primary_color: str = "#667eea"
    secondary_color: str = "#764ba2"
    accent_color: str = "#28a745"
    
    # Dashboard settings
    dashboard_refresh_rate: int = 30  # seconds
    max_recent_activities: int = 10
    
    # Mobile settings
    mobile_optimized: bool = True
    thumb_zone_enabled: bool = True

@dataclass
class LocalizationConfig:
    """Localization and cultural settings"""
    supported_languages: List[str] = field(default_factory=lambda: [
        "English", "Hindi", "Marathi", "Telugu", "Tamil", 
        "Bengali", "Gujarati", "Kannada", "Malayalam", 
        "Punjabi", "Odia", "Assamese"
    ])
    default_language: str = "English"
    cultural_contexts: List[str] = field(default_factory=lambda: [
        "Rural farming community",
        "Urban middle class",
        "Tribal community",
        "Coastal fishing village",
        "Mountain region",
        "Desert region"
    ])

@dataclass
class SecurityConfig:
    """Security and privacy settings"""
    data_encryption: bool = True
    user_authentication: bool = True
    content_filtering: bool = True
    privacy_compliance: bool = True
    
    # Content safety settings
    safety_filters: Dict[str, Any] = field(default_factory=lambda: {
        "harassment": "BLOCK_MEDIUM_AND_ABOVE",
        "hate_speech": "BLOCK_MEDIUM_AND_ABOVE",
        "sexually_explicit": "BLOCK_MEDIUM_AND_ABOVE",
        "dangerous_content": "BLOCK_MEDIUM_AND_ABOVE"
    })

class GuruSahayamConfig:
    """Main configuration class for Guru Sahayam"""
    
    def __init__(self):
        self.google_cloud = GoogleCloudConfig()
        self.agents = AgentConfig()
        self.ui = UIConfig()
        self.localization = LocalizationConfig()
        self.security = SecurityConfig()
        
        # Load environment variables
        self._load_env_vars()
        
    def _load_env_vars(self):
        """Load configuration from environment variables"""
        # Google Cloud settings
        if os.getenv("GOOGLE_CLOUD_PROJECT"):
            self.google_cloud.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        if os.getenv("GOOGLE_CLOUD_REGION"):
            self.google_cloud.region = os.getenv("GOOGLE_CLOUD_REGION", "")
        if os.getenv("GOOGLE_CLOUD_LOCATION"):
            self.google_cloud.vertex_ai_location = os.getenv("GOOGLE_CLOUD_LOCATION", "")
            
        # Service account key
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.google_cloud.service_account_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get configuration for specific agent"""
        agent_configs = {
            "Content Creation Agent": self.agents.content_creation,
            "Differentiation Agent": self.agents.differentiation,
            "Localization Agent": self.agents.localization,
            "Assessment Agent": self.agents.assessment,
            "Teaching Support Agent": self.agents.teaching_support
        }
        return agent_configs.get(agent_name, {})
    
    def get_language_config(self, language: str) -> Dict[str, Any]:
        """Get configuration for specific language"""
        return {
            "supported": language in self.localization.supported_languages,
            "default": language == self.localization.default_language,
            "cultural_contexts": self.localization.cultural_contexts
        }
    
    def get_safety_config(self) -> Dict[str, Any]:
        """Get content safety configuration"""
        return self.security.safety_filters
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "google_cloud": {
                "project_id": self.google_cloud.project_id,
                "region": self.google_cloud.region,
                "vertex_ai_location": self.google_cloud.vertex_ai_location,
                "gemini_model": self.google_cloud.gemini_model
            },
            "agents": {
                "content_creation": self.agents.content_creation,
                "differentiation": self.agents.differentiation,
                "localization": self.agents.localization,
                "assessment": self.agents.assessment,
                "teaching_support": self.agents.teaching_support
            },
            "ui": {
                "theme": self.ui.theme,
                "primary_color": self.ui.primary_color,
                "mobile_optimized": self.ui.mobile_optimized
            },
            "localization": {
                "supported_languages": self.localization.supported_languages,
                "default_language": self.localization.default_language,
                "cultural_contexts": self.localization.cultural_contexts
            },
            "security": {
                "data_encryption": self.security.data_encryption,
                "content_filtering": self.security.content_filtering,
                "safety_filters": self.security.safety_filters
            }
        }
    
    def save_config(self, filepath: str):
        """Save configuration to file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_config(cls, filepath: str) -> 'GuruSahayamConfig':
        """Load configuration from file"""
        config = cls()
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        # Update configuration from file
        if 'google_cloud' in data:
            for key, value in data['google_cloud'].items():
                setattr(config.google_cloud, key, value)
        
        if 'agents' in data:
            for key, value in data['agents'].items():
                setattr(config.agents, key, value)
        
        return config

# Global configuration instance
config = GuruSahayamConfig()

def get_config() -> GuruSahayamConfig:
    """Get the global configuration instance"""
    return config 