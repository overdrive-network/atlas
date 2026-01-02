"""AI-powered health data analysis using OpenAI"""
from openai import OpenAI
import json
import logging

logger = logging.getLogger(__name__)


class HealthAnalyzer:
    """Analyze health metrics using AI"""
    
    def __init__(self, api_key):
        """
        Initialize Health Analyzer
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key) if api_key else None
    
    def analyze_today(self, metrics):
        """
        Analyze today's health metrics
        
        Args:
            metrics: Dictionary with today's health data
            
        Returns:
            AI-generated analysis and insights
        """
        if not self.client:
            return self._get_fallback_analysis("today", metrics)
        
        try:
            prompt = self._create_today_prompt(metrics)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a health and fitness expert providing personalized insights based on Garmin health data. Be encouraging, specific, and actionable."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in AI analysis for today: {str(e)}")
            return self._get_fallback_analysis("today", metrics)
    
    def analyze_yesterday(self, metrics):
        """
        Analyze yesterday's health metrics
        
        Args:
            metrics: Dictionary with yesterday's health data
            
        Returns:
            AI-generated analysis and insights
        """
        if not self.client:
            return self._get_fallback_analysis("yesterday", metrics)
        
        try:
            prompt = self._create_yesterday_prompt(metrics)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a health and fitness expert reviewing yesterday's performance. Provide constructive feedback and suggestions for improvement."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in AI analysis for yesterday: {str(e)}")
            return self._get_fallback_analysis("yesterday", metrics)
    
    def analyze_last_month(self, metrics):
        """
        Analyze last month's health trends
        
        Args:
            metrics: List of daily metrics for the past month
            
        Returns:
            AI-generated trend analysis
        """
        if not self.client:
            return self._get_fallback_analysis("month", metrics)
        
        try:
            prompt = self._create_monthly_prompt(metrics)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a health and fitness expert analyzing monthly trends. Identify patterns, improvements, and areas needing attention."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in AI analysis for month: {str(e)}")
            return self._get_fallback_analysis("month", metrics)
    
    def get_all_insights(self, all_metrics):
        """
        Generate insights for all timeframes
        
        Args:
            all_metrics: Dictionary with 'today', 'week', and 'month' data
            
        Returns:
            Dictionary with insights for each timeframe
        """
        insights = {}
        
        # Today's insights
        if all_metrics.get('today'):
            insights['today'] = self.analyze_today(all_metrics['today'])
        
        # Yesterday's insights
        if all_metrics.get('week') and len(all_metrics['week']) > 1:
            insights['yesterday'] = self.analyze_yesterday(all_metrics['week'][1])
        
        # Monthly insights
        if all_metrics.get('month'):
            insights['month'] = self.analyze_last_month(all_metrics['month'])
        
        return insights
    
    def _create_today_prompt(self, metrics):
        """Create prompt for today's analysis"""
        return f"""
Analyze today's health metrics and provide personalized insights:

Steps: {metrics.get('steps', 0):,}
Distance: {metrics.get('distance', 0):.2f} km
Calories Burned: {metrics.get('calories', 0):,}
Resting Heart Rate: {metrics.get('heart_rate', {}).get('restingHeartRate', 'N/A')} bpm
Sleep: {metrics.get('sleep', {}).get('total_hours', 0):.1f} hours
Stress Level: {json.dumps(metrics.get('stress', 'N/A'))}
Body Battery: {metrics.get('body_battery', 'N/A')}

Provide:
1. Positive feedback on good metrics
2. Suggestions for improvement
3. Any health concerns or risks to watch
4. Actionable recommendations for the rest of the day
"""
    
    def _create_yesterday_prompt(self, metrics):
        """Create prompt for yesterday's analysis"""
        return f"""
Review yesterday's health performance:

Steps: {metrics.get('steps', 0):,}
Distance: {metrics.get('distance', 0):.2f} km
Calories Burned: {metrics.get('calories', 0):,}
Resting Heart Rate: {metrics.get('resting_heart_rate', 'N/A')} bpm
Sleep: {metrics.get('sleep_hours', 0):.1f} hours

Provide:
1. What went well yesterday
2. Areas that could be improved
3. Specific suggestions for today based on yesterday's data
4. Any concerning patterns
"""
    
    def _create_monthly_prompt(self, metrics):
        """Create prompt for monthly analysis"""
        # Calculate averages
        total_days = len(metrics)
        if total_days == 0:
            return "No data available for monthly analysis."
        
        avg_steps = sum(m.get('steps', 0) for m in metrics) / total_days
        avg_distance = sum(m.get('distance', 0) for m in metrics) / total_days
        avg_calories = sum(m.get('calories', 0) for m in metrics) / total_days
        avg_sleep = sum(m.get('sleep_hours', 0) for m in metrics) / total_days
        avg_hr = sum(m.get('resting_heart_rate', 0) for m in metrics if m.get('resting_heart_rate', 0) > 0)
        hr_count = sum(1 for m in metrics if m.get('resting_heart_rate', 0) > 0)
        avg_hr = avg_hr / hr_count if hr_count > 0 else 0
        
        return f"""
Analyze the last {total_days} days of health data:

Average Daily Steps: {avg_steps:,.0f}
Average Daily Distance: {avg_distance:.2f} km
Average Daily Calories: {avg_calories:,.0f}
Average Sleep: {avg_sleep:.1f} hours
Average Resting Heart Rate: {avg_hr:.0f} bpm

Provide:
1. Key trends and patterns observed
2. Overall health assessment
3. Areas of improvement over the month
4. Concerns or red flags to address
5. Recommendations for next month
"""
    
    def _get_fallback_analysis(self, timeframe, metrics):
        """Provide basic analysis when AI is not available"""
        if timeframe == "today":
            steps = metrics.get('steps', 0)
            sleep_hours = metrics.get('sleep', {}).get('total_hours', 0)
            
            analysis = "📊 **Today's Health Summary**\n\n"
            
            if steps >= 10000:
                analysis += "✅ Great job! You've hit your step goal today.\n"
            elif steps >= 7000:
                analysis += "🚶 Good progress on steps. Try to reach 10,000 for optimal health.\n"
            else:
                analysis += "⚠️ Your step count is below recommended levels. Consider a walk!\n"
            
            if sleep_hours >= 7:
                analysis += "😴 Excellent sleep! You're well-rested.\n"
            elif sleep_hours >= 6:
                analysis += "😴 Decent sleep, but aim for 7-9 hours for optimal recovery.\n"
            else:
                analysis += "⚠️ Low sleep detected. Prioritize rest tonight.\n"
            
            analysis += "\n💡 **Tip**: Stay hydrated and maintain consistent activity throughout the day."
            return analysis
        
        elif timeframe == "yesterday":
            return "📅 **Yesterday's Performance**\n\nYour data shows consistent activity. Keep up the good work!"
        
        else:  # month
            return "📈 **Monthly Overview**\n\nYou're tracking your health metrics consistently. Continue monitoring your progress!"
