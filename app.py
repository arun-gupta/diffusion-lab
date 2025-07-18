import gradio as gr
import torch
from diffusers import StableDiffusionXLPipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
import io
import time
from config import *
from utils import *

# Global variables for models
pipe = None
tokenizer = None
model = None

def load_models():
    """Load the AI models for image and text generation"""
    global pipe, tokenizer, model
    
    print("Loading Stable Diffusion XL...")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_CONFIG["diffusion_model"],
        torch_dtype=getattr(torch, MODEL_CONFIG["torch_dtype"]),
        use_safetensors=MODEL_CONFIG["use_safetensors"],
        variant=MODEL_CONFIG["variant"]
    )
    
    device = get_optimal_device()
    if device == "cuda":
        pipe = pipe.to("cuda")
        print("Using CUDA for image generation")
    elif device == "mps":
        pipe = pipe.to("mps")
        print("Using MPS for image generation")
    else:
        print("Using CPU for image generation (slower)")
    
    # Apply performance optimizations
    if PERFORMANCE_CONFIG["enable_attention_slicing"]:
        pipe.enable_attention_slicing()
    
    print("Loading StableLM for caption generation...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG["text_model"])
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_CONFIG["text_model"],
        torch_dtype=getattr(torch, MODEL_CONFIG["torch_dtype"]),
        device_map="auto" if device != "cpu" else None
    )
    
    print("Models loaded successfully!")

def generate_scene_variations(prompt, style):
    """Generate 5 different scene variations from the input prompt"""
    # Get style preset
    style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
    style_text = style_preset["prompt_suffix"]
    
    # Create 5 different scene variations using templates
    variations = []
    for variation in SCENE_VARIATIONS:
        enhanced_prompt = enhance_prompt_with_style(prompt, style)
        full_prompt = f"{enhanced_prompt}, {variation['suffix']}, {style_text}"
        variations.append(full_prompt)
    
    return variations

def generate_caption(scene_description):
    """Generate a caption for a scene using StableLM"""
    if tokenizer is None or model is None:
        return "Scene description"
    
    prompt = f"Describe this scene in one short sentence: {scene_description}"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    device = get_optimal_device()
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=TEXT_CONFIG["max_new_tokens"],
            temperature=TEXT_CONFIG["temperature"],
            do_sample=TEXT_CONFIG["do_sample"],
            top_p=TEXT_CONFIG["top_p"],
            top_k=TEXT_CONFIG["top_k"],
            pad_token_id=tokenizer.eos_token_id
        )
    
    caption = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the new generated text
    caption = caption.replace(prompt, "").strip()
    
    # Clean up the caption
    if caption.startswith(":"):
        caption = caption[1:].strip()
    
    return caption if caption else "Scene description"

def generate_storyboard(prompt, style, progress=gr.Progress()):
    """Generate a complete 5-panel storyboard"""
    # Validate input
    is_valid, message = validate_prompt(prompt)
    if not is_valid:
        return None, message
    
    try:
        # Generate scene variations
        progress(0.1, desc="Generating scene variations...")
        scene_variations = generate_scene_variations(prompt, style)
        
        images = []
        captions = []
        
        # Get negative prompt for the style
        style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
        negative_prompt = style_preset["negative_prompt"]
        
        # Generate images and captions for each scene
        for i, scene in enumerate(scene_variations):
            progress((i + 1) * 0.15, desc=f"Generating image {i+1}/5...")
            
            # Generate image
            image = pipe(
                scene,
                negative_prompt=negative_prompt,
                num_inference_steps=IMAGE_CONFIG["num_inference_steps"],
                guidance_scale=IMAGE_CONFIG["guidance_scale"],
                width=IMAGE_CONFIG["width"],
                height=IMAGE_CONFIG["height"]
            ).images[0]
            
            # Generate caption
            caption = generate_caption(scene)
            
            images.append(image)
            captions.append(caption)
            
            # Small delay to prevent overwhelming the system
            time.sleep(0.5)
        
        progress(0.9, desc="Creating storyboard layout...")
        
        # Create a storyboard layout
        storyboard = create_storyboard_layout(images, captions)
        
        progress(1.0, desc="Complete!")
        
        return storyboard, "Storyboard generated successfully!"
        
    except Exception as e:
        return None, f"Error generating storyboard: {str(e)}"

def create_storyboard_layout(images, captions):
    """Create a horizontal layout of the 5 images with captions"""
    return create_storyboard_grid(images, captions, "horizontal")

def export_to_pdf(storyboard_image, prompt="", style=""):
    """Export the storyboard to PDF"""
    if storyboard_image is None:
        return None
    
    # Create metadata
    metadata = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "style": style
    }
    
    return create_pdf_with_metadata(storyboard_image, prompt, style, metadata)

# Create the Gradio interface
def create_interface():
    with gr.Blocks(title="Storyboard Generator", theme=getattr(gr.themes, UI_CONFIG["theme"].title())()) as demo:
        gr.Markdown("# 🎬 Storyboard Generator")
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
                
                generate_btn = gr.Button("Generate Storyboard", variant="primary")
                
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
            fn=generate_storyboard,
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
    print("Starting Storyboard Generator...")
    print("Loading AI models (this may take a few minutes on first run)...")
    
    # Load models
    load_models()
    
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name=UI_CONFIG["server_name"],
        server_port=UI_CONFIG["server_port"],
        share=UI_CONFIG["share"],
        show_error=UI_CONFIG["show_error"]
    ) 