// Storyboard Generator Web App JavaScript

class StoryboardGenerator {
    constructor() {
        this.currentFilename = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStyleDescription();
        this.updateModeLabel(); // Initialize mode label on load
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

        // Example prompts
        document.querySelectorAll('.example-prompt').forEach(button => {
            button.addEventListener('click', (e) => {
                const prompt = e.target.dataset.prompt;
                document.getElementById('prompt').value = prompt;
                this.updateStatus('Example prompt loaded', 'info');
            });
        });

        // Download button
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadStoryboard();
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

    getCurrentMode() {
        return document.getElementById('modeSwitch').checked ? 'ai' : 'demo';
    }

    async generateStoryboard() {
        const prompt = document.getElementById('prompt').value.trim();
        const style = document.getElementById('style').value;
        const mode = this.getCurrentMode();

        // Validation
        if (!prompt) {
            this.updateStatus('Please enter a scene description', 'error');
            return;
        }

        if (prompt.length < 10) {
            this.updateStatus('Scene description should be at least 10 characters', 'error');
            return;
        }

        // Show loading state
        if (mode === 'ai') {
            this.showAiLoadingModal();
        } else {
            this.showLoading();
        }
        this.updateStatus('Generating storyboard...', 'info');

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    style: style,
                    mode: mode
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.displayStoryboard(data);
                this.updateStatus('Storyboard generated successfully!', 'success');
            } else {
                this.updateStatus(data.error || 'Failed to generate storyboard', 'error');
            }
        } catch (error) {
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
        
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        
        progressBar.classList.remove('d-none');
        this.simulateProgress();
    }

    hideLoading() {
        const generateBtn = document.getElementById('generateBtn');
        const progressBar = document.getElementById('progressBar');
        
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Storyboard';
        
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
                statusElement.textContent = 'Ready to generate storyboard';
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
        this._aiModal = modal;
        modal.show();
    }

    hideAiLoadingModal() {
        if (this._aiModal) {
            this._aiModal.hide();
            this._aiModal = null;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.storyboardApp = new StoryboardGenerator();
    
    // Add some nice animations
    document.querySelectorAll('.card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate__animated', 'animate__fadeInUp');
    });
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