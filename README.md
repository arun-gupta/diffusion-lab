# Diffusion Lab

A Python application and creative toolkit for generating storyboards, single-image art, and more using Stable Diffusion and AI-powered features.

# ![License](https://img.shields.io/github/license/arun-gupta/diffusion-lab)
# ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

# Table of Contents
- [Main Features](#main-features)
- [Configurable Options](#configurable-options)
- [Quick Start Example](#quick-start-example)
- [Screenshot](#screenshot)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Planned Features](#planned-features)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Main Features

- **Storyboard Mode:** Generate a 5-panel storyboard from a scene description, with AI-generated images and captions.
- **Single-Image Art Mode:** Generate a single, high-quality AI image from a prompt in your chosen style.
- **Image-to-Image (img2img):** Transform sketches, photos, or rough concepts into polished art by uploading an input image and applying AI transformation.
- **Export:** Save storyboards as PDF or images.

## Configurable Options

- **Style Options:** Choose from different visual styles (cinematic, anime, noir, etc.).
- **Demo/AI Mode Toggle:** Choose between fast demo mode (placeholder images) and full AI mode (real Stable Diffusion/StableLM generation) using the toggle above the generation type selector.

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
   python3 -m diffusionlab.api.webapp
   # Then open http://localhost:5001 in your browser
   ```

   **Option B: Gradio Interface**
   ```bash
   python3 -m diffusionlab.tasks.storyboard
   # Then open http://localhost:7860 in your browser
   ```

   **Option C: Demo Version**
   ```bash
   python3 -m diffusionlab.tasks.demo
   ```

## Quick Start Example

```bash
# 1. Start the web application from the project root
python3 -m diffusionlab.api.webapp

# 2. Open your browser and go to:
http://localhost:5001

# 3. Enter a prompt, e.g.:
#   "A robot wanders a post-apocalyptic desert searching for signs of life"
# 4. Select your desired mode and style, then click Generate.
```

## Screenshot

![Diffusion Lab Main UI](docs/main-ui.png)

## Example Outputs

### 📖 Storyboard Generation
**"A detective walks into a neon-lit alley at midnight, rain pouring down"** *(Cinematic style)*

![Sample Storyboard](docs/sample-storyboard.png)

### 🎨 Single-Image Art
**"A spaceship crew encounters an alien artifact on a distant planet"** *(Pixar style)*

![Sample Art](docs/sample-art.png)

### 🔄 Image-to-Image Transformation
**"A polished character design for a sci-fi video game protagonist"** *(Photorealistic style, strength: 0.5)*

<div style="display: flex; gap: 20px; align-items: center;">
  <div style="text-align: center;">
    <strong>Input Image</strong><br>
    <small class="text-muted">(1870×2493 → 1024×1024)</small><br>
    <img src="docs/sample-img2img-input.jpeg" alt="Input Image" style="max-width: 300px; height: auto;">
  </div>
  <div style="text-align: center;">
    <strong>Output Image</strong><br>
    <small class="text-muted">(AI standard size)</small><br>
    <img src="docs/sample-img2img-output.png" alt="Output Image" style="max-width: 300px; height: auto;">
  </div>
</div>

### 🎯 Inpainting (Content-aware Fill)
**Object removal: "Natural landscape continuation with trees and sky"** *(Photorealistic style)*

![Sample Inpainting](docs/sample-inpainting.png)

### 🔗 Prompt Chaining (Story Evolution)
**Character Journey: "A young adventurer's quest from village to mountain peak"** *(Pixar style, 5-step evolution)*

**Template Steps:**
1. Character introduction and setting
2. Character faces a challenge or conflict  
3. Character overcomes the challenge
4. Character learns and grows
5. Character reaches their goal or destination

![Sample Prompt Chaining](docs/sample-promptchaining.png)

<!--
To add your own examples, place images in the docs/ directory and update the paths above.
Examples include: main-ui.png, sample-storyboard.png, sample-art.png, sample-img2img-input.jpeg, sample-img2img-output.png, sample-inpainting.png, sample-promptchaining.png
-->

## How It Works

1. **User Input:**
   - The user enters a scene description or art prompt in the web UI and selects the desired mode (Storyboard, Single-Image Art, Image-to-Image, or Inpainting), style, and Demo/AI mode.
   - For Image-to-Image mode, the user uploads an input image and adjusts the transformation strength.
   - For Inpainting mode, the user uploads an image, draws masks on areas to change, and describes what should fill those areas.
2. **Request Sent to Backend:**
   - The frontend sends the input to the Flask backend via an AJAX request.
   - For img2img, the input image is uploaded separately and processed.
3. **AI Model Processing:**
   - In Demo mode, the backend generates placeholder images and captions.
   - In AI mode, the backend uses Stable Diffusion XL (for images) and StableLM (for captions) to generate real, high-quality outputs based on the prompt and style.
   - For img2img, the AI model transforms the uploaded image according to the prompt and strength setting.
   - For inpainting, the AI model fills masked areas with new content based on the prompt and surrounding context.
4. **Output Generation:**
   - The backend assembles the images (and captions, if storyboard) into a single output image (storyboard or single art piece).
5. **Result Displayed:**
   - The generated image is sent back to the frontend and displayed in the UI, where the user can view or download it.

<!-- Optional: Simple diagram (text-based) -->
```
User Input → [Frontend] → /generate → [Flask Backend]
    └─> [Demo Mode] → Placeholder Images
    └─> [AI Mode] → Stable Diffusion XL + StableLM
        └─> Output Image(s) → [Frontend Display]
```

## Usage

### Web Application (Recommended)
1. Open your browser and go to `http://localhost:5001`
2. Select your desired mode: **Storyboard**, **Single-Image Art**, **Image-to-Image**, or **Inpainting**
3. Use the Demo/AI toggle to choose between fast demo mode and full AI mode
4. Enter your scene description or art prompt in the text box
5. Choose your preferred style from the dropdown
6. **For Image-to-Image mode:**
   - Upload an input image (sketch, photo, or concept)
   - Adjust the transformation strength slider (0.1 = keep original, 1.0 = complete transformation)
7. **For Inpainting mode:**
   - Upload an image to edit
   - Draw masks on areas you want to change using the canvas tools
   - Describe what should fill the masked areas
8. Click "Generate"
9. Download the PNG file or view the results

**Note:** Generated images are saved locally in the `static/storyboards/` directory.

## Image-to-Image (img2img) Usage Guide

### Getting Started with Image-to-Image

The Image-to-Image feature allows you to transform existing images using AI. This is perfect for:
- Converting sketches into finished artwork
- Enhancing or stylizing photographs
- Developing concept art from rough ideas
- Changing image styles while preserving content

> **💡 See the example above**: Check out the "Image-to-Image Example" in the Example Outputs section to see a before/after transformation of a sketch into a detailed oil painting.

### Step-by-Step Process

1. **Select Image-to-Image Mode**
   - Choose "Image-to-Image" from the Generation Type dropdown
   - The image upload section will automatically appear

2. **Upload Your Input Image**
   - Click "Choose File" and select your image
   - Supported formats: JPEG, PNG, GIF, BMP, WebP
   - Maximum file size: 10MB
   - The image will be automatically resized to 512x512 pixels

3. **Adjust Transformation Strength**
   - Use the slider to control how much the AI should transform your image
   - **0.1-0.3**: Subtle changes, preserves most of the original
   - **0.4-0.6**: Moderate transformation, good balance
   - **0.7-0.9**: Significant changes, more creative interpretation
   - **1.0**: Complete transformation, maximum creativity

4. **Write Your Transformation Prompt**
   - Describe what you want the AI to do with your image
   - Be specific about style, mood, and desired changes
   - Example: "Transform this into a cyberpunk cityscape with neon lights"

5. **Choose Your Style**
   - Select from available styles (Cinematic, Anime, Photorealistic, etc.)
   - The style will influence the final appearance

6. **Generate and Download**
   - Click "Generate" to start the transformation
   - Wait for processing (faster in Demo mode, slower in AI mode)
   - Download your transformed image when complete

### Tips for Best Results

- **Start with Clear Images**: Higher quality input images produce better results
- **Use Descriptive Prompts**: Be specific about what you want to change
- **Experiment with Strength**: Try different strength values for the same image
- **Combine with Styles**: Use style presets to enhance your transformations
- **Iterate**: Generate multiple versions and refine your prompts

### Common Use Cases

- **Artists**: Convert rough sketches into finished illustrations
- **Photographers**: Enhance or stylize existing photos
- **Designers**: Develop concepts from basic drawings
- **Content Creators**: Create variations of existing images
- **Students**: Practice art techniques and styles

### Quick Reference

| Input Type | Recommended Strength | Example Prompt |
|------------|---------------------|----------------|
| Pencil Sketch | 0.7-0.9 | "A detailed oil painting with vibrant colors" |
| Blurry Photo | 0.4-0.6 | "A sharp, high-resolution photograph" |
| Portrait | 0.5-0.8 | "A renaissance-style oil painting" |
| Landscape | 0.6-0.9 | "A cyberpunk cityscape with neon lights" |
| Character Design | 0.7-1.0 | "A professional character concept for a video game" |

## Inpainting (Content-aware Fill) Usage Guide

### What is Inpainting?
Inpainting allows you to remove unwanted objects, fill gaps, or replace content in images by drawing masks on areas you want to change and describing what should fill those areas.

### Step-by-Step Instructions

1. **Select Inpainting Mode**
   - Choose "Inpainting (Content-aware Fill)" from the Generation Type dropdown
   - The inpainting interface will automatically appear

2. **Upload Your Image**
   - Click "Choose File" and select your image
   - Supported formats: JPEG, PNG, GIF, BMP, WebP
   - Maximum file size: 10MB
   - The image will be displayed on a drawing canvas

3. **Draw Your Mask**
   - Use the **Brush tool** to mark areas you want to change (red overlay)
   - Use the **Eraser tool** to remove parts of your mask
   - Draw carefully around the edges of objects you want to remove or replace
   - The mask should cover the entire area you want to change

4. **Mask Tools**
   - **Clear Mask**: Remove all masking and start over
   - **Invert Mask**: Switch which areas are masked vs. preserved
   - **Preview**: See how your mask looks before generating

5. **Write Your Inpainting Prompt**
   - Describe what should fill the masked areas
   - Be specific about the content, style, and how it should blend
   - Example: "A beautiful flower garden with colorful blooms"

6. **Choose Your Style**
   - Select from available styles (Cinematic, Anime, Photorealistic, etc.)
   - The style will influence how the new content is generated

7. **Generate and Download**
   - Click "Generate" to start the inpainting process
   - Wait for processing (faster in Demo mode, slower in AI mode)
   - Download your inpainted image when complete

### Tips for Best Results

- **Precise Masking**: Draw masks carefully around object edges for better blending
- **Contextual Prompts**: Describe content that fits naturally with the surrounding area
- **Style Consistency**: Choose a style that matches the original image
- **Iterative Process**: Start with small areas and refine your masks
- **Background Awareness**: Consider what should be behind removed objects
- **Mask Quality**: Use the red brush tool and draw thick, visible strokes for better detection
- **Test Your Mask**: Use the "Test Mask" button to verify your mask is being detected correctly

### Enhanced Mask Processing Features

The inpainting system includes advanced mask detection and processing:

- **Smart Detection**: Uses multiple criteria to detect brush strokes (red channel analysis, alpha validation)
- **Noise Reduction**: Automatically removes small, isolated pixels that aren't part of brush strokes
- **Adaptive Thresholds**: Automatically adjusts detection sensitivity based on mask coverage
- **Morphological Operations**: Cleans up masks by filling holes and removing noise
- **Debug Tools**: Test Mask button shows detailed information about mask detection
- **Fallback Mechanisms**: Works with both original and inverted mask orientations

### Common Use Cases

- **Object Removal**: Remove unwanted people, objects, or blemishes from photos
- **Background Replacement**: Change backgrounds while keeping the main subject
- **Content Addition**: Add new elements like windows, doors, or decorations
- **Art Restoration**: Fill in damaged or missing parts of artwork
- **Creative Editing**: Replace objects with something completely different

### Quick Reference

| Use Case | Mask Strategy | Example Prompt |
|----------|---------------|----------------|
| Object Removal | Mask the object completely | "Natural background continuation" |
| Background Change | Mask around the subject | "A modern office interior" |
| Content Addition | Mask the area to fill | "A cozy fireplace with crackling flames" |
| Art Restoration | Mask damaged areas | "Original artwork continuation" |
| Creative Replacement | Mask the object to replace | "A vintage wooden door with ornate carvings" |

## Prompt Chaining (Story Evolution) Usage Guide

### What is Prompt Chaining?
Prompt Chaining creates a sequence of images that tell a story by generating multiple images based on a series of connected prompts. Each image builds upon the previous one, creating a visual narrative that evolves over time.

### Step-by-Step Instructions

1. **Select Prompt Chaining Mode**
   - Choose "Prompt Chaining (Story Evolution)" from the Generation Type dropdown
   - The prompt chaining interface will automatically appear

2. **Create Your Story Prompts**
   - **Add Steps**: Click "Add Step" to add new prompts to your story
   - **Edit Prompts**: Write descriptive prompts for each step of your story
   - **Remove Steps**: Click the X button to remove unwanted steps
   - **Clear All**: Start over with the "Clear All" button

3. **Use Story Templates**
   - Click "Load Template" to choose from pre-built story structures:
     - **Character Journey**: Follow a character through their adventure
     - **Environmental Progression**: Show how a setting changes over time
     - **Emotional Arc**: Visualize an emotional transformation
     - **Action Sequence**: Create a dynamic action story

4. **Adjust Evolution Settings**
   - **Evolution Strength**: Controls how much each image influences the next (0.0-1.0)
   - **Layout**: Choose how images are arranged (Horizontal, Vertical, Grid)

5. **Choose Your Style**
   - Select from available styles (Cinematic, Anime, Photorealistic, etc.)
   - The style will be applied consistently across all story images

6. **Generate Your Story**
   - Click "Generate" to create your story evolution
   - Wait for processing (faster in Demo mode, slower in AI mode)
   - Download your storyboard when complete

### Tips for Best Results

- **Story Flow**: Create prompts that naturally progress from one to the next
- **Character Consistency**: Keep character descriptions consistent across prompts
- **Environmental Continuity**: Maintain setting details throughout the story
- **Emotional Progression**: Build emotional intensity or resolution over time
- **Action Sequences**: Create clear cause-and-effect relationships
- **Style Consistency**: Use the same style for all images in your story



### Common Use Cases

- **Storytelling**: Create visual narratives for books, comics, or presentations
- **Character Development**: Show character growth and transformation
- **Environmental Stories**: Document how settings change over time
- **Educational Content**: Create step-by-step visual guides
- **Marketing**: Show product evolution or user journey
- **Creative Writing**: Visualize story scenes and progression

### Quick Reference

| Story Type | Evolution Strength | Layout | Example Use |
|------------|-------------------|--------|-------------|
| Character Journey | 0.3-0.5 | Horizontal | Character development stories |
| Environmental | 0.4-0.6 | Grid | Setting transformation |
| Emotional Arc | 0.2-0.4 | Vertical | Emotional storytelling |
| Action Sequence | 0.5-0.7 | Horizontal | Dynamic action stories |

### Gradio Interface
1. Open your browser and go to `http://localhost:7860`
2. Enter your scene description in the text box
3. Choose your preferred style from the dropdown
4. Click "Generate Storyboard"
5. Wait for the AI to generate your 5-panel storyboard
6. Download or view the results

## Example Inputs

### Storyboard & Single-Image Art Prompts
- "A detective walks into a neon-lit alley at midnight, rain pouring down"
- "A robot wanders a post-apocalyptic desert searching for signs of life"
- "A young wizard discovers an ancient library hidden in the mountains"

### Image-to-Image Transformation Examples
- **Sketch to Art**: Upload a pencil sketch + "A detailed oil painting of a majestic dragon in a fantasy landscape"
- **Photo Enhancement**: Upload a blurry photo + "A sharp, professional photograph with enhanced details and vibrant colors"
- **Style Transfer**: Upload a portrait photo + "A renaissance-style oil painting with dramatic lighting and rich textures"
- **Concept Development**: Upload a rough doodle + "A polished character design for a sci-fi video game protagonist"
- **Background Change**: Upload a person photo + "The same person standing in a cyberpunk cityscape at night"

### Inpainting Examples
- **Object Removal**: Mask an unwanted person + "Natural background continuation with trees and sky"
- **Background Replacement**: Mask around a subject + "A modern glass window with city skyline view"
- **Content Addition**: Mask a wall area + "A cozy fireplace with crackling flames and warm lighting"
- **Art Restoration**: Mask damaged areas + "Original artwork continuation matching the existing style"
- **Creative Replacement**: Mask an object + "A vintage wooden door with ornate carvings and brass handle"

### Prompt Chaining Examples
- **Character Journey**: 
  1. "A young knight stands at the castle gates, ready for adventure"
  2. "The knight enters a dark forest, sword drawn and cautious"
  3. "The knight battles a fierce dragon in a clearing"
  4. "The knight emerges victorious, holding the dragon's treasure"
  5. "The knight returns to the castle, hailed as a hero"
- **Environmental Progression**:
  1. "A peaceful village in the morning light"
  2. "Dark clouds gather over the village"
  3. "A storm rages through the village streets"
  4. "The storm passes, leaving destruction behind"
  5. "The village rebuilds, stronger than before"
- **Emotional Arc**:
  1. "A person sits alone in a quiet room, looking thoughtful"
  2. "The person faces a difficult decision, tension visible"
  3. "The person reaches a moment of crisis and despair"
  4. "The person begins to find inner peace and acceptance"
  5. "The person emerges transformed, confident and happy"

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
- Key Dependencies:
  - **PyTorch**: Deep learning framework
  - **Diffusers**: Stable Diffusion models
  - **Transformers**: Language models for captions
  - **Flask**: Web framework
  - **Pillow**: Image processing
  - **NumPy**: Numerical computing
  - **SciPy**: Advanced image processing (for mask operations)

## Planned Features

- **✅ 1. Image-to-Image (img2img):** Transform sketches, photos, or rough concepts into polished art. *(Implemented)*
- **✅ 2. Inpainting (Content-aware Fill):** Remove or replace parts of an image by masking them and describing what should go there. *(Implemented)*
- **3. Outpainting (Image Expansion):** Extend the borders of an image with new, contextually appropriate content.
- **4. Style Transfer:** Apply the style of one image (e.g., a famous painting) to another image.
- **✅ 5. Prompt Chaining / Story Evolution:** Generate a sequence of images that evolve based on a series of prompts. *(Implemented)*
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

## Directory Structure

```
diffusion-lab/
├── diffusionlab/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── setup.py
│   ├── requirements.txt
│   ├── static/
│   ├── templates/
│   ├── api/
│   │   ├── __init__.py
│   │   └── webapp.py
│   └── tasks/
│       ├── __init__.py
│       ├── storyboard.py
│       └── demo.py
├── tests/
│   └── test_installation.py
├── README.md
├── LICENSE
├── QUICKSTART.md
├── WEBAPP_README.md
├── run_webapp.sh
├── run.sh
├── run.bat
├── requirements.txt
├── setup.py
```

- **diffusionlab/**: Main package code, feature modules, static assets, templates, and API logic
- **tests/**: Test scripts
- **README.md, LICENSE, QUICKSTART.md, etc.**: Top-level documentation and legal files
- **run_*.sh, run.bat**: Entrypoint scripts 

## Troubleshooting

### Static Files Not Loading (JS/CSS 404)
- **Symptom:** The UI is broken, or clicking Generate does nothing. Browser console shows 404 for /static/js/app.js or /static/css/style.css.
- **Solution:**
  - Make sure you run the app from the project root with:
    ```bash
    python3 -m diffusionlab.api.webapp
    ```
  - Ensure Flask is configured with the correct static and template folder paths and `static_url_path='/static'`.

### AI Mode Not Available / ImportError
- **Symptom:** Error message: "AI mode is not available. Please ensure diffusionlab/tasks/storyboard.py and dependencies are present."
- **Solution:**
  - Make sure all imports in your code use absolute package paths (e.g., `from diffusionlab.config import *`).
  - Run the app from the project root.
  - Check for typos or missing files in the `diffusionlab/tasks/` directory.

### Accessibility Warning: aria-hidden and Focus
- **Symptom:** Browser console warning: "Blocked aria-hidden on an element because its descendant retained focus..."
- **Solution:**
  - This is a warning, not an error. The app will still work.
  - The app moves focus to the Generate button when the modal closes to improve accessibility.

### No /generate Request When Clicking Generate
- **Symptom:** Nothing happens when clicking Generate, and no request appears in Flask logs.
- **Solution:**
  - Check that `app.js` is loaded (no 404 in Network tab).
  - Check for JavaScript errors in the browser console.
  - Ensure the form and button IDs in the HTML match those in the JS.

### General Tips
- Always run the app from the project root.
- If you make structural changes, restart the Flask server.
- For more help, check the browser console, Flask logs, and the [Issues](https://github.com/arun-gupta/diffusion-lab/issues) page.

### Image-to-Image Specific Issues

**Upload Fails**
- **Symptom**: "Invalid file type" error when uploading images
- **Solution**: Ensure your image is in a supported format (JPEG, PNG, GIF, BMP, WebP)

**File Too Large**
- **Symptom**: "Image file too large" error
- **Solution**: Resize your image to under 10MB before uploading

### Inpainting Specific Issues

**Canvas Not Loading**
- **Symptom**: Drawing canvas doesn't appear after uploading image
- **Solution**: Refresh the page and try uploading again. Ensure JavaScript is enabled.

**Mask Not Drawing**
- **Symptom**: Can't draw on the canvas or mask doesn't appear
- **Solution**: Check that you've selected the Brush tool (should be highlighted). Try refreshing the page.

**Poor Inpainting Results**
- **Symptom**: Generated content doesn't blend well or looks unrealistic
- **Solution**: 
  - Draw more precise masks around object edges
  - Use more descriptive prompts that match the image context
  - Try different styles that complement the original image
  - Start with smaller areas and refine your masks
  - Use the "Test Mask" button to verify your mask is being detected correctly
  - Check the mask coverage percentage in the test results

**Entire Image Being Changed Instead of Masked Areas**
- **Symptom**: The whole image gets transformed instead of just the masked portions
- **Solution**:
  - Use the "Test Mask" button to check if your mask is being detected
  - Ensure you're drawing with the red brush tool (not eraser)
  - Try the inverted mask option if the original mask doesn't work
  - Check that the inpainting pipeline is available in the test results
  - Draw larger, more visible brush strokes for better detection

**Mask Detection Issues**
- **Symptom**: Mask not being detected or very low coverage percentage
- **Solution**:
  - Use pure red brush strokes (the system detects red channel)
  - Draw thicker strokes for better detection
  - Avoid very small, isolated brush strokes
  - Check the debug information in the Test Mask results
  - Try redrawing the mask with more coverage

**Mask Preview Not Working**
- **Symptom**: Preview button doesn't show mask overlay
- **Solution**: Ensure you've drawn a mask first. Try clearing and redrawing the mask.

**No Transformation Effect**
- **Symptom**: Output looks identical to input
- **Solution**: Increase the strength slider value (try 0.7-1.0)

**Too Much Transformation**
- **Symptom**: Output is completely different from input
- **Solution**: Decrease the strength slider value (try 0.1-0.3)

**Poor Quality Results**
- **Symptom**: Transformed image looks blurry or distorted
- **Solution**: 
  - Use higher quality input images
  - Try different strength values
  - Experiment with different style presets
  - Use more descriptive prompts

### How to Check Flask Logs
- When running the app, watch the terminal for error messages or tracebacks after you perform an action in the UI (like clicking Generate).
- 500 errors or ImportErrors will be shown here and can help pinpoint the problem.

### How to Use Browser Developer Tools
- **Open Developer Tools:** Press F12 or right-click and select "Inspect" in your browser.
- **Console Tab:** Shows JavaScript errors, warnings, and logs. Red errors here often indicate why the UI is not working.
- **Network Tab:** Shows all network requests. Look for 404s (missing files) or 500s (server errors) when you click Generate or load the page.
- **Tip:** If you see a request to `/generate` with a 500 error, check the Flask logs for the cause. 

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details. 