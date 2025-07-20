import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class PatternAnalyzer:
    def __init__(self):
        self.insight_thresholds = {
            'high_energy_threshold': 0.4,  # 40% high energy days
            'low_energy_threshold': 0.3,   # 30% low energy days
            'confidence_threshold': 70.0,   # 70% confidence
            'pattern_days': 7              # Minimum days for pattern detection
        }
    
    def analyze_patterns(self, energy_data):
        """
        Analyze energy data and return actionable insights
        """
        if energy_data.empty:
            return []
        
        insights = []
        
        # Basic statistics
        total_records = len(energy_data)
        avg_confidence = energy_data['confidence'].mean()
        
        # Energy distribution
        energy_dist = energy_data['energy_level'].value_counts(normalize=True)
        high_energy_pct = energy_dist.get('High', 0) * 100
        low_energy_pct = energy_dist.get('Low', 0) * 100
        medium_energy_pct = energy_dist.get('Medium', 0) * 100
        
        # Time-based patterns
        if 'hour' in energy_data.columns:
            hourly_insights = self._analyze_hourly_patterns(energy_data)
            insights.extend(hourly_insights)
        
        # Day-of-week patterns
        if 'day_of_week' in energy_data.columns:
            weekly_insights = self._analyze_weekly_patterns(energy_data)
            insights.extend(weekly_insights)
        
        # Overall energy insights
        if high_energy_pct > 50:
            insights.append(f"🎯 You're high-energy {high_energy_pct:.1f}% of the time - great for productivity!")
        elif low_energy_pct > 40:
            insights.append(f"⚠️ You're experiencing low energy {low_energy_pct:.1f}% of the time - consider rest breaks")
        else:
            insights.append(f"⚖️ Your energy is well-balanced: {high_energy_pct:.1f}% high, {medium_energy_pct:.1f}% medium, {low_energy_pct:.1f}% low")
        
        # Confidence insights
        if avg_confidence < 60:
            insights.append("📊 Consider manual entries for more accurate tracking")
        elif avg_confidence > 80:
            insights.append("🎯 Great detection accuracy - your patterns are clear!")
        
        # Trend analysis
        trend_insight = self._analyze_trends(energy_data)
        if trend_insight:
            insights.append(trend_insight)
        
        return insights
    
    def _analyze_hourly_patterns(self, energy_data):
        """Analyze energy patterns by hour of day"""
        insights = []
        
        # Group by hour and energy level
        hourly_data = energy_data.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        
        if hourly_data.empty:
            return insights
        
        # Find peak energy hours
        if 'High' in hourly_data.columns:
            peak_hours = hourly_data['High'].nlargest(3)
            if not peak_hours.empty and peak_hours.iloc[0] > 0:
                peak_hour = peak_hours.index[0]
                insights.append(f"🌅 Your peak energy time: {peak_hour}:00 - schedule important tasks then!")
        
        # Find low energy hours
        if 'Low' in hourly_data.columns:
            low_hours = hourly_data['Low'].nlargest(3)
            if not low_hours.empty and low_hours.iloc[0] > 0:
                low_hour = low_hours.index[0]
                insights.append(f"😴 Your energy dip: {low_hour}:00 - plan lighter activities")
        
        return insights
    
    def _analyze_weekly_patterns(self, energy_data):
        """Analyze energy patterns by day of week"""
        insights = []
        
        # Group by day and energy level
        weekly_data = energy_data.groupby(['day_of_week', 'energy_level']).size().unstack(fill_value=0)
        
        if weekly_data.empty:
            return insights
        
        # Find best and worst days
        if 'High' in weekly_data.columns:
            best_day = weekly_data['High'].idxmax()
            best_count = weekly_data['High'].max()
            if best_count > 0:
                insights.append(f"🌟 Your most productive day: {best_day}")
        
        if 'Low' in weekly_data.columns:
            worst_day = weekly_data['Low'].idxmax()
            worst_count = weekly_data['Low'].max()
            if worst_count > 0:
                insights.append(f"📉 Your most challenging day: {worst_day} - plan accordingly")
        
        return insights
    
    def _analyze_trends(self, energy_data):
        """Analyze energy trends over time"""
        if len(energy_data) < 3:
            return None
        
        # Sort by timestamp
        sorted_data = energy_data.sort_values('timestamp')
        
        # Calculate energy scores (High=3, Medium=2, Low=1)
        energy_scores = sorted_data['energy_level'].map({'High': 3, 'Medium': 2, 'Low': 1})
        
        # Simple trend analysis
        if len(energy_scores) >= 3:
            recent_avg = energy_scores.tail(3).mean()
            earlier_avg = energy_scores.head(3).mean()
            
            if recent_avg > earlier_avg + 0.5:
                return "📈 Your energy is trending upward - great momentum!"
            elif recent_avg < earlier_avg - 0.5:
                return "📉 Your energy is declining - consider rest or routine changes"
        
        return None
    
    def get_productivity_tips(self, energy_data):
        """
        Get personalized productivity tips based on energy patterns
        """
        tips = []
        
        if energy_data.empty:
            return ["💡 Start tracking your energy to get personalized tips!"]
        
        # Energy distribution tips
        energy_dist = energy_data['energy_level'].value_counts(normalize=True)
        high_energy_pct = energy_dist.get('High', 0) * 100
        low_energy_pct = energy_dist.get('Low', 0) * 100
        
        if high_energy_pct > 50:
            tips.append("🚀 You're naturally high-energy - leverage this for creative projects!")
            tips.append("⏰ Schedule important meetings during your peak hours")
        elif low_energy_pct > 40:
            tips.append("😴 Consider shorter work sessions with more breaks")
            tips.append("🌅 Try morning routines to boost your energy")
        else:
            tips.append("⚖️ Your balanced energy is perfect for varied tasks")
            tips.append("📅 Mix high-focus and routine tasks throughout your day")
        
        # Time-based tips
        if 'hour' in energy_data.columns:
            hourly_tips = self._get_hourly_tips(energy_data)
            tips.extend(hourly_tips)
        
        # Confidence tips
        avg_confidence = energy_data['confidence'].mean()
        if avg_confidence < 60:
            tips.append("📸 Try different lighting for better energy detection")
            tips.append("✏️ Use manual entries when detection is unclear")
        
        return tips[:5]  # Limit to top 5 tips
    
    def _get_hourly_tips(self, energy_data):
        """Get tips based on hourly patterns"""
        tips = []
        
        hourly_data = energy_data.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        
        if hourly_data.empty:
            return tips
        
        # Find peak hours
        if 'High' in hourly_data.columns:
            peak_hours = hourly_data['High'].nlargest(2)
            for hour, count in peak_hours.items():
                if count > 0:
                    tips.append(f"⏰ {hour}:00 is your power hour - block it for important work")
        
        # Find low energy hours
        if 'Low' in hourly_data.columns:
            low_hours = hourly_data['Low'].nlargest(2)
            for hour, count in low_hours.items():
                if count > 0:
                    tips.append(f"😴 {hour}:00 is your energy dip - plan breaks or routine tasks")
        
        return tips
    
    def get_optimization_suggestions(self, energy_data):
        """
        Get specific optimization suggestions for productivity
        """
        suggestions = []
        
        if energy_data.empty:
            return ["📊 Start tracking to get optimization suggestions"]
        
        # Analyze patterns for specific suggestions
        if 'hour' in energy_data.columns:
            hourly_suggestions = self._get_hourly_suggestions(energy_data)
            suggestions.extend(hourly_suggestions)
        
        # Overall suggestions
        energy_dist = energy_data['energy_level'].value_counts(normalize=True)
        high_energy_pct = energy_dist.get('High', 0) * 100
        
        if high_energy_pct > 60:
            suggestions.append("🎯 You're naturally high-energy - consider longer focused work sessions")
        elif high_energy_pct < 30:
            suggestions.append("⏱️ Try the Pomodoro technique with 25-minute work sessions")
        
        return suggestions
    
    def _get_hourly_suggestions(self, energy_data):
        """Get specific hourly optimization suggestions"""
        suggestions = []
        
        hourly_data = energy_data.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        
        if hourly_data.empty:
            return suggestions
        
        # Morning optimization
        morning_energy = hourly_data.loc[6:11, 'High'].sum() if 'High' in hourly_data.columns else 0
        if morning_energy > 0:
            suggestions.append("🌅 Your mornings are productive - start with creative work")
        
        # Afternoon optimization
        afternoon_energy = hourly_data.loc[12:17, 'Low'].sum() if 'Low' in hourly_data.columns else 0
        if afternoon_energy > 0:
            suggestions.append("☕ Afternoon energy dip detected - schedule meetings or routine tasks")
        
        return suggestions 