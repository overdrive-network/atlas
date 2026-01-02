"""Main Streamlit application for Garmin Health Web App"""
import streamlit as st
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from garmin.auth import GarminAuth
from garmin.api import GarminAPI
from ai.analyzer import HealthAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Garmin Health Dashboard",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for health-focused color scheme
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'garmin_email' not in st.session_state:
    st.session_state.garmin_email = ""
if 'garmin_password' not in st.session_state:
    st.session_state.garmin_password = ""
if 'garmin_client' not in st.session_state:
    st.session_state.garmin_client = None


def login_page():
    """Display login page"""
    st.title("🔐 Garmin Health Dashboard")
    st.markdown("### Sign in with your Garmin Connect credentials")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input(
                "Email",
                value=os.getenv('GARMIN_EMAIL', ''),
                placeholder="your-email@example.com"
            )
            password = st.text_input(
                "Password",
                type="password",
                value=os.getenv('GARMIN_PASSWORD', ''),
                placeholder="Your Garmin password"
            )
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("❌ Please provide both email and password")
                else:
                    with st.spinner("Authenticating with Garmin Connect..."):
                        auth = GarminAuth(email, password)
                        client = auth.login()
                        
                        if client:
                            st.session_state.authenticated = True
                            st.session_state.garmin_email = email
                            st.session_state.garmin_password = password
                            st.session_state.garmin_client = client
                            logger.info(f"User logged in: {email}")
                            st.success("✅ Successfully authenticated!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to authenticate. Please check your credentials.")
        
        # Information box
        st.info("💡 **Tip**: You can store your credentials in a `.env` file to avoid entering them each time.")


def get_garmin_client():
    """Get or create Garmin client"""
    if st.session_state.garmin_client is None:
        auth = GarminAuth(st.session_state.garmin_email, st.session_state.garmin_password)
        client = auth.get_client()
        st.session_state.garmin_client = client
    return st.session_state.garmin_client


def display_metric_card(label, value, delta=None, delta_color="normal"):
    """Display a metric card"""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


def create_heart_rate_chart(weekly_data):
    """Create heart rate trend chart"""
    if not weekly_data:
        return None
    
    df = pd.DataFrame(weekly_data)
    df = df.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['resting_heart_rate'],
        mode='lines+markers',
        name='Resting Heart Rate',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Resting Heart Rate Trend (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Heart Rate (bpm)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_steps_chart(weekly_data):
    """Create steps bar chart"""
    if not weekly_data:
        return None
    
    df = pd.DataFrame(weekly_data)
    df = df.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['steps'],
        name='Steps',
        marker_color='#3498db',
        text=df['steps'],
        textposition='outside'
    ))
    
    # Add goal line
    fig.add_hline(y=10000, line_dash="dash", line_color="green", 
                  annotation_text="Goal: 10,000 steps")
    
    fig.update_layout(
        title="Daily Steps (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Steps",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_sleep_chart(weekly_data):
    """Create sleep bar chart"""
    if not weekly_data:
        return None
    
    df = pd.DataFrame(weekly_data)
    df = df.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['sleep_hours'],
        name='Sleep Hours',
        marker_color='#9b59b6',
        text=df['sleep_hours'].apply(lambda x: f"{x:.1f}h"),
        textposition='outside'
    ))
    
    # Add recommended sleep range
    fig.add_hrect(y0=7, y1=9, line_width=0, fillcolor="green", opacity=0.1,
                  annotation_text="Recommended: 7-9h", annotation_position="top right")
    
    fig.update_layout(
        title="Sleep Duration (Last 7 Days)",
        xaxis_title="Date",
        yaxis_title="Hours",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def dashboard_page():
    """Display main dashboard"""
    st.title("📊 Health Dashboard")
    
    # Get Garmin client
    client = get_garmin_client()
    if not client:
        st.error("Failed to connect to Garmin. Please log in again.")
        st.session_state.authenticated = False
        st.rerun()
        return
    
    # Fetch metrics
    with st.spinner("📡 Fetching your health data..."):
        try:
            api = GarminAPI(client)
            metrics = api.get_all_metrics()
            
            if not metrics:
                st.error("Failed to fetch metrics. Please try again.")
                return
            
            today_metrics = metrics.get('today', {})
            weekly_metrics = metrics.get('week', [])
            
            # Today's Overview
            st.markdown("### 🎯 Today's Overview")
            st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
            
            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                steps = today_metrics.get('steps', 0)
                display_metric_card(
                    "🚶 Steps",
                    f"{steps:,}",
                    delta=f"Goal: 10,000" if steps < 10000 else "✓ Goal reached!"
                )
            
            with col2:
                distance = today_metrics.get('distance', 0)
                display_metric_card(
                    "🛤️ Distance",
                    f"{distance:.2f} km",
                    delta=None
                )
            
            with col3:
                calories = today_metrics.get('calories', 0)
                display_metric_card(
                    "🔥 Calories",
                    f"{calories:,}",
                    delta=None
                )
            
            with col4:
                sleep_data = today_metrics.get('sleep', {})
                sleep_hours = sleep_data.get('total_hours', 0)
                display_metric_card(
                    "😴 Sleep",
                    f"{sleep_hours:.1f}h",
                    delta="Good" if sleep_hours >= 7 else "Need more"
                )
            
            # Second row of metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                hr_data = today_metrics.get('heart_rate', {})
                resting_hr = hr_data.get('restingHeartRate', 'N/A')
                display_metric_card(
                    "❤️ Resting HR",
                    f"{resting_hr} bpm" if resting_hr != 'N/A' else 'N/A',
                    delta=None
                )
            
            with col2:
                body_battery = today_metrics.get('body_battery', 'N/A')
                display_metric_card(
                    "🔋 Body Battery",
                    str(body_battery) if body_battery != 'N/A' else 'N/A',
                    delta=None
                )
            
            with col3:
                stress = today_metrics.get('stress', {})
                avg_stress = stress.get('avgStressLevel', 'N/A') if isinstance(stress, dict) else 'N/A'
                display_metric_card(
                    "😰 Stress Level",
                    str(avg_stress) if avg_stress != 'N/A' else 'N/A',
                    delta=None
                )
            
            with col4:
                if sleep_data:
                    quality = sleep_data.get('quality', 0)
                    display_metric_card(
                        "🌙 Sleep Quality",
                        f"{quality}/100",
                        delta=None
                    )
                else:
                    display_metric_card("🌙 Sleep Quality", "N/A", delta=None)
            
            # Charts section
            st.markdown("---")
            st.markdown("### 📈 Weekly Trends")
            
            # Create tabs for different charts
            tab1, tab2, tab3 = st.tabs(["Steps", "Heart Rate", "Sleep"])
            
            with tab1:
                steps_chart = create_steps_chart(weekly_metrics)
                if steps_chart:
                    st.plotly_chart(steps_chart, use_container_width=True)
                else:
                    st.info("No step data available for the past week")
            
            with tab2:
                hr_chart = create_heart_rate_chart(weekly_metrics)
                if hr_chart:
                    st.plotly_chart(hr_chart, use_container_width=True)
                else:
                    st.info("No heart rate data available for the past week")
            
            with tab3:
                sleep_chart = create_sleep_chart(weekly_metrics)
                if sleep_chart:
                    st.plotly_chart(sleep_chart, use_container_width=True)
                else:
                    st.info("No sleep data available for the past week")
            
        except Exception as e:
            logger.error(f"Error fetching metrics: {str(e)}")
            st.error(f"Error fetching data: {str(e)}")


def insights_page():
    """Display AI-powered insights"""
    st.title("🤖 AI-Powered Insights")
    st.markdown("Get personalized health analysis and recommendations")
    
    # Get Garmin client
    client = get_garmin_client()
    if not client:
        st.error("Failed to connect to Garmin. Please log in again.")
        st.session_state.authenticated = False
        st.rerun()
        return
    
    # Check if OpenAI API key is configured
    openai_key = os.getenv('OPENAI_API_KEY', '')
    if not openai_key:
        st.warning("⚠️ OpenAI API key not configured. Basic insights will be provided.")
    
    # Fetch metrics
    with st.spinner("📡 Fetching your health data..."):
        try:
            api = GarminAPI(client)
            metrics = api.get_all_metrics()
            
            if not metrics:
                st.error("Failed to fetch metrics. Please try again.")
                return
    
    # Generate insights
    with st.spinner("🧠 Analyzing your health data with AI..."):
        try:
            analyzer = HealthAnalyzer(openai_key)
            insights = analyzer.get_all_insights(metrics)
            
            # Display insights in expandable sections
            st.markdown("---")
            
            # Today's insights
            if 'today' in insights:
                with st.expander("📅 Today's Analysis", expanded=True):
                    st.markdown(insights['today'])
            
            # Yesterday's insights
            if 'yesterday' in insights:
                with st.expander("📆 Yesterday's Review", expanded=False):
                    st.markdown(insights['yesterday'])
            
            # Monthly insights
            if 'month' in insights:
                with st.expander("📊 Last Month's Trends", expanded=False):
                    st.markdown(insights['month'])
            
            # Additional tips
            st.markdown("---")
            st.info("💡 **Pro Tip**: Check your insights daily to track your progress and identify patterns in your health metrics!")
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            st.error(f"Error generating insights: {str(e)}")


def settings_page():
    """Display settings page"""
    st.title("⚙️ Settings")
    
    st.markdown("### Account Information")
    st.text_input("Garmin Email", value=st.session_state.garmin_email, disabled=True)
    
    st.markdown("---")
    
    st.markdown("### Configuration")
    st.info("""
    **Environment Variables:**
    - `GARMIN_EMAIL`: Your Garmin Connect email
    - `GARMIN_PASSWORD`: Your Garmin Connect password
    - `OPENAI_API_KEY`: Your OpenAI API key (optional)
    
    Configure these in your `.env` file for automatic login.
    """)
    
    st.markdown("---")
    
    st.markdown("### About")
    st.markdown("""
    **Garmin Health Dashboard** v2.0
    
    A comprehensive health tracking application built with Streamlit that:
    - Connects to your Garmin device
    - Visualizes your health metrics
    - Provides AI-powered insights
    
    Powered by:
    - Streamlit
    - python-garminconnect
    - OpenAI
    - Plotly
    """)
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", type="primary"):
        st.session_state.authenticated = False
        st.session_state.garmin_client = None
        st.session_state.garmin_email = ""
        st.session_state.garmin_password = ""
        st.success("Successfully logged out!")
        st.rerun()


def main():
    """Main application"""
    
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.title("💪 Garmin Health")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🤖 Insights", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown(f"**Logged in as:**")
        st.text(st.session_state.garmin_email)
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.markdown(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    
    # Route to appropriate page
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "🤖 Insights":
        insights_page()
    elif page == "⚙️ Settings":
        settings_page()


if __name__ == '__main__':
    main()
