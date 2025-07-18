# Diffusion Lab

A Python application and creative toolkit for generating storyboards, single-image art, and more using Stable Diffusion and AI-powered features.

## Features

- **Storyboard Mode**: Input a scene description and generate a 5-panel storyboard with AI-generated images and captions.
- **Single-Image Art Mode**: Input a prompt and generate a single, high-quality AI image in your chosen style.
- **Style Options**: Choose from different visual styles (cinematic, anime, noir, etc.)
- **Export**: Save storyboards as PDF or images
- **Demo/AI Mode Toggle**: Choose between fast demo mode (placeholder images) and full AI mode (real Stable Diffusion/StableLM generation) using the toggle above the generation type selector.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arun-gupta/diffusion-lab.git
   cd diffusion-lab
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
2. Select either **Storyboard** or **Single-Image Art** mode
3. Use the Demo/AI toggle to choose between fast demo mode and full AI mode
4. Enter your scene description or art prompt in the text box
5. Choose your preferred style from the dropdown
6. Click "Generate"
7. Download the PNG file or view the results

**Note:** Generated images are saved locally in the `static/storyboards/` directory.

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

## Planned Features

- **1. Image-to-Image (img2img):** Transform sketches, photos, or rough concepts into polished art.
- **2. Inpainting (Content-aware Fill):** Remove or replace parts of an image by masking them and describing what should go there.
- **3. Outpainting (Image Expansion):** Extend the borders of an image with new, contextually appropriate content.
- **4. Style Transfer:** Apply the style of one image (e.g., a famous painting) to another image.
- **5. Prompt Chaining / Story Evolution:** Generate a sequence of images that evolve based on a series of prompts.
- **6. Batch Generation & Variations:** Generate multiple variations for a single prompt to explore creative diversity.
- **7. Animated Diffusion (Frame Interpolation):** Create short animations by generating frames that morph between prompts or images.
- **8. DreamBooth / Custom Subject Training:** Fine-tune Stable Diffusion on a small set of images of a person, pet, or object, so you can generate that subject in any context.
- **9. Text-Guided Image Editing:** Edit an existing image by describing the change in text.
- **10. Super-Resolution / Image Enhancement:** Upscale low-resolution images or enhance details using diffusion-based super-resolution models.
- **11. AI Avatars and Profile Pictures:** Generate unique avatars or profile pictures in various styles from a photo or prompt.
- **12. AI Art Gallery / Curation:** Curate and display the best generations, or let users vote on their favorites.
- **13. API Playground:** Let users experiment with all Stable Diffusion parameters (guidance scale, steps, seed, etc.).
- **14. Prompt Engineering Tools:** Help users craft better prompts with suggestions, negative prompts, and prompt templates.
- **15. Model Comparison:** Let users compare outputs from different Stable Diffusion checkpoints or custom models.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details. 