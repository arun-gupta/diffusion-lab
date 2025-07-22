// Storyboard Generator Web App JavaScript

class StoryboardGenerator {
    constructor() {
        this.currentFilename = null;
        this._aiModal = null;
        this._aiCancelled = false;
        this.uploadedImagePath = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStyleDescription();
        this.updateModeLabel(); // Initialize mode label on load
        this.updateStatusMessage(); // Initialize status message
    }

    bindEvents() {
        // Form submission
        document.getElementById('storyboardForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateStoryboard();
        });

        // Style change
        document.getElementById('style').addEventListener('change', () => {
            this.updateStyleDescription();
        });

        // Mode switch
        document.getElementById('modeSwitch').addEventListener('change', (e) => {
            this.updateModeLabel();
        });

        // Mode selector
        document.getElementById('generationMode').addEventListener('change', () => {
            this.updateModeUI();
        });

        // Example prompts
        document.querySelectorAll('.example-prompt').forEach(button => {
            button.addEventListener('click', (e) => {
                const prompt = e.target.dataset.prompt;
                document.getElementById('prompt').value = prompt;
                this.updateStatus('Example prompt loaded', 'info');
                // Optionally scroll to the form or focus the prompt field
                document.getElementById('prompt').focus();
            });
        });

        // Download button
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadStoryboard();
        });

        // Cancel AI modal
        document.getElementById('aiCancelBtn').addEventListener('click', () => {
            this.cancelAiGeneration();
        });

        // Image-to-Image functionality
        document.getElementById('inputImage').addEventListener('change', (e) => {
            this.handleImageUpload(e);
        });

        document.getElementById('removeImage').addEventListener('click', () => {
            this.removeUploadedImage();
        });

        document.getElementById('strengthSlider').addEventListener('input', (e) => {
            document.getElementById('strengthValue').textContent = e.target.value;
        });
    }

    updateStyleDescription() {
        const styleSelect = document.getElementById('style');
        const selectedOption = styleSelect.options[styleSelect.selectedIndex];
        const description = selectedOption.dataset.description;
        document.getElementById('styleDescription').textContent = description;
    }

    updateModeLabel() {
        const modeSwitch = document.getElementById('modeSwitch');
        const modeLabel = document.getElementById('modeLabel');
        const modeDescription = document.getElementById('modeDescription');
        if (modeSwitch.checked) {
            modeLabel.textContent = 'Full AI (Slower)';
            modeDescription.textContent = 'Full AI mode uses Stable Diffusion and StableLM for real image and caption generation. This is much slower and requires more resources.';
        } else {
            modeLabel.textContent = 'Demo (Fast)';
            modeDescription.textContent = 'Demo mode is fast and uses placeholder images. Switch to Full AI for real AI-generated art (slower).';
        }
    }

    updateModeUI() {
        const mode = this.getCurrentMode();
        const genType = document.getElementById('generationMode').value;
        
        if (genType === 'single' || genType === 'img2img') {
            document.getElementById('captionsCard').classList.add('d-none');
            document.getElementById('singleImageContainer').classList.remove('d-none');
            document.getElementById('storyboardContainer').classList.add('d-none');
            // Show img2img section for single image and img2img modes
            document.getElementById('img2imgSection').style.display = 'block';
        } else {
            document.getElementById('captionsCard').classList.add('d-none');
            document.getElementById('singleImageContainer').classList.add('d-none');
            document.getElementById('storyboardContainer').classList.remove('d-none');
            // Hide img2img section for storyboard mode
            document.getElementById('img2imgSection').style.display = 'none';
            // Clear any uploaded image when switching to storyboard mode
            this.removeUploadedImage();
        }
        
        // Update status message
        this.updateStatusMessage();
    }

    updateStatusMessage() {
        const genType = document.getElementById('generationMode').value;
        const statusElement = document.getElementById('status');
        
        if (statusElement.className.includes('text-muted')) {
            const defaultMessage = genType === 'img2img' ? 'Ready to transform image' :
                                 genType === 'single' ? 'Ready to generate art' :
                                 'Ready to generate storyboard';
            statusElement.textContent = defaultMessage;
        }
    }

    getCurrentMode() {
        // Return 'ai' if switch is checked, else 'demo'
        return document.getElementById('modeSwitch').checked ? 'ai' : 'demo';
    }

    async generateStoryboard() {
        const prompt = document.getElementById('prompt').value.trim();
        const style = document.getElementById('style').value;
        const mode = this.getCurrentMode();
        const genType = document.getElementById('generationMode').value;

        // Validation
        if (!prompt) {
            this.updateStatus('Please enter a scene description', 'error');
            return;
        }

        if (prompt.length < 10) {
            this.updateStatus('Scene description should be at least 10 characters', 'error');
            return;
        }

        // Additional validation for img2img mode
        if (genType === 'img2img' && !this.uploadedImagePath) {
            this.updateStatus('Please upload an input image for Image-to-Image mode', 'error');
            return;
        }

        // Show loading state
        if (mode === 'ai') {
            this._aiCancelled = false;
            this.showAiLoadingModal();
        } else {
            this.showLoading();
        }
        const statusMessage = genType === 'img2img' ? 'Transforming image...' : 
                             genType === 'single' ? 'Generating art...' : 
                             'Generating storyboard...';
        this.updateStatus(statusMessage, 'info');

        try {
            const strength = parseFloat(document.getElementById('strengthSlider').value);
            const img2img = this.uploadedImagePath !== null;
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    style: style,
                    mode: mode,
                    genType: genType,
                    img2img: img2img,
                    inputImagePath: this.uploadedImagePath,
                    strength: strength
                })
            });

            // If cancelled, ignore the result
            if (mode === 'ai' && this._aiCancelled) {
                this.updateStatus('AI generation cancelled.', 'info');
                return;
            }

            const data = await response.json();

            if (response.ok && data.success) {
                if (genType === 'single' || genType === 'img2img') {
                    this.displaySingleImage(data);
                } else {
                    this.displayStoryboard(data);
                }
                this.updateStatus('Generation successful!', 'success');
            } else {
                this.updateStatus(data.error || 'Failed to generate', 'error');
            }
        } catch (error) {
            if (mode === 'ai' && this._aiCancelled) {
                this.updateStatus('AI generation cancelled.', 'info');
                return;
            }
            console.error('Error:', error);
            this.updateStatus('Network error. Please try again.', 'error');
        } finally {
            if (mode === 'ai') {
                this.hideAiLoadingModal();
            } else {
                this.hideLoading();
            }
        }
    }

    displayStoryboard(data) {
        const container = document.getElementById('storyboardContainer');
        const downloadSection = document.getElementById('downloadSection');
        const captionsCard = document.getElementById('captionsCard');
        const captionsContainer = document.getElementById('captionsContainer');

        // Display storyboard image
        container.innerHTML = `
            <img src="data:image/png;base64,${data.image}" 
                 alt="Generated Storyboard" 
                 class="storyboard-image">
        `;

        // Show download button
        downloadSection.classList.remove('d-none');
        this.currentFilename = data.filename;

        // Display captions
        if (data.captions && data.captions.length > 0) {
            captionsContainer.innerHTML = '';
            data.captions.forEach((caption, index) => {
                const captionHtml = `
                    <div class="col-md-6 col-lg-4 mb-3">
                        <div class="caption-card">
                            <div class="caption-number">Panel ${index + 1}</div>
                            <div class="caption-text">${caption}</div>
                        </div>
                    </div>
                `;
                captionsContainer.innerHTML += captionHtml;
            });
            captionsCard.classList.remove('d-none');
        }

        // Scroll to storyboard
        container.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    displaySingleImage(data) {
        // Ensure correct container visibility
        document.getElementById('singleImageContainer').classList.remove('d-none');
        document.getElementById('storyboardContainer').classList.add('d-none');
        const container = document.getElementById('singleImageContainer');
        const downloadSection = document.getElementById('downloadSection');
        container.innerHTML = `
            <img src="data:image/png;base64,${data.image}" 
                 alt="Generated Art" 
                 class="storyboard-image">
        `;
        downloadSection.classList.remove('d-none');
        this.currentFilename = data.filename;
        container.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    async downloadStoryboard() {
        if (!this.currentFilename) {
            this.updateStatus('No storyboard to download', 'error');
            return;
        }

        try {
            const response = await fetch(`/download/${this.currentFilename}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = this.currentFilename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.updateStatus('Download started!', 'success');
            } else {
                this.updateStatus('Download failed', 'error');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.updateStatus('Download failed', 'error');
        }
    }

    showLoading() {
        const generateBtn = document.getElementById('generateBtn');
        const progressBar = document.getElementById('progressBar');
        const genType = document.getElementById('generationMode').value;
        
        generateBtn.disabled = true;
        const btnText = genType === 'img2img' ? 'Transforming...' : 
                       genType === 'single' ? 'Generating...' : 
                       'Generating...';
        generateBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${btnText}`;
        
        progressBar.classList.remove('d-none');
        this.simulateProgress();
    }

    hideLoading() {
        const generateBtn = document.getElementById('generateBtn');
        const progressBar = document.getElementById('progressBar');
        
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate';
        
        progressBar.classList.add('d-none');
        progressBar.querySelector('.progress-bar').style.width = '0%';
    }

    simulateProgress() {
        const progressBar = document.getElementById('progressBar').querySelector('.progress-bar');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 90) {
                progress = 90;
                clearInterval(interval);
            }
            progressBar.style.width = progress + '%';
        }, 200);
    }

    updateStatus(message, type = 'info') {
        const statusElement = document.getElementById('status');
        statusElement.textContent = message;
        statusElement.className = `status-${type}`;
        
        // Auto-clear success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                const genType = document.getElementById('generationMode').value;
                const defaultMessage = genType === 'img2img' ? 'Ready to transform image' :
                                     genType === 'single' ? 'Ready to generate art' :
                                     'Ready to generate storyboard';
                statusElement.textContent = defaultMessage;
                statusElement.className = 'text-muted';
            }, 5000);
        }
    }

    // Utility method to show toast notifications
    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        // Add to page
        const toastContainer = document.getElementById('toastContainer') || this.createToastContainer();
        toastContainer.appendChild(toast);
        
        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove after hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }

    showAiLoadingModal() {
        const modal = new bootstrap.Modal(document.getElementById('aiLoadingModal'));
        const genType = document.getElementById('generationMode').value;
        
        // Update loading modal content based on generation type
        const loadingTitle = document.getElementById('loadingTitle');
        const loadingDescription = document.getElementById('loadingDescription');
        
        if (genType === 'img2img') {
            loadingTitle.textContent = 'Transforming Your Image';
            loadingDescription.textContent = 'Applying AI transformation to your uploaded image...';
        } else if (genType === 'single') {
            loadingTitle.textContent = 'Generating Your Art';
            loadingDescription.textContent = 'Creating a unique piece of art from your prompt...';
        } else {
            loadingTitle.textContent = 'Generating Your Storyboard';
            loadingDescription.textContent = 'Creating 5 unique panels for your scene...';
        }
        
        this._aiModal = modal;
        modal.show();
    }

    hideAiLoadingModal() {
        if (this._aiModal) {
            this._aiModal.hide();
            this._aiModal = null;
        }
    }

    cancelAiGeneration() {
        this._aiCancelled = true;
        this.hideAiLoadingModal();
        this.updateStatus('AI generation cancelled.', 'info');
    }

    async handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            this.updateStatus('Please select a valid image file (JPEG, PNG, GIF, BMP, WebP)', 'error');
            event.target.value = '';
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.updateStatus('Image file too large. Please select an image smaller than 10MB', 'error');
            event.target.value = '';
            return;
        }

        try {
            this.updateStatus('Uploading image...', 'info');
            
            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.uploadedImagePath = data.filepath;
                this.showImagePreview(file);
                this.updateStatus('Image uploaded successfully!', 'success');
            } else {
                this.updateStatus(data.error || 'Failed to upload image', 'error');
                event.target.value = '';
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.updateStatus('Failed to upload image', 'error');
            event.target.value = '';
        }
    }

    showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('previewImg').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    removeUploadedImage() {
        this.uploadedImagePath = null;
        document.getElementById('inputImage').value = '';
        document.getElementById('imagePreview').style.display = 'none';
        document.getElementById('previewImg').src = '';
        this.updateStatus('Image removed', 'info');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.storyboardApp = new StoryboardGenerator();
    // Event delegation for example prompts
    const listGroup = document.querySelector('.list-group');
    if (listGroup) {
        listGroup.addEventListener('click', function(e) {
            if (e.target.classList.contains('example-prompt')) {
                const prompt = e.target.dataset.prompt;
                document.getElementById('prompt').value = prompt;
                window.storyboardApp.updateStatus('Example prompt loaded', 'info');
                document.getElementById('prompt').focus();
            }
        });
    }
    // Add some nice animations
    document.querySelectorAll('.card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    // Accessibility: Move focus to Generate button when AI modal is hidden or about to be hidden
    const aiModal = document.getElementById('aiLoadingModal');
    if (aiModal) {
        aiModal.addEventListener('hide.bs.modal', function () {
            const generateBtn = document.getElementById('generateBtn');
            if (generateBtn) generateBtn.focus();
        });
        aiModal.addEventListener('hidden.bs.modal', function () {
            const generateBtn = document.getElementById('generateBtn');
            if (generateBtn) generateBtn.focus();
        });
    }
});

// Add CSS for animations if not already present
if (!document.querySelector('#animation-styles')) {
    const style = document.createElement('style');
    style.id = 'animation-styles';
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate__animated {
            animation-duration: 0.6s;
            animation-fill-mode: both;
        }
        
        .animate__fadeInUp {
            animation-name: fadeInUp;
        }
    `;
    document.head.appendChild(style);
} 