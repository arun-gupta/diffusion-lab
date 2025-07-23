import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

def get_optimal_device():
    """Determine the best available device for model inference"""
    # For now, use CPU to avoid MPS device issues
    return "cpu"
    
    # Original device detection (commented out for now)
    # if torch.cuda.is_available():
    #     return "cuda"
    # elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    #     return "mps"
    # else:
    #     return "cpu"

def create_negative_prompt(style):
    """Generate negative prompts based on style to improve image quality"""
    base_negative = "blurry, low quality, distorted, deformed, ugly, bad anatomy"
    
    style_negatives = {
        "cinematic": f"{base_negative}, amateur, poorly lit",
        "anime": f"{base_negative}, realistic, photographic",
        "photorealistic": f"{base_negative}, cartoon, anime, illustration",
        "noir": f"{base_negative}, colorful, bright lighting",
        "pixar": f"{base_negative}, realistic, dark, scary"
    }
    
    return style_negatives.get(style, base_negative)

def enhance_prompt_with_style(prompt, style):
    """Enhance the base prompt with style-specific elements"""
    style_enhancements = {
        "cinematic": {
            "lighting": "cinematic lighting, dramatic shadows",
            "composition": "rule of thirds, professional cinematography",
            "aspect_ratio": "2.35:1 aspect ratio, widescreen"
        },
        "anime": {
            "lighting": "anime lighting, vibrant colors",
            "composition": "anime composition, detailed illustration",
            "aspect_ratio": "16:9 aspect ratio"
        },
        "photorealistic": {
            "lighting": "natural lighting, professional photography",
            "composition": "photographic composition, high detail",
            "aspect_ratio": "3:2 aspect ratio"
        },
        "noir": {
            "lighting": "film noir lighting, dramatic shadows, high contrast",
            "composition": "noir composition, moody atmosphere",
            "aspect_ratio": "4:3 aspect ratio, classic film"
        },
        "pixar": {
            "lighting": "3D animation lighting, warm colors",
            "composition": "3D animation composition, family-friendly",
            "aspect_ratio": "16:9 aspect ratio"
        }
    }
    
    enhancement = style_enhancements.get(style, style_enhancements["cinematic"])
    enhanced_prompt = f"{prompt}, {enhancement['lighting']}, {enhancement['composition']}, {enhancement['aspect_ratio']}"
    
    return enhanced_prompt

def create_storyboard_grid(images, captions, layout="horizontal"):
    """Create a storyboard layout with flexible grid options"""
    if layout == "horizontal":
        return create_horizontal_layout(images, captions)
    elif layout == "vertical":
        return create_vertical_layout(images, captions)
    elif layout == "grid":
        return create_grid_layout(images, captions)
    else:
        return create_horizontal_layout(images, captions)

def create_horizontal_layout(images, captions):
    """Create a horizontal layout of images with captions"""
    img_width, img_height = images[0].size
    caption_height = 60
    spacing = 20
    
    total_width = img_width * 5 + spacing * 4
    total_height = img_height + caption_height + spacing
    
    storyboard = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(storyboard)
    
    # Load font
    font = load_font(16)
    
    for i, (image, caption) in enumerate(zip(images, captions)):
        x = i * (img_width + spacing)
        
        # Paste image
        storyboard.paste(image, (x, 0))
        
        # Draw caption
        caption_y = img_height + 10
        draw.text((x, caption_y), f"Panel {i+1}: {caption}", fill='black', font=font)
    
    return storyboard

def create_vertical_layout(images, captions):
    """Create a vertical layout of images with captions"""
    img_width, img_height = images[0].size
    caption_height = 60
    spacing = 20
    
    total_width = img_width + 200  # Extra space for captions
    total_height = (img_height + caption_height + spacing) * 5
    
    storyboard = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(storyboard)
    
    font = load_font(16)
    
    for i, (image, caption) in enumerate(zip(images, captions)):
        y = i * (img_height + caption_height + spacing)
        
        # Paste image
        storyboard.paste(image, (0, y))
        
        # Draw caption
        caption_x = img_width + 10
        caption_y = y + 10
        draw.text((caption_x, caption_y), f"Panel {i+1}: {caption}", fill='black', font=font)
    
    return storyboard

def create_grid_layout(images, captions):
    """Create a 2x3 grid layout (5 images + 1 empty space)"""
    img_width, img_height = images[0].size
    caption_height = 60
    spacing = 20
    
    # 2 columns, 3 rows
    total_width = img_width * 2 + spacing
    total_height = (img_height + caption_height + spacing) * 3
    
    storyboard = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(storyboard)
    
    font = load_font(16)
    
    for i, (image, caption) in enumerate(zip(images, captions)):
        row = i // 2
        col = i % 2
        
        x = col * (img_width + spacing)
        y = row * (img_height + caption_height + spacing)
        
        # Paste image
        storyboard.paste(image, (x, y))
        
        # Draw caption
        caption_y_pos = y + img_height + 10
        draw.text((x, caption_y_pos), f"Panel {i+1}: {caption}", fill='black', font=font)
    
    return storyboard

def load_font(size):
    """Load a font with fallback options"""
    font_paths = [
        "/System/Library/Fonts/Arial.ttf",  # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "C:/Windows/Fonts/arial.ttf",  # Windows
        "/System/Library/Fonts/Helvetica.ttc",  # macOS alternative
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except:
            continue
    
    return ImageFont.load_default()

def save_storyboard_as_images(storyboard, output_dir="output"):
    """Save individual panels as separate images"""
    os.makedirs(output_dir, exist_ok=True)
    
    # For now, this is a placeholder - in a full implementation,
    # you'd want to save each panel separately
    storyboard.save(os.path.join(output_dir, "storyboard.png"))
    
    return os.path.join(output_dir, "storyboard.png")

def create_pdf_with_metadata(storyboard_image, prompt, style, metadata=None):
    """Create a PDF with storyboard and metadata"""
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Convert PIL image to reportlab format
    img_buffer = io.BytesIO()
    storyboard_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Calculate image dimensions
    page_width, page_height = A4
    img_width, img_height = storyboard_image.size
    
    margin = 50
    max_width = page_width - 2 * margin
    max_height = page_height - 2 * margin - 100  # Space for metadata
    
    scale = min(max_width / img_width, max_height / img_height)
    new_width = img_width * scale
    new_height = img_height * scale
    
    # Center the image
    x = (page_width - new_width) / 2
    y = page_height - margin - new_height - 50  # Space for title
    
    # Add title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(page_width / 2 - 100, page_height - 30, "Storyboard")
    
    # Add metadata
    c.setFont("Helvetica", 12)
    c.drawString(margin, page_height - 60, f"Prompt: {prompt}")
    c.drawString(margin, page_height - 75, f"Style: {style}")
    
    if metadata:
        c.drawString(margin, page_height - 90, f"Generated: {metadata.get('timestamp', 'Unknown')}")
    
    # Add the image
    c.drawImage(ImageReader(img_buffer), x, y, width=new_width, height=new_height)
    
    c.save()
    pdf_buffer.seek(0)
    
    return pdf_buffer

def validate_prompt(prompt):
    """Validate and clean the input prompt"""
    if not prompt or not prompt.strip():
        return False, "Prompt cannot be empty"
    
    if len(prompt.strip()) < 10:
        return False, "Prompt should be at least 10 characters long"
    
    if len(prompt.strip()) > 500:
        return False, "Prompt should be less than 500 characters"
    
    return True, "Valid prompt" 