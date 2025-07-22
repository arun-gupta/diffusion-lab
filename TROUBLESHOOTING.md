# Troubleshooting Guide

Comprehensive troubleshooting guide for Diffusion Lab issues and solutions.

## Table of Contents
- [Common Issues](#common-issues)
- [Installation Problems](#installation-problems)
- [Web Application Issues](#web-application-issues)
- [Image-to-Image Issues](#image-to-image-issues)
- [Inpainting Issues](#inpainting-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tools](#debugging-tools)

## Common Issues

### Static Files Not Loading (JS/CSS 404)
- **Symptom:** The UI is broken, or clicking Generate does nothing. Browser console shows 404 for /static/js/app.js or /static/css/style.css.
- **Solution:**
  - Make sure you run the app from the project root with:
    ```bash
    python3 -m diffusionlab.api.webapp
    ```
  - Ensure Flask is configured with the correct static and template folder paths and `static_url_path='/static'`.

### AI Mode Not Available / ImportError
- **Symptom:** Error message: "AI mode is not available. Please ensure diffusionlab/tasks/storyboard.py and dependencies are present."
- **Solution:**
  - Make sure all imports in your code use absolute package paths (e.g., `from diffusionlab.config import *`).
  - Run the app from the project root.
  - Check for typos or missing files in the `diffusionlab/tasks/` directory.

### Accessibility Warning: aria-hidden and Focus
- **Symptom:** Browser console warning: "Blocked aria-hidden on an element because its descendant retained focus..."
- **Solution:**
  - This is a warning, not an error. The app will still work.
  - The app moves focus to the Generate button when the modal closes to improve accessibility.

### No /generate Request When Clicking Generate
- **Symptom:** Nothing happens when clicking Generate, and no request appears in Flask logs.
- **Solution:**
  - Check that `app.js` is loaded (no 404 in Network tab).
  - Check for JavaScript errors in the browser console.
  - Ensure the form and button IDs in the HTML match those in the JS.

### General Tips
- Always run the app from the project root.
- If you make structural changes, restart the Flask server.
- For more help, check the browser console, Flask logs, and the [Issues](https://github.com/arun-gupta/diffusion-lab/issues) page.

## Installation Problems

### Python Version Issues
- **Symptom:** "Python 3.8+ required" error
- **Solution:**
  ```bash
  python --version  # Check your Python version
  # If below 3.8, install a newer version
  ```

### Virtual Environment Issues
- **Symptom:** Package conflicts or import errors
- **Solution:**
  ```bash
  # Create a fresh virtual environment
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

### CUDA/GPU Issues
- **Symptom:** "CUDA not available" or slow performance
- **Solution:**
  - Install CUDA toolkit if you have an NVIDIA GPU
  - Use CPU mode if GPU is not available (slower but functional)
  - Check PyTorch installation: `python -c "import torch; print(torch.cuda.is_available())"`

### Memory Issues
- **Symptom:** "Out of memory" errors during generation
- **Solution:**
  - Close other applications to free up RAM
  - Use Demo mode for testing
  - Reduce image resolution in config.py
  - Use CPU mode if GPU memory is insufficient

## Web Application Issues

### Flask Server Won't Start
- **Symptom:** "Address already in use" or port conflicts
- **Solution:**
  ```bash
  # Kill existing processes on port 5001
  lsof -ti:5001 | xargs kill -9
  # Or use a different port
  export FLASK_RUN_PORT=5002
  python3 -m diffusionlab.api.webapp
  ```

### Browser Compatibility Issues
- **Symptom:** UI doesn't work in certain browsers
- **Solution:**
  - Use Chrome, Firefox, or Safari (latest versions)
  - Enable JavaScript
  - Clear browser cache and cookies
  - Try incognito/private mode

### File Upload Issues
- **Symptom:** "File upload failed" or "Invalid file type"
- **Solution:**
  - Check file size (max 10MB)
  - Ensure file format is supported (JPEG, PNG, GIF, BMP, WebP)
  - Try a different browser
  - Check file permissions

## Image-to-Image Issues

### Upload Fails
- **Symptom**: "Invalid file type" error when uploading images
- **Solution**: Ensure your image is in a supported format (JPEG, PNG, GIF, BMP, WebP)

### File Too Large
- **Symptom**: "Image file too large" error
- **Solution**: Resize your image to under 10MB before uploading

### No Transformation Effect
- **Symptom**: Output looks identical to input
- **Solution**: Increase the strength slider value (try 0.7-1.0)

### Too Much Transformation
- **Symptom**: Output is completely different from input
- **Solution**: Decrease the strength slider value (try 0.1-0.3)

### Poor Quality Results
- **Symptom**: Transformed image looks blurry or distorted
- **Solution**: 
  - Use higher quality input images
  - Try different strength values
  - Experiment with different style presets
  - Use more descriptive prompts

### Index Out of Bounds Error
- **Symptom**: "index 31 is out of bounds for dimension 0 with size 31"
- **Solution**:
  - This is a known issue with certain inference step configurations
  - The system automatically reduces steps for img2img mode
  - Try using Demo mode first to test functionality

## Inpainting Issues

### Canvas Not Loading
- **Symptom**: Drawing canvas doesn't appear after uploading image
- **Solution**: Refresh the page and try uploading again. Ensure JavaScript is enabled.

### Mask Not Drawing
- **Symptom**: Can't draw on the canvas or mask doesn't appear
- **Solution**: Check that you've selected the Brush tool (should be highlighted). Try refreshing the page.

### Poor Inpainting Results
- **Symptom**: Generated content doesn't blend well or looks unrealistic
- **Solution**: 
  - Draw more precise masks around object edges
  - Use more descriptive prompts that match the image context
  - Try different styles that complement the original image
  - Start with smaller areas and refine your masks
  - Use the "Test Mask" button to verify your mask is being detected correctly
  - Check the mask coverage percentage in the test results

### Entire Image Being Changed Instead of Masked Areas
- **Symptom**: The whole image gets transformed instead of just the masked portions
- **Solution**:
  - Use the "Test Mask" button to check if your mask is being detected
  - Ensure you're drawing with the red brush tool (not eraser)
  - Try the inverted mask option if the original mask doesn't work
  - Check that the inpainting pipeline is available in the test results
  - Draw larger, more visible brush strokes for better detection

### Mask Detection Issues
- **Symptom**: Mask not being detected or very low coverage percentage
- **Solution**:
  - Use pure red brush strokes (the system detects red channel)
  - Draw thicker strokes for better detection
  - Avoid very small, isolated brush strokes
  - Check the debug information in the Test Mask results
  - Try redrawing the mask with more coverage

### Mask Preview Not Working
- **Symptom**: Preview button doesn't show mask overlay
- **Solution**: Ensure you've drawn a mask first. Try clearing and redrawing the mask.

### Inpainting Pipeline Not Available
- **Symptom**: "Inpainting pipeline not available" in test results
- **Solution**:
  - Ensure you're running in AI mode (not Demo mode)
  - Check that StableDiffusionXLInpaintPipeline is properly loaded
  - Restart the application
  - Check for memory issues

## Performance Issues

### Slow Generation
- **Symptom**: Takes a very long time to generate images
- **Solution**:
  - Use Demo mode for quick testing
  - Ensure you have a GPU with CUDA support
  - Close other applications to free up resources
  - Reduce image resolution in configuration
  - Use fewer inference steps

### High Memory Usage
- **Symptom**: System becomes slow or crashes during generation
- **Solution**:
  - Monitor memory usage with `htop` or Task Manager
  - Use smaller batch sizes
  - Generate one image at a time
  - Restart the application periodically
  - Use CPU mode if GPU memory is insufficient

### Model Loading Issues
- **Symptom**: "Model not found" or long loading times
- **Solution**:
  - Check internet connection for model downloads
  - Clear model cache: `rm -rf ~/.cache/huggingface/`
  - Use Demo mode if models fail to load
  - Check available disk space

## Debugging Tools

### How to Check Flask Logs
- When running the app, watch the terminal for error messages or tracebacks after you perform an action in the UI (like clicking Generate).
- 500 errors or ImportErrors will be shown here and can help pinpoint the problem.

### How to Use Browser Developer Tools
- **Open Developer Tools:** Press F12 or right-click and select "Inspect" in your browser.
- **Console Tab:** Shows JavaScript errors, warnings, and logs. Red errors here often indicate why the UI is not working.
- **Network Tab:** Shows all network requests. Look for 404s (missing files) or 500s (server errors) when you click Generate or load the page.
- **Tip:** If you see a request to `/generate` with a 500 error, check the Flask logs for the cause.

### Debug Mode
- Enable debug mode for more detailed error messages:
  ```bash
  export FLASK_DEBUG=1
  python3 -m diffusionlab.api.webapp
  ```

### Test Individual Components
- Test image generation separately:
  ```bash
  python3 -m diffusionlab.tasks.storyboard
  ```
- Test demo mode:
  ```bash
  python3 -m diffusionlab.tasks.demo
  ```

### Common Error Messages

#### ImportError: No module named 'diffusionlab'
- **Cause**: Running from wrong directory or virtual environment not activated
- **Solution**: Ensure you're in the project root and virtual environment is active

#### CUDA out of memory
- **Cause**: GPU memory insufficient for model
- **Solution**: Use CPU mode or reduce image resolution

#### 500 Internal Server Error
- **Cause**: Backend processing error
- **Solution**: Check Flask logs for specific error details

#### 404 Not Found
- **Cause**: Static files not found
- **Solution**: Ensure running from project root with correct static file paths

## Getting Help

### Before Asking for Help
1. Check this troubleshooting guide
2. Search existing [Issues](https://github.com/arun-gupta/diffusion-lab/issues)
3. Check browser console for JavaScript errors
4. Check Flask logs for server errors
5. Try reproducing the issue in Demo mode

### When Reporting Issues
Include the following information:
- Operating system and Python version
- Error messages from browser console and Flask logs
- Steps to reproduce the issue
- Screenshots if applicable
- Whether the issue occurs in Demo mode or AI mode only

### Community Resources
- [GitHub Issues](https://github.com/arun-gupta/diffusion-lab/issues)
- [GitHub Discussions](https://github.com/arun-gupta/diffusion-lab/discussions)
- [Documentation](https://github.com/arun-gupta/diffusion-lab#readme) 