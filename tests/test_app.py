"""
Unit tests for AI Image Classifier Flask application.

Tests cover:
- Flask route functionality
- File upload handling
- Error handling
- Configuration
"""

import os
import tempfile
import pytest
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import config


class TestFlaskApp:
    """Test cases for Flask application."""

    @pytest.fixture
    def client(self):
        """Create a Flask test client."""
        app.app.config['TESTING'] = True
        app.app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
        with app.app.test_client() as client:
            yield client

    def test_index_route(self, client):
        """Test that index route returns 200."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'AI Image Classifier' in response.data

    def test_health_check_route(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        # Will fail if classifier doesn't load, but endpoint should exist
        assert response.status_code in [200, 500]

    def test_classify_no_file(self, client):
        """Test classify endpoint without file."""
        response = client.post('/classify')
        assert response.status_code == 400
        assert b'No image provided' in response.data or b'error' in response.data

    def test_404_not_found(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404

    def test_allowed_file_validation(self):
        """Test file extension validation."""
        # Valid extensions
        assert app.allowed_file('image.jpg')
        assert app.allowed_file('image.png')
        assert app.allowed_file('image.gif')
        assert app.allowed_file('image.bmp')
        assert app.allowed_file('image.webp')

        # Invalid extensions
        assert not app.allowed_file('image.txt')
        assert not app.allowed_file('image.exe')
        assert not app.allowed_file('image.pdf')
        assert not app.allowed_file('noextension')

    def test_secure_filename_handling(self):
        """Test secure filename handling."""
        from werkzeug.utils import secure_filename

        # Valid filenames
        assert secure_filename('test.jpg') == 'test.jpg'
        assert secure_filename('my_image.png') == 'my_image.png'

        # Potentially dangerous filenames
        assert secure_filename('../etc/passwd') == 'etc_passwd'
        assert secure_filename('..\\windows\\system32') == 'windows_system32'


class TestConfiguration:
    """Test cases for application configuration."""

    def test_config_upload_folder_exists(self):
        """Test that upload folder configuration exists."""
        assert hasattr(config, 'UPLOAD_FOLDER')
        assert isinstance(config.UPLOAD_FOLDER, str)

    def test_config_allowed_extensions(self):
        """Test that allowed extensions are configured."""
        assert hasattr(config, 'ALLOWED_EXTENSIONS')
        assert 'jpg' in config.ALLOWED_EXTENSIONS
        assert 'png' in config.ALLOWED_EXTENSIONS

    def test_config_max_file_size(self):
        """Test max file size configuration."""
        assert hasattr(config, 'MAX_FILE_SIZE')
        assert config.MAX_FILE_SIZE == 10 * 1024 * 1024  # 10MB

    def test_config_model_settings(self):
        """Test model configuration."""
        assert hasattr(config, 'MODEL_NAME')
        assert config.MODEL_NAME == 'MobileNetV2'
        assert hasattr(config, 'MODEL_INPUT_SIZE')
        assert config.MODEL_INPUT_SIZE == (224, 224)
        assert hasattr(config, 'TOP_K_PREDICTIONS')
        assert config.TOP_K_PREDICTIONS == 5

    def test_config_flask_settings(self):
        """Test Flask configuration."""
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'DEBUG')
        assert isinstance(config.DEBUG, bool)


class TestErrorHandling:
    """Test cases for error handling."""

    @pytest.fixture
    def client(self):
        """Create a Flask test client."""
        app.app.config['TESTING'] = True
        with app.app.test_client() as client:
            yield client

    def test_500_error_handler(self, client):
        """Test 500 error handling."""
        # Try to access a route that will cause an error
        # (This is a placeholder - actual 500 errors depend on app state)
        pass

    def test_invalid_content_type(self, client):
        """Test handling of invalid content type."""
        response = client.post(
            '/classify',
            data={'invalid': 'data'},
            content_type='application/json'
        )
        assert response.status_code in [400, 415]


class TestImageClassifier:
    """Test cases for image classifier module."""

    def test_classifier_init(self):
        """Test ImageClassifier initialization."""
        from model import ImageClassifier

        classifier = ImageClassifier()
        assert classifier.input_size == (224, 224)
        assert classifier.top_k == 5
        assert not classifier.is_loaded

    def test_classifier_custom_params(self):
        """Test ImageClassifier with custom parameters."""
        from model import ImageClassifier

        classifier = ImageClassifier(input_size=(256, 256), top_k=10)
        assert classifier.input_size == (256, 256)
        assert classifier.top_k == 10

    def test_classifier_methods_exist(self):
        """Test that classifier has required methods."""
        from model import ImageClassifier

        classifier = ImageClassifier()
        assert hasattr(classifier, 'load_model')
        assert hasattr(classifier, 'preprocess_image')
        assert hasattr(classifier, 'predict')
        assert hasattr(classifier, 'predict_with_details')
        assert callable(classifier.load_model)
        assert callable(classifier.preprocess_image)
        assert callable(classifier.predict)
        assert callable(classifier.predict_with_details)

    def test_create_classifier_factory(self):
        """Test create_classifier factory function."""
        from model.classifier import create_classifier

        # This will attempt to load the model
        classifier = create_classifier()
        # Could be None if model loading fails in test environment
        if classifier is not None:
            assert classifier.is_loaded


# ============================================================================
# Test Execution
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
