import openai
import json
import numpy as np
from typing import Dict, List, Tuple, Any
import pandas as pd
from config import Config

class AIEngine:
    def __init__(self):
        self.config = Config()
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
        self._load_data()
    
    def _load_data(self):
        """Load cities and personality questions data"""
        try:
            with open('data/cities.json', 'r') as f:
                self.cities_data = json.load(f)['cities']
            
            with open('data/personality_questions.json', 'r') as f:
                self.personality_questions = json.load(f)['questions']
        except FileNotFoundError:
            print("Warning: Data files not found. Using default data.")
            self.cities_data = []
            self.personality_questions = []
    
    def calculate_personality_scores(self, answers: List[int]) -> Dict[str, float]:
        """
        Calculate personality scores based on quiz answers
        
        Args:
            answers: List of answer indices (0-3 for each question)
            
        Returns:
            Dictionary with personality dimension scores
        """
        if len(answers) != len(self.personality_questions):
            raise ValueError(f"Expected {len(self.personality_questions)} answers, got {len(answers)}")
        
        # Initialize scores
        scores = {
            'openness': 0,
            'conscientiousness': 0,
            'extraversion': 0,
            'agreeableness': 0,
            'neuroticism': 0
        }
        
        # Calculate scores based on answers
        for i, answer_idx in enumerate(answers):
            if answer_idx < 0 or answer_idx >= 4:
                continue
                
            question = self.personality_questions[i]
            options = question['options']
            mapping = question['personality_mapping']
            
            # Get the selected option key
            option_keys = list(mapping.keys())
            if answer_idx < len(option_keys):
                selected_key = option_keys[answer_idx]
                personality_impact = mapping[selected_key]
                
                # Apply the personality impact
                for dimension, impact in personality_impact.items():
                    if dimension in scores:
                        scores[dimension] += impact
        
        # Normalize scores to 0-100 scale
        for dimension in scores:
            scores[dimension] = max(0, min(100, 50 + scores[dimension] * 5))
        
        return scores
    
    def analyze_city_compatibility(self, user_profile: Dict, city_data: Dict) -> Dict[str, Any]:
        """
        Analyze compatibility between user profile and city using AI
        
        Args:
            user_profile: User's profile including personality, preferences, etc.
            city_data: City information
            
        Returns:
            Compatibility analysis with scores and reasoning
        """
        if not self.config.OPENAI_API_KEY:
            return self._fallback_analysis(user_profile, city_data)
        
        try:
            prompt = self._build_analysis_prompt(user_profile, city_data)
            
            response = openai.ChatCompletion.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert relocation consultant with deep knowledge of cities, job markets, and lifestyle factors. Provide detailed, practical analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            analysis = response.choices[0].message.content
            
            # Parse the analysis and extract scores
            compatibility_score = self._extract_compatibility_score(analysis)
            
            return {
                'compatibility_score': compatibility_score,
                'analysis': analysis,
                'city_name': city_data['name'],
                'user_profile': user_profile
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_analysis(user_profile, city_data)
    
    def _build_analysis_prompt(self, user_profile: Dict, city_data: Dict) -> str:
        """Build the analysis prompt for OpenAI"""
        
        personality = user_profile.get('personality_scores', {})
        career = user_profile.get('career_info', {})
        preferences = user_profile.get('preferences', {})
        
        prompt = f"""
        Analyze the compatibility between this user profile and {city_data['name']}:

        USER PROFILE:
        - Personality: Openness={personality.get('openness', 50)}, Conscientiousness={personality.get('conscientiousness', 50)}, Extraversion={personality.get('extraversion', 50)}, Agreeableness={personality.get('agreeableness', 50)}, Neuroticism={personality.get('neuroticism', 50)}
        - Career: {career.get('field', 'Not specified')} with salary ${career.get('salary', 0):,}
        - Preferences: {preferences}

        CITY DATA:
        - Cost of Living: ${sum(city_data['cost_of_living'].values()):,}/month
        - Climate: Summer {city_data['climate']['avg_temp_summer']}°F, Winter {city_data['climate']['avg_temp_winter']}°F
        - Culture: Diversity {city_data['culture']['diversity_score']}, Arts {city_data['culture']['arts_score']}, Nightlife {city_data['culture']['nightlife_score']}
        - Career: Tech jobs {city_data['career']['tech_jobs']}, Avg salary ${city_data['career']['avg_salary']:,}
        - Lifestyle: Walkability {city_data['lifestyle']['walkability']}, Safety {city_data['lifestyle']['safety_score']}

        Provide a comprehensive analysis including:
        1. Overall compatibility score (0-100)
        2. Cost of living impact analysis
        3. Career opportunities assessment
        4. Lifestyle and cultural fit
        5. Potential challenges and considerations
        6. Specific recommendations for this user

        Format your response with clear sections and a compatibility score at the end.
        """
        
        return prompt
    
    def _fallback_analysis(self, user_profile: Dict, city_data: Dict) -> Dict[str, Any]:
        """Fallback analysis when OpenAI is not available"""
        
        # Simple scoring algorithm
        personality = user_profile.get('personality_scores', {})
        career = user_profile.get('career_info', {})
        
        # Calculate basic compatibility score
        cost_score = self._calculate_cost_score(user_profile, city_data)
        career_score = self._calculate_career_score(user_profile, city_data)
        lifestyle_score = self._calculate_lifestyle_score(user_profile, city_data)
        
        overall_score = (cost_score + career_score + lifestyle_score) / 3
        
        return {
            'compatibility_score': overall_score,
            'analysis': f"Compatibility analysis for {city_data['name']}: Cost Score: {cost_score:.1f}, Career Score: {career_score:.1f}, Lifestyle Score: {lifestyle_score:.1f}",
            'city_name': city_data['name'],
            'user_profile': user_profile
        }
    
    def _calculate_cost_score(self, user_profile: Dict, city_data: Dict) -> float:
        """Calculate cost compatibility score"""
        user_salary = user_profile.get('career_info', {}).get('salary', 50000)
        city_costs = sum(city_data['cost_of_living'].values())
        
        # Simple affordability calculation
        if user_salary * 0.3 >= city_costs:  # 30% of salary should cover costs
            return 85
        elif user_salary * 0.4 >= city_costs:
            return 70
        elif user_salary * 0.5 >= city_costs:
            return 50
        else:
            return 25
    
    def _calculate_career_score(self, user_profile: Dict, city_data: Dict) -> float:
        """Calculate career compatibility score"""
        user_field = user_profile.get('career_info', {}).get('field', '').lower()
        
        if 'tech' in user_field or 'software' in user_field:
            return city_data['career']['tech_jobs']
        elif 'finance' in user_field or 'banking' in user_field:
            return city_data['career']['finance_jobs']
        elif 'health' in user_field or 'medical' in user_field:
            return city_data['career']['healthcare_jobs']
        elif 'education' in user_field or 'teaching' in user_field:
            return city_data['career']['education_jobs']
        else:
            return 70  # Default score
    
    def _calculate_lifestyle_score(self, user_profile: Dict, city_data: Dict) -> float:
        """Calculate lifestyle compatibility score"""
        personality = user_profile.get('personality_scores', {})
        
        # Factor in personality preferences
        extraversion = personality.get('extraversion', 50)
        openness = personality.get('openness', 50)
        
        # Calculate lifestyle score based on city characteristics
        culture_score = (city_data['culture']['diversity_score'] + 
                        city_data['culture']['arts_score'] + 
                        city_data['culture']['nightlife_score']) / 3
        
        lifestyle_score = (culture_score + city_data['lifestyle']['walkability'] + 
                          city_data['lifestyle']['safety_score']) / 3
        
        # Adjust based on personality
        if extraversion > 70:
            lifestyle_score += 10
        if openness > 70:
            lifestyle_score += 10
        
        return min(100, max(0, lifestyle_score))
    
    def _extract_compatibility_score(self, analysis: str) -> float:
        """Extract compatibility score from AI analysis"""
        try:
            # Look for score patterns in the text
            import re
            score_match = re.search(r'compatibility score[:\s]*(\d+)', analysis.lower())
            if score_match:
                return float(score_match.group(1))
            
            # Fallback: estimate based on positive/negative language
            positive_words = ['excellent', 'great', 'good', 'strong', 'high', 'compatible']
            negative_words = ['poor', 'bad', 'weak', 'low', 'incompatible', 'challenging']
            
            analysis_lower = analysis.lower()
            positive_count = sum(1 for word in positive_words if word in analysis_lower)
            negative_count = sum(1 for word in negative_words if word in analysis_lower)
            
            if positive_count > negative_count:
                return 75
            elif negative_count > positive_count:
                return 35
            else:
                return 55
                
        except:
            return 50
    
    def get_recommendations(self, user_profile: Dict, num_recommendations: int = 5) -> List[Dict]:
        """
        Get top city recommendations for user
        
        Args:
            user_profile: User's profile
            num_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended cities with analysis
        """
        recommendations = []
        
        for city in self.cities_data:
            analysis = self.analyze_city_compatibility(user_profile, city)
            recommendations.append(analysis)
        
        # Sort by compatibility score
        recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return recommendations[:num_recommendations]
    
    def compare_cities(self, user_profile: Dict, city_names: List[str]) -> List[Dict]:
        """
        Compare specific cities for a user
        
        Args:
            user_profile: User's profile
            city_names: List of city names to compare
            
        Returns:
            List of city comparisons
        """
        comparisons = []
        
        for city_name in city_names:
            city_data = next((city for city in self.cities_data if city['name'] == city_name), None)
            if city_data:
                analysis = self.analyze_city_compatibility(user_profile, city_data)
                comparisons.append(analysis)
        
        return comparisons
    
    def generate_cost_analysis(self, current_city: str, target_city: str, current_salary: float) -> Dict:
        """
        Generate detailed cost analysis between cities
        
        Args:
            current_city: Name of current city
            target_city: Name of target city
            current_salary: Current salary
            
        Returns:
            Cost analysis dictionary
        """
        current_city_data = next((city for city in self.cities_data if city['name'] == current_city), None)
        target_city_data = next((city for city in self.cities_data if city['name'] == target_city), None)
        
        if not current_city_data or not target_city_data:
            return {"error": "City data not found"}
        
        current_costs = current_city_data['cost_of_living']
        target_costs = target_city_data['cost_of_living']
        
        analysis = {
            'current_city': current_city,
            'target_city': target_city,
            'current_salary': current_salary,
            'cost_changes': {},
            'total_monthly_change': 0,
            'salary_adjustment_needed': 0,
            'recommendations': []
        }
        
        total_current = sum(current_costs.values())
        total_target = sum(target_costs.values())
        
        for category in current_costs:
            current_cost = current_costs[category]
            target_cost = target_costs[category]
            change = target_cost - current_cost
            percentage_change = (change / current_cost * 100) if current_cost > 0 else 0
            
            analysis['cost_changes'][category] = {
                'current': current_cost,
                'target': target_cost,
                'change': change,
                'percentage_change': percentage_change
            }
        
        analysis['total_monthly_change'] = total_target - total_current
        analysis['total_percentage_change'] = (analysis['total_monthly_change'] / total_current * 100) if total_current > 0 else 0
        
        # Calculate salary adjustment needed
        if analysis['total_monthly_change'] > 0:
            analysis['salary_adjustment_needed'] = analysis['total_monthly_change'] * 12 * 1.3  # 30% buffer
        
        # Generate recommendations
        if analysis['total_percentage_change'] > 20:
            analysis['recommendations'].append("Significant cost increase - consider negotiating higher salary")
        elif analysis['total_percentage_change'] < -10:
            analysis['recommendations'].append("Cost savings opportunity - you may be able to save money")
        
        return analysis 