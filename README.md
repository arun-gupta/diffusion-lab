# Storyboard Generator

A Python application that transforms short scripts or ideas into 5-panel storyboards using Stable Diffusion and AI-generated captions.

## Features

- **Input**: Single prompt (1-2 sentences describing a scene)
- **Output**: 5 generated images representing different moments of the scene
- **AI Captions**: Each image comes with a descriptive caption
- **Style Options**: Choose from different visual styles (cinematic, anime, noir, etc.)
- **Export**: Save storyboards as PDF or images

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd storyboard-generator
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   **Option A: Web Application (Recommended)**
   ```bash
   python3 webapp.py
   # Then open http://localhost:5001 in your browser
   ```

   **Option B: Gradio Interface**
   ```bash
   python app.py
   # Then open http://localhost:7860 in your browser
   ```

   **Option C: Demo Version**
   ```bash
   python demo.py
   ```

## Usage

### Web Application (Recommended)
1. Open your browser and go to `http://localhost:5001`
2. Enter your scene description in the text box
3. Choose your preferred style from the dropdown
4. Click "Generate Storyboard"
5. Watch the progress bar as your storyboard is created
6. Download the PNG file or view the results

### Gradio Interface
1. Open your browser and go to `http://localhost:7860`
2. Enter your scene description in the text box
3. Choose your preferred style from the dropdown
4. Click "Generate Storyboard"
5. Wait for the AI to generate your 5-panel storyboard
6. Download or view the results

## Example Inputs

- "A detective walks into a neon-lit alley at midnight, rain pouring down"
- "A robot wanders a post-apocalyptic desert searching for signs of life"
- "A young wizard discovers an ancient library hidden in the mountains"

## Technical Details

### Web Application
- **Backend**: Flask web framework with RESTful API
- **Frontend**: Modern HTML5/CSS3/JavaScript with Bootstrap 5
- **Image Processing**: PIL/Pillow for image generation and manipulation
- **Real-time Updates**: AJAX-powered interface with progress tracking

### Gradio Interface
- **Image Generation**: Uses Stable Diffusion XL for high-quality image generation
- **Caption Generation**: Uses StableLM for contextual descriptions
- **UI Framework**: Gradio for a clean, web-based interface
- **Export**: PDF generation with reportlab

## Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended for faster generation)
- 8GB+ RAM
- Internet connection for model downloads

## License

This project is licensed under the MIT License - see the LICENSE file for details. 