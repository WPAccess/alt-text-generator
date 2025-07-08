class AltTextGenerator {
    constructor() {
        this.currentData = [];
        this.currentFilename = null;
        this.processingRows = new Set();
        
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        const fileInput = document.getElementById('file-input');
        const uploadBtn = document.getElementById('upload-btn');
        const generateAllBtn = document.getElementById('generate-all-btn');
        const downloadBtn = document.getElementById('download-btn');
        
        fileInput.addEventListener('change', () => {
            uploadBtn.disabled = !fileInput.files.length;
        });
        
        uploadBtn.addEventListener('click', () => this.uploadFile());
        generateAllBtn.addEventListener('click', () => this.generateAllMissing());
        downloadBtn.addEventListener('click', () => this.downloadFile());
    }
    
    showError(message) {
        const errorSection = document.getElementById('error-section');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorSection.classList.remove('d-none');
        
        setTimeout(() => {
            errorSection.classList.add('d-none');
        }, 5000);
    }
    
    updateProgress(percentage, text) {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        progressBar.style.width = `${percentage}%`;
        progressText.textContent = text;
    }
    
    showProgress() {
        document.getElementById('progress-section').classList.remove('d-none');
    }
    
    hideProgress() {
        document.getElementById('progress-section').classList.add('d-none');
    }
    
    async uploadFile() {
        const fileInput = document.getElementById('file-input');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showError('Please select a file');
            return;
        }
        
        this.showProgress();
        this.updateProgress(10, 'Uploading file...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.currentFilename = result.filename;
                this.currentData = result.data;
                this.updateProgress(100, 'File uploaded successfully!');
                
                setTimeout(() => {
                    this.hideProgress();
                    this.displayResults();
                }, 1000);
            } else {
                this.hideProgress();
                this.showError(result.error || 'Upload failed');
            }
        } catch (error) {
            this.hideProgress();
            this.showError('Network error occurred');
            console.error('Upload error:', error);
        }
    }
    
    displayResults() {
        const resultsSection = document.getElementById('results-section');
        const tbody = document.getElementById('results-tbody');
        
        tbody.innerHTML = '';
        
        this.currentData.forEach((row, index) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.row_index}</td>
                <td>
                    <a href="${row.image_url}" target="_blank" class="text-decoration-none">
                        <i class="fas fa-external-link-alt me-1"></i>
                        ${this.truncateUrl(row.image_url)}
                    </a>
                </td>
                <td>
                    <span class="badge ${row.alt_text ? 'bg-success' : 'bg-warning'} me-2">
                        ${row.alt_text ? 'Has Alt Text' : 'Missing'}
                    </span>
                    ${row.alt_text || 'No alt text'}
                </td>
                <td>
                    <div class="generated-alt-text" id="generated-${index}">
                        ${row.needs_alt_text ? '<em class="text-muted">Not generated yet</em>' : '<em class="text-muted">Not needed</em>'}
                    </div>
                </td>
                <td>
                    ${row.needs_alt_text ? `
                        <button class="btn btn-sm btn-outline-primary me-2" onclick="altTextGenerator.generateSingle(${index})">
                            <i class="fas fa-magic me-1"></i>
                            Generate
                        </button>
                    ` : ''}
                    <button class="btn btn-sm btn-outline-secondary" onclick="altTextGenerator.editAltText(${index})">
                        <i class="fas fa-edit me-1"></i>
                        Edit
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        
        resultsSection.classList.remove('d-none');
    }
    
    truncateUrl(url) {
        return url.length > 50 ? url.substring(0, 47) + '...' : url;
    }
    
    async generateSingle(index) {
        const row = this.currentData[index];
        
        if (this.processingRows.has(index)) {
            return;
        }
        
        this.processingRows.add(index);
        
        const generatedDiv = document.getElementById(`generated-${index}`);
        generatedDiv.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
        
        try {
            const response = await fetch('/generate_alt_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: this.currentFilename,
                    row_indices: [row.row_index]
                })
            });
            
            const result = await response.json();
            
            if (response.ok && result.results.length > 0) {
                const resultData = result.results[0];
                
                if (resultData.success) {
                    generatedDiv.innerHTML = `
                        <div class="alert alert-success py-2 mb-0">
                            <strong>Generated:</strong> ${resultData.alt_text}
                        </div>
                    `;
                    
                    // Update current data
                    this.currentData[index].generated_alt_text = resultData.alt_text;
                    this.currentData[index].alt_text = resultData.alt_text;
                    this.currentData[index].was_generated = true;
                } else {
                    generatedDiv.innerHTML = `
                        <div class="alert alert-danger py-2 mb-0">
                            <strong>Error:</strong> ${resultData.error}
                        </div>
                    `;
                }
            } else {
                generatedDiv.innerHTML = `
                    <div class="alert alert-danger py-2 mb-0">
                        <strong>Error:</strong> ${result.error || 'Generation failed'}
                    </div>
                `;
            }
        } catch (error) {
            generatedDiv.innerHTML = `
                <div class="alert alert-danger py-2 mb-0">
                    <strong>Error:</strong> Network error occurred
                </div>
            `;
            console.error('Generate single error:', error);
        } finally {
            this.processingRows.delete(index);
        }
    }
    
    async generateAllMissing() {
        const missingRows = this.currentData
            .map((row, index) => ({ row, index }))
            .filter(({ row }) => row.needs_alt_text);
        
        if (missingRows.length === 0) {
            this.showError('No missing alt text found');
            return;
        }
        
        this.showProgress();
        this.updateProgress(0, `Generating alt text for ${missingRows.length} images...`);
        
        const batchSize = 3; // Process 3 images at a time
        const total = missingRows.length;
        let completed = 0;
        
        for (let i = 0; i < missingRows.length; i += batchSize) {
            const batch = missingRows.slice(i, i + batchSize);
            const promises = batch.map(({ index }) => this.generateSingle(index));
            
            await Promise.all(promises);
            
            completed += batch.length;
            const percentage = Math.round((completed / total) * 100);
            this.updateProgress(percentage, `Completed ${completed} of ${total} images`);
        }
        
        setTimeout(() => {
            this.hideProgress();
        }, 1000);
    }
    
    editAltText(index) {
        const currentAltText = this.currentData[index].alt_text || '';
        
        const newAltText = prompt('Edit alt text:', currentAltText);
        
        if (newAltText !== null) {
            this.currentData[index].alt_text = newAltText;
            this.currentData[index].was_generated = false;
            
            // Update the display
            const generatedDiv = document.getElementById(`generated-${index}`);
            if (newAltText.trim()) {
                generatedDiv.innerHTML = `
                    <div class="alert alert-info py-2 mb-0">
                        <strong>Manual:</strong> ${newAltText}
                    </div>
                `;
            } else {
                generatedDiv.innerHTML = '<em class="text-muted">No alt text</em>';
            }
        }
    }
    
    async downloadFile() {
        if (!this.currentFilename || !this.currentData.length) {
            this.showError('No data to download');
            return;
        }
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: this.currentFilename,
                    data: this.currentData
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `updated_${this.currentFilename}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } else {
                const result = await response.json();
                this.showError(result.error || 'Download failed');
            }
        } catch (error) {
            this.showError('Network error occurred');
            console.error('Download error:', error);
        }
    }
}

// Initialize the application
const altTextGenerator = new AltTextGenerator();
