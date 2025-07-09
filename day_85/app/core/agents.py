"""
Guru Sahayam - Multi-Agent AI System
Core Agent Architecture using Google Cloud ADK
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import google.cloud.aiplatform as aiplatform
from google.cloud import translate_v2 as translate
from google.cloud import storage
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Configuration for each AI agent"""
    name: str
    description: str
    capabilities: List[str]
    model: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7

class BaseAgent:
    """Base class for all AI agents in Guru Sahayam"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.capabilities = config.capabilities
        self.model = config.model
        self.temperature = config.temperature
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return response"""
        raise NotImplementedError
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return True
        
    def format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Format response for consistency"""
        return {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "data": response
        }

class MasterTeachingAgent(BaseAgent):
    """Orchestrates all specialized agents for comprehensive teaching support"""
    
    def __init__(self):
        config = AgentConfig(
            name="Master Teaching Agent",
            description="Coordinates all specialized teaching agents",
            capabilities=["orchestration", "context_management", "workflow_coordination"],
            temperature=0.5
        )
        super().__init__(config)
        self.sub_agents = {}
        
    def register_agent(self, agent: BaseAgent):
        """Register a sub-agent"""
        self.sub_agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate the workflow across all agents"""
        try:
            # Validate input
            if not self.validate_input(input_data):
                return {"error": "Invalid input data"}
                
            # Extract task type and route to appropriate agents
            task_type = input_data.get("task_type", "general")
            
            if task_type == "lesson_creation":
                return self._handle_lesson_creation(input_data)
            elif task_type == "content_differentiation":
                return self._handle_content_differentiation(input_data)
            elif task_type == "assessment_generation":
                return self._handle_assessment_generation(input_data)
            elif task_type == "localization":
                return self._handle_localization(input_data)
            else:
                return self._handle_general_support(input_data)
                
        except Exception as e:
            logger.error(f"Error in Master Teaching Agent: {str(e)}")
            return {"error": f"Processing error: {str(e)}"}
    
    def _handle_lesson_creation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle lesson plan creation workflow"""
        content_agent = self.sub_agents.get("Content Creation Agent")
        diff_agent = self.sub_agents.get("Differentiation Agent")
        local_agent = self.sub_agents.get("Localization Agent")
        
        # Step 1: Create base content
        content_result = content_agent.process(input_data) if content_agent else {}
        
        # Step 2: Differentiate for multiple grades
        if content_result and not content_result.get("error"):
            diff_input = {**input_data, "base_content": content_result.get("data", {})}
            diff_result = diff_agent.process(diff_input) if diff_agent else {}
            
            # Step 3: Localize content
            if diff_result and not diff_result.get("error"):
                local_input = {**input_data, "differentiated_content": diff_result.get("data", {})}
                local_result = local_agent.process(local_input) if local_agent else {}
                
                return self.format_response({
                    "lesson_plan": local_result.get("data", {}),
                    "metadata": {
                        "grades": input_data.get("grades", []),
                        "languages": input_data.get("languages", []),
                        "cultural_context": input_data.get("cultural_context", "")
                    }
                })
        
        return {"error": "Failed to create lesson plan"}

class ContentCreationAgent(BaseAgent):
    """Generates culturally relevant educational content"""
    
    def __init__(self):
        config = AgentConfig(
            name="Content Creation Agent",
            description="Creates hyper-local, culturally relevant educational content",
            capabilities=["content_generation", "cultural_context", "curriculum_alignment"],
            temperature=0.8
        )
        super().__init__(config)
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate educational content with cultural context"""
        try:
            subject = input_data.get("subject", "")
            topic = input_data.get("topic", "")
            grade_levels = input_data.get("grades", [])
            cultural_context = input_data.get("cultural_context", "")
            
            # Create culturally relevant content
            content = self._generate_content(subject, topic, grade_levels, cultural_context)
            
            return self.format_response({
                "content": content,
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grades": grade_levels,
                    "cultural_context": cultural_context
                }
            })
            
        except Exception as e:
            logger.error(f"Error in Content Creation Agent: {str(e)}")
            return {"error": f"Content creation error: {str(e)}"}
    
    def _generate_content(self, subject: str, topic: str, grades: List[str], cultural_context: str) -> Dict[str, Any]:
        """Generate content with cultural relevance"""
        
        # Enhanced prompt with cultural context
        prompt = f"""
        Create a comprehensive lesson plan for {subject} - {topic} for grades {', '.join(grades)}.
        
        Cultural Context: {cultural_context}
        
        Include:
        1. Learning Objectives (grade-appropriate)
        2. Introduction with local examples
        3. Main content with visual aids
        4. Interactive activities
        5. Assessment questions
        6. Homework assignments
        
        Make it culturally relevant and engaging for Indian students.
        """
        
        # Simulate AI content generation (replace with actual Google Cloud AI call)
        content = {
            "learning_objectives": [
                f"Understand {topic} concepts appropriate for {grade}" for grade in grades
            ],
            "introduction": f"Today we'll learn about {topic} with examples from our local community...",
            "main_content": f"Let's explore {topic} through interactive examples...",
            "activities": [
                "Group discussion with local examples",
                "Hands-on demonstration",
                "Problem-solving exercises"
            ],
            "assessment": [
                "Multiple choice questions",
                "Short answer responses",
                "Practical application"
            ],
            "homework": f"Complete the {topic} worksheet with family examples"
        }
        
        return content

class DifferentiationAgent(BaseAgent):
    """Adapts content for multiple grade levels simultaneously"""
    
    def __init__(self):
        config = AgentConfig(
            name="Differentiation Agent",
            description="Creates grade-appropriate versions of content",
            capabilities=["grade_differentiation", "complexity_adjustment", "skill_mapping"],
            temperature=0.6
        )
        super().__init__(config)
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create differentiated content for multiple grades"""
        try:
            base_content = input_data.get("base_content", {})
            grades = input_data.get("grades", [])
            
            differentiated_content = {}
            
            for grade in grades:
                grade_content = self._adapt_for_grade(base_content, grade)
                differentiated_content[grade] = grade_content
            
            return self.format_response({
                "differentiated_content": differentiated_content,
                "metadata": {
                    "grades_processed": grades,
                    "adaptation_levels": len(grades)
                }
            })
            
        except Exception as e:
            logger.error(f"Error in Differentiation Agent: {str(e)}")
            return {"error": f"Differentiation error: {str(e)}"}
    
    def _adapt_for_grade(self, base_content: Dict[str, Any], grade: str) -> Dict[str, Any]:
        """Adapt content for specific grade level"""
        
        # Grade-specific adaptations
        grade_adaptations = {
            "Grade 3": {
                "complexity": "basic",
                "vocabulary": "simple",
                "examples": "concrete",
                "activities": "hands-on"
            },
            "Grade 4": {
                "complexity": "intermediate",
                "vocabulary": "developing",
                "examples": "mixed",
                "activities": "interactive"
            },
            "Grade 5": {
                "complexity": "advanced",
                "vocabulary": "rich",
                "examples": "abstract",
                "activities": "analytical"
            }
        }
        
        adaptation = grade_adaptations.get(grade, grade_adaptations["Grade 4"])
        
        # Adapt content based on grade level
        adapted_content = {
            "learning_objectives": self._adapt_objectives(base_content.get("learning_objectives", []), adaptation),
            "main_content": self._adapt_content(base_content.get("main_content", ""), adaptation),
            "activities": self._adapt_activities(base_content.get("activities", []), adaptation),
            "assessment": self._adapt_assessment(base_content.get("assessment", []), adaptation)
        }
        
        return adapted_content
    
    def _adapt_objectives(self, objectives: List[str], adaptation: Dict[str, str]) -> List[str]:
        """Adapt learning objectives for grade level"""
        adapted = []
        for objective in objectives:
            if adaptation["complexity"] == "basic":
                adapted.append(f"Basic understanding of {objective}")
            elif adaptation["complexity"] == "intermediate":
                adapted.append(f"Develop understanding of {objective}")
            else:
                adapted.append(f"Master {objective} with advanced applications")
        return adapted

class LocalizationAgent(BaseAgent):
    """Translates and localizes content for regional languages"""
    
    def __init__(self):
        config = AgentConfig(
            name="Localization Agent",
            description="Translates content to regional languages with cultural context",
            capabilities=["translation", "cultural_adaptation", "regional_context"],
            temperature=0.7
        )
        super().__init__(config)
        self.supported_languages = ["Hindi", "Marathi", "Telugu", "Tamil", "Bengali", "Gujarati"]
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Localize content for multiple languages"""
        try:
            content = input_data.get("differentiated_content", {})
            target_languages = input_data.get("languages", ["English"])
            cultural_context = input_data.get("cultural_context", "")
            
            localized_content = {}
            
            for language in target_languages:
                if language in self.supported_languages:
                    localized_content[language] = self._localize_content(content, language, cultural_context)
                else:
                    localized_content[language] = content  # Keep original for unsupported languages
            
            return self.format_response({
                "localized_content": localized_content,
                "metadata": {
                    "languages_processed": target_languages,
                    "cultural_context": cultural_context
                }
            })
            
        except Exception as e:
            logger.error(f"Error in Localization Agent: {str(e)}")
            return {"error": f"Localization error: {str(e)}"}
    
    def _localize_content(self, content: Dict[str, Any], language: str, cultural_context: str) -> Dict[str, Any]:
        """Localize content for specific language and culture"""
        
        # Simulate translation and cultural adaptation
        # In production, use Google Cloud Translation API
        
        language_adaptations = {
            "Hindi": {
                "greeting": "नमस्ते",
                "examples": "भारतीय संदर्भ में",
                "activities": "समूह चर्चा"
            },
            "Marathi": {
                "greeting": "नमस्कार",
                "examples": "महाराष्ट्रातील उदाहरणे",
                "activities": "गट चर्चा"
            },
            "Telugu": {
                "greeting": "నమస్కారం",
                "examples": "తెలంగాణ సందర్భంలో",
                "activities": "గ్రూప్ చర్చ"
            }
        }
        
        adaptation = language_adaptations.get(language, {})
        
        localized = {}
        for key, value in content.items():
            if isinstance(value, str):
                localized[key] = f"[{language}] {value}"
            elif isinstance(value, list):
                localized[key] = [f"[{language}] {item}" for item in value]
            else:
                localized[key] = value
        
        return localized

class AssessmentAgent(BaseAgent):
    """Generates and evaluates assessments"""
    
    def __init__(self):
        config = AgentConfig(
            name="Assessment Agent",
            description="Creates grade-appropriate assessments and evaluations",
            capabilities=["assessment_generation", "evaluation", "progress_tracking"],
            temperature=0.6
        )
        super().__init__(config)
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate assessments for different grade levels"""
        try:
            subject = input_data.get("subject", "")
            topic = input_data.get("topic", "")
            grades = input_data.get("grades", [])
            
            assessments = {}
            
            for grade in grades:
                grade_assessment = self._generate_assessment(subject, topic, grade)
                assessments[grade] = grade_assessment
            
            return self.format_response({
                "assessments": assessments,
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grades": grades
                }
            })
            
        except Exception as e:
            logger.error(f"Error in Assessment Agent: {str(e)}")
            return {"error": f"Assessment generation error: {str(e)}"}
    
    def _generate_assessment(self, subject: str, topic: str, grade: str) -> Dict[str, Any]:
        """Generate assessment for specific grade"""
        
        assessment_types = {
            "Grade 3": ["multiple_choice", "fill_blank", "matching"],
            "Grade 4": ["multiple_choice", "short_answer", "problem_solving"],
            "Grade 5": ["multiple_choice", "essay", "analytical"]
        }
        
        types = assessment_types.get(grade, ["multiple_choice"])
        
        assessment = {
            "title": f"{subject} - {topic} Assessment",
            "grade": grade,
            "duration": "30 minutes",
            "questions": []
        }
        
        for q_type in types:
            question = self._create_question(topic, q_type, grade)
            assessment["questions"].append(question)
        
        return assessment
    
    def _create_question(self, topic: str, q_type: str, grade: str) -> Dict[str, Any]:
        """Create a question of specific type"""
        
        question_templates = {
            "multiple_choice": {
                "type": "multiple_choice",
                "question": f"What is the main concept of {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 0
            },
            "short_answer": {
                "type": "short_answer",
                "question": f"Explain {topic} in your own words.",
                "expected_length": "2-3 sentences"
            },
            "problem_solving": {
                "type": "problem_solving",
                "question": f"Solve a problem related to {topic}.",
                "steps": ["Step 1", "Step 2", "Step 3"]
            }
        }
        
        return question_templates.get(q_type, question_templates["multiple_choice"])

class TeachingSupportAgent(BaseAgent):
    """Provides real-time teaching assistance and Q&A"""
    
    def __init__(self):
        config = AgentConfig(
            name="Teaching Support Agent",
            description="Provides real-time assistance and answers teacher questions",
            capabilities=["qa_support", "teaching_tips", "classroom_management"],
            temperature=0.7
        )
        super().__init__(config)
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide teaching support and answer questions"""
        try:
            question = input_data.get("question", "")
            context = input_data.get("context", "")
            
            answer = self._generate_answer(question, context)
            
            return self.format_response({
                "answer": answer,
                "metadata": {
                    "question_type": self._classify_question(question),
                    "context": context
                }
            })
            
        except Exception as e:
            logger.error(f"Error in Teaching Support Agent: {str(e)}")
            return {"error": f"Support error: {str(e)}"}
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate helpful answer for teacher question"""
        
        # Simulate AI-powered teaching support
        # In production, use Google Cloud AI for sophisticated responses
        
        common_questions = {
            "classroom_management": "Try grouping students by learning style and using differentiated activities.",
            "student_engagement": "Use local examples and hands-on activities to make lessons more engaging.",
            "assessment": "Create grade-appropriate assessments with clear learning objectives.",
            "parent_communication": "Send regular updates and involve parents in learning activities."
        }
        
        # Simple keyword matching (replace with AI-powered analysis)
        for keyword, answer in common_questions.items():
            if keyword.lower() in question.lower():
                return answer
        
        return f"Here's a helpful approach for your question about '{question}': Consider the cultural context and grade level of your students when planning activities."

class AgentOrchestrator:
    """Manages the complete multi-agent system"""
    
    def __init__(self):
        self.master_agent = MasterTeachingAgent()
        self.agents = {}
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        agents = [
            ContentCreationAgent(),
            DifferentiationAgent(),
            LocalizationAgent(),
            AssessmentAgent(),
            TeachingSupportAgent()
        ]
        
        for agent in agents:
            self.agents[agent.name] = agent
            self.master_agent.register_agent(agent)
            
        logger.info(f"Initialized {len(agents)} agents")
    
    def process_request(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process request through the multi-agent system"""
        try:
            return self.master_agent.process(input_data)
        except Exception as e:
            logger.error(f"Error in agent orchestration: {str(e)}")
            return {"error": f"System error: {str(e)}"}
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "status": "active",
                "capabilities": agent.capabilities,
                "model": agent.model
            }
        return status

# Global orchestrator instance
orchestrator = AgentOrchestrator()

def get_orchestrator() -> AgentOrchestrator:
    """Get the global agent orchestrator"""
    return orchestrator 