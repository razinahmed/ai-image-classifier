/**
 * AI Image Classifier - Client-side JavaScript
 * Handles drag-and-drop, image preview, form submission, and loading states
 */

// ============================================================================
// DOM Elements
// ============================================================================

const uploadZone = document.getElementById('uploadZone');
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const previewFilename = document.getElementById('previewFilename');
const classifyBtn = document.getElementById('classifyBtn');
const changeBtn = document.getElementById('changeBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultsSection = document.getElementById('resultsSection');
const resultsImage = document.getElementById('resultsImage');
const resultsImageElement = document.querySelector('.results-image img');
const tryAgainBtn = document.getElementById('tryAgainBtn');
const downloadResultsBtn = document.getElementById('downloadResultsBtn');
const errorMessage = document.getElementById('errorMessage');

// ============================================================================
// Event Listeners
// ============================================================================

/**
 * Upload zone click handler - triggers file input
 */
uploadZone.addEventListener('click', () => {
    imageInput.click();
});

/**
 * Prevent default drag and drop behavior
 */
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

/**
 * Handle file drop
 */
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

/**
 * Handle file input change
 */
imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

/**
 * Classify button click
 */
if (classifyBtn) {
    classifyBtn.addEventListener('click', classifyImage);
}

/**
 * Change image button click
 */
if (changeBtn) {
    changeBtn.addEventListener('click', resetUpload);
}

/**
 * Try again button click
 */
if (tryAgainBtn) {
    tryAgainBtn.addEventListener('click', resetUpload);
}

/**
 * Download results button
 */
if (downloadResultsBtn) {
    downloadResultsBtn.addEventListener('click', downloadResults);
}

// ============================================================================
// File Handling
// ============================================================================

/**
 * Handle file selection and preview
 * @param {File} file - The selected image file
 */
function handleFileSelect(file) {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please select a valid image file.');
        return;
    }

    // Validate file size (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File is too large. Maximum size is 10MB.');
        return;
    }

    // Create file reader and preview
    const reader = new FileReader();
    reader.onload = (e) => {
        // Update preview image
        previewImage.src = e.target.result;
        previewFilename.textContent = file.name;

        // Show preview container, hide upload zone
        uploadZone.style.display = 'none';
        previewContainer.style.display = 'grid';

        // Clear any previous errors
        hideError();

        // Store file reference for later
        window.selectedFile = file;
    };

    reader.onerror = () => {
        showError('Error reading file. Please try again.');
    };

    reader.readAsDataURL(file);
}

// ============================================================================
// Image Classification
// ============================================================================

/**
 * Classify the selected image
 */
async function classifyImage() {
    if (!window.selectedFile) {
        showError('No image selected.');
        return;
    }

    // Show loading overlay
    showLoading();

    try {
        // Create form data
        const formData = new FormData();
        formData.append('image', window.selectedFile);

        // Send classification request
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Classification failed');
        }

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Classification error:', error);
        showError(error.message || 'An error occurred during classification.');
    } finally {
        hideLoading();
    }
}

/**
 * Display classification results
 * @param {Object} data - Classification response data
 */
function displayResults(data) {
    // Update results with prediction data
    document.getElementById('topPrediction').textContent = data.top_prediction;

    const topConfidenceBar = document.getElementById('topConfidenceBar');
    if (topConfidenceBar) {
        topConfidenceBar.style.width = data.top_confidence + '%';
    }

    const topConfidenceText = document.getElementById('topConfidenceText');
    if (topConfidenceText) {
        topConfidenceText.textContent = `${data.top_confidence}% confidence`;
    }

    // Create predictions list
    const predictionsList = document.getElementById('predictionsList');
    if (predictionsList) {
        predictionsList.innerHTML = '';
        data.predictions.forEach((pred, index) => {
            const barClass = index === 0 ? 'bar-primary' : index === 1 ? 'bar-secondary' : 'bar-tertiary';
            const predElement = document.createElement('div');
            predElement.className = 'prediction-item';
            predElement.innerHTML = `
                <div class="prediction-label-row">
                    <span class="pred-name">${escapeHtml(pred.label)}</span>
                    <span class="pred-confidence">${pred.percentage.toFixed(1)}%</span>
                </div>
                <div class="prediction-bar">
                    <div class="prediction-bar-fill ${barClass}" style="width: ${pred.percentage}%"></div>
                </div>
            `;
            predictionsList.appendChild(predElement);
        });
    }

    // Update result image
    resultsImage.src = URL.createObjectURL(window.selectedFile);

    // Scroll to results and display
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============================================================================
// Loading States
// ============================================================================

/**
 * Show loading overlay
 */
function showLoading() {
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

// ============================================================================
// Error Handling
// ============================================================================

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * Hide error message
 */
function hideError() {
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
}

// ============================================================================
// Reset & Navigation
// ============================================================================

/**
 * Reset upload form
 */
function resetUpload() {
    // Reset file input
    imageInput.value = '';
    window.selectedFile = null;

    // Show upload zone, hide preview and results
    uploadZone.style.display = 'flex';
    previewContainer.style.display = 'none';
    resultsSection.style.display = 'none';

    // Clear error messages
    hideError();

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Download results as JSON
 */
function downloadResults() {
    const topPrediction = document.getElementById('topPrediction')?.textContent || '';
    const topConfidence = document.getElementById('topConfidenceText')?.textContent || '';

    const predictions = [];
    const predItems = document.querySelectorAll('.prediction-item');
    predItems.forEach((item) => {
        const name = item.querySelector('.pred-name')?.textContent || '';
        const confidence = item.querySelector('.pred-confidence')?.textContent || '';
        predictions.push({ label: name, confidence: confidence });
    });

    const results = {
        timestamp: new Date().toISOString(),
        topPrediction: topPrediction,
        topConfidence: topConfidence,
        allPredictions: predictions
    };

    // Create download link
    const dataStr = JSON.stringify(results, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `classification-results-${new Date().getTime()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Escape HTML special characters
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

// ============================================================================
// Page Load Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Set up initial state
    if (uploadZone) {
        uploadZone.style.display = 'flex';
    }

    // Prevent default drag behavior on entire page
    document.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    document.addEventListener('drop', (e) => {
        e.preventDefault();
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Escape key to reset
        if (e.key === 'Escape' && previewContainer?.style.display !== 'none') {
            resetUpload();
        }
    });
});
