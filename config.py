import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Garmin Connect credentials
    GARMIN_EMAIL = os.getenv('GARMIN_EMAIL', '')
    GARMIN_PASSWORD = os.getenv('GARMIN_PASSWORD', '')
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
