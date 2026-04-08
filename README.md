# AI Image Classifier

An AI-powered image classification app using Python, TensorFlow & Flask — upload any image and get instant predictions with a clean web UI.

## Features

- Upload any image for instant classification
- Pre-trained deep learning model (MobileNetV2)
- Top-5 prediction results with confidence scores
- Clean, responsive web interface
- REST API endpoint for programmatic access
- Supports JPEG, PNG, and WebP formats

## Tech Stack

- **ML Framework:** TensorFlow / Keras
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Model:** MobileNetV2 (ImageNet)
- **Deployment:** Docker, Gunicorn

## Getting Started

```bash
git clone https://github.com/razinahmed/ai-image-classifier.git
cd ai-image-classifier
pip install -r requirements.txt
python app.py
```

## API Usage

```bash
curl -X POST -F "image=@photo.jpg" http://localhost:5000/predict
```

## Screenshots

Coming soon...

## License

MIT License

---

Made with passion by [Abdul Rasak V](https://github.com/razinahmed)
