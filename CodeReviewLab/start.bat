@echo off
echo ========================================
echo Vulnerable Web Application - Quick Start
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/4] Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
echo.

echo [4/4] Starting application...
echo.
echo ========================================
echo Application will start on http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
