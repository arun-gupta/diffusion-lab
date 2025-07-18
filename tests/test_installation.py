#!/usr/bin/env python3
"""
Test script to verify Storyboard Generator installation
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name}: {e}")
        return False

def test_torch():
    """Test PyTorch installation and CUDA availability"""
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CUDA not available (will use CPU)")
        
        return True
    except ImportError as e:
        print(f"❌ PyTorch: {e}")
        return False

def test_diffusers():
    """Test diffusers installation"""
    try:
        from diffusers import StableDiffusionXLPipeline
        print("✅ Diffusers")
        return True
    except ImportError as e:
        print(f"❌ Diffusers: {e}")
        return False

def test_transformers():
    """Test transformers installation"""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        print("✅ Transformers")
        return True
    except ImportError as e:
        print(f"❌ Transformers: {e}")
        return False

def test_gradio():
    """Test Gradio installation"""
    try:
        import gradio as gr
        print(f"✅ Gradio {gr.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Gradio: {e}")
        return False

def test_pillow():
    """Test Pillow installation"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✅ Pillow")
        return True
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False

def test_reportlab():
    """Test ReportLab installation"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        print("✅ ReportLab")
        return True
    except ImportError as e:
        print(f"❌ ReportLab: {e}")
        return False

def test_numpy():
    """Test NumPy installation"""
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
        return True
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False

def test_matplotlib():
    """Test Matplotlib installation"""
    try:
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Matplotlib: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Storyboard Generator Installation")
    print("=" * 50)
    
    tests = [
        test_torch,
        test_diffusers,
        test_transformers,
        test_gradio,
        test_pillow,
        test_reportlab,
        test_numpy,
        test_matplotlib
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Installation is complete.")
        print("\nYou can now run the application with:")
        print("python app.py")
    else:
        print("❌ Some tests failed. Please check the installation.")
        print("\nTry running:")
        print("pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 