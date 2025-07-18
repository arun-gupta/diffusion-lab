#!/usr/bin/env python3
"""
Flask Web Application for Storyboard Generator
"""

from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import time
import io
import base64
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/storyboards', exist_ok=True)

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

@app.route('/generate', methods=['POST'])
def generate_storyboard():
    """Generate storyboard endpoint"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        style = data.get('style', 'cinematic')
        mode = data.get('mode', 'demo')
        print(f"[DEBUG] /generate called with mode={mode}, style={style}, prompt={prompt[:40]}")
        
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
                from app import generate_scene_variations, generate_caption
                from app import pipe, STYLE_PRESETS, IMAGE_CONFIG
            except ImportError as e:
                print(f"[DEBUG] ImportError in AI mode: {e}")
                return jsonify({'error': 'AI mode is not available. Please ensure app.py and dependencies are present.'}), 500
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
        else:
            print("[DEBUG] Entering Demo mode.")
            storyboard, captions = generate_demo_storyboard(prompt, style)
        
        # Save storyboard
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"storyboard_{timestamp}.png"
        filepath = os.path.join('static/storyboards', filename)
        storyboard.save(filepath)
        print(f"[DEBUG] Storyboard saved to {filepath}")
        
        # Convert to base64 for immediate display
        buffer = io.BytesIO()
        storyboard.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        print(f"[DEBUG] Returning response for mode={mode}")
        
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
        return jsonify({'error': f'Error generating storyboard: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_storyboard(filename):
    """Download storyboard as PNG"""
    try:
        filepath = os.path.join('static/storyboards', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.route('/api/styles')
def get_styles():
    """Get available styles"""
    return jsonify(STYLES)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🎬 Starting Storyboard Generator Web App...")
    print("🌐 Open your browser to: http://localhost:5001")
    print("📝 This is a demo version - AI models not loaded")
    print("🔧 For full AI generation, run: python app.py")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 