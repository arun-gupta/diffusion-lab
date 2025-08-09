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

# Check if port 5001 is already in use and clean it up
echo "Checking for existing processes on port 5001..."
EXISTING_PID=$(lsof -ti :5001)
if [ ! -z "$EXISTING_PID" ]; then
    echo "🔧 Found existing process on port 5001 (PID: $EXISTING_PID)"
    echo "🛑 Stopping existing process..."
    kill -9 $EXISTING_PID 2>/dev/null || true
    sleep 2
    echo "✅ Port 5001 cleared"
else
    echo "✅ Port 5001 is available"
fi

# Activate virtual environment and run the web app
echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting Flask web application..."
echo "🌐 Opening browser to: http://localhost:5001"
echo "🚀 AI-powered diffusion models ready for generation"
echo "✨ Ready to create amazing AI-generated art and storyboards!"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the webapp in the background briefly to allow browser to open
python3 -m diffusionlab.api.webapp &
WEBAPP_PID=$!

# Wait a moment for the server to start
sleep 3

# Open the URL in the default browser
if command -v open >/dev/null 2>&1; then
    # macOS
    open http://localhost:5001
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open http://localhost:5001
elif command -v start >/dev/null 2>&1; then
    # Windows (Git Bash/WSL)
    start http://localhost:5001
else
    echo "⚠️  Could not detect browser command. Please open http://localhost:5001 manually."
fi

echo "🚀 Browser should now open automatically!"
echo "   If not, manually open: http://localhost:5001"

# Bring the webapp back to foreground
wait $WEBAPP_PID 