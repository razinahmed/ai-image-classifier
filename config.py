"""
Configuration settings for the AI Image Classifier application.
"""

import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask configuration
FLASK_ENV = os.getenv("FLASK_ENV", "production")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Model configuration
MODEL_NAME = "MobileNetV2"
MODEL_INPUT_SIZE = (224, 224)
TOP_K_PREDICTIONS = 5

# Application settings
DEBUG = FLASK_ENV == "development"
MAX_WORKERS = 4
