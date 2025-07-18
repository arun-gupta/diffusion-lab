#!/bin/bash

echo "🎬 Starting Storyboard Generator Web App..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    python3 setup.py
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please check the error messages above."
        exit 1
    fi
fi

# Activate virtual environment and run the web app
echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting Flask web application..."
echo "🌐 Open your browser to: http://localhost:5001"
echo "📝 This is a demo version - AI models not loaded"
echo "🔧 For full AI generation, run: python app.py"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 webapp.py 