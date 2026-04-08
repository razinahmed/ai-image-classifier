"""
TensorFlow/Keras-based image classifier using MobileNetV2 pretrained model.

This module provides functionality for loading a pretrained MobileNetV2 model
and performing image classification with top-5 predictions and confidence scores.
"""

import logging
from typing import List, Tuple, Optional
from pathlib import Path

import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

logger = logging.getLogger(__name__)


class ImageClassifier:
    """
    Image classification model using MobileNetV2 pretrained on ImageNet.

    Provides methods to load the model, preprocess images, and generate
    predictions with confidence scores.
    """

    def __init__(self, input_size: Tuple[int, int] = (224, 224), top_k: int = 5):
        """
        Initialize the image classifier.

        Args:
            input_size: Target input dimensions for the model (height, width).
            top_k: Number of top predictions to return.
        """
        self.input_size = input_size
        self.top_k = top_k
        self.model = None
        self.is_loaded = False

    def load_model(self) -> bool:
        """
        Load the pretrained MobileNetV2 model from TensorFlow.

        Returns:
            bool: True if model loaded successfully, False otherwise.
        """
        try:
            logger.info("Loading MobileNetV2 model...")
            self.model = MobileNetV2(
                input_shape=(*self.input_size, 3),
                include_top=True,
                weights='imagenet'
            )
            self.is_loaded = True
            logger.info("Model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False

    def preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load and preprocess an image for model input.

        Args:
            image_path: Path to the image file.

        Returns:
            Preprocessed image array or None if preprocessing fails.
        """
        try:
            # Open image and convert to RGB if necessary
            image = Image.open(image_path).convert('RGB')

            # Resize to model input size
            image = image.resize(self.input_size, Image.Resampling.LANCZOS)

            # Convert to numpy array
            image_array = np.array(image)

            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)

            # Apply MobileNetV2 preprocessing
            image_array = preprocess_input(image_array)

            logger.debug(f"Image preprocessed: {image_path}")
            return image_array

        except Exception as e:
            logger.error(f"Failed to preprocess image {image_path}: {str(e)}")
            return None

    def predict(self, image_path: str) -> Optional[List[Tuple[str, float]]]:
        """
        Perform image classification and return top-k predictions.

        Args:
            image_path: Path to the image file.

        Returns:
            List of tuples (class_name, confidence) or None if prediction fails.
        """
        if not self.is_loaded:
            logger.error("Model not loaded. Call load_model() first.")
            return None

        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return None

        try:
            # Get predictions
            predictions = self.model.predict(processed_image, verbose=0)

            # Decode predictions to human-readable labels
            decoded_predictions = decode_predictions(predictions, top=self.top_k)[0]

            # Format results as list of (class_name, confidence)
            results = []
            for class_id, class_name, confidence in decoded_predictions:
                # Clean up class name (replace underscores with spaces, capitalize)
                clean_name = class_name.replace('_', ' ').title()
                results.append((clean_name, float(confidence)))

            logger.info(f"Prediction complete for {image_path}: {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Prediction failed for {image_path}: {str(e)}")
            return None

    def predict_with_details(self, image_path: str) -> Optional[dict]:
        """
        Perform image classification and return detailed results.

        Args:
            image_path: Path to the image file.

        Returns:
            Dictionary with predictions and metadata or None if prediction fails.
        """
        predictions = self.predict(image_path)
        if predictions is None:
            return None

        # Calculate total confidence for normalization
        total_confidence = sum(conf for _, conf in predictions)

        # Normalize confidences to percentages
        normalized_predictions = [
            {
                'label': label,
                'confidence': confidence,
                'percentage': (confidence / total_confidence * 100) if total_confidence > 0 else 0
            }
            for label, confidence in predictions
        ]

        return {
            'predictions': normalized_predictions,
            'top_prediction': normalized_predictions[0]['label'] if normalized_predictions else None,
            'top_confidence': normalized_predictions[0]['percentage'] if normalized_predictions else 0,
            'image_path': image_path
        }


def create_classifier(input_size: Tuple[int, int] = (224, 224),
                     top_k: int = 5) -> Optional[ImageClassifier]:
    """
    Factory function to create and load an ImageClassifier instance.

    Args:
        input_size: Target input dimensions for the model.
        top_k: Number of top predictions to return.

    Returns:
        Loaded ImageClassifier instance or None if loading fails.
    """
    classifier = ImageClassifier(input_size=input_size, top_k=top_k)
    if classifier.load_model():
        return classifier
    return None
