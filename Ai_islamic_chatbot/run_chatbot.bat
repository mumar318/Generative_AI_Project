@echo off
echo ========================================
echo Islamic Chatbot - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run the chatbot
echo.
echo ========================================
echo Starting Islamic Chatbot
echo ========================================
echo.
python islamic_chatbot.py

pause
