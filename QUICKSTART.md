# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup (One-time)
```bash
# Run the setup script
python setup.py
```

### 2. Activate Virtual Environment
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Run the Application
```bash
# Full version with AI models (recommended)
python app.py

# OR Demo version (no AI models required)
python demo.py
```

## 🎯 What You'll Get

- **Input**: A text prompt describing your scene
- **Output**: 5 AI-generated images showing different moments of your scene
- **Features**: Multiple visual styles, PDF export, progress tracking

## 📝 Example Usage

1. Enter a scene description like:
   - "A detective walks into a neon-lit alley at midnight, rain pouring down"
   - "A robot wanders a post-apocalyptic desert searching for signs of life"

2. Choose a visual style:
   - **Cinematic**: Professional film-style
   - **Anime**: Japanese animation style
   - **Photorealistic**: High-quality photography
   - **Noir**: Classic black and white
   - **Pixar**: 3D animation style

3. Click "Generate Storyboard" and wait for the AI to create your 5-panel storyboard

4. Export to PDF or save the images

## 🔧 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB+ (16GB+ recommended)
- **GPU**: CUDA-compatible GPU recommended (but not required)
- **Storage**: 10GB+ free space for models

## 🆘 Troubleshooting

### Common Issues

**"CUDA not available"**
- This is normal if you don't have a GPU
- The app will run on CPU (slower but functional)

**"Out of memory"**
- Reduce image size in `config.py`
- Close other applications
- Use the demo version for testing

**"Models not downloading"**
- Check your internet connection
- Try running `python demo.py` first to test the UI

### Getting Help

1. Run the test script: `python test_installation.py`
2. Check the logs in the terminal
3. Try the demo version first: `python demo.py`

## 🎨 Customization

Edit `config.py` to customize:
- Image generation settings
- Model parameters
- UI appearance
- Export options

## 📁 File Structure

```
storyboard-generator/
├── app.py              # Main application
├── demo.py             # Demo version
├── config.py           # Configuration
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
├── setup.py           # Setup script
├── test_installation.py # Test script
├── run.sh             # Unix launcher
├── run.bat            # Windows launcher
└── output/            # Generated files
```

## 🎬 Ready to Create?

Open your browser to `http://localhost:7860` and start creating amazing storyboards! 