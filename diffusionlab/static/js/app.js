// Storyboard Generator Web App JavaScript

class StoryboardGenerator {
    constructor() {
        this.currentFilename = null;
        this._aiModal = null;
        this._aiCancelled = false;
        this.uploadedImagePath = null;
        this.inpaintingImagePath = null;
        this.controlnetImagePath = null;
        this.canvas = null;
        this.ctx = null;
        this.isDrawing = false;
        this.currentTool = 'brush';
        this.brushSize = 20;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStyleDescription();

        this.updateStatusMessage(); // Initialize status message
        this.updateModeIndicator(); // Initialize mode indicator on load
        this.updateExamplePromptVisibility(); // Initialize example prompt visibility on load
        this.updateModeUI(); // Initialize mode-specific UI sections on load
    }

    bindEvents() {
        // Form submission
        const form = document.getElementById('storyboardForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateStoryboard();
        });

        // Style change
        document.getElementById('style').addEventListener('change', () => {
            this.updateStyleDescription();
        });



        // Mode selector
        document.getElementById('generationMode').addEventListener('change', () => {
            console.log('[DEBUG] Generation mode changed');
            this.updateModeUI();
        });

        // Example prompts are handled by event delegation at the bottom of the file

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

        // Batch generation functionality
        document.getElementById('batchCount').addEventListener('input', (e) => {
            document.getElementById('batchCountValue').textContent = e.target.value;
        });

        document.getElementById('variationStrength').addEventListener('input', (e) => {
            document.getElementById('variationStrengthValue').textContent = e.target.value;
        });

        // ControlNet functionality
        document.getElementById('controlStrength').addEventListener('input', (e) => {
            document.getElementById('controlStrengthValue').textContent = e.target.value;
        });

        document.getElementById('guidanceStart').addEventListener('input', (e) => {
            document.getElementById('guidanceStartValue').textContent = e.target.value;
        });

        document.getElementById('guidanceEnd').addEventListener('input', (e) => {
            document.getElementById('guidanceEndValue').textContent = e.target.value;
        });

        // ControlNet functionality
        document.getElementById('controlnetImage').addEventListener('change', (e) => {
            this.handleControlnetImageUpload(e);
        });

        document.getElementById('removeControlnetImage').addEventListener('click', () => {
            this.removeControlnetImage();
        });

        // Inpainting functionality
        document.getElementById('inpaintingImage').addEventListener('change', (e) => {
            this.handleInpaintingImageUpload(e);
        });

        document.getElementById('removeInpaintingImage').addEventListener('click', () => {
            this.removeInpaintingImage();
        });

        // Canvas tools
        document.getElementById('brushTool').addEventListener('click', () => {
            this.setTool('brush');
        });

        document.getElementById('eraserTool').addEventListener('click', () => {
            this.setTool('eraser');
        });

        document.getElementById('clearMask').addEventListener('click', () => {
            this.clearMask();
        });

        document.getElementById('invertMask').addEventListener('click', () => {
            this.invertMask();
        });

        document.getElementById('previewMask').addEventListener('click', () => {
            this.previewMask();
        });

        document.getElementById('testMask').addEventListener('click', () => {
            this.testMask();
        });

        // Prompt Chaining functionality
        document.getElementById('addPromptStep').addEventListener('click', () => {
            this.addPromptStep();
        });

        document.getElementById('loadTemplate').addEventListener('click', () => {
            this.loadTemplate();
        });

        document.getElementById('clearPrompts').addEventListener('click', () => {
            this.clearPrompts();
        });

        document.getElementById('evolutionStrength').addEventListener('input', (e) => {
            document.getElementById('strengthValue2').textContent = e.target.value;
        });

        // Example prompt chain templates
        document.querySelectorAll('.example-prompt-chain').forEach(button => {
            button.addEventListener('click', (e) => {
                const template = e.target.dataset.template;
                this.loadPromptChainTemplate(template);
            });
        });
    }

    async handleControlnetImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            this.updateStatus('Please select a valid image file', 'error');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('/upload-controlnet', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                this.controlnetImagePath = data.image_path;
                this.showControlnetPreview(file);
                this.updateStatus('ControlNet reference image uploaded successfully', 'success');
            } else {
                const errorData = await response.json();
                this.updateStatus(errorData.error || 'Failed to upload image', 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.updateStatus('Upload failed. Please try again.', 'error');
        }
    }

    showControlnetPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewImg = document.getElementById('controlnetPreviewImg');
            const previewContainer = document.getElementById('controlnetPreview');
            
            previewImg.src = e.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    removeControlnetImage() {
        this.controlnetImagePath = null;
        document.getElementById('controlnetImage').value = '';
        document.getElementById('controlnetPreview').style.display = 'none';
        this.updateStatus('ControlNet reference image removed', 'info');
    }

    updateStyleDescription() {
        const styleSelect = document.getElementById('style');
        const selectedOption = styleSelect.options[styleSelect.selectedIndex];
        const description = selectedOption.dataset.description;
        document.getElementById('styleDescription').textContent = description;
    }



    updateModeUI() {
        const mode = this.getCurrentMode();
        const genType = document.getElementById('generationMode').value;
        console.log('[DEBUG] updateModeUI called, genType:', genType);
        
        // Helper function to safely add/remove classes
        const safeClassAction = (elementId, action, className) => {
            const element = document.getElementById(elementId);
            if (element) {
                if (action === 'add') element.classList.add(className);
                else if (action === 'remove') element.classList.remove(className);
            }
        };
        
        // Hide all sections first
        document.getElementById('img2imgSection').style.display = 'none';
        document.getElementById('inpaintingSection').style.display = 'none';
        document.getElementById('promptChainingSection').style.display = 'none';
        document.getElementById('batchSection').style.display = 'none';
        document.getElementById('controlnetSection').style.display = 'none';
        document.getElementById('mainPromptSection').style.display = 'block';
        
        if (genType === 'single') {
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.remove('d-none');
            document.getElementById('storyboardContainer').classList.add('d-none');
        } else if (genType === 'img2img') {
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.remove('d-none');
            document.getElementById('storyboardContainer').classList.add('d-none');
            document.getElementById('img2imgSection').style.display = 'block';
            // Show placeholder if no image is uploaded
            if (!this.uploadedImagePath) {
                document.getElementById('img2imgPlaceholder').style.display = 'block';
                document.getElementById('imagePreview').style.display = 'none';
            }
        } else if (genType === 'inpainting') {
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.remove('d-none');
            document.getElementById('storyboardContainer').classList.add('d-none');
            document.getElementById('inpaintingSection').style.display = 'block';
            // Show placeholder if no image is uploaded
            if (!this.inpaintingImagePath) {
                document.getElementById('inpaintingPlaceholder').style.display = 'block';
                document.getElementById('inpaintingPreview').style.display = 'none';
                document.getElementById('inpaintingCanvasContainer').style.display = 'none';
            }
        } else if (genType === 'batch') {
            console.log('[DEBUG] Showing batch section');
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.add('d-none');
            document.getElementById('storyboardContainer').classList.remove('d-none');
            document.getElementById('batchSection').style.display = 'block';
            // Clear any uploaded images when switching to batch mode
            this.removeUploadedImage();
            this.removeInpaintingImage();
        } else if (genType === 'controlnet') {
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.remove('d-none');
            document.getElementById('storyboardContainer').classList.add('d-none');
            document.getElementById('controlnetSection').style.display = 'block';
            // Clear any uploaded images when switching to controlnet mode
            this.removeUploadedImage();
            this.removeInpaintingImage();
        } else if (genType === 'prompt-chaining') {
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.add('d-none');
            document.getElementById('storyboardContainer').classList.remove('d-none');
            document.getElementById('promptChainingSection').style.display = 'block';
            document.getElementById('mainPromptSection').style.display = 'none';
            // Clear any uploaded images when switching to prompt chaining mode
            this.removeUploadedImage();
            this.removeInpaintingImage();
        } else {
            // Storyboard mode
            const captionsCard = document.getElementById('captionsCard');
            safeClassAction('captionsCard', 'add', 'd-none');
            document.getElementById('singleImageContainer').classList.add('d-none');
            document.getElementById('storyboardContainer').classList.remove('d-none');
            // Clear any uploaded images when switching to storyboard mode
            this.removeUploadedImage();
            this.removeInpaintingImage();
        }
        
        // Update status message
        this.updateStatusMessage();
        
        // Update example prompt visibility
        this.updateExamplePromptVisibility();
        
        // Update mode indicator
        this.updateModeIndicator();
    }

    updateStatusMessage() {
        const genType = document.getElementById('generationMode').value;
        const statusElement = document.getElementById('status');
        
        if (statusElement.className.includes('text-muted')) {
            const defaultMessage = genType === 'img2img' ? 'Ready to transform image' :
                                 genType === 'inpainting' ? 'Ready to fill masked areas' :
                                 genType === 'prompt-chaining' ? 'Ready to create story evolution' :
                                 genType === 'batch' ? 'Ready to generate variations' :
                                 genType === 'controlnet' ? 'Ready to generate with precise control' :
                                 genType === 'single' ? 'Ready to generate art' :
                                 'Ready to generate storyboard';
            statusElement.textContent = defaultMessage;
        }
    }

    updateExamplePromptVisibility() {
        const genType = document.getElementById('generationMode').value;
        
        // Get all example prompt tabs
        const storyboardTab = document.getElementById('storyboard-tab');
        const singleTab = document.getElementById('single-tab');
        const batchTab = document.getElementById('batch-tab');
        const controlnetTab = document.getElementById('controlnet-tab');
        const img2imgTab = document.getElementById('img2img-tab');
        const inpaintingTab = document.getElementById('inpainting-tab');
        const promptChainingTab = document.getElementById('prompt-chaining-tab');
        
        // Get all example prompt tab panes
        const storyboardExamples = document.getElementById('storyboard-examples');
        const singleExamples = document.getElementById('single-examples');
        const batchExamples = document.getElementById('batch-examples');
        const controlnetExamples = document.getElementById('controlnet-examples');
        const img2imgExamples = document.getElementById('img2img-examples');
        const inpaintingExamples = document.getElementById('inpainting-examples');
        const promptChainingExamples = document.getElementById('prompt-chaining-examples');
        
        // Reset all tabs and panes to default state
        [storyboardTab, singleTab, batchTab, controlnetTab, img2imgTab, inpaintingTab, promptChainingTab].forEach(tab => {
            if (tab) {
                tab.classList.remove('disabled');
                tab.style.opacity = '1';
                tab.style.pointerEvents = 'auto';
            }
        });
        
        // Disable tabs that don't match the current generation type
        if (genType === 'storyboard') {
            // Enable only storyboard examples
            this.disableExampleTab(singleTab, 'Single-Image Art');
            this.disableExampleTab(img2imgTab, 'Image-to-Image');
            this.disableExampleTab(inpaintingTab, 'Inpainting');
            this.disableExampleTab(promptChainingTab, 'Prompt Chaining');
            
            // Show storyboard examples by default
            if (storyboardTab && !storyboardTab.classList.contains('active')) {
                storyboardTab.click();
            }
        } else if (genType === 'single') {
            // Enable only single image examples
            this.disableExampleTab(storyboardTab, 'Storyboard');
            this.disableExampleTab(batchTab, 'Batch Generation');
            this.disableExampleTab(img2imgTab, 'Image-to-Image');
            this.disableExampleTab(inpaintingTab, 'Inpainting');
            this.disableExampleTab(promptChainingTab, 'Prompt Chaining');
            
            // Show single image examples by default
            if (singleTab && !singleTab.classList.contains('active')) {
                singleTab.click();
            }
        } else if (genType === 'batch') {
            // Enable only batch generation examples
            this.disableExampleTab(storyboardTab, 'Storyboard');
            this.disableExampleTab(singleTab, 'Single-Image Art');
            this.disableExampleTab(controlnetTab, 'ControlNet');
            this.disableExampleTab(img2imgTab, 'Image-to-Image');
            this.disableExampleTab(inpaintingTab, 'Inpainting');
            this.disableExampleTab(promptChainingTab, 'Prompt Chaining');
            
            // Show batch examples by default
            if (batchTab && !batchTab.classList.contains('active')) {
                batchTab.click();
            }
        } else if (genType === 'controlnet') {
            // Enable only controlnet examples
            this.disableExampleTab(storyboardTab, 'Storyboard');
            this.disableExampleTab(singleTab, 'Single-Image Art');
            this.disableExampleTab(batchTab, 'Batch Generation');
            this.disableExampleTab(img2imgTab, 'Image-to-Image');
            this.disableExampleTab(inpaintingTab, 'Inpainting');
            this.disableExampleTab(promptChainingTab, 'Prompt Chaining');
            
            // Show controlnet examples by default
            if (controlnetTab && !controlnetTab.classList.contains('active')) {
                controlnetTab.click();
            }
        } else if (genType === 'img2img') {
            // Enable only img2img examples
            this.disableExampleTab(storyboardTab, 'Storyboard');
            this.disableExampleTab(singleTab, 'Single-Image Art');
            this.disableExampleTab(batchTab, 'Batch Generation');
            this.disableExampleTab(inpaintingTab, 'Inpainting');
            this.disableExampleTab(promptChainingTab, 'Prompt Chaining');
            
            // Show img2img examples by default
            if (img2imgTab && !img2imgTab.classList.contains('active')) {
                img2imgTab.click();
            }
        } else if (genType === 'inpainting') {
            // Enable only inpainting examples
            this.disableExampleTab(storyboardTab, 'Storyboard');
            this.disableExampleTab(singleTab, 'Single-Image Art');
            this.disableExampleTab(batchTab, 'Batch Generation');
            this.disableExampleTab(img2imgTab, 'Image-to-Image');
            this.disableExampleTab(promptChainingTab, 'Prompt Chaining');
            
            // Show inpainting examples by default
            if (inpaintingTab && !inpaintingTab.classList.contains('active')) {
                inpaintingTab.click();
            }
        } else if (genType === 'prompt-chaining') {
            // Enable only prompt chaining examples
            this.disableExampleTab(storyboardTab, 'Storyboard');
            this.disableExampleTab(singleTab, 'Single-Image Art');
            this.disableExampleTab(batchTab, 'Batch Generation');
            this.disableExampleTab(img2imgTab, 'Image-to-Image');
            this.disableExampleTab(inpaintingTab, 'Inpainting');
            
            // Show prompt chaining examples by default
            if (promptChainingTab && !promptChainingTab.classList.contains('active')) {
                promptChainingTab.click();
            }
        }
    }

    disableExampleTab(tab, modeName) {
        if (tab) {
            tab.classList.add('disabled');
            tab.style.opacity = '0.5';
            tab.style.pointerEvents = 'none';
            tab.title = `Not available in ${modeName} mode`;
            
            // Add click handler to show helpful message
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.updateStatus(`Switch to ${modeName} mode to see these examples`, 'info');
            });
        }
    }

    updateModeIndicator() {
        const genType = document.getElementById('generationMode').value;
        const indicator = document.getElementById('currentModeIndicator');
        
        if (indicator) {
            const modeNames = {
                'storyboard': 'Storyboard',
                'single': 'Single-Image Art',
                'batch': 'Batch Generation',
                'controlnet': 'ControlNet',
                'img2img': 'Image-to-Image',
                'inpainting': 'Inpainting',
                'prompt-chaining': 'Story Evolution'
            };
            
            const modeName = modeNames[genType] || 'Storyboard';
            indicator.textContent = modeName;
            
            // Update badge color based on mode
            indicator.className = 'badge ms-2';
            if (genType === 'storyboard') {
                indicator.classList.add('bg-primary');
            } else if (genType === 'single') {
                indicator.classList.add('bg-success');
            } else if (genType === 'batch') {
                indicator.classList.add('bg-secondary');
            } else if (genType === 'controlnet') {
                indicator.classList.add('bg-dark');
            } else if (genType === 'img2img') {
                indicator.classList.add('bg-info');
            } else if (genType === 'inpainting') {
                indicator.classList.add('bg-warning');
            } else if (genType === 'prompt-chaining') {
                indicator.classList.add('bg-danger');
            }
        }
    }

    getCurrentMode() {
        // Always return 'ai' mode now that demo mode is removed
        return 'ai';
    }

    async generateStoryboard() {
        const prompt = document.getElementById('prompt').value.trim();
        const style = document.getElementById('style').value;
        const mode = this.getCurrentMode();
        const genType = document.getElementById('generationMode').value;

        // Validation - Skip main prompt validation for prompt chaining and controlnet modes
        if (genType !== 'prompt-chaining' && genType !== 'controlnet') {
            if (!prompt) {
                this.updateStatus('Please enter a scene description', 'error');
                return;
            }

            if (prompt.length < 10) {
                this.updateStatus('Scene description should be at least 10 characters', 'error');
                return;
            }
        }

        // Additional validation for img2img mode
        if (genType === 'img2img' && !this.uploadedImagePath) {
            this.updateStatus('Please upload an input image for Image-to-Image mode', 'error');
            return;
        }

        // Additional validation for inpainting mode
        if (genType === 'inpainting' && !this.inpaintingImagePath) {
            this.updateStatus('Please upload an input image for Inpainting mode', 'error');
            return;
        }

        // Additional validation for prompt chaining mode
        if (genType === 'prompt-chaining') {
            const promptSteps = document.querySelectorAll('.prompt-input');
            const validPrompts = Array.from(promptSteps).filter(step => step.value.trim().length >= 10);
            
            if (validPrompts.length < 2) {
                this.updateStatus('Please enter at least 2 prompts with at least 10 characters each', 'error');
                return;
            }
        }
        
        // Additional validation for batch generation mode
        if (genType === 'batch') {
            if (!prompt) {
                this.updateStatus('Please enter a scene description for batch generation', 'error');
                return;
            }
            if (prompt.length < 10) {
                this.updateStatus('Scene description should be at least 10 characters for batch generation', 'error');
                return;
            }
        }

        // Additional validation for controlnet mode
        if (genType === 'controlnet') {
            if (!prompt) {
                this.updateStatus('Please enter a scene description for ControlNet generation', 'error');
                return;
            }
            if (prompt.length < 10) {
                this.updateStatus('Scene description should be at least 10 characters for ControlNet generation', 'error');
                return;
            }
            if (!this.controlnetImagePath) {
                this.updateStatus('Please upload a reference image for ControlNet', 'error');
                return;
            }
        }

        // Show loading state
        if (mode === 'ai') {
            this._aiCancelled = false;
            this.showAiLoadingModal();
        } else {
            this.showLoading();
        }
        const statusMessage = genType === 'img2img' ? 'Transforming image...' : 
                             genType === 'inpainting' ? 'Filling masked areas...' :
                             genType === 'prompt-chaining' ? 'Creating story evolution...' :
                             genType === 'batch' ? 'Generating variations...' :
                             genType === 'controlnet' ? 'Generating with precise control...' :
                             genType === 'single' ? 'Generating art...' : 
                             'Generating storyboard...';
        this.updateStatus(statusMessage, 'info');

        try {
            const strength = parseFloat(document.getElementById('strengthSlider').value);
            const img2img = this.uploadedImagePath !== null;
            const inpainting = this.inpaintingImagePath !== null;
            
            // Get mask data for inpainting
            let maskData = null;
            if (genType === 'inpainting' && this.canvas) {
                maskData = this.canvas.toDataURL('image/png');
                console.log('[DEBUG] Canvas mask data length:', maskData.length);
                console.log('[DEBUG] Canvas mask data preview:', maskData.substring(0, 100) + '...');
            }
            
            // Get prompt chaining data
            let promptChainData = null;
            if (genType === 'prompt-chaining') {
                const promptSteps = document.querySelectorAll('.prompt-input');
                promptChainData = Array.from(promptSteps)
                    .map(step => step.value.trim())
                    .filter(prompt => prompt.length >= 10);
                
                const evolutionStrength = parseFloat(document.getElementById('evolutionStrength').value);
                const chainLayout = document.getElementById('chainLayout').value;
                
                promptChainData = {
                    prompts: promptChainData,
                    evolutionStrength: evolutionStrength,
                    layout: chainLayout
                };
            }
            
            // Get batch generation data
            let batchData = null;
            if (genType === 'batch') {
                const batchCount = parseInt(document.getElementById('batchCount').value);
                const batchLayout = document.getElementById('batchLayout').value;
                const variationStrength = parseFloat(document.getElementById('variationStrength').value);
                
                batchData = {
                    count: batchCount,
                    layout: batchLayout,
                    variationStrength: variationStrength
                };
            }

            // Get ControlNet data
            let controlnetData = null;
            if (genType === 'controlnet') {
                const controlnetModel = document.getElementById('controlnetModel').value;
                const controlStrength = parseFloat(document.getElementById('controlStrength').value);
                const guidanceStart = parseFloat(document.getElementById('guidanceStart').value);
                const guidanceEnd = parseFloat(document.getElementById('guidanceEnd').value);
                
                controlnetData = {
                    model: controlnetModel,
                    controlStrength: controlStrength,
                    guidanceStart: guidanceStart,
                    guidanceEnd: guidanceEnd
                };
            }

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
                    inpainting: inpainting,
                    inputImagePath: this.uploadedImagePath,
                    inpaintingImagePath: this.inpaintingImagePath,
                    controlnetImagePath: this.controlnetImagePath,
                    maskData: maskData,
                    strength: strength,
                    promptChain: promptChainData,
                    batch: batchData,
                    controlnet: controlnetData
                })
            });

            // If cancelled, ignore the result
            if (mode === 'ai' && this._aiCancelled) {
                this.updateStatus('AI generation cancelled.', 'info');
                return;
            }

            const data = await response.json();

            if (response.ok && data.success) {
                if (genType === 'single' || genType === 'img2img' || genType === 'inpainting' || genType === 'prompt-chaining' || genType === 'batch' || genType === 'controlnet') {
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
            if (captionsCard) captionsCard.classList.remove('d-none');
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
                                     genType === 'inpainting' ? 'Ready to fill masked areas' :
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
        } else if (genType === 'inpainting') {
            loadingTitle.textContent = 'Filling Masked Areas';
            loadingDescription.textContent = 'Generating new content for the masked areas...';
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
            document.getElementById('img2imgPlaceholder').style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    removeUploadedImage() {
        this.uploadedImagePath = null;
        document.getElementById('inputImage').value = '';
        document.getElementById('imagePreview').style.display = 'none';
        document.getElementById('img2imgPlaceholder').style.display = 'block';
        document.getElementById('previewImg').src = '';
        this.updateStatus('Image removed', 'info');
    }

    // Inpainting methods
    async handleInpaintingImageUpload(event) {
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
            this.updateStatus('Uploading image for inpainting...', 'info');
            
            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.inpaintingImagePath = data.filepath;
                this.showInpaintingCanvas(file);
                this.updateStatus('Image uploaded successfully! Draw masks on areas you want to change.', 'success');
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

    showInpaintingCanvas(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('inpaintingPreviewImg').src = e.target.result;
            document.getElementById('inpaintingPreview').style.display = 'block';
            document.getElementById('inpaintingCanvasContainer').style.display = 'block';
            document.getElementById('inpaintingPlaceholder').style.display = 'none';
            
            // Initialize canvas
            this.initCanvas(e.target.result);
        };
        reader.readAsDataURL(file);
    }

    initCanvas(imageSrc) {
        this.canvas = document.getElementById('inpaintingCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Load image and draw it on canvas as background
        const img = new Image();
        img.onload = () => {
            // Clear canvas and draw image as background
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
            
            // Set up drawing events
            this.setupCanvasEvents();
            
            console.log('[DEBUG] Canvas initialized with image background');
            console.log('[DEBUG] Canvas size:', this.canvas.width, 'x', this.canvas.height);
            console.log('[DEBUG] Image size:', img.naturalWidth, 'x', img.naturalHeight);
        };
        img.src = imageSrc;
    }

    setupCanvasEvents() {
        this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
        this.canvas.addEventListener('mousemove', this.draw.bind(this));
        this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
        this.canvas.addEventListener('mouseout', this.stopDrawing.bind(this));
        
        // Touch events for mobile
        this.canvas.addEventListener('touchstart', this.handleTouch.bind(this));
        this.canvas.addEventListener('touchmove', this.handleTouch.bind(this));
        this.canvas.addEventListener('touchend', this.stopDrawing.bind(this));
    }

    startDrawing(e) {
        this.isDrawing = true;
        this.draw(e);
    }

    draw(e) {
        if (!this.isDrawing) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);
        
        this.ctx.lineWidth = this.brushSize;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        
        if (this.currentTool === 'brush') {
            this.ctx.globalCompositeOperation = 'source-over';
            // Use pure red with full opacity for better mask detection
            this.ctx.strokeStyle = 'rgb(255, 0, 0)';  // Pure red, no transparency
            console.log('[DEBUG] Drawing red brush stroke at:', x, y);
        } else {
            this.ctx.globalCompositeOperation = 'destination-out';
            console.log('[DEBUG] Erasing at:', x, y);
        }
        
        this.ctx.lineTo(x, y);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
    }

    stopDrawing() {
        this.isDrawing = false;
        this.ctx.beginPath();
    }

    handleTouch(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 
                                        e.type === 'touchmove' ? 'mousemove' : 'mouseup', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        this.canvas.dispatchEvent(mouseEvent);
    }

    setTool(tool) {
        this.currentTool = tool;
        
        // Update button states
        document.getElementById('brushTool').classList.remove('active');
        document.getElementById('eraserTool').classList.remove('active');
        
        if (tool === 'brush') {
            document.getElementById('brushTool').classList.add('active');
        } else {
            document.getElementById('eraserTool').classList.add('active');
        }
    }

    clearMask() {
        if (this.ctx) {
            // Clear the canvas and redraw the original image
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            // Redraw the original image as background
            const img = new Image();
            img.onload = () => {
                this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
            };
            img.src = document.getElementById('inpaintingPreviewImg').src;
        }
    }

    invertMask() {
        if (this.ctx) {
            const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
            const data = imageData.data;
            
            for (let i = 0; i < data.length; i += 4) {
                // Invert the red channel (mask) - red channel is at index 0
                data[i] = 255 - data[i];
            }
            
            this.ctx.putImageData(imageData, 0, 0);
        }
    }

    previewMask() {
        if (this.canvas) {
            // Create a preview by overlaying the mask on the original image
            const previewCanvas = document.createElement('canvas');
            previewCanvas.width = this.canvas.width;
            previewCanvas.height = this.canvas.height;
            const previewCtx = previewCanvas.getContext('2d');
            
            // Draw original image
            const img = new Image();
            img.onload = () => {
                previewCtx.drawImage(img, 0, 0, previewCanvas.width, previewCanvas.height);
                
                // Overlay mask
                previewCtx.globalCompositeOperation = 'multiply';
                previewCtx.drawImage(this.canvas, 0, 0);
                
                // Show preview
                const previewUrl = previewCanvas.toDataURL();
                const previewWindow = window.open();
                previewWindow.document.write(`
                    <html>
                        <head><title>Mask Preview</title></head>
                        <body style="margin:0;background:#333;display:flex;justify-content:center;align-items:center;min-height:100vh;">
                            <img src="${previewUrl}" style="max-width:90%;max-height:90%;border:2px solid #fff;">
                        </body>
                    </html>
                `);
            };
            img.src = document.getElementById('inpaintingPreviewImg').src;
        }
    }

    removeInpaintingImage() {
        this.inpaintingImagePath = null;
        document.getElementById('inpaintingImage').value = '';
        document.getElementById('inpaintingPreview').style.display = 'none';
        document.getElementById('inpaintingPreviewImg').src = '';
        document.getElementById('inpaintingCanvasContainer').style.display = 'none';
        document.getElementById('inpaintingPlaceholder').style.display = 'block';
        this.canvas = null;
        this.ctx = null;
        this.updateStatus('Inpainting image removed', 'info');
    }

    async testMask() {
        if (!this.canvas) {
            this.updateStatus('No canvas available for testing', 'error');
            return;
        }

        try {
            this.updateStatus('Testing mask processing...', 'info');
            
            const maskData = this.canvas.toDataURL('image/png');
                            console.log('[DEBUG] Testing mask data length:', maskData.length);
                console.log('[DEBUG] Canvas actual size:', this.canvas.width, 'x', this.canvas.height);
                console.log('[DEBUG] Canvas display size:', this.canvas.offsetWidth, 'x', this.canvas.offsetHeight);
            
            const response = await fetch('/test-mask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    maskData: maskData
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                console.log('[DEBUG] Mask test successful:', data);
                this.updateStatus(`Mask test successful! Size: ${data.mask_size[0]}x${data.mask_size[1]}, Mode: ${data.mask_mode}`, 'success');
                
                // Create and show a modal instead of popup
                this.showMaskTestModal(data);
            } else {
                console.error('[DEBUG] Mask test failed:', data);
                this.updateStatus(data.error || 'Mask test failed', 'error');
            }
        } catch (error) {
            console.error('[DEBUG] Mask test error:', error);
            this.updateStatus('Error testing mask', 'error');
        }
    }

    showMaskTestModal(data) {
        // Remove existing modal if any
        const existingModal = document.getElementById('maskTestModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Create modal HTML
        const modalHTML = `
            <div class="modal fade" id="maskTestModal" tabindex="-1" aria-labelledby="maskTestModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="maskTestModalLabel">Mask Test Results</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Size:</strong> ${data.mask_size[0]}x${data.mask_size[1]}
                                </div>
                                <div class="col-md-6">
                                    <strong>Mode:</strong> ${data.mask_mode}
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Masked Pixels:</strong> ${data.masked_pixels} out of ${data.total_pixels}
                                </div>
                                <div class="col-md-6">
                                    <strong>Inpainting Pipeline:</strong> ${data.inpaint_available ? 'Available' : 'Not Available'}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Original Mask (White = Inpaint)</h6>
                                    <img src="data:image/png;base64,${data.processed_mask}" class="img-fluid border rounded" alt="Original Mask">
                                </div>
                                <div class="col-md-6">
                                    <h6>Inverted Mask (Black = Inpaint)</h6>
                                    <img src="data:image/png;base64,${data.inverted_mask}" class="img-fluid border rounded" alt="Inverted Mask">
                                </div>
                            </div>
                            <div class="alert alert-info mt-3">
                                <strong>Note:</strong> Try both masks to see which one works better for inpainting.<br>
                                If the entire image is being changed, the mask might be inverted.<br>
                                <strong>Pipeline Type:</strong> ${data.inpaint_type}
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('maskTestModal'));
        modal.show();

        // Clean up modal when hidden
        document.getElementById('maskTestModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

    // Prompt Chaining Methods
    addPromptStep() {
        const container = document.getElementById('promptChainContainer');
        const currentSteps = container.querySelectorAll('.prompt-chain-item');
        const newStepNumber = currentSteps.length + 1;
        
        if (newStepNumber > 5) {
            this.updateStatus('Maximum 5 steps allowed', 'error');
            return;
        }
        
        const stepHTML = `
            <div class="prompt-chain-item mb-3" data-step="${newStepNumber}">
                <div class="d-flex align-items-center mb-2">
                    <span class="badge bg-primary me-2">Step ${newStepNumber}</span>
                    <button type="button" class="btn btn-sm btn-outline-danger ms-auto" onclick="window.storyboardApp.removePromptStep(this)">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <textarea class="form-control prompt-input" rows="2" 
                    placeholder="e.g., The adventurer enters the cave and discovers ancient ruins"
                    required></textarea>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', stepHTML);
        this.updateStatus(`Added step ${newStepNumber}`, 'info');
    }

    removePromptStep(button) {
        const stepItem = button.closest('.prompt-chain-item');
        stepItem.remove();
        this.renumberSteps();
        this.updateStatus('Step removed', 'info');
    }

    renumberSteps() {
        const steps = document.querySelectorAll('.prompt-chain-item');
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            step.dataset.step = stepNumber;
            step.querySelector('.badge').textContent = `Step ${stepNumber}`;
        });
    }

    clearPrompts() {
        const container = document.getElementById('promptChainContainer');
        container.innerHTML = `
            <div class="prompt-chain-item mb-3" data-step="1">
                <div class="d-flex align-items-center mb-2">
                    <span class="badge bg-primary me-2">Step 1</span>
                    <button type="button" class="btn btn-sm btn-outline-danger ms-auto" onclick="window.storyboardApp.removePromptStep(this)">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <textarea class="form-control prompt-input" rows="2" 
                    placeholder="e.g., A young adventurer stands at the entrance of a mysterious cave"
                    required></textarea>
            </div>
        `;
        this.updateStatus('All prompts cleared', 'info');
    }

    loadTemplate() {
        // This will be implemented to show a template selection modal
        this.showTemplateModal();
    }

    showTemplateModal() {
        const modalHTML = `
            <div class="modal fade" id="templateModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Choose Story Template</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="list-group">
                                <button class="list-group-item list-group-item-action" data-template="character-journey">
                                    <h6>🚶 Character Journey</h6>
                                    <small>Follow a character through different stages of their journey</small>
                                </button>
                                <button class="list-group-item list-group-item-action" data-template="environmental-progression">
                                    <h6>🌍 Environmental Progression</h6>
                                    <small>Show how an environment changes over time</small>
                                </button>
                                <button class="list-group-item list-group-item-action" data-template="emotional-arc">
                                    <h6>💫 Emotional Arc</h6>
                                    <small>Visualize an emotional journey or transformation</small>
                                </button>
                                <button class="list-group-item list-group-item-action" data-template="action-sequence">
                                    <h6>⚡ Action Sequence</h6>
                                    <small>Create a dynamic action sequence</small>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('templateModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Add event listeners
        const modal = new bootstrap.Modal(document.getElementById('templateModal'));
        document.querySelectorAll('#templateModal .list-group-item').forEach(button => {
            button.addEventListener('click', (e) => {
                const template = e.currentTarget.dataset.template;
                this.loadPromptChainTemplate(template);
                modal.hide();
            });
        });

        modal.show();

        // Clean up modal when hidden
        document.getElementById('templateModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

    loadPromptChainTemplate(template) {
        const templates = {
            'character-journey': [
                'A young adventurer stands at the entrance of a mysterious cave',
                'The adventurer enters the cave and discovers ancient ruins',
                'The adventurer faces a dangerous challenge or obstacle',
                'The adventurer overcomes the challenge and finds treasure',
                'The adventurer emerges victorious with new knowledge and power'
            ],
            'environmental-progression': [
                'A peaceful forest in the early morning light',
                'Dark clouds gather and the wind begins to howl',
                'A powerful storm rages through the forest',
                'The storm passes, leaving destruction in its wake',
                'New life begins to emerge from the aftermath'
            ],
            'emotional-arc': [
                'A person sits alone in a quiet, contemplative moment',
                'Tension builds as they face an internal conflict',
                'The emotional climax reaches its peak',
                'Resolution begins as they find inner peace',
                'A transformed person emerges with new understanding'
            ],
            'action-sequence': [
                'A hero prepares for battle, checking their equipment',
                'The hero charges into action against their enemy',
                'The battle reaches its most intense moment',
                'The hero delivers the final decisive blow',
                'The hero stands victorious over the defeated foe'
            ]
        };

        if (templates[template]) {
            this.clearPrompts();
            const container = document.getElementById('promptChainContainer');
            container.innerHTML = '';
            
            templates[template].forEach((prompt, index) => {
                const stepNumber = index + 1;
                const stepHTML = `
                    <div class="prompt-chain-item mb-3" data-step="${stepNumber}">
                        <div class="d-flex align-items-center mb-2">
                            <span class="badge bg-primary me-2">Step ${stepNumber}</span>
                            <button type="button" class="btn btn-sm btn-outline-danger ms-auto" onclick="window.storyboardApp.removePromptStep(this)">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <textarea class="form-control prompt-input" rows="2" 
                            placeholder="Enter your prompt here"
                            required>${prompt}</textarea>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', stepHTML);
            });
            
            this.updateStatus(`Loaded ${template.replace('-', ' ')} template`, 'success');
        }
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
                console.log('[DEBUG] Example prompt clicked:', e.target.dataset.prompt);
                
                // Prevent any default behavior
                e.preventDefault();
                e.stopPropagation();
                
                // Check if the tab is disabled
                const tab = e.target.closest('.tab-pane');
                if (tab) {
                    const tabId = tab.id;
                    const tabButton = document.querySelector(`[data-bs-target="#${tabId}"]`);
                    if (tabButton && tabButton.classList.contains('disabled')) {
                        console.log('[DEBUG] Tab disabled, ignoring click');
                        return; // Don't process click if tab is disabled
                    }
                }
                
                const prompt = e.target.dataset.prompt;
                document.getElementById('prompt').value = prompt;
                window.storyboardApp.updateStatus('Example prompt loaded', 'info');
                document.getElementById('prompt').focus();
                console.log('[DEBUG] Prompt set, should NOT trigger generation');
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