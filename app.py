"""Main Flask application for Garmin Health Web App"""
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from config import Config
from garmin.auth import GarminAuth
from garmin.api import GarminAPI
from ai.analyzer import HealthAnalyzer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize AI analyzer
analyzer = HealthAnalyzer(app.config['OPENAI_API_KEY'])


@app.route('/')
def index():
    """Homepage - Dashboard with health metrics"""
    if 'garmin_authenticated' not in session:
        return redirect(url_for('login'))
    
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Garmin Connect login page"""
    if request.method == 'POST':
        email = request.form.get('email') or app.config['GARMIN_EMAIL']
        password = request.form.get('password') or app.config['GARMIN_PASSWORD']
        
        if not email or not password:
            return render_template('login.html', error="Please provide email and password")
        
        # Authenticate with Garmin
        auth = GarminAuth(email, password)
        client = auth.login()
        
        if client:
            session['garmin_authenticated'] = True
            session['garmin_email'] = email
            # Note: In production, use OAuth tokens instead of storing credentials
            # For demo purposes with Garmin Connect, we need to re-authenticate per session
            session['garmin_password'] = password
            logger.info(f"User logged in: {email}")
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Failed to authenticate with Garmin Connect")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/metrics')
def get_metrics():
    """API endpoint to fetch health metrics"""
    if 'garmin_authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Re-authenticate to get client
        auth = GarminAuth(session['garmin_email'], session['garmin_password'])
        client = auth.get_client()
        
        if not client:
            return jsonify({'error': 'Failed to connect to Garmin'}), 500
        
        # Fetch metrics
        api = GarminAPI(client)
        metrics = api.get_all_metrics()
        
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/insights')
def insights():
    """AI-generated insights page"""
    if 'garmin_authenticated' not in session:
        return redirect(url_for('login'))
    
    return render_template('insights.html')


@app.route('/api/insights')
def get_insights():
    """API endpoint to fetch AI-generated insights"""
    if 'garmin_authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Re-authenticate to get client
        auth = GarminAuth(session['garmin_email'], session['garmin_password'])
        client = auth.get_client()
        
        if not client:
            return jsonify({'error': 'Failed to connect to Garmin'}), 500
        
        # Fetch metrics
        api = GarminAPI(client)
        all_metrics = api.get_all_metrics()
        
        # Generate insights
        insights_data = analyzer.get_all_insights(all_metrics)
        
        return jsonify(insights_data)
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
