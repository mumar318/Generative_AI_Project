#!/bin/bash

echo "========================================"
echo "Islamic Chatbot - Starting..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/Scripts/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the chatbot
echo ""
echo "========================================"
echo "Starting Islamic Chatbot"
echo "========================================"
echo ""
python islamic_chatbot.py
