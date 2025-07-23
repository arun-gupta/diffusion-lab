# Usage Guide

Detailed instructions for using all features of Diffusion Lab.

## Table of Contents
- [Web Application Usage](#web-application-usage)
- [Batch Generation Guide](#batch-generation-guide)
- [Image-to-Image (img2img) Guide](#image-to-image-img2img-guide)
- [Inpainting Guide](#inpainting-guide)
- [ControlNet Guide](#controlnet-guide)
- [Prompt Chaining Guide](#prompt-chaining-guide)
- [Example Prompts](#example-prompts)
- [Technical Details](#technical-details)

## Web Application Usage

### Getting Started
1. Open your browser and go to `http://localhost:5001`
2. Select your desired mode: **Storyboard**, **Single-Image Art**, **Batch Generation**, **Image-to-Image**, or **Inpainting**
3. Use the Demo/AI toggle to choose between fast demo mode and full AI mode
4. Enter your scene description or art prompt in the text box
5. Choose your preferred style from the dropdown
6. Click "Generate"
7. Download the PNG file or view the results

**Note:** Generated images are saved locally in the `static/storyboards/` directory.

## Batch Generation Guide

### What is Batch Generation?
Batch Generation creates multiple variations of the same prompt, allowing you to explore creative diversity and choose the best result. It's perfect for finding the perfect interpretation of your idea.

### Step-by-Step Instructions

1. **Select Batch Generation Mode**
   - Choose "Batch Generation (Multiple Variations)" from the Generation Type dropdown
   - The batch generation interface will automatically appear

2. **Configure Your Batch Settings**
   - **Number of Variations**: Choose how many variations to generate (2-8)
   - **Layout**: Select how to arrange the results (Grid, Horizontal, Vertical)
   - **Variation Strength**: Control how different the variations are (0.1-1.0)

3. **Enter Your Prompt**
   - Write a descriptive prompt for your scene
   - The same prompt will be used for all variations with slight parameter adjustments

4. **Choose Your Style**
   - Select from available styles (Cinematic, Anime, Photorealistic, etc.)
   - The style will be applied consistently across all variations

5. **Generate Your Variations**
   - Click "Generate" to create your batch
   - Wait for processing (faster in Demo mode, slower in AI mode)
   - Download your batch results when complete

### Tips for Best Results

- **Clear Prompts**: Use detailed, specific prompts for better variation quality
- **Style Consistency**: Choose a style that matches your creative vision
- **Variation Strength**: Use lower values (0.1-0.3) for subtle variations, higher values (0.7-1.0) for dramatic differences
- **Batch Size**: Start with 4 variations for a good balance of options and generation time
- **Layout Choice**: Grid layout works well for comparing variations, horizontal/vertical for sequential viewing

### Common Use Cases

- **Concept Exploration**: Generate multiple interpretations of a character or scene
- **Style Testing**: See how different parameters affect the same prompt
- **Creative Selection**: Create a pool of options to choose the best result
- **Iterative Design**: Use variations as starting points for further refinement
- **Client Presentations**: Show multiple options to stakeholders

### Quick Reference

| Variation Count | Generation Time | Best For |
|-----------------|-----------------|----------|
| 2-3 | Fast | Quick exploration |
| 4-6 | Medium | Balanced options |
| 7-8 | Slow | Comprehensive exploration |

## Image-to-Image (img2img) Guide

### What is Image-to-Image?
Image-to-Image allows you to transform existing images using AI. This is perfect for:
- Converting sketches into finished artwork
- Enhancing or stylizing photographs
- Developing concept art from rough ideas
- Changing image styles while preserving content

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

## Inpainting Guide

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

## ControlNet Guide

### What is ControlNet?
ControlNet provides precise control over image generation by using reference images to guide the AI's understanding of composition, structure, and spatial relationships. It's perfect for:
- Maintaining specific poses or layouts from reference images
- Creating consistent architectural or structural elements
- Controlling the spatial arrangement of objects
- Ensuring precise line work or edge detection
- Maintaining depth and perspective relationships

### Step-by-Step Instructions

1. **Select ControlNet Mode**
   - Choose "ControlNet (Precise Control)" from the Generation Type dropdown
   - The ControlNet interface will automatically appear

2. **Upload Your Reference Image**
   - Click "Choose File" in the Reference Image section
   - Select an image that represents the structure or composition you want to control
   - Supported formats: JPEG, PNG, GIF, BMP, WebP
   - Maximum file size: 10MB

3. **Choose Control Type**
   - **Canny Edge Detection**: Best for line art, architectural drawings, precise outlines
   - **Depth Map**: Ideal for 3D scenes, architectural visualization, spatial control
   - **Human Pose**: Perfect for character poses, figure drawing, animation
   - **Semantic Segmentation**: Great for object placement, scene composition, layout control

4. **Adjust Control Parameters**
   - **Control Strength**: Controls how much the reference image influences generation (0.0-2.0)
     - 0.0: No control (regular generation)
     - 1.0: Full control (follows reference closely)
     - 2.0: Strong control (strict adherence to reference)
   - **Guidance Start**: When to start applying control (0.0-1.0)
     - 0.0: Apply control from the beginning
     - 1.0: Apply control only at the end
   - **Guidance End**: When to stop applying control (0.0-1.0)
     - 0.0: Stop control at the beginning
     - 1.0: Apply control until the end

5. **Enter Your Prompt**
   - Write a descriptive prompt for what you want to generate
   - The prompt will work with the reference image to create the final result
   - Be specific about style, content, and artistic direction

6. **Choose Your Style**
   - Select from available styles (Cinematic, Anime, Photorealistic, etc.)
   - The style will be applied while respecting the control image structure

7. **Generate Your Image**
   - Click "Generate" to create your controlled image
   - Wait for processing (faster in Demo mode, slower in AI mode)
   - Download your result when complete

### Tips for Best Results

- **Reference Quality**: Use clear, high-contrast reference images for better control
- **Control Type Matching**: Choose the control type that matches your reference image characteristics
- **Strength Balance**: Start with 1.0 strength and adjust based on results
- **Prompt Alignment**: Ensure your prompt aligns with what the reference image suggests
- **Style Consistency**: Choose styles that work well with your reference image type
- **Guidance Timing**: Use default guidance settings (0.0-1.0) for most cases

### Common Use Cases

- **Character Poses**: Use pose reference images to maintain specific character positions
- **Architectural Design**: Control building layouts and structural elements
- **Line Art Conversion**: Transform sketches into finished artwork while preserving lines
- **Composition Control**: Maintain specific spatial arrangements and layouts
- **Depth Control**: Create images with precise depth and perspective relationships
- **Object Placement**: Control where and how objects are positioned in the scene

### Quick Reference

| Control Type | Best For | Strength Range | Example Use |
|--------------|----------|----------------|-------------|
| Canny Edge | Line art, architecture | 0.8-1.2 | Converting sketches to finished art |
| Depth Map | 3D scenes, spatial control | 0.7-1.1 | Architectural visualization |
| Human Pose | Character poses | 0.9-1.3 | Figure drawing, animation |
| Segmentation | Object placement | 0.6-1.0 | Scene composition control |

### Troubleshooting

- **Weak Control**: Increase control strength or check reference image quality
- **Over-Control**: Reduce control strength or adjust guidance timing
- **Poor Results**: Try different control types or reference images
- **Memory Issues**: Use Demo mode or reduce image resolution
- **Import Errors**: Ensure `opencv-python` and `controlnet-aux` are installed

## Prompt Chaining Guide

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

## Example Prompts

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

### ControlNet Examples
- **Canny Edge Control**: Upload line art + "A majestic dragon in a fantasy landscape with detailed scales and wings"
- **Depth Map Control**: Upload architectural blueprint + "A futuristic cityscape with towering skyscrapers and flying cars"
- **Human Pose Control**: Upload pose reference + "A heroic warrior in medieval armor standing proudly"
- **Segmentation Control**: Upload layout sketch + "A cozy living room with fireplace, bookshelves, and comfortable furniture"

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

### How It Works

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

### System Architecture

```
User Input → [Frontend] → /generate → [Flask Backend]
    └─> [Demo Mode] → Placeholder Images
    └─> [AI Mode] → Stable Diffusion XL + StableLM
        └─> Output Image(s) → [Frontend Display]
```

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

### Key Dependencies
- **PyTorch**: Deep learning framework
- **Diffusers**: Stable Diffusion models
- **Transformers**: Language models for captions
- **Flask**: Web framework
- **Pillow**: Image processing
- **NumPy**: Numerical computing
- **SciPy**: Advanced image processing (for mask operations) 