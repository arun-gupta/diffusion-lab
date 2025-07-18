#!/bin/bash
set -e

# Remove Python cache and build artifacts
echo "Removing Python cache and build artifacts..."
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# Remove generated images and uploads
echo "Cleaning up generated images and uploads..."
rm -rf diffusionlab/static/storyboards/*
rm -rf diffusionlab/static/uploads/*

# Remove virtual environment if it exists
echo "Removing old virtual environment (if any)..."
rm -rf venv

# Recreate virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Cleanup and reinstall complete!"
echo "To run the app:"
echo "  python3 -m diffusionlab.api.webapp" 