#!/usr/bin/env python3
"""
Demo script for Storyboard Generator
This version shows the UI without loading the full AI models
"""

import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
from config import *

def create_demo_image(prompt, style):
    """Create a demo image with placeholder content"""
    # Create a simple placeholder image
    width, height = IMAGE_CONFIG["width"], IMAGE_CONFIG["height"]
    image = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(image)
    
    # Add some demo content
    draw.rectangle([50, 50, width-50, height-50], outline='black', width=3)
    draw.text((width//2, height//2), f"Demo: {style}", fill='black', anchor='mm')
    draw.text((width//2, height//2 + 30), "AI Model Not Loaded", fill='red', anchor='mm')
    
    return image

def generate_demo_storyboard(prompt, style, progress=gr.Progress()):
    """Generate a demo storyboard with placeholder images"""
    # Validate input
    is_valid, message = validate_prompt(prompt)
    if not is_valid:
        return None, message
    
    try:
        progress(0.1, desc="Generating scene variations...")
        time.sleep(1)  # Simulate processing time
        
        images = []
        captions = []
        
        # Generate 5 demo images
        for i in range(5):
            progress((i + 1) * 0.15, desc=f"Generating image {i+1}/5...")
            
            # Create demo image
            image = create_demo_image(prompt, style)
            
            # Create demo caption
            caption = f"Demo panel {i+1}: {prompt[:30]}..."
            
            images.append(image)
            captions.append(caption)
            
            time.sleep(0.5)  # Simulate processing time
        
        progress(0.9, desc="Creating storyboard layout...")
        time.sleep(1)
        
        # Create storyboard layout
        storyboard = create_storyboard_grid(images, captions, "horizontal")
        
        progress(1.0, desc="Complete!")
        
        return storyboard, "Demo storyboard generated successfully! (AI models not loaded)"
        
    except Exception as e:
        return None, f"Error generating demo storyboard: {str(e)}"

def create_demo_interface():
    """Create the demo interface"""
    with gr.Blocks(title="Storyboard Generator - Demo Mode", theme=getattr(gr.themes, UI_CONFIG["theme"].title())()) as demo:
        gr.Markdown("# 🎬 Storyboard Generator - Demo Mode")
        gr.Markdown("**This is a demo version without AI models loaded.**")
        gr.Markdown("Transform your script ideas into visual storyboards using AI")
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("## Input")
                prompt_input = gr.Textbox(
                    label="Scene Description",
                    placeholder="e.g., A detective walks into a neon-lit alley at midnight, rain pouring down",
                    lines=3
                )
                
                style_dropdown = gr.Dropdown(
                    choices=list(STYLE_PRESETS.keys()),
                    value="cinematic",
                    label="Visual Style"
                )
                
                # Style description
                style_info = gr.Markdown("**Cinematic**: Professional film-style with dramatic lighting")
                
                generate_btn = gr.Button("Generate Demo Storyboard", variant="primary")
                
                # Status output
                status_output = gr.Textbox(label="Status", interactive=False)
                
                # Export section
                gr.Markdown("## Export")
                export_btn = gr.Button("Export to PDF")
                pdf_output = gr.File(label="Download PDF")
            
            with gr.Column(scale=2):
                # Output section
                gr.Markdown("## Generated Storyboard")
                storyboard_output = gr.Image(label="Storyboard", type="pil")
        
        # Update style description when style changes
        def update_style_info(style):
            preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
            return f"**{style.title()}**: {preset['description']}"
        
        style_dropdown.change(
            fn=update_style_info,
            inputs=[style_dropdown],
            outputs=[style_info]
        )
        
        # Event handlers
        generate_btn.click(
            fn=generate_demo_storyboard,
            inputs=[prompt_input, style_dropdown],
            outputs=[storyboard_output, status_output]
        )
        
        export_btn.click(
            fn=export_to_pdf,
            inputs=[storyboard_output, prompt_input, style_dropdown],
            outputs=[pdf_output]
        )
        
        # Example inputs
        gr.Examples(
            examples=[
                ["A detective walks into a neon-lit alley at midnight, rain pouring down"],
                ["A robot wanders a post-apocalyptic desert searching for signs of life"],
                ["A young wizard discovers an ancient library hidden in the mountains"],
                ["A spaceship crew encounters an alien artifact on a distant planet"],
                ["A street artist creates a mural that comes to life at night"]
            ],
            inputs=prompt_input
        )
    
    return demo

if __name__ == "__main__":
    print("Starting Storyboard Generator Demo...")
    print("This is a demo version without AI models.")
    print("Run 'python app.py' for the full version with AI generation.")
    
    # Create and launch the demo interface
    demo = create_demo_interface()
    demo.launch(
        server_name=UI_CONFIG["server_name"],
        server_port=UI_CONFIG["server_port"],
        share=UI_CONFIG["share"],
        show_error=UI_CONFIG["show_error"]
    ) 