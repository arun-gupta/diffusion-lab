#!/usr/bin/env python3
"""
Flask Web Application for Storyboard Generator
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import time
import io
import base64
from datetime import datetime
import json
from werkzeug.utils import secure_filename
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'diffusionlab', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'diffusionlab', 'static'),
    static_url_path='/static'
)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def get_project_root():
    """Get the absolute path to the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_storyboards_dir():
    """Get the absolute path to the storyboards directory"""
    project_root = get_project_root()
    return os.path.join(project_root, 'static', 'storyboards')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
storyboards_dir = get_storyboards_dir()
os.makedirs(storyboards_dir, exist_ok=True)

# Configuration
STYLES = {
    'cinematic': {
        'name': 'Cinematic',
        'description': 'Professional film-style with dramatic lighting',
        'color': '#2c3e50'
    },
    'anime': {
        'name': 'Anime',
        'description': 'Japanese animation style with vibrant colors',
        'color': '#e74c3c'
    },
    'photorealistic': {
        'name': 'Photorealistic',
        'description': 'High-quality photographic realism',
        'color': '#27ae60'
    },
    'noir': {
        'name': 'Noir',
        'description': 'Classic film noir with dramatic shadows',
        'color': '#34495e'
    },
    'pixar': {
        'name': 'Pixar',
        'description': '3D animation style like Pixar films',
        'color': '#f39c12'
    }
}

def create_demo_image(prompt, style, panel_num):
    """Create a demo image with placeholder content"""
    width, height = 512, 512
    # Use a different color and icon for each panel
    demo_colors = ['#2c3e50', '#e74c3c', '#27ae60', '#34495e', '#f39c12']
    demo_icons = ['🎬', '🤖', '🧙', '🚀', '🎨']
    bg_color = demo_colors[(panel_num - 1) % len(demo_colors)]
    icon = demo_icons[(panel_num - 1) % len(demo_icons)]
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    # Add border
    draw.rectangle([10, 10, width-10, height-10], outline='white', width=3)
    # Add icon
    try:
        font_icon = ImageFont.truetype("/System/Library/Fonts/AppleColorEmoji.ttc", 80)
    except:
        font_icon = ImageFont.load_default()
    draw.text((width//2, 120), icon, fill='white', anchor='mm', font=font_icon)
    # Add panel number
    draw.text((width//2, 50), f"Panel {panel_num}", fill='white', anchor='mm')
    # Add style name
    draw.text((width//2, height//2), STYLES[style]['name'], fill='white', anchor='mm')
    # Add prompt preview
    prompt_preview = prompt[:40] + "..." if len(prompt) > 40 else prompt
    draw.text((width//2, height//2 + 50), prompt_preview, fill='white', anchor='mm')
    # Add demo indicator
    draw.text((width//2, height - 50), "Demo Mode", fill='yellow', anchor='mm')
    return image

def create_storyboard_layout(images, captions):
    """Create a horizontal layout of the 5 images with captions"""
    img_width, img_height = images[0].size
    caption_height = 80
    spacing = 20
    
    # Create the storyboard canvas
    total_width = img_width * 5 + spacing * 4
    total_height = img_height + caption_height + spacing
    
    storyboard = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(storyboard)
    
    # Try to load a font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
    
    # Place images and captions
    for i, (image, caption) in enumerate(zip(images, captions)):
        x = i * (img_width + spacing)
        
        # Paste image
        storyboard.paste(image, (x, 0))
        
        # Draw caption background
        caption_y = img_height + 10
        draw.rectangle([x, caption_y, x + img_width, caption_y + caption_height - 10], 
                      fill='#f8f9fa', outline='#dee2e6')
        
        # Draw caption text
        draw.text((x + 10, caption_y + 10), f"Panel {i+1}: {caption}", 
                 fill='black', font=font)
    
    return storyboard

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image, target_size=(512, 512)):
    """Resize image to target size while maintaining aspect ratio"""
    # Calculate aspect ratio
    img_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]
    
    if img_ratio > target_ratio:
        # Image is wider than target
        new_width = target_size[0]
        new_height = int(target_size[0] / img_ratio)
    else:
        # Image is taller than target
        new_height = target_size[1]
        new_width = int(target_size[1] * img_ratio)
    
    # Resize image
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create new image with target size and paste resized image in center
    result = Image.new('RGB', target_size, (255, 255, 255))
    paste_x = (target_size[0] - new_width) // 2
    paste_y = (target_size[1] - new_height) // 2
    result.paste(resized, (paste_x, paste_y))
    
    return result

def resize_image_for_inpainting(image, target_size=(512, 512)):
    """Resize image to target size for inpainting (no padding, direct resize)"""
    # Direct resize to target size without maintaining aspect ratio
    # This ensures the image and mask are exactly the same size
    return image.resize(target_size, Image.Resampling.LANCZOS)

def process_mask_data(mask_data_url):
    """Process base64 mask data and convert to PIL Image for inpainting"""
    try:
        # Remove data URL prefix
        if mask_data_url.startswith('data:image/png;base64,'):
            mask_data_url = mask_data_url.split(',')[1]
        
        # Decode base64 data
        mask_bytes = base64.b64decode(mask_data_url)
        
        # Create PIL Image from bytes
        mask_image = Image.open(io.BytesIO(mask_bytes))
        
        # Convert to RGBA if needed
        if mask_image.mode != 'RGBA':
            mask_image = mask_image.convert('RGBA')
        
        # Convert to numpy array
        mask_array = np.array(mask_image)
        
        # Extract channels
        red_channel = mask_array[:, :, 0]
        green_channel = mask_array[:, :, 1]
        blue_channel = mask_array[:, :, 2]
        alpha_channel = mask_array[:, :, 3] if mask_array.shape[2] == 4 else np.full(red_channel.shape, 255)
        
        # More precise mask detection:
        # 1. Red channel should be significantly higher than other channels
        # 2. Red channel should be above a reasonable threshold
        # 3. The difference between red and other channels should be significant
        # 4. Alpha channel should be high (not transparent)
        
        # Calculate differences
        red_green_diff = red_channel - green_channel
        red_blue_diff = red_channel - blue_channel
        
        # Create more precise mask criteria
        red_threshold = 80  # Minimum red value
        diff_threshold = 30  # Minimum difference between red and other channels
        alpha_threshold = 200  # Minimum alpha value
        
        # Create mask based on multiple criteria
        red_brush_mask = (
            (red_channel > red_threshold) &  # Red channel above threshold
            (red_green_diff > diff_threshold) &  # Red significantly higher than green
            (red_blue_diff > diff_threshold) &  # Red significantly higher than blue
            (alpha_channel > alpha_threshold)  # Not transparent
        )
        
        # Apply morphological operations to clean up the mask
        try:
            from scipy import ndimage
            
            # Remove small isolated pixels (noise)
            red_brush_mask = ndimage.binary_opening(red_brush_mask, structure=np.ones((2, 2)))
            
            # Fill small holes
            red_brush_mask = ndimage.binary_closing(red_brush_mask, structure=np.ones((3, 3)))
            
            print(f"[DEBUG] Applied morphological operations")
        except ImportError:
            print(f"[DEBUG] Scipy not available, skipping morphological operations")
            # Simple alternative: remove very small isolated areas
            try:
                from scipy import ndimage as ndi
                labeled, num_features = ndi.label(red_brush_mask)
                for i in range(1, num_features + 1):
                    component_size = np.sum(labeled == i)
                    if component_size < 10:  # Remove components smaller than 10 pixels
                        red_brush_mask[labeled == i] = False
                print(f"[DEBUG] Removed {num_features} small components")
            except:
                print(f"[DEBUG] Could not clean mask, using as-is")
        
        # Create binary mask (white = inpaint, black = preserve)
        binary_mask = np.where(red_brush_mask, 255, 0).astype(np.uint8)
        
        # Validate mask has sufficient coverage
        masked_pixels = np.sum(binary_mask > 0)
        total_pixels = binary_mask.size
        mask_coverage = (masked_pixels / total_pixels) * 100
        
        print(f"[DEBUG] Mask coverage: {mask_coverage:.2f}% ({masked_pixels} pixels)")
        
        # If mask coverage is too low, it might be a detection issue
        if mask_coverage < 0.1:  # Less than 0.1% coverage
            print(f"[DEBUG] Warning: Very low mask coverage, might be detection issue")
            # Try with more lenient thresholds
            red_brush_mask_relaxed = (
                (red_channel > 60) &  # Lower red threshold
                (red_green_diff > 20) &  # Lower difference threshold
                (red_blue_diff > 20) &
                (alpha_channel > 150)  # Lower alpha threshold
            )
            binary_mask_relaxed = np.where(red_brush_mask_relaxed, 255, 0).astype(np.uint8)
            relaxed_coverage = (np.sum(binary_mask_relaxed > 0) / total_pixels) * 100
            print(f"[DEBUG] Relaxed mask coverage: {relaxed_coverage:.2f}%")
            
            if relaxed_coverage > mask_coverage:
                binary_mask = binary_mask_relaxed
                print(f"[DEBUG] Using relaxed mask detection")
        
        # Convert back to PIL Image
        mask_pil = Image.fromarray(binary_mask, mode='L')
        
        print(f"[DEBUG] Mask processed: shape={binary_mask.shape}, unique values={np.unique(binary_mask)}")
        print(f"[DEBUG] Red channel stats: min={red_channel.min()}, max={red_channel.max()}, mean={red_channel.mean():.2f}")
        print(f"[DEBUG] Green channel stats: min={green_channel.min()}, max={green_channel.max()}, mean={green_channel.mean():.2f}")
        print(f"[DEBUG] Blue channel stats: min={blue_channel.min()}, max={blue_channel.max()}, mean={blue_channel.mean():.2f}")
        print(f"[DEBUG] Alpha channel stats: min={alpha_channel.min()}, max={alpha_channel.max()}, mean={alpha_channel.mean():.2f}")
        print(f"[DEBUG] Red-Green diff stats: min={red_green_diff.min()}, max={red_green_diff.max()}, mean={red_green_diff.mean():.2f}")
        print(f"[DEBUG] Red-Blue diff stats: min={red_blue_diff.min()}, max={red_blue_diff.max()}, mean={red_blue_diff.mean():.2f}")
        print(f"[DEBUG] Red brush mask pixels: {np.sum(red_brush_mask)} out of {red_brush_mask.size}")
        print(f"[DEBUG] Binary mask stats: min={binary_mask.min()}, max={binary_mask.max()}, mean={binary_mask.mean():.2f}")
        
        # Save mask for debugging
        debug_mask_path = os.path.join(get_storyboards_dir(), 'debug_mask.png')
        mask_pil.save(debug_mask_path)
        print(f"[DEBUG] Debug mask saved to: {debug_mask_path}")
        
        return mask_pil
    except Exception as e:
        print(f"[DEBUG] Error processing mask data: {e}")
        return None

def generate_demo_storyboard(prompt, style):
    """Generate a demo storyboard with placeholder images"""
    images = []
    captions = []
    
    # Generate 5 demo images
    for i in range(5):
        # Create demo image
        image = create_demo_image(prompt, style, i + 1)
        
        # Create demo caption
        caption = f"Demo panel {i+1}: {prompt[:30]}..."
        
        images.append(image)
        captions.append(caption)
    
    # Create storyboard layout
    storyboard = create_storyboard_layout(images, captions)
    
    return storyboard, captions

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', styles=STYLES)

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload for img2img"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"upload_{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the uploaded file
            file.save(filepath)
            
            # Open and resize the image
            with Image.open(filepath) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                resized_img = resize_image(img)
                resized_img.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })
        else:
            return jsonify({'error': 'Invalid file type. Please upload a valid image file.'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_storyboard():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        style = data.get('style', 'cinematic')
        mode = data.get('mode', 'demo')
        gen_type = data.get('genType', 'storyboard')
        img2img_mode = data.get('img2img', False)
        inpainting_mode = data.get('inpainting', False)
        input_image_path = data.get('inputImagePath', None)
        inpainting_image_path = data.get('inpaintingImagePath', None)
        mask_data = data.get('maskData', None)
        strength = data.get('strength', 0.75)
        prompt_chain_data = data.get('promptChain', None)
        batch_data = data.get('batch', None)
        print(f"[DEBUG] /generate called with mode={mode}, genType={gen_type}, style={style}, prompt={prompt[:40]}")
        
        # Skip main prompt validation for prompt chaining mode
        if gen_type != 'prompt-chaining' and gen_type != 'batch':
            if not prompt:
                print("[DEBUG] No prompt provided.")
                return jsonify({'error': 'Please enter a scene description'}), 400
            if len(prompt) < 10:
                print("[DEBUG] Prompt too short.")
                return jsonify({'error': 'Scene description should be at least 10 characters'}), 400
        if style not in STYLES:
            print(f"[DEBUG] Invalid style '{style}', defaulting to cinematic.")
            style = 'cinematic'
        if mode == 'ai':
            print("[DEBUG] Entering Full AI mode.")
            try:
                from diffusionlab.tasks.storyboard import generate_scene_variations, generate_caption, pipe, inpaint_pipe, STYLE_PRESETS, IMAGE_CONFIG
                from diffusionlab.config import INPAINTING_CONFIG, BATCH_CONFIG
            except ImportError as e:
                print(f"[DEBUG] ImportError in AI mode: {e}")
                return jsonify({'error': 'AI mode is not available. Please ensure diffusionlab/tasks/storyboard.py and dependencies are present.'}), 500
            if gen_type == 'single' or gen_type == 'img2img' or gen_type == 'inpainting' or gen_type == 'prompt-chaining' or gen_type == 'batch':
                print(f"[DEBUG] AI {'Batch Generation' if gen_type == 'batch' else 'Prompt Chaining' if gen_type == 'prompt-chaining' else 'Inpainting' if gen_type == 'inpainting' else 'Image-to-Image' if gen_type == 'img2img' else 'Single-Image Art'} mode.")
                # Generate a single AI image
                scene = prompt
                style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
                negative_prompt = style_preset["negative_prompt"]
                
                if inpainting_mode and inpainting_image_path and mask_data:
                    print(f"[DEBUG] AI Inpainting mode")
                    print(f"[DEBUG] inpaint_pipe available: {inpaint_pipe is not None}")
                    
                    # Load the input image
                    input_image = Image.open(inpainting_image_path).convert('RGB')
                    input_image = resize_image_for_inpainting(input_image)
                    print(f"[DEBUG] Input image size: {input_image.size}")
                    
                    # Process mask data
                    mask = process_mask_data(mask_data)
                    if mask is None:
                        return jsonify({'error': 'Failed to process mask data'}), 400
                    print(f"[DEBUG] Mask size: {mask.size}, mode: {mask.mode}")
                    
                    # Ensure mask and image are the same size
                    if mask.size != input_image.size:
                        mask = mask.resize(input_image.size, Image.Resampling.NEAREST)
                        print(f"[DEBUG] Resized mask to match image: {mask.size}")
                    
                    # Check if mask contains any masked pixels
                    mask_array = np.array(mask)
                    masked_pixels = np.sum(mask_array > 0)
                    total_pixels = mask_array.size
                    mask_percentage = (masked_pixels / total_pixels) * 100
                    print(f"[DEBUG] Mask contains {masked_pixels} masked pixels out of {total_pixels} ({mask_percentage:.2f}%)")
                    
                    if masked_pixels == 0:
                        return jsonify({'error': 'No masked areas detected. Please draw on areas you want to change.'}), 400
                    
                    # Check if inpaint_pipe is available, fallback to regular pipe if not
                    if inpaint_pipe is not None:
                        print(f"[DEBUG] Using inpaint_pipe for inpainting")
                        print(f"[DEBUG] inpaint_pipe type: {type(inpaint_pipe)}")
                        try:
                            # Try with original mask first
                            print(f"[DEBUG] Trying inpainting with original mask")
                            image = inpaint_pipe(
                                scene,
                                image=input_image,
                                mask_image=mask,
                                negative_prompt=negative_prompt,
                                num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                                guidance_scale=IMAGE_CONFIG["guidance_scale"],
                                # Add inpainting-specific parameters
                                inpaint_full_res=True,
                                inpaint_full_res_padding=32,
                                mask_blur=4
                            ).images[0]
                            print(f"[DEBUG] Inpainting completed successfully with original mask")
                        except Exception as e:
                            print(f"[DEBUG] Inpainting failed with original mask: {e}")
                            try:
                                # Try with inverted mask
                                print(f"[DEBUG] Trying inpainting with inverted mask")
                                mask_array = np.array(mask)
                                inverted_mask = np.where(mask_array > 0, 0, 255).astype(np.uint8)
                                inverted_mask_pil = Image.fromarray(inverted_mask, mode='L')
                                
                                image = inpaint_pipe(
                                    scene,
                                    image=input_image,
                                    mask_image=inverted_mask_pil,
                                    negative_prompt=negative_prompt,
                                    num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                                    guidance_scale=IMAGE_CONFIG["guidance_scale"],
                                    inpaint_full_res=True,
                                    inpaint_full_res_padding=32,
                                    mask_blur=4
                                ).images[0]
                                print(f"[DEBUG] Inpainting completed successfully with inverted mask")
                            except Exception as e2:
                                print(f"[DEBUG] Inpainting failed with inverted mask: {e2}")
                                print(f"[DEBUG] Falling back to regular pipe")
                                # Fallback to regular pipe if inpainting fails
                                image = pipe(
                                    scene,
                                    image=input_image,
                                    strength=0.8,
                                    negative_prompt=negative_prompt,
                                    num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                                    guidance_scale=IMAGE_CONFIG["guidance_scale"]
                                ).images[0]
                    else:
                        print(f"[DEBUG] inpaint_pipe not available, falling back to regular pipe")
                        # Fallback to regular pipe (this will replace the entire image)
                        image = pipe(
                            scene,
                            image=input_image,
                            strength=0.8,  # High strength for more transformation
                            negative_prompt=negative_prompt,
                            num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                            guidance_scale=IMAGE_CONFIG["guidance_scale"]
                        ).images[0]
                elif img2img_mode and input_image_path:
                    print(f"[DEBUG] AI Image-to-Image mode with strength={strength}")
                    # Load the input image
                    input_image = Image.open(input_image_path).convert('RGB')
                    input_image = resize_image(input_image)
                    
                    # Use the inpainting pipeline for img2img by creating a full mask
                    # This gives us proper img2img functionality
                    width, height = IMAGE_CONFIG["width"], IMAGE_CONFIG["height"]
                    
                    # Create a full mask (all white = inpaint everything)
                    mask = Image.new('L', (width, height), 255)
                    
                    # Use the inpainting pipeline for img2img
                    # Use fewer inference steps to avoid index out of bounds error
                    num_steps = min(20, INPAINTING_CONFIG["num_inference_steps"])
                    image = inpaint_pipe(
                        prompt=scene,
                        image=input_image,
                        mask_image=mask,
                        negative_prompt=negative_prompt,
                        num_inference_steps=num_steps,
                        guidance_scale=INPAINTING_CONFIG["guidance_scale"],
                        strength=strength  # This controls how much to change
                    ).images[0]
                elif gen_type == 'prompt-chaining' and prompt_chain_data:
                    print(f"[DEBUG] AI Prompt Chaining mode")
                    # Generate a sequence of images for prompt chaining
                    prompts = prompt_chain_data.get('prompts', [])
                    evolution_strength = prompt_chain_data.get('evolutionStrength', 0.3)
                    layout = prompt_chain_data.get('layout', 'horizontal')
                    
                    if len(prompts) < 2:
                        return jsonify({'error': 'At least 2 prompts required for prompt chaining'}), 400
                    
                    print(f"[DEBUG] Generating {len(prompts)} images for prompt chain")
                    images = []
                    captions = []
                    style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
                    negative_prompt = style_preset["negative_prompt"]
                    
                    for i, chain_prompt in enumerate(prompts):
                        print(f"[DEBUG] Generating prompt chain image {i+1}/{len(prompts)}: {chain_prompt[:60]}")
                        
                        # Add style suffix to the prompt
                        full_prompt = f"{chain_prompt}, {style_preset['prompt_suffix']}"
                        
                        image = pipe(
                            full_prompt,
                            negative_prompt=negative_prompt,
                            num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                            guidance_scale=IMAGE_CONFIG["guidance_scale"],
                            width=IMAGE_CONFIG["width"],
                            height=IMAGE_CONFIG["height"]
                        ).images[0]
                        
                        caption = f"Step {i+1}: {chain_prompt[:50]}..."
                        images.append(image)
                        captions.append(caption)
                    
                    # Create storyboard layout for the prompt chain
                    storyboard = create_storyboard_layout(images, captions)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"prompt_chain_{timestamp}.png"
                    filepath = os.path.join(get_storyboards_dir(), filename)
                    storyboard.save(filepath)
                    buffer = io.BytesIO()
                    storyboard.save(buffer, format='PNG')
                    buffer.seek(0)
                    img_base64 = base64.b64encode(buffer.getvalue()).decode()
                    return jsonify({
                        'success': True,
                        'image': img_base64,
                        'filename': filename,
                        'captions': captions,
                        'prompt': prompt or "Story Evolution",  # Use default if main prompt is empty
                        'style': style,
                        'mode': mode,
                        'promptChain': True,
                        'evolutionStrength': evolution_strength,
                        'layout': layout
                    })
                elif gen_type == 'batch' and batch_data:
                    print(f"[DEBUG] AI Batch Generation mode")
                    # Generate multiple variations of the same prompt
                    batch_count = batch_data.get('count', BATCH_CONFIG["default_variations"])
                    batch_layout = batch_data.get('layout', BATCH_CONFIG["default_layout"])
                    variation_strength = batch_data.get('variationStrength', 0.5)
                    
                    # Validate batch count
                    max_variations = BATCH_CONFIG["max_variations_demo"] if mode == 'demo' else BATCH_CONFIG["max_variations"]
                    batch_count = min(max(batch_count, BATCH_CONFIG["min_variations"]), max_variations)
                    
                    print(f"[DEBUG] Generating {batch_count} variations with layout={batch_layout}, variation_strength={variation_strength}")
                    
                    images = []
                    captions = []
                    style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
                    negative_prompt = style_preset["negative_prompt"]
                    
                    # Add style suffix to the prompt
                    full_prompt = f"{scene}, {style_preset['prompt_suffix']}"
                    
                    for i in range(batch_count):
                        print(f"[DEBUG] Generating batch variation {i+1}/{batch_count}")
                        
                        # Vary the guidance scale and inference steps for diversity
                        guidance_variation = IMAGE_CONFIG["guidance_scale"] + (variation_strength - 0.5) * 2
                        step_variation = max(20, IMAGE_CONFIG["num_inference_steps"] + int((variation_strength - 0.5) * 10))
                        
                        image = pipe(
                            full_prompt,
                            negative_prompt=negative_prompt,
                            num_inference_steps=step_variation,
                            guidance_scale=guidance_variation,
                            width=IMAGE_CONFIG["width"],
                            height=IMAGE_CONFIG["height"]
                        ).images[0]
                        
                        caption = f"Variation {i+1}: {scene[:50]}..."
                        images.append(image)
                        captions.append(caption)
                    
                    # Create batch layout
                    storyboard = create_storyboard_layout(images, captions)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"batch_{timestamp}.png"
                    filepath = os.path.join(get_storyboards_dir(), filename)
                    storyboard.save(filepath)
                    buffer = io.BytesIO()
                    storyboard.save(buffer, format='PNG')
                    buffer.seek(0)
                    img_base64 = base64.b64encode(buffer.getvalue()).decode()
                    return jsonify({
                        'success': True,
                        'image': img_base64,
                        'filename': filename,
                        'captions': captions,
                        'prompt': prompt,
                        'style': style,
                        'mode': mode,
                        'batch': True,
                        'batchCount': batch_count,
                        'layout': batch_layout,
                        'variationStrength': variation_strength
                    })
                else:
                    # Generate image using text-to-image
                    image = pipe(
                        scene,
                        negative_prompt=negative_prompt,
                        num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                        guidance_scale=IMAGE_CONFIG["guidance_scale"],
                        width=IMAGE_CONFIG["width"],
                        height=IMAGE_CONFIG["height"]
                    ).images[0]
                
                caption = generate_caption(scene)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"single_art_{timestamp}.png"
                filepath = os.path.join(get_storyboards_dir(), filename)
                image.save(filepath)
                buffer = io.BytesIO()
                image.save(buffer, format='PNG')
                buffer.seek(0)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                return jsonify({
                    'success': True,
                    'image': img_base64,
                    'filename': filename,
                    'caption': caption,
                    'prompt': prompt,
                    'style': style,
                    'mode': mode,
                    'img2img': img2img_mode,
                    'inpainting': inpainting_mode
                })
            else:
                print("[DEBUG] AI Storyboard mode.")
                scene_variations = generate_scene_variations(prompt, style)
                images = []
                captions = []
                style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
                negative_prompt = style_preset["negative_prompt"]
                for i, scene in enumerate(scene_variations):
                    print(f"[DEBUG] Generating AI image {i+1}/5 for: {scene[:60]}")
                    image = pipe(
                        scene,
                        negative_prompt=negative_prompt,
                        num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                        guidance_scale=IMAGE_CONFIG["guidance_scale"],
                        width=IMAGE_CONFIG["width"],
                        height=IMAGE_CONFIG["height"]
                    ).images[0]
                    caption = generate_caption(scene)
                    images.append(image)
                    captions.append(caption)
                storyboard = create_storyboard_layout(images, captions)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"storyboard_{timestamp}.png"
                filepath = os.path.join(get_storyboards_dir(), filename)
                storyboard.save(filepath)
                buffer = io.BytesIO()
                storyboard.save(buffer, format='PNG')
                buffer.seek(0)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                return jsonify({
                    'success': True,
                    'image': img_base64,
                    'filename': filename,
                    'captions': captions,
                    'prompt': prompt,
                    'style': style,
                    'mode': mode
                })
        else:
            print("[DEBUG] Entering Demo mode.")
            if gen_type == 'single' or gen_type == 'img2img' or gen_type == 'inpainting' or gen_type == 'prompt-chaining' or gen_type == 'batch':
                print(f"[DEBUG] Demo {'Batch Generation' if gen_type == 'batch' else 'Prompt Chaining' if gen_type == 'prompt-chaining' else 'Inpainting' if gen_type == 'inpainting' else 'Image-to-Image' if gen_type == 'img2img' else 'Single-Image Art'} mode.")
                if inpainting_mode and inpainting_image_path and mask_data:
                    print(f"[DEBUG] Demo Inpainting mode")
                    # Load the input image and create a demo inpainting
                    input_image = Image.open(inpainting_image_path).convert('RGB')
                    input_image = resize_image(input_image)
                    
                    # Create a demo inpainting by overlaying text
                    demo_image = input_image.copy()
                    draw = ImageDraw.Draw(demo_image)
                    try:
                        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                    except:
                        font = ImageFont.load_default()
                    
                    # Add inpainting indicator
                    draw.text((10, 10), "Demo Inpainting", fill='yellow', font=font)
                    draw.text((10, 40), f"Prompt: {prompt[:30]}...", fill='white', font=font)
                    draw.text((10, 70), "Style: " + STYLES[style]['name'], fill='white', font=font)
                    draw.text((10, 100), "Masked areas will be filled", fill='red', font=font)
                    
                    image = demo_image
                elif img2img_mode and input_image_path:
                    print(f"[DEBUG] Demo Image-to-Image mode with strength={strength}")
                    # Load the input image and create a demo transformation
                    input_image = Image.open(input_image_path).convert('RGB')
                    input_image = resize_image(input_image)
                    
                    # Create a demo transformation by overlaying text
                    demo_image = input_image.copy()
                    draw = ImageDraw.Draw(demo_image)
                    try:
                        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                    except:
                        font = ImageFont.load_default()
                    
                    # Add transformation indicator
                    draw.text((10, 10), f"Demo Img2Img (Strength: {strength})", fill='yellow', font=font)
                    draw.text((10, 40), f"Prompt: {prompt[:30]}...", fill='white', font=font)
                    draw.text((10, 70), "Style: " + STYLES[style]['name'], fill='white', font=font)
                    
                    image = demo_image
                elif gen_type == 'prompt-chaining' and prompt_chain_data:
                    print(f"[DEBUG] Demo Prompt Chaining mode")
                    # Create demo prompt chaining storyboard
                    prompts = prompt_chain_data.get('prompts', [])
                    evolution_strength = prompt_chain_data.get('evolutionStrength', 0.3)
                    layout = prompt_chain_data.get('layout', 'horizontal')
                    
                    if len(prompts) < 2:
                        return jsonify({'error': 'At least 2 prompts required for prompt chaining'}), 400
                    
                    print(f"[DEBUG] Creating demo prompt chain with {len(prompts)} steps")
                    images = []
                    captions = []
                    
                    for i, chain_prompt in enumerate(prompts):
                        # Create demo image for each prompt
                        demo_image = create_demo_image(chain_prompt, style, i + 1)
                        
                        # Add prompt chaining indicator
                        draw = ImageDraw.Draw(demo_image)
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
                        except:
                            font = ImageFont.load_default()
                        
                        draw.text((10, 10), f"Demo Prompt Chain - Step {i+1}", fill='yellow', font=font)
                        draw.text((10, 35), f"Evolution Strength: {evolution_strength}", fill='cyan', font=font)
                        draw.text((10, 60), f"Layout: {layout}", fill='cyan', font=font)
                        
                        images.append(demo_image)
                        captions.append(f"Step {i+1}: {chain_prompt[:50]}...")
                    
                    # Create storyboard layout for the prompt chain
                    storyboard = create_storyboard_layout(images, captions)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"demo_prompt_chain_{timestamp}.png"
                    filepath = os.path.join(get_storyboards_dir(), filename)
                    storyboard.save(filepath)
                    buffer = io.BytesIO()
                    storyboard.save(buffer, format='PNG')
                    buffer.seek(0)
                    img_base64 = base64.b64encode(buffer.getvalue()).decode()
                    return jsonify({
                        'success': True,
                        'image': img_base64,
                        'filename': filename,
                        'captions': captions,
                        'prompt': prompt or "Story Evolution",  # Use default if main prompt is empty
                        'style': style,
                        'mode': mode,
                        'promptChain': True,
                        'evolutionStrength': evolution_strength,
                        'layout': layout
                    })
                elif gen_type == 'batch' and batch_data:
                    print(f"[DEBUG] Demo Batch Generation mode")
                    # Create demo batch generation storyboard
                    batch_count = batch_data.get('count', BATCH_CONFIG["default_variations"])
                    batch_layout = batch_data.get('layout', BATCH_CONFIG["default_layout"])
                    variation_strength = batch_data.get('variationStrength', 0.5)
                    
                    # Validate batch count
                    max_variations = BATCH_CONFIG["max_variations_demo"] if mode == 'demo' else BATCH_CONFIG["max_variations"]
                    batch_count = min(max(batch_count, BATCH_CONFIG["min_variations"]), max_variations)
                    
                    print(f"[DEBUG] Creating demo batch with {batch_count} variations")
                    images = []
                    captions = []
                    
                    for i in range(batch_count):
                        # Create demo image for each variation
                        demo_image = create_demo_image(prompt, style, i + 1)
                        
                        # Add batch generation indicator
                        draw = ImageDraw.Draw(demo_image)
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
                        except:
                            font = ImageFont.load_default()
                        
                        draw.text((10, 10), f"Demo Batch - Variation {i+1}", fill='yellow', font=font)
                        draw.text((10, 35), f"Variation Strength: {variation_strength}", fill='cyan', font=font)
                        draw.text((10, 60), f"Layout: {batch_layout}", fill='cyan', font=font)
                        
                        images.append(demo_image)
                        captions.append(f"Variation {i+1}: {prompt[:50]}...")
                    
                    # Create storyboard layout for the batch
                    storyboard = create_storyboard_layout(images, captions)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"demo_batch_{timestamp}.png"
                    filepath = os.path.join(get_storyboards_dir(), filename)
                    storyboard.save(filepath)
                    buffer = io.BytesIO()
                    storyboard.save(buffer, format='PNG')
                    buffer.seek(0)
                    img_base64 = base64.b64encode(buffer.getvalue()).decode()
                    return jsonify({
                        'success': True,
                        'image': img_base64,
                        'filename': filename,
                        'captions': captions,
                        'prompt': prompt,
                        'style': style,
                        'mode': mode,
                        'batch': True,
                        'batchCount': batch_count,
                        'layout': batch_layout,
                        'variationStrength': variation_strength
                    })
                else:
                    image = create_demo_image(prompt, style, 1)
                
                caption = f"Art: {prompt[:30]}..."
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"single_art_{timestamp}.png"
                filepath = os.path.join(get_storyboards_dir(), filename)
                image.save(filepath)
                buffer = io.BytesIO()
                image.save(buffer, format='PNG')
                buffer.seek(0)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                return jsonify({
                    'success': True,
                    'image': img_base64,
                    'filename': filename,
                    'caption': caption,
                    'prompt': prompt,
                    'style': style,
                    'mode': mode,
                    'img2img': img2img_mode,
                    'inpainting': inpainting_mode
                })
            else:
                print("[DEBUG] Demo Storyboard mode.")
                storyboard, captions = generate_demo_storyboard(prompt, style)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"storyboard_{timestamp}.png"
                filepath = os.path.join(get_storyboards_dir(), filename)
                storyboard.save(filepath)
                buffer = io.BytesIO()
                storyboard.save(buffer, format='PNG')
                buffer.seek(0)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                return jsonify({
                    'success': True,
                    'image': img_base64,
                    'filename': filename,
                    'captions': captions,
                    'prompt': prompt,
                    'style': style,
                    'mode': mode
                })
    except Exception as e:
        print(f"[DEBUG] Exception in /generate: {e}")
        return jsonify({'error': f'Error generating: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_storyboard(filename):
    """Download storyboard as PNG"""
    try:
        filepath = os.path.join(get_storyboards_dir(), filename)
        
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': f'File not found: {filepath}'}), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.route('/api/styles')
def get_styles():
    """Get available styles"""
    return jsonify(STYLES)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test if inpainting pipeline is available
        from diffusionlab.tasks.storyboard import inpaint_pipe
        inpaint_available = inpaint_pipe is not None
    except:
        inpaint_available = False
    
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'inpainting_available': inpaint_available
    })

@app.route('/test-mask', methods=['POST'])
def test_mask():
    """Test endpoint for mask processing"""
    try:
        data = request.get_json()
        mask_data = data.get('maskData')
        
        if not mask_data:
            return jsonify({'error': 'No mask data provided'}), 400
        
        # Process mask data
        mask = process_mask_data(mask_data)
        
        if mask is None:
            return jsonify({'error': 'Failed to process mask data'}), 400
        
        # Convert mask back to base64 for verification
        buffer = io.BytesIO()
        mask.save(buffer, format='PNG')
        buffer.seek(0)
        mask_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Also create an inverted mask for testing
        mask_array = np.array(mask)
        inverted_mask = np.where(mask_array > 0, 0, 255).astype(np.uint8)
        inverted_mask_pil = Image.fromarray(inverted_mask, mode='L')
        
        buffer_inverted = io.BytesIO()
        inverted_mask_pil.save(buffer_inverted, format='PNG')
        buffer_inverted.seek(0)
        inverted_mask_base64 = base64.b64encode(buffer_inverted.getvalue()).decode()
        
        # Check if inpainting pipeline is available
        try:
            from diffusionlab.tasks.storyboard import inpaint_pipe
            inpaint_available = inpaint_pipe is not None
            inpaint_type = str(type(inpaint_pipe)) if inpaint_pipe is not None else "None"
        except:
            inpaint_available = False
            inpaint_type = "Import Error"
        
        return jsonify({
            'success': True,
            'mask_size': mask.size,
            'mask_mode': mask.mode,
            'processed_mask': mask_base64,
            'inverted_mask': inverted_mask_base64,
            'masked_pixels': int(np.sum(mask_array > 0)),
            'total_pixels': mask_array.size,
            'inpaint_available': inpaint_available,
            'inpaint_type': inpaint_type
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing mask: {str(e)}'}), 500

@app.route('/test-inpainting', methods=['POST'])
def test_inpainting():
    """Test endpoint for inpainting functionality"""
    try:
        data = request.get_json()
        image_data = data.get('imageData')
        mask_data = data.get('maskData')
        prompt = data.get('prompt', 'A beautiful flower')
        
        if not image_data or not mask_data:
            return jsonify({'error': 'Both image and mask data required'}), 400
        
        # Process image data
        if image_data.startswith('data:image/png;base64,'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        input_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        input_image = resize_image_for_inpainting(input_image)
        
        # Process mask data
        mask = process_mask_data(mask_data)
        if mask is None:
            return jsonify({'error': 'Failed to process mask data'}), 400
        
        # Check if inpainting pipeline is available
        try:
            from diffusionlab.tasks.storyboard import inpaint_pipe
            if inpaint_pipe is not None:
                # Try inpainting
                result = inpaint_pipe(
                    prompt,
                    image=input_image,
                    mask_image=mask,
                    num_inference_steps=10,  # Use fewer steps for testing
                    guidance_scale=7.5
                ).images[0]
                
                # Convert result to base64
                buffer = io.BytesIO()
                result.save(buffer, format='PNG')
                buffer.seek(0)
                result_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                return jsonify({
                    'success': True,
                    'result': result_base64,
                    'message': 'Inpainting test completed successfully'
                })
            else:
                return jsonify({'error': 'Inpainting pipeline not available'}), 400
        except Exception as e:
            return jsonify({'error': f'Inpainting test failed: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error in inpainting test: {str(e)}'}), 500

if __name__ == '__main__':
    print("🎬 Starting Storyboard Generator Web App...")
    print("🌐 Open your browser to: http://localhost:5001")
    print("📝 This is a demo version - AI models not loaded")
    print("🔧 For full AI generation, run: python app.py")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 