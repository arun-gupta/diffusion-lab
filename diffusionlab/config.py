"""
Configuration file for Storyboard Generator
"""

# Model Configuration
MODEL_CONFIG = {
    "diffusion_model": "stabilityai/stable-diffusion-xl-base-1.0",
    "text_model": "stabilityai/stablelm-3b-4e1t",
    "torch_dtype": "float32",
    "use_safetensors": True,
    "variant": "fp16"
}

# Image Generation Settings
IMAGE_CONFIG = {
    "width": 512,
    "height": 512,
    "num_inference_steps": 30,
    "guidance_scale": 7.5,
    "num_images_per_prompt": 1
}

# Text Generation Settings
TEXT_CONFIG = {
    "max_new_tokens": 50,
    "temperature": 0.7,
    "do_sample": True,
    "top_p": 0.9,
    "top_k": 50
}

# UI Configuration
UI_CONFIG = {
    "server_name": "0.0.0.0",
    "server_port": 7860,
    "share": False,
    "show_error": True,
    "theme": "soft"
}

# Style Presets
STYLE_PRESETS = {
    "cinematic": {
        "description": "Professional film-style with dramatic lighting",
        "prompt_suffix": "cinematic lighting, dramatic composition, film noir style",
        "negative_prompt": "blurry, low quality, amateur, poorly lit",
        "aspect_ratio": "2.35:1"
    },
    "anime": {
        "description": "Japanese animation style with vibrant colors",
        "prompt_suffix": "anime style, vibrant colors, detailed illustration",
        "negative_prompt": "realistic, photographic, blurry, low quality",
        "aspect_ratio": "16:9"
    },
    "photorealistic": {
        "description": "High-quality photographic realism",
        "prompt_suffix": "photorealistic, high detail, professional photography",
        "negative_prompt": "cartoon, anime, illustration, blurry, low quality",
        "aspect_ratio": "3:2"
    },
    "noir": {
        "description": "Classic film noir with dramatic shadows",
        "prompt_suffix": "film noir, black and white, dramatic shadows, moody atmosphere",
        "negative_prompt": "colorful, bright lighting, blurry, low quality",
        "aspect_ratio": "4:3"
    },
    "pixar": {
        "description": "3D animation style like Pixar films",
        "prompt_suffix": "3D animation style, Pixar-like, colorful, family-friendly",
        "negative_prompt": "realistic, dark, scary, blurry, low quality",
        "aspect_ratio": "16:9"
    }
}

# Scene Variation Templates
SCENE_VARIATIONS = [
    {
        "name": "Establishing Shot",
        "suffix": "wide shot, establishing scene",
        "description": "Shows the overall setting and context"
    },
    {
        "name": "Character Focus",
        "suffix": "medium shot, character focus",
        "description": "Focuses on the main character or subject"
    },
    {
        "name": "Emotional Close-up",
        "suffix": "close-up shot, emotional moment",
        "description": "Captures emotional details and expressions"
    },
    {
        "name": "Action Shot",
        "suffix": "action shot, dynamic composition",
        "description": "Shows movement and action in the scene"
    },
    {
        "name": "Atmospheric Shot",
        "suffix": "atmospheric shot, mood and tone",
        "description": "Emphasizes the mood and atmosphere"
    }
]

# Layout Options
LAYOUT_OPTIONS = {
    "horizontal": {
        "name": "Horizontal",
        "description": "5 panels in a single row",
        "function": "create_horizontal_layout"
    },
    "vertical": {
        "name": "Vertical",
        "description": "5 panels in a single column",
        "function": "create_vertical_layout"
    },
    "grid": {
        "name": "Grid",
        "description": "2x3 grid layout (5 panels + 1 empty)",
        "function": "create_grid_layout"
    }
}

# Export Settings
EXPORT_CONFIG = {
    "pdf_page_size": "A4",
    "pdf_margin": 50,
    "image_format": "PNG",
    "image_quality": 95,
    "output_directory": "output"
}

# Performance Settings
PERFORMANCE_CONFIG = {
    "enable_memory_efficient_attention": True,
    "enable_xformers_memory_efficient_attention": True,
    "enable_attention_slicing": True,
    "enable_model_cpu_offload": False,
    "enable_sequential_cpu_offload": False
}

# Image-to-Image Settings
IMG2IMG_CONFIG = {
    "strength": 0.75,  # How much to transform the input image (0.0 = keep original, 1.0 = completely new)
    "guidance_scale": 7.5,
    "num_inference_steps": 30,
    "width": 512,
    "height": 512,
    "num_images_per_prompt": 1
}

# Inpainting Settings
INPAINTING_CONFIG = {
    "guidance_scale": 7.5,
    "num_inference_steps": 30,
    "width": 512,
    "height": 512,
    "num_images_per_prompt": 1,
    "mask_blur": 4,  # Blur radius for mask edges
    "fill_mode": "fill",  # fill, original, latent_fill, latent_noise
    "inpaint_full_res": True,
    "inpaint_full_res_padding": 32
}

# Prompt Chaining / Story Evolution Settings
PROMPT_CHAINING_CONFIG = {
    "max_prompts": 5,  # Maximum number of prompts in a chain
    "min_prompts": 2,  # Minimum number of prompts required
    "evolution_strength": 0.3,  # How much each image influences the next (0.0-1.0)
    "style_consistency": True,  # Maintain consistent style across the chain
    "character_consistency": True,  # Maintain consistent characters across the chain
    "guidance_scale": 7.5,
    "num_inference_steps": 30,
    "width": 512,
    "height": 512,
    "num_images_per_prompt": 1,
    "chain_layout": "horizontal"  # horizontal, vertical, grid
}

# Story Evolution Templates
STORY_EVOLUTION_TEMPLATES = [
    {
        "name": "Character Journey",
        "description": "Follow a character through different stages of their journey",
        "template": [
            "Character introduction and setting",
            "Character faces a challenge or conflict",
            "Character overcomes the challenge",
            "Character learns and grows",
            "Character reaches their goal or destination"
        ]
    },
    {
        "name": "Environmental Progression",
        "description": "Show how an environment changes over time",
        "template": [
            "Initial peaceful state",
            "First signs of change or conflict",
            "Major transformation or event",
            "Aftermath and consequences",
            "New equilibrium or resolution"
        ]
    },
    {
        "name": "Emotional Arc",
        "description": "Visualize an emotional journey or transformation",
        "template": [
            "Starting emotional state",
            "Building tension or conflict",
            "Climax or peak emotion",
            "Resolution and acceptance",
            "New emotional state or growth"
        ]
    },
    {
        "name": "Action Sequence",
        "description": "Create a dynamic action sequence",
        "template": [
            "Setup and preparation",
            "First action or movement",
            "Escalation and conflict",
            "Climax of action",
            "Resolution and aftermath"
        ]
    }
]

# Validation Rules
VALIDATION_RULES = {
    "min_prompt_length": 10,
    "max_prompt_length": 500,
    "forbidden_words": ["nsfw", "explicit", "adult", "inappropriate"],
    "required_words": []
} 