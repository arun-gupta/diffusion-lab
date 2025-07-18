#!/usr/bin/env python3
"""
Setup script for Storyboard Generator
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment '{venv_name}' already exists")
        return True
    
    print(f"📦 Creating virtual environment '{venv_name}'...")
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activation_command():
    """Get the activation command for the virtual environment"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the pip command to use
    if os.path.exists("venv"):
        if platform.system().lower() == "windows":
            pip_cmd = "venv\\Scripts\\pip"
        else:
            pip_cmd = "venv/bin/pip"
    else:
        pip_cmd = "pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_output_directory():
    """Create output directory for generated storyboards"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created output directory: {output_dir}")
    else:
        print(f"✅ Output directory already exists: {output_dir}")

def main():
    """Main setup function"""
    print("🎬 Storyboard Generator Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create output directory
    create_output_directory()
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\nTo run the application:")
    print(f"1. Activate the virtual environment:")
    print(f"   {get_activation_command()}")
    print("2. Run the application:")
    print("   python app.py")
    print("\nThe application will be available at: http://localhost:7860")
    print("\nNote: First run may take several minutes to download AI models.")

if __name__ == "__main__":
    main() 