"""Garmin Connect OAuth authentication module"""
from garminconnect import Garmin
import logging

logger = logging.getLogger(__name__)


class GarminAuth:
    """Handle Garmin Connect authentication"""
    
    def __init__(self, email, password):
        """
        Initialize Garmin authentication
        
        Args:
            email: Garmin Connect email
            password: Garmin Connect password
        """
        self.email = email
        self.password = password
        self.client = None
        
    def login(self):
        """
        Authenticate with Garmin Connect
        
        Returns:
            Garmin client object if successful, None otherwise
        """
        try:
            logger.info(f"Attempting to login to Garmin Connect with email: {self.email}")
            self.client = Garmin(self.email, self.password)
            self.client.login()
            logger.info("Successfully logged in to Garmin Connect")
            return self.client
        except Exception as e:
            logger.error(f"Failed to login to Garmin Connect: {str(e)}")
            return None
    
    def get_client(self):
        """
        Get the authenticated Garmin client
        
        Returns:
            Garmin client object or None
        """
        if not self.client:
            return self.login()
        return self.client
