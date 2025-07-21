import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

class InsightsGenerator:
    def __init__(self):
        self.insight_templates = {
            'peak_performance': [
                "Your peak performance window: {day} {time} ({energy_pct}% high energy)",
                "You're most productive on {day}s at {time} - block this time for important work!",
                "Discovery: {day} {time} is your power hour with {energy_pct}% high energy"
            ],
            'energy_dip': [
                "Energy dip detected: {day} {time} - plan lighter activities",
                "Your energy drops at {time} on {day}s - schedule breaks accordingly",
                "Optimization tip: Avoid important meetings at {time} on {day}s"
            ],
            'pattern_discovery': [
                "You're {energy_pct}% more energetic on {condition} days",
                "Discovery: {condition} correlates with {energy_pct}% higher energy",
                "Pattern found: {condition} = {energy_pct}% productivity boost"
            ],
            'productivity_insight': [
                "Your optimal work rhythm: {pattern}",
                "Productivity hack: {insight}",
                "Energy optimization: {insight}"
            ]
        }
    
    def generate_weekly_report(self, energy_data, user_name="You"):
        """
        Generate a comprehensive weekly energy insights report
        """
        if energy_data.empty:
            return self._generate_empty_report(user_name)
        
        # Filter for last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        weekly_data = energy_data[energy_data['timestamp'] >= week_ago]
        
        if weekly_data.empty:
            return self._generate_empty_report(user_name)
        
        # Generate insights
        insights = {
            'summary': self._generate_summary(weekly_data, user_name),
            'peak_performance': self._find_peak_performance(weekly_data),
            'energy_dips': self._find_energy_dips(weekly_data),
            'pattern_discoveries': self._find_pattern_discoveries(weekly_data),
            'productivity_tips': self._generate_productivity_tips(weekly_data),
            'next_week_goals': self._generate_next_week_goals(weekly_data),
            'shareable_quote': self._generate_shareable_quote(weekly_data)
        }
        
        return insights
    
    def _generate_summary(self, data, user_name):
        """Generate weekly summary statistics"""
        total_records = len(data)
        high_energy_pct = (data['energy_level'] == 'High').mean() * 100
        avg_confidence = data['confidence'].mean()
        
        return {
            'total_readings': total_records,
            'high_energy_percentage': high_energy_pct,
            'avg_confidence': avg_confidence,
            'most_productive_day': data['day_of_week'].mode().iloc[0] if 'day_of_week' in data.columns else 'Unknown',
            'energy_trend': self._calculate_trend(data)
        }
    
    def _find_peak_performance(self, data):
        """Find peak performance times"""
        if 'hour' in data.columns and 'day_of_week' in data.columns:
            # Group by hour and day, find highest energy periods
            hourly_data = data.groupby(['hour', 'day_of_week', 'energy_level']).size().unstack(fill_value=0)
            
            if 'High' in hourly_data.columns:
                peak_times = hourly_data['High'].nlargest(3)
                insights = []
                
                for (hour, day), count in peak_times.items():
                    if count > 0:
                        energy_pct = (count / hourly_data.loc[(hour, day)].sum()) * 100
                        # Format time more accurately
                        if hour < 12:
                            time_str = f"{hour}:00 AM"
                        elif hour == 12:
                            time_str = "12:00 PM"
                        else:
                            time_str = f"{hour-12}:00 PM"
                        day_name = day
                        
                        insight = random.choice(self.insight_templates['peak_performance']).format(
                            day=day_name, time=time_str, energy_pct=int(energy_pct)
                        )
                        insights.append(insight)
                
                return insights[:2]  # Return top 2 insights
        
        return ["Your peak performance patterns are emerging - keep tracking to discover more!"]
    
    def _find_energy_dips(self, data):
        """Find energy dip times"""
        if 'hour' in data.columns and 'day_of_week' in data.columns:
            hourly_data = data.groupby(['hour', 'day_of_week', 'energy_level']).size().unstack(fill_value=0)
            
            if 'Low' in hourly_data.columns:
                dip_times = hourly_data['Low'].nlargest(3)
                insights = []
                
                for (hour, day), count in dip_times.items():
                    if count > 0:
                        # Format time more accurately
                        if hour < 12:
                            time_str = f"{hour}:00 AM"
                        elif hour == 12:
                            time_str = "12:00 PM"
                        else:
                            time_str = f"{hour-12}:00 PM"
                        day_name = day
                        
                        insight = random.choice(self.insight_templates['energy_dip']).format(
                            day=day_name, time=time_str
                        )
                        insights.append(insight)
                
                return insights[:2]
        
        return ["Energy dips are normal - use them for lighter tasks and breaks"]
    
    def _find_pattern_discoveries(self, data):
        """Find interesting pattern discoveries"""
        discoveries = []
        
        # Day of week patterns
        if 'day_of_week' in data.columns:
            day_energy = data.groupby('day_of_week')['energy_level'].apply(
                lambda x: (x == 'High').mean() * 100
            )
            
            best_day = day_energy.idxmax()
            worst_day = day_energy.idxmin()
            
            if day_energy[best_day] > 50:
                discoveries.append(f"You're {int(day_energy[best_day])}% more energetic on {best_day}s")
            
            if day_energy[worst_day] < 30:
                discoveries.append(f"Energy challenges on {worst_day}s - plan accordingly")
        
        # Time patterns
        if 'hour' in data.columns:
            hour_energy = data.groupby('hour')['energy_level'].apply(
                lambda x: (x == 'High').mean() * 100
            )
            
            peak_hour = hour_energy.idxmax()
            if hour_energy[peak_hour] > 60:
                # Format time more accurately
                if peak_hour < 12:
                    time_str = f"{peak_hour}:00 AM"
                elif peak_hour == 12:
                    time_str = "12:00 PM"
                else:
                    time_str = f"{peak_hour-12}:00 PM"
                discoveries.append(f"Peak energy at {time_str} - your power hour!")
        
        return discoveries[:3]
    
    def _generate_productivity_tips(self, data):
        """Generate actionable productivity tips"""
        tips = []
        
        high_energy_pct = (data['energy_level'] == 'High').mean() * 100
        
        if high_energy_pct > 60:
            tips.append("You're naturally high-energy - leverage this for creative projects!")
            tips.append("Schedule important meetings during your peak hours")
        elif high_energy_pct < 30:
            tips.append("Consider shorter work sessions with more breaks")
            tips.append("Try morning routines to boost your energy")
        else:
            tips.append("Your balanced energy is perfect for varied tasks")
            tips.append("Mix high-focus and routine tasks throughout your day")
        
        # Add time-specific tips
        if 'hour' in data.columns:
            hourly_tips = self._get_hourly_tips(data)
            tips.extend(hourly_tips)
        
        return tips[:4]
    
    def _get_hourly_tips(self, data):
        """Get tips based on hourly patterns"""
        tips = []
        
        hourly_data = data.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        
        if 'High' in hourly_data.columns:
            peak_hours = hourly_data['High'].nlargest(2)
            for hour, count in peak_hours.items():
                if count > 0:
                    # Format time more accurately
                    if hour < 12:
                        time_str = f"{hour}:00 AM"
                    elif hour == 12:
                        time_str = "12:00 PM"
                    else:
                        time_str = f"{hour-12}:00 PM"
                    tips.append(f"Block {time_str} for important work - your power hour")
        
        if 'Low' in hourly_data.columns:
            low_hours = hourly_data['Low'].nlargest(2)
            for hour, count in low_hours.items():
                if count > 0:
                    # Format time more accurately
                    if hour < 12:
                        time_str = f"{hour}:00 AM"
                    elif hour == 12:
                        time_str = "12:00 PM"
                    else:
                        time_str = f"{hour-12}:00 PM"
                    tips.append(f"Plan breaks or routine tasks at {time_str}")
        
        return tips
    
    def _generate_next_week_goals(self, data):
        """Generate goals for next week"""
        goals = []
        
        # Based on current patterns, suggest optimizations
        if 'hour' in data.columns and 'day_of_week' in data.columns:
            hourly_data = data.groupby(['hour', 'day_of_week', 'energy_level']).size().unstack(fill_value=0)
            
            if 'High' in hourly_data.columns:
                peak_time = hourly_data['High'].idxmax()
                if isinstance(peak_time, tuple):
                    hour, day = peak_time
                    # Format time more accurately
                    if hour < 12:
                        time_str = f"{hour}:00 AM"
                    elif hour == 12:
                        time_str = "12:00 PM"
                    else:
                        time_str = f"{hour-12}:00 PM"
                    goals.append(f"Test scheduling important tasks at {time_str} on {day}s")
        
        goals.append("Track your energy before and after meetings")
        goals.append("Experiment with different work environments")
        goals.append("Notice how sleep and exercise affect your energy")
        
        return goals[:3]
    
    def _generate_shareable_quote(self, data):
        """Generate a shareable quote for LinkedIn"""
        high_energy_pct = (data['energy_level'] == 'High').mean() * 100
        
        quotes = [
            f"After tracking my energy for a week, I discovered I'm {int(high_energy_pct)}% more productive during my peak hours. Energy optimization is real! ⚡",
            f"Your energy patterns don't lie. Mine revealed I'm most creative at unexpected times. Data-driven productivity is the future! 📊",
            f"We spend 40+ hours working but never track our energy. This week I discovered my true productivity rhythm. Game changer! 🎯",
            f"Energy Lens taught me: {int(high_energy_pct)}% of my high-energy time was wasted on low-impact tasks. Time to optimize! 🚀"
        ]
        
        return random.choice(quotes)
    
    def _calculate_trend(self, data):
        """Calculate energy trend over the week"""
        if len(data) < 3:
            return "stable"
        
        # Sort by timestamp and calculate trend
        sorted_data = data.sort_values('timestamp')
        energy_scores = sorted_data['energy_level'].map({'High': 3, 'Medium': 2, 'Low': 1})
        
        if len(energy_scores) >= 3:
            recent_avg = energy_scores.tail(3).mean()
            earlier_avg = energy_scores.head(3).mean()
            
            if recent_avg > earlier_avg + 0.5:
                return "improving"
            elif recent_avg < earlier_avg - 0.5:
                return "declining"
        
        return "stable"
    
    def _generate_empty_report(self, user_name):
        """Generate report for users with no data"""
        return {
            'summary': {
                'total_readings': 0,
                'high_energy_percentage': 0,
                'avg_confidence': 0,
                'most_productive_day': 'Unknown',
                'energy_trend': 'stable'
            },
            'peak_performance': ["Start tracking your energy to discover your peak performance times!"],
            'energy_dips': ["Energy tracking will help you identify your natural rhythms"],
            'pattern_discoveries': ["Your energy patterns will emerge as you track more data"],
            'productivity_tips': ["Begin your energy optimization journey today!"],
            'next_week_goals': ["Take your first energy reading", "Track energy before important meetings", "Notice how different activities affect your energy"],
            'shareable_quote': "Starting my energy optimization journey! Excited to discover my true productivity patterns. ⚡"
        }
    
    def create_linkedin_post(self, insights):
        """Create a LinkedIn-ready post from insights"""
        summary = insights['summary']
        
        post = f"""⚡ Energy Lens Weekly Report

📊 This Week's Insights:
• {summary['total_readings']} energy readings tracked
• {summary['high_energy_percentage']:.1f}% high-energy time
• Most productive day: {summary['most_productive_day']}

🎯 Key Discoveries:
"""
        
        # Add top insights
        for insight in insights['peak_performance'][:1]:
            post += f"• {insight}\n"
        
        for insight in insights['pattern_discoveries'][:1]:
            post += f"• {insight}\n"
        
        post += f"""
💡 Productivity Tip:
{insights['productivity_tips'][0] if insights['productivity_tips'] else "Track your energy to optimize your schedule!"}

🔗 Try Energy Lens: [Your App URL]

#EnergyOptimization #ProductivityHacks #DataDriven #PersonalDevelopment
"""
        
        return post 