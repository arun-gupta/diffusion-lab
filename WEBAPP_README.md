# 🎬 Storyboard Generator - Web Application

A modern, responsive web application that transforms script ideas into visual storyboards using AI.

## 🌟 Features

- **Modern Web Interface**: Clean, responsive design with Bootstrap 5
- **Real-time Generation**: AJAX-powered storyboard generation
- **Multiple Visual Styles**: Cinematic, anime, photorealistic, noir, pixar
- **Interactive UI**: Progress tracking, status updates, and smooth animations
- **Download Functionality**: Save storyboards as PNG files
- **Example Prompts**: Quick-start with pre-written scene descriptions
- **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile

## 🚀 Quick Start

### Option 1: Using the Launcher Script
```bash
./run_webapp.sh
```

### Option 2: Manual Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install Flask (if not already installed)
pip install flask

# Run the web application
python3 webapp.py
```

### Option 3: Using the Setup Script
```bash
# Run setup (creates venv and installs dependencies)
python3 setup.py

# Activate and run
source venv/bin/activate
python3 webapp.py
```

## 🌐 Access the Application

Once running, open your browser to:
**http://localhost:5001**

## 📱 How to Use

1. **Enter Scene Description**: Describe the scene you want to visualize
   - Minimum 10 characters required
   - Be descriptive for better results

2. **Choose Visual Style**: Select from 5 different styles:
   - **Cinematic**: Professional film-style with dramatic lighting
   - **Anime**: Japanese animation style with vibrant colors
   - **Photorealistic**: High-quality photographic realism
   - **Noir**: Classic film noir with dramatic shadows
   - **Pixar**: 3D animation style like Pixar films

3. **Generate Storyboard**: Click the "Generate Storyboard" button
   - Watch the progress bar as your storyboard is created
   - 5 unique panels will be generated with captions

4. **Download**: Save your storyboard as a PNG file

## 🎨 Example Prompts

Try these example prompts to get started:

- "A detective walks into a neon-lit alley at midnight, rain pouring down"
- "A robot wanders a post-apocalyptic desert searching for signs of life"
- "A young wizard discovers an ancient library hidden in the mountains"
- "A spaceship crew encounters an alien artifact on a distant planet"

## 🏗️ Architecture

### Frontend
- **HTML5**: Semantic markup with Bootstrap 5
- **CSS3**: Custom styling with animations and responsive design
- **JavaScript**: Modern ES6+ with async/await for API calls
- **Bootstrap 5**: Responsive grid system and components
- **Font Awesome**: Icons for better UX

### Backend
- **Flask**: Lightweight Python web framework
- **PIL/Pillow**: Image processing and generation
- **JSON API**: RESTful endpoints for data exchange
- **Base64 Encoding**: Image transfer to frontend

### File Structure
```
storyboard-generator/
├── webapp.py              # Main Flask application
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   └── app.js         # Frontend JavaScript
│   └── storyboards/       # Generated storyboards
├── run_webapp.sh          # Launcher script
└── requirements.txt       # Dependencies
```

## 🔧 Configuration

### Port Configuration
The default port is 5001 (changed from 5000 to avoid conflicts with macOS AirPlay).

To change the port, edit `webapp.py`:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

### Style Customization
Edit the `STYLES` dictionary in `webapp.py` to add or modify visual styles:
```python
STYLES = {
    'your_style': {
        'name': 'Your Style Name',
        'description': 'Description of the style',
        'color': '#hexcolor'
    }
}
```

## 🎯 API Endpoints

- `GET /` - Main web interface
- `POST /generate` - Generate storyboard
- `GET /download/<filename>` - Download storyboard
- `GET /api/styles` - Get available styles
- `GET /health` - Health check

## 🎨 Demo Mode

This web application runs in **demo mode** by default, which means:
- ✅ Full UI functionality
- ✅ Real-time generation
- ✅ Download capabilities
- ✅ All visual styles
- ❌ No AI models loaded (faster startup)

For full AI-powered generation, run the main application:
```bash
python3 app.py
```

## 🚀 Deployment

### Local Development
```bash
python3 webapp.py
```

### Production Deployment
For production deployment, consider:
- Using Gunicorn or uWSGI
- Setting up a reverse proxy (nginx)
- Environment variables for configuration
- SSL/TLS certificates

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 webapp:app
```

## 🔍 Troubleshooting

### Port Already in Use
If you get "Address already in use":
- Change the port in `webapp.py`
- Or kill the process using the port:
  ```bash
  lsof -ti:5001 | xargs kill -9
  ```

### Flask Not Found
```bash
pip install flask
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Performance

- **Startup Time**: ~2-3 seconds (demo mode)
- **Generation Time**: ~1-2 seconds per storyboard
- **Memory Usage**: ~50-100MB
- **File Size**: Generated storyboards ~500KB-1MB

## 🎬 What's Next?

This web application provides a solid foundation for:
- Adding real AI model integration
- User authentication and accounts
- Storyboard history and sharing
- Advanced customization options
- API access for third-party integrations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Ready to create amazing storyboards?** Open http://localhost:5001 and start visualizing your stories! 🎬✨ 