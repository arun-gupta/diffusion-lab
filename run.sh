#!/bin/bash

echo "Starting Storyboard Generator..."
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

# Activate virtual environment and run the app
echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting the application..."
python app.py 