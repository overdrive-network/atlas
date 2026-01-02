# 💪 Garmin Health Dashboard

A comprehensive Streamlit web application that connects to your Garmin device, fetches health metrics, visualizes them with interactive charts, and provides AI-powered insights to help you understand and improve your health.

## Features

- 🔐 **Garmin Connect Integration**: Simple credential-based authentication
- 📊 **Health Metrics Dashboard**: Real-time visualization of all your health data
- 📈 **Interactive Charts**: Weekly trends with Plotly visualizations
- 🤖 **AI-Powered Insights**: Personalized health analysis using OpenAI
- 🎨 **Modern UI**: Clean, responsive Streamlit interface optimized for all devices
- 🪟 **Windows-Friendly**: Easy one-click startup with `run.bat`
- ⚡ **Fast & Simple**: Pure Python with Streamlit - no HTML/CSS/JavaScript needed!

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
   ```

4. **Run the application**
   ```batch
   run.bat
   ```
   
   That's it! The application will:
   - Create a virtual environment (first time only)
   - Install all dependencies
   - Start the Streamlit server
   - Open your browser automatically

5. **Access the app** - Your browser will open automatically to the Streamlit app

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
streamlit run app.py
```

The app will open automatically in your browser (typically at `http://localhost:8501`)

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Garmin Connect Credentials
GARMIN_EMAIL=your_garmin_email@example.com
GARMIN_PASSWORD=your_garmin_password

# OpenAI API Key (Optional - for AI insights)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Security Notes

- **Never commit your `.env` file** - It's already in `.gitignore`
- Your Garmin credentials are stored in session state during use only
- OpenAI API is optional - basic insights will work without it

## Usage

### 1. Login
- The app will show a login page on first launch
- Enter your Garmin Connect credentials
- Or leave fields empty if you've set credentials in `.env`

### 2. Dashboard
- View today's key metrics (steps, heart rate, sleep, calories)
- Explore weekly trends with interactive Plotly charts
- Monitor your progress over time in beautiful visualizations

### 3. AI Insights
- Click "🤖 Insights" in the sidebar
- Get personalized analysis for:
  - **Today**: Current day recommendations
  - **Yesterday**: Performance review
  - **Last Month**: Long-term trends and patterns
- AI provides actionable health recommendations

### 4. Settings
- View your account information
- Access configuration details
- Logout when done

## Project Structure

```
├── app.py                    # Main Streamlit application (everything in one file!)
├── requirements.txt          # Python dependencies
├── run.bat                   # Windows batch file for easy startup
├── .env.example              # Environment variables template
├── README.md                 # This file
│
├── garmin/
│   ├── __init__.py
│   ├── auth.py               # Garmin authentication
│   └── api.py                # Health data fetching with caching
│
└── ai/
    ├── __init__.py
    └── analyzer.py           # AI-powered insights
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

### Streamlit port issues
- Default port is 8501
- If already in use, Streamlit will automatically try the next available port
- You can specify a custom port: `streamlit run app.py --server.port 8502`

## Dependencies

- **Streamlit** - Modern web framework for data apps
- **python-garminconnect** - Garmin API client
- **OpenAI** - AI insights generation
- **python-dotenv** - Environment variable management
- **Plotly** - Interactive data visualizations
- **Pandas** - Data manipulation

## Development

### Adding New Metrics

1. Update `garmin/api.py` to fetch additional data
2. Modify `app.py` dashboard to display new metrics
3. Add new chart functions using Plotly

### Customizing AI Insights

Edit `ai/analyzer.py` to modify:
- Prompt templates
- Analysis criteria
- Output formatting

## Key Advantages of Streamlit

✅ **No HTML/CSS/JavaScript** - Pure Python development  
✅ **No Secret Keys** - Streamlit handles sessions automatically  
✅ **Built-in Widgets** - Forms, charts, and UI components out of the box  
✅ **Auto-reload** - Changes reflect instantly during development  
✅ **Easy Deployment** - Deploy to Streamlit Cloud with one click

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
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Plotly](https://plotly.com/) for beautiful interactive charts
- [OpenAI](https://openai.com/) for AI capabilities

---

**Stay healthy! 💪**
