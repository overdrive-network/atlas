"""Garmin Connect data fetching module"""
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GarminAPI:
    """Fetch health data from Garmin Connect"""
    
    def __init__(self, client):
        """
        Initialize Garmin API
        
        Args:
            client: Authenticated Garmin client
        """
        self.client = client
    
    def get_today_metrics(self):
        """
        Fetch today's health metrics
        
        Returns:
            Dictionary with today's metrics
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Fetch various metrics
            stats = self.client.get_stats(today)
            heart_rate = self.client.get_heart_rates(today)
            sleep = self._get_sleep_data(today)
            stress = self.client.get_stress_data(today)
            body_battery = self._get_body_battery(today)
            steps = stats.get('totalSteps', 0)
            distance = stats.get('totalDistanceMeters', 0)
            calories = stats.get('activeKilocalories', 0)
            
            return {
                'date': today,
                'heart_rate': heart_rate,
                'sleep': sleep,
                'steps': steps,
                'distance': distance / 1000,  # Convert to km
                'stress': stress,
                'body_battery': body_battery,
                'calories': calories,
                'stats': stats
            }
        except Exception as e:
            logger.error(f"Error fetching today's metrics: {str(e)}")
            return {}
    
    def get_weekly_metrics(self):
        """
        Fetch last 7 days of metrics
        
        Returns:
            List of daily metrics for the past week
        """
        try:
            metrics = []
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                daily_data = self._get_daily_data(date)
                if daily_data:
                    metrics.append(daily_data)
            return metrics
        except Exception as e:
            logger.error(f"Error fetching weekly metrics: {str(e)}")
            return []
    
    def get_monthly_metrics(self):
        """
        Fetch last 30 days of metrics
        
        Returns:
            List of daily metrics for the past month
        """
        try:
            metrics = []
            for i in range(30):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                daily_data = self._get_daily_data(date)
                if daily_data:
                    metrics.append(daily_data)
            return metrics
        except Exception as e:
            logger.error(f"Error fetching monthly metrics: {str(e)}")
            return []
    
    def get_all_metrics(self):
        """
        Fetch comprehensive health metrics for today, week, and month
        
        Returns:
            Dictionary with all timeframe metrics
        """
        return {
            'today': self.get_today_metrics(),
            'week': self.get_weekly_metrics(),
            'month': self.get_monthly_metrics()
        }
    
    def _get_daily_data(self, date):
        """
        Fetch metrics for a specific date
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Dictionary with daily metrics
        """
        try:
            stats = self.client.get_stats(date)
            
            # Extract key metrics
            steps = stats.get('totalSteps', 0)
            distance = stats.get('totalDistanceMeters', 0) / 1000
            calories = stats.get('activeKilocalories', 0)
            
            # Get heart rate data
            heart_rate_data = self.client.get_heart_rates(date)
            resting_hr = heart_rate_data.get('restingHeartRate', 0) if heart_rate_data else 0
            
            # Get sleep data
            sleep_data = self._get_sleep_data(date)
            
            return {
                'date': date,
                'steps': steps,
                'distance': distance,
                'calories': calories,
                'resting_heart_rate': resting_hr,
                'sleep_hours': sleep_data.get('total_hours', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching data for {date}: {str(e)}")
            return None
    
    def _get_sleep_data(self, date):
        """
        Fetch sleep data for a specific date
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Dictionary with sleep metrics
        """
        try:
            sleep = self.client.get_sleep_data(date)
            if sleep and 'dailySleepDTO' in sleep:
                sleep_dto = sleep['dailySleepDTO']
                total_seconds = sleep_dto.get('sleepTimeSeconds', 0)
                total_hours = total_seconds / 3600
                
                return {
                    'total_hours': round(total_hours, 2),
                    'deep_sleep': sleep_dto.get('deepSleepSeconds', 0) / 3600,
                    'light_sleep': sleep_dto.get('lightSleepSeconds', 0) / 3600,
                    'rem_sleep': sleep_dto.get('remSleepSeconds', 0) / 3600,
                    'awake': sleep_dto.get('awakeSleepSeconds', 0) / 3600,
                    'quality': self._calculate_sleep_quality(sleep_dto)
                }
            return {}
        except Exception as e:
            logger.error(f"Error fetching sleep data for {date}: {str(e)}")
            return {}
    
    def _get_body_battery(self, date):
        """
        Fetch body battery data
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Body battery value or None
        """
        try:
            # Body battery might not be available for all users
            stats = self.client.get_stats(date)
            return stats.get('bodyBattery', None)
        except Exception as e:
            logger.error(f"Error fetching body battery for {date}: {str(e)}")
            return None
    
    def _calculate_sleep_quality(self, sleep_dto):
        """
        Calculate sleep quality score based on sleep stages
        
        Args:
            sleep_dto: Sleep data dictionary
            
        Returns:
            Sleep quality score (0-100)
        """
        try:
            total_sleep = sleep_dto.get('sleepTimeSeconds', 0)
            deep_sleep = sleep_dto.get('deepSleepSeconds', 0)
            rem_sleep = sleep_dto.get('remSleepSeconds', 0)
            
            if total_sleep == 0:
                return 0
            
            # Quality based on percentage of deep and REM sleep
            deep_percentage = (deep_sleep / total_sleep) * 100
            rem_percentage = (rem_sleep / total_sleep) * 100
            
            # Ideal: 15-25% deep, 20-25% REM
            quality = 0
            if 15 <= deep_percentage <= 25:
                quality += 50
            else:
                quality += max(0, 50 - abs(20 - deep_percentage) * 2)
            
            if 20 <= rem_percentage <= 25:
                quality += 50
            else:
                quality += max(0, 50 - abs(22.5 - rem_percentage) * 2)
            
            return min(100, max(0, int(quality)))
        except Exception as e:
            logger.error(f"Error calculating sleep quality: {str(e)}")
            return 0
