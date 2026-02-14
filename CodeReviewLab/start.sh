# Quick Start Script for Unix/Linux/Mac
#!/bin/bash

echo "========================================"
echo "Vulnerable Web Application - Quick Start"
echo "========================================"
echo

echo "[1/4] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed"
    exit 1
fi
echo

echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo

echo "[3/4] Initializing database..."
python3 init_db.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize database"
    exit 1
fi
echo

echo "[4/4] Starting application..."
echo
echo "========================================"
echo "Application will start on http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

python3 app.py
