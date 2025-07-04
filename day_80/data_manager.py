import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from config import Config

class DataManager:
    def __init__(self):
        self.config = Config()
        self.cities_data = []
        self.personality_questions = []
        self.user_sessions = {}
        self.cache = {}
        self.cache_expiry = {}
        self._load_data()
    
    def _load_data(self):
        """Load all data files"""
        try:
            # Load cities data
            with open('data/cities.json', 'r') as f:
                self.cities_data = json.load(f)['cities']
            
            # Load personality questions
            with open('data/personality_questions.json', 'r') as f:
                self.personality_questions = json.load(f)['questions']
                
        except FileNotFoundError as e:
            print(f"Warning: Data file not found: {e}")
            self.cities_data = []
            self.personality_questions = []
    
    def get_cities(self) -> List[Dict]:
        """Get all cities data"""
        return self.cities_data
    
    def get_city_by_name(self, city_name: str) -> Optional[Dict]:
        """Get city data by name"""
        for city in self.cities_data:
            if city['name'].lower() == city_name.lower():
                return city
        return None
    
    def get_cities_by_state(self, state: str) -> List[Dict]:
        """Get cities by state"""
        return [city for city in self.cities_data if city['state'].lower() == state.lower()]
    
    def get_personality_questions(self) -> List[Dict]:
        """Get personality assessment questions"""
        return self.personality_questions
    
    def search_cities(self, query: str) -> List[Dict]:
        """Search cities by name or state"""
        query = query.lower()
        results = []
        
        for city in self.cities_data:
            if (query in city['name'].lower() or 
                query in city['state'].lower() or
                query in city['country'].lower()):
                results.append(city)
        
        return results
    
    def get_city_statistics(self) -> Dict[str, Any]:
        """Get overall statistics about cities"""
        if not self.cities_data:
            return {}
        
        costs = []
        populations = []
        climates = []
        
        for city in self.cities_data:
            total_cost = sum(city['cost_of_living'].values())
            costs.append(total_cost)
            populations.append(city['population'])
            climates.append(city['climate']['avg_temp_summer'])
        
        return {
            'total_cities': len(self.cities_data),
            'avg_cost_of_living': np.mean(costs),
            'min_cost_of_living': min(costs),
            'max_cost_of_living': max(costs),
            'avg_population': np.mean(populations),
            'avg_summer_temp': np.mean(climates),
            'states_represented': len(set(city['state'] for city in self.cities_data))
        }
    
    def get_cost_comparison_data(self) -> pd.DataFrame:
        """Get cost comparison data as DataFrame"""
        if not self.cities_data:
            return pd.DataFrame()
        
        cost_data = []
        for city in self.cities_data:
            city_costs = city['cost_of_living'].copy()
            city_costs['city'] = city['name']
            city_costs['state'] = city['state']
            cost_data.append(city_costs)
        
        return pd.DataFrame(cost_data)
    
    def get_career_data(self) -> pd.DataFrame:
        """Get career data as DataFrame"""
        if not self.cities_data:
            return pd.DataFrame()
        
        career_data = []
        for city in self.cities_data:
            career_info = city['career'].copy()
            career_info['city'] = city['name']
            career_info['state'] = city['state']
            career_data.append(career_info)
        
        return pd.DataFrame(career_data)
    
    def get_lifestyle_data(self) -> pd.DataFrame:
        """Get lifestyle data as DataFrame"""
        if not self.cities_data:
            return pd.DataFrame()
        
        lifestyle_data = []
        for city in self.cities_data:
            lifestyle_info = city['lifestyle'].copy()
            lifestyle_info['city'] = city['name']
            lifestyle_info['state'] = city['state']
            lifestyle_data.append(lifestyle_info)
        
        return pd.DataFrame(lifestyle_data)
    
    def cache_data(self, key: str, data: Any, expiry_hours: int = 1):
        """Cache data with expiry"""
        self.cache[key] = data
        self.cache_expiry[key] = datetime.now() + timedelta(hours=expiry_hours)
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data if not expired"""
        if key in self.cache:
            if datetime.now() < self.cache_expiry[key]:
                return self.cache[key]
            else:
                # Remove expired cache
                del self.cache[key]
                del self.cache_expiry[key]
        return None
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_expiry.clear()
    
    def save_user_session(self, session_id: str, data: Dict):
        """Save user session data"""
        self.user_sessions[session_id] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def get_user_session(self, session_id: str) -> Optional[Dict]:
        """Get user session data"""
        if session_id in self.user_sessions:
            session = self.user_sessions[session_id]
            # Check if session is not too old (24 hours)
            if datetime.now() - session['timestamp'] < timedelta(hours=24):
                return session['data']
            else:
                # Remove old session
                del self.user_sessions[session_id]
        return None
    
    def export_user_data(self, session_id: str) -> Dict:
        """Export user data for download"""
        session_data = self.get_user_session(session_id)
        if not session_data:
            return {}
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'user_profile': session_data.get('user_profile', {}),
            'personality_scores': session_data.get('personality_scores', {}),
            'recommendations': session_data.get('recommendations', []),
            'comparisons': session_data.get('comparisons', []),
            'cost_analysis': session_data.get('cost_analysis', {}),
            'app_version': self.config.APP_VERSION
        }
        
        return export_data
    
    def get_top_cities_by_category(self, category: str, limit: int = 5) -> List[Dict]:
        """Get top cities by specific category"""
        if not self.cities_data:
            return []
        
        if category == 'cost':
            # Sort by total cost of living (ascending)
            sorted_cities = sorted(self.cities_data, 
                                 key=lambda x: sum(x['cost_of_living'].values()))
        elif category == 'career':
            # Sort by average salary (descending)
            sorted_cities = sorted(self.cities_data, 
                                 key=lambda x: x['career']['avg_salary'], reverse=True)
        elif category == 'lifestyle':
            # Sort by average lifestyle score
            sorted_cities = sorted(self.cities_data, 
                                 key=lambda x: (x['lifestyle']['walkability'] + 
                                              x['lifestyle']['safety_score']) / 2, reverse=True)
        elif category == 'culture':
            # Sort by average culture score
            sorted_cities = sorted(self.cities_data, 
                                 key=lambda x: (x['culture']['diversity_score'] + 
                                              x['culture']['arts_score'] + 
                                              x['culture']['nightlife_score']) / 3, reverse=True)
        else:
            return []
        
        return sorted_cities[:limit]
    
    def get_city_rankings(self) -> Dict[str, List[Dict]]:
        """Get city rankings by different categories"""
        rankings = {
            'most_affordable': self.get_top_cities_by_category('cost', 5),
            'best_career_opportunities': self.get_top_cities_by_category('career', 5),
            'best_lifestyle': self.get_top_cities_by_category('lifestyle', 5),
            'best_culture': self.get_top_cities_by_category('culture', 5)
        }
        
        return rankings
    
    def validate_city_names(self, city_names: List[str]) -> Dict[str, bool]:
        """Validate if city names exist in database"""
        available_cities = [city['name'] for city in self.cities_data]
        validation = {}
        
        for city_name in city_names:
            validation[city_name] = city_name in available_cities
        
        return validation
    
    def get_city_suggestions(self, partial_name: str, limit: int = 5) -> List[str]:
        """Get city name suggestions based on partial input"""
        if not partial_name:
            return []
        
        partial_name = partial_name.lower()
        suggestions = []
        
        for city in self.cities_data:
            if partial_name in city['name'].lower():
                suggestions.append(city['name'])
                if len(suggestions) >= limit:
                    break
        
        return suggestions 