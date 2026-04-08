"""
Flask web application for AI-powered image classification.

Provides routes for image upload, classification, and results display
with a modern, responsive user interface.
"""

import logging
import os
from typing import Tuple
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

import config
from model import ImageClassifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE
app.secret_key = config.SECRET_KEY

# Initialize classifier (lazy load on first request)
classifier = None


def get_classifier() -> ImageClassifier:
    """
    Get or initialize the image classifier instance.

    Returns:
        ImageClassifier: The loaded classifier instance.
    """
    global classifier
    if classifier is None:
        logger.info("Initializing classifier...")
        classifier = ImageClassifier(
            input_size=config.MODEL_INPUT_SIZE,
            top_k=config.TOP_K_PREDICTIONS
        )
        if not classifier.load_model():
            logger.error("Failed to load classifier model")
            raise RuntimeError("Failed to load image classification model")
    return classifier


def allowed_file(filename: str) -> bool:
    """
    Check if a filename has an allowed extension.

    Args:
        filename: The filename to check.

    Returns:
        bool: True if file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def save_uploaded_file(file) -> Tuple[bool, str]:
    """
    Save an uploaded file to the upload folder.

    Args:
        file: Flask FileStorage object.

    Returns:
        Tuple of (success: bool, filename: str or error_message: str)
    """
    try:
        if not file or file.filename == '':
            return False, "No file selected"

        if not allowed_file(file.filename):
            return False, f"File type not allowed. Allowed types: {', '.join(config.ALLOWED_EXTENSIONS)}"

        # Create secure filename with timestamp to avoid collisions
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        logger.info(f"File uploaded successfully: {filename}")
        return True, filename

    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return False, f"Upload error: {str(e)}"


@app.route('/', methods=['GET'])
def index() -> str:
    """
    Render the image upload page.

    Returns:
        str: Rendered HTML template for upload page.
    """
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify_image() -> dict:
    """
    Classify an uploaded image and return predictions.

    Returns:
        dict: JSON response with classification results or error message.
    """
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400

        file = request.files['image']

        # Save uploaded file
        success, result = save_uploaded_file(file)
        if not success:
            return jsonify({'success': False, 'error': result}), 400

        filename = result
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Get classifier and perform prediction
        clf = get_classifier()
        predictions = clf.predict_with_details(filepath)

        if predictions is None:
            return jsonify({
                'success': False,
                'error': 'Failed to classify image'
            }), 500

        logger.info(f"Classification successful for {filename}")

        # Store in session for results page
        session['last_classification'] = {
            'filename': filename,
            'predictions': predictions['predictions'],
            'top_prediction': predictions['top_prediction'],
            'top_confidence': predictions['top_confidence']
        }

        return jsonify({
            'success': True,
            'predictions': predictions['predictions'],
            'top_prediction': predictions['top_prediction'],
            'top_confidence': round(predictions['top_confidence'], 2),
            'filename': filename
        }), 200

    except RequestEntityTooLarge:
        logger.warning("File size exceeded maximum limit")
        return jsonify({
            'success': False,
            'error': f'File too large. Maximum size: {config.MAX_FILE_SIZE / (1024*1024):.1f} MB'
        }), 413

    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@app.route('/results/<filename>', methods=['GET'])
def results(filename: str) -> str:
    """
    Render the results page with classification results.

    Args:
        filename: The filename of the classified image.

    Returns:
        str: Rendered HTML template for results page.
    """
    # Validate filename to prevent directory traversal
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Verify file exists
    if not os.path.exists(filepath):
        return render_template('index.html'), 404

    # Get classification from session or re-classify
    classification = session.get('last_classification', {})

    if not classification or classification.get('filename') != filename:
        try:
            clf = get_classifier()
            classification = clf.predict_with_details(filepath)
            if classification is None:
                return render_template('index.html'), 500
        except Exception as e:
            logger.error(f"Error retrieving results: {str(e)}")
            return render_template('index.html'), 500

    return render_template(
        'results.html',
        filename=filename,
        top_prediction=classification.get('top_prediction'),
        top_confidence=round(classification.get('top_confidence', 0), 2),
        predictions=classification.get('predictions', [])
    )


@app.route('/image/<filename>', methods=['GET'])
def get_image(filename: str) -> Tuple:
    """
    Serve an uploaded image file.

    Args:
        filename: The filename of the image to serve.

    Returns:
        Tuple: Flask response with image file.
    """
    from flask import send_from_directory

    filename = secure_filename(filename)

    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"Error serving image {filename}: {str(e)}")
        return jsonify({'error': 'Image not found'}), 404


@app.route('/health', methods=['GET'])
def health() -> dict:
    """
    Health check endpoint for monitoring.

    Returns:
        dict: JSON response indicating application health.
    """
    try:
        clf = get_classifier()
        return jsonify({'status': 'healthy', 'model_loaded': clf.is_loaded}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error) -> Tuple:
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error) -> Tuple:
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Run Flask development server
    logger.info("Starting AI Image Classifier application...")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG,
        threaded=True
    )
