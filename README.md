# 💪 Garmin Health Web App

A comprehensive web application that connects to your Garmin device, fetches health metrics, visualizes them with interactive charts, and provides AI-powered insights to help you understand and improve your health.

## Features

- 🔐 **Garmin Connect Integration**: Secure OAuth authentication
- 📊 **Health Metrics Dashboard**: Real-time visualization of all your health data
- 📈 **Interactive Charts**: Weekly and monthly trends with Chart.js
- 🤖 **AI-Powered Insights**: Personalized health analysis using OpenAI
- 🎨 **Modern UI**: Clean, responsive design optimized for all devices
- 🪟 **Windows-Friendly**: Easy one-click startup with `run.bat`

## Health Metrics Tracked

- ❤️ Heart rate (resting & active)
- 😴 Sleep data (duration, stages, quality)
- 🚶 Steps and distance
- 😰 Stress levels
- 🔋 Body battery
- 💓 HRV (Heart Rate Variability)
- 🔥 Calories burned
- 🏃 Activity/workout data
- ⚖️ Weight/body composition (if available)

## Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Garmin Connect Account** - Sign up at [Garmin Connect](https://connect.garmin.com/)
- **OpenAI API Key** (Optional) - For AI insights, get one from [OpenAI](https://platform.openai.com/api-keys)

## Quick Start (Windows)

1. **Clone or download this repository**

2. **Create your configuration file**
   ```batch
   copy .env.example .env
   ```

3. **Edit `.env` file** with your credentials:
   ```env
   GARMIN_EMAIL=your_email@example.com
   GARMIN_PASSWORD=your_garmin_password
   OPENAI_API_KEY=sk-your-openai-api-key
   FLASK_SECRET_KEY=your-secret-key
   ```

4. **Run the application**
   ```batch
   run.bat
   ```
   
   That's it! The application will:
   - Create a virtual environment (first time only)
   - Install all dependencies
   - Start the web server
   - Open your browser automatically

5. **Access the app** at `http://localhost:5000`

## Manual Setup (All Platforms)

### Installation

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   
   **Windows:**
   ```batch
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

### Running the App

```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Garmin Connect Credentials
GARMIN_EMAIL=your_garmin_email@example.com
GARMIN_PASSWORD=your_garmin_password

# OpenAI API Key (Optional - for AI insights)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here-change-in-production
FLASK_DEBUG=True
```

### Security Notes

- **Never commit your `.env` file** - It's already in `.gitignore`
- **Change the `FLASK_SECRET_KEY`** in production
- Your Garmin credentials are only stored in the session during use
- OpenAI API is optional - basic insights will work without it

## Usage

### 1. Login
- Navigate to `http://localhost:5000`
- Enter your Garmin Connect credentials
- Or leave fields empty if you've set credentials in `.env`

### 2. Dashboard
- View today's key metrics (steps, heart rate, sleep, calories)
- Explore weekly trends with interactive charts
- Monitor your progress over time

### 3. AI Insights
- Click "AI Insights" in the navigation
- Get personalized analysis for:
  - **Today**: Current day recommendations
  - **Yesterday**: Performance review
  - **Last Month**: Long-term trends and patterns

## Project Structure

```
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── run.bat                   # Windows launcher
├── .env.example              # Environment variables template
├── README.md                 # This file
│
├── garmin/
│   ├── __init__.py
│   ├── auth.py               # Garmin OAuth authentication
│   └── api.py                # Health data fetching
│
├── ai/
│   ├── __init__.py
│   └── analyzer.py           # AI-powered insights
│
├── static/
│   ├── css/
│   │   └── styles.css        # Application styles
│   └── js/
│       └── charts.js         # Chart.js visualizations
│
└── templates/
    ├── base.html             # Base template
    ├── login.html            # Login page
    ├── index.html            # Dashboard
    └── insights.html         # AI insights
```

## Troubleshooting

### Python not found
- Make sure Python 3.8+ is installed
- Add Python to your system PATH
- Restart your terminal/command prompt

### Garmin authentication fails
- Verify your email and password are correct
- Check if you can login at [Garmin Connect](https://connect.garmin.com/)
- Some accounts with 2FA may have issues - try creating an app-specific password

### OpenAI API errors
- Verify your API key is correct
- Check your OpenAI account has available credits
- The app will work without OpenAI, providing basic insights

### Port 5000 already in use
- Another application is using port 5000
- Stop the other application or change the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
  ```

## Dependencies

- **Flask** - Web framework
- **python-garminconnect** - Garmin API client
- **OpenAI** - AI insights generation
- **python-dotenv** - Environment variable management
- **Chart.js** - Frontend data visualization

## Development

### Adding New Metrics

1. Update `garmin/api.py` to fetch additional data
2. Modify the dashboard template to display new metrics
3. Update chart configurations in `static/js/charts.js`

### Customizing AI Insights

Edit `ai/analyzer.py` to modify:
- Prompt templates
- Analysis criteria
- Output formatting

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check the Troubleshooting section above
2. Review [Garmin Connect API documentation](https://github.com/cyberjunky/python-garminconnect)
3. Open an issue in this repository

## Acknowledgments

- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) for Garmin API integration
- [Chart.js](https://www.chartjs.org/) for beautiful charts
- [OpenAI](https://openai.com/) for AI capabilities

---

**Stay healthy! 💪**
