import gradio as gr
import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLInpaintPipeline, ControlNetModel, StableDiffusionXLControlNetPipeline
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
import cv2
from controlnet_aux import CannyDetector, OpenposeDetector, MLSDdetector, HEDdetector
from diffusionlab.config import *
from diffusionlab.utils import *

# --- Model and Pipeline Setup (Top Level) ---
pipe = None
inpaint_pipe = None
controlnet_pipes = {}
model = None
tokenizer = None
controlnet_processors = {}

# Load models at import time for webapp AI mode
# (If you want to delay loading for Gradio UI, you can move this into a function)
def load_models():
    global pipe, inpaint_pipe, tokenizer, model, controlnet_processors
    if pipe is not None and inpaint_pipe is not None and tokenizer is not None and model is not None:
        return
    print("Loading Stable Diffusion XL...")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_CONFIG["diffusion_model"],
        torch_dtype=getattr(torch, MODEL_CONFIG["torch_dtype"]),
        use_safetensors=MODEL_CONFIG["use_safetensors"],
        variant=MODEL_CONFIG["variant"]
    )
    print("Loading Stable Diffusion XL Inpainting...")
    inpaint_pipe = StableDiffusionXLInpaintPipeline.from_pretrained(
        MODEL_CONFIG["diffusion_model"],
        torch_dtype=getattr(torch, MODEL_CONFIG["torch_dtype"]),
        use_safetensors=MODEL_CONFIG["use_safetensors"],
        variant=MODEL_CONFIG["variant"]
    )
    
    # Initialize ControlNet processors (lightweight) - moved to on-demand loading
    # This prevents import issues at startup
    print("ControlNet processors will be loaded on-demand")
    
    device = get_optimal_device()
    if device == "cuda":
        pipe = pipe.to("cuda")
        inpaint_pipe = inpaint_pipe.to("cuda")
        print("Using CUDA for image generation")
    elif device == "mps":
        pipe = pipe.to("mps")
        inpaint_pipe = inpaint_pipe.to("mps")
        print("Using MPS for image generation")
    
    if PERFORMANCE_CONFIG["enable_attention_slicing"]:
        pipe.enable_attention_slicing()
        inpaint_pipe.enable_attention_slicing()
    
    print("Loading StableLM for caption generation...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG["caption_model"])
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_CONFIG["caption_model"],
        torch_dtype=getattr(torch, MODEL_CONFIG["torch_dtype"]),
        device_map="auto" if device == "cuda" else None
    )
    print("Models loaded successfully!")

def load_controlnet_model(control_type):
    """Load a specific ControlNet model on-demand"""
    global controlnet_pipes
    
    if control_type in controlnet_pipes:
        return controlnet_pipes[control_type]
    
    try:
        print(f"Loading ControlNet model: {control_type}")
        device = get_optimal_device()
        
        # Get model config
        if control_type not in CONTROLNET_CONFIG["models"]:
            print(f"Unknown control type: {control_type}")
            return None
        
        config = CONTROLNET_CONFIG["models"][control_type]
        
        # For now, let's use a simpler approach that doesn't require downloading large models
        # This will allow the feature to work in demo mode while we work on full implementation
        print(f"ControlNet model {control_type} not fully implemented yet, using fallback")
        return None
        
    except Exception as e:
        print(f"Error loading ControlNet model {control_type}: {e}")
        return None

# --- Expose style presets and image config for webapp ---
STYLE_PRESETS = STYLE_PRESETS
IMAGE_CONFIG = IMAGE_CONFIG

# --- ControlNet Functions ---
def process_control_image(image, control_type):
    """Process an image for ControlNet based on the control type"""
    if control_type not in controlnet_processors:
        return image
    
    # Convert PIL image to numpy array
    image_np = np.array(image)
    
    try:
        if control_type == "canny":
            # Apply Canny edge detection
            low_threshold = CONTROLNET_CONFIG["preprocessor_settings"]["canny"]["low_threshold"]
            high_threshold = CONTROLNET_CONFIG["preprocessor_settings"]["canny"]["high_threshold"]
            processed = controlnet_processors["canny"](image_np, low_threshold, high_threshold)
        elif control_type == "pose":
            # Apply pose detection
            detect_resolution = CONTROLNET_CONFIG["preprocessor_settings"]["pose"]["detect_resolution"]
            image_resolution = CONTROLNET_CONFIG["preprocessor_settings"]["pose"]["image_resolution"]
            processed = controlnet_processors["pose"](image_np, detect_resolution, image_resolution)
        elif control_type == "depth":
            # For depth, we'll use a simple grayscale conversion as a fallback
            # In a full implementation, you'd use a depth estimation model
            processed = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
        elif control_type == "segmentation":
            # For segmentation, we'll use a simple color-based segmentation as a fallback
            # In a full implementation, you'd use a segmentation model
            detect_resolution = CONTROLNET_CONFIG["preprocessor_settings"]["segmentation"]["detect_resolution"]
            processed = controlnet_processors["hed"](image_np, detect_resolution)
        else:
            return image
        
        # Convert back to PIL Image
        return Image.fromarray(processed)
    except Exception as e:
        print(f"Error processing control image for {control_type}: {e}")
        return image

def generate_with_controlnet(prompt, control_image, control_type, control_strength=1.0, guidance_start=0.0, guidance_end=1.0, negative_prompt="", **kwargs):
    """Generate an image using ControlNet"""
    try:
        # Load ControlNet pipeline on-demand
        controlnet_pipe = load_controlnet_model(control_type)
        if controlnet_pipe is None:
            print(f"ControlNet model {control_type} not available, falling back to regular generation")
            return pipe(prompt, negative_prompt=negative_prompt, **kwargs).images[0]
        
        # Process the control image
        processed_control_image = process_control_image(control_image, control_type)
        
        # Generate with ControlNet
        result = controlnet_pipe(
            prompt,
            image=processed_control_image,
            negative_prompt=negative_prompt,
            controlnet_conditioning_scale=control_strength,
            guidance_start=guidance_start,
            guidance_end=guidance_end,
            **kwargs
        )
        
        return result.images[0]
    except Exception as e:
        print(f"Error in ControlNet generation: {e}")
        print("Falling back to regular generation")
        return pipe(prompt, negative_prompt=negative_prompt, **kwargs).images[0]

# --- AI Functions (Top Level) ---
def generate_scene_variations(prompt, style):
    style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
    style_text = style_preset["prompt_suffix"]
    variations = []
    for variation in SCENE_VARIATIONS:
        enhanced_prompt = enhance_prompt_with_style(prompt, style)
        full_prompt = f"{enhanced_prompt}, {variation['suffix']}, {style_text}"
        variations.append(full_prompt)
    return variations

def generate_caption(scene_description):
    if tokenizer is None or model is None:
        return "Scene description"
    prompt = f"Describe this scene in one short sentence: {scene_description}"
    inputs = tokenizer(prompt, return_tensors="pt")
    device = get_optimal_device()
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    # Ensure pad_token is set to eos_token if missing
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
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
    caption = caption.replace(prompt, "").strip()
    if caption.startswith(":"):
        caption = caption[1:].strip()
    return caption if caption else "Scene description"

# --- Gradio UI Launch (Only under __main__) ---
def generate_storyboard(prompt, style, progress=gr.Progress()):
    is_valid, message = validate_prompt(prompt)
    if not is_valid:
        return None, message
    try:
        progress(0.1, desc="Generating scene variations...")
        scene_variations = generate_scene_variations(prompt, style)
        images = []
        captions = []
        style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
        negative_prompt = style_preset["negative_prompt"]
        for i, scene in enumerate(scene_variations):
            progress((i + 1) * 0.15, desc=f"Generating image {i+1}/5...")
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
            time.sleep(0.5)
        progress(0.9, desc="Creating storyboard layout...")
        storyboard = create_storyboard_layout(images, captions)
        progress(1.0, desc="Complete!")
        return storyboard, "Storyboard generated successfully!"
    except Exception as e:
        return None, f"Error generating storyboard: {str(e)}"

def create_interface():
    with gr.Blocks(title="Storyboard Generator", theme=getattr(gr.themes, UI_CONFIG["theme"].title())()) as demo:
        gr.Markdown("# 🎬 Storyboard Generator")
        gr.Markdown("Transform your script ideas into visual storyboards using AI")
        with gr.Row():
            with gr.Column(scale=1):
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
                style_info = gr.Markdown("**Cinematic**: Professional film-style with dramatic lighting")
                generate_btn = gr.Button("Generate Storyboard", variant="primary")
                status_output = gr.Textbox(label="Status", interactive=False)
                gr.Markdown("## Export")
                export_btn = gr.Button("Export to PDF")
                pdf_output = gr.File(label="Download PDF")
            with gr.Column(scale=2):
                gr.Markdown("## Generated Storyboard")
                storyboard_output = gr.Image(label="Storyboard", type="pil")
        def update_style_info(style):
            preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic"])
            return f"**{style.title()}**: {preset['description']}"
        style_dropdown.change(
            fn=update_style_info,
            inputs=[style_dropdown],
            outputs=[style_info]
        )
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
    # Models are loaded at import time
    demo = create_interface()
    demo.launch(
        server_name=UI_CONFIG["server_name"],
        server_port=UI_CONFIG["server_port"],
        share=UI_CONFIG["share"],
        show_error=UI_CONFIG["show_error"]
    ) 