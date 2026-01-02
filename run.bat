@echo off
echo ========================================
echo  Garmin Health Web App Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python 3.8+ is installed and in PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create a .env file with your credentials.
    echo You can copy .env.example and fill in your details:
    echo   copy .env.example .env
    echo.
    echo The app will still run, but you'll need to enter credentials manually.
    echo.
    pause
)

REM Start Flask application
echo.
echo Starting Garmin Health Web App...
echo The app will be available at: http://localhost:5000
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Run the Flask app
python app.py

REM If we reach here, the app has stopped
echo.
echo App stopped.
pause
