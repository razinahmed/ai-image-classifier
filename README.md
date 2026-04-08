# 🤖 AI Image Classifier

> An AI-powered image classification app using Python, TensorFlow & Flask — upload any image and get instant predictions with a clean, modern web UI.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-ff6f00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Keras](https://img.shields.io/badge/Keras-API-d00000?style=for-the-badge&logo=keras&logoColor=white)](https://keras.io/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📸 Visual Overview

<div align="center">

| Upload Interface | Classification Results |
|---|---|
| ![Upload](https://via.placeholder.com/800x450/0d1117/00d4aa?text=AI+Image+Classifier+Upload) | ![Results](https://via.placeholder.com/800x450/0d1117/ff6b6b?text=Classification+Results) |

| MobileNetV2 Model | Top-5 Predictions |
|---|---|
| ![Model](https://via.placeholder.com/400x250/0d1117/7c3aed?text=MobileNetV2+Model) | ![Predictions](https://via.placeholder.com/400x250/0d1117/f59e0b?text=Top-5+Predictions) |

</div>

---

## ⚡ How It Works

1. **📤 Upload Image** - Choose any image from your device (JPEG, PNG, or WebP)
2. **🧠 AI Processing** - The MobileNetV2 model analyzes the image in real-time
3. **📊 Get Results** - Receive top-5 predictions with confidence percentages
4. **✨ Instant Display** - View beautiful, formatted results in your browser

---

## ✨ Key Features

- 🖼️ **Universal Image Support** - Works with JPEG, PNG, and WebP formats
- ⚡ **Lightning Fast** - MobileNetV2 optimized for speed and accuracy
- 📊 **Confidence Scores** - Top-5 predictions with detailed percentages
- 🎨 **Beautiful UI** - Clean, responsive, modern web interface
- 🔌 **REST API** - Programmatic access via HTTP endpoints
- 🐳 **Docker Ready** - Containerized deployment for easy scaling
- 📱 **Mobile Friendly** - Works seamlessly on all devices
- 🔒 **Secure** - Local processing, no data sent to external servers

---

## 🛠️ Tech Stack

<div align="center">

![Tech Stack](https://skillicons.dev/icons?i=python,tensorflow,flask,html,css,js,docker,git)

| Component | Technology |
|-----------|-----------|
| **ML Framework** | TensorFlow / Keras |
| **Backend** | Python, Flask |
| **Frontend** | HTML, CSS, JavaScript |
| **Pre-trained Model** | MobileNetV2 (ImageNet) |
| **Server** | Gunicorn |
| **Containerization** | Docker |
| **Model Size** | ~13 MB |

</div>

---

## 📁 Project Structure

```
ai-image-classifier/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker compose setup
├── static/
│   ├── css/
│   │   └── style.css     # Application styling
│   └── js/
│       └── script.js     # Frontend logic
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Upload page
│   └── results.html      # Results display
├── models/
│   └── mobilenetv2.h5    # Pre-trained model
└── utils/
    ├── predictor.py      # Prediction logic
    └── image_handler.py  # Image processing
```

---

## 🚀 Quick Start

### Option 1: Using pip

```bash
# Clone the repository
git clone https://github.com/razinahmed/ai-image-classifier.git
cd ai-image-classifier

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open in browser
# Navigate to http://localhost:5000
```

### Option 2: Using Docker

```bash
# Build the Docker image
docker build -t ai-image-classifier .

# Run the container
docker run -p 5000:5000 ai-image-classifier

# Access the application
# Navigate to http://localhost:5000
```

### Option 3: Using Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## 🔌 API Reference

### Classification Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | `POST` | Classify an uploaded image |
| `/` | `GET` | Serve the web interface |
| `/health` | `GET` | Check API health status |

### Request Format

```bash
curl -X POST -F "image=@photo.jpg" http://localhost:5000/predict
```

### Response Format

```json
{
  "success": true,
  "predictions": [
    {
      "class": "dog",
      "confidence": 0.9834
    },
    {
      "class": "puppy",
      "confidence": 0.0145
    }
  ],
  "processing_time": 0.23
}
```

### Error Handling

```json
{
  "success": false,
  "error": "No image provided",
  "status_code": 400
}
```

---

## 🧠 Model Information

### MobileNetV2

**MobileNetV2** is a lightweight convolutional neural network architecture designed by Google for mobile and embedded vision applications.

| Property | Details |
|----------|---------|
| **Parameters** | 3.5M |
| **Model Size** | ~13 MB |
| **Input Shape** | 224 × 224 × 3 |
| **Training Data** | ImageNet-1k |
| **Classes** | 1,000 object classes |
| **Accuracy (Top-1)** | ~71.8% |
| **Inference Speed** | ~25ms (CPU) |
| **Architecture** | Inverted Residuals with Linear Bottlenecks |

### Why MobileNetV2?

✅ **Lightweight** - Perfect for real-time inference  
✅ **Fast** - Minimal latency on CPU-only hardware  
✅ **Accurate** - Solid ImageNet performance  
✅ **Portable** - Easy deployment on any platform  
✅ **Proven** - Battle-tested across millions of devices  

---

## 📸 Screenshots Gallery

| Feature | Preview |
|---------|---------|
| **Main Upload Interface** | ![Upload](https://via.placeholder.com/600x400/0d1117/00d4aa?text=Upload+Image) |
| **Real-time Classification** | ![Classify](https://via.placeholder.com/600x400/0d1117/ff6b6b?text=AI+Processing) |
| **Detailed Results** | ![Results](https://via.placeholder.com/600x400/0d1117/7c3aed?text=Top-5+Predictions) |
| **Mobile View** | ![Mobile](https://via.placeholder.com/600x400/0d1117/f59e0b?text=Responsive+Design) |

---

## 📋 Requirements

```
tensorflow>=2.10.0
flask>=2.2.0
keras>=2.10.0
pillow>=9.0.0
numpy>=1.22.0
python-dotenv>=0.20.0
gunicorn>=20.1.0
```

For complete requirements, see `requirements.txt`

---

## 🤝 Contributing

Contributions are welcome and greatly appreciated! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution

- 🎨 UI/UX improvements
- 📈 Model accuracy enhancements
- 📚 Documentation improvements
- 🧪 Test coverage expansion
- 🐛 Bug fixes and optimizations

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

MIT License summary:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Liability limitation
- ⚠️ Warranty disclaimer

---

## 📞 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/razinahmed/ai-image-classifier/issues)
- **Author**: [Abdul Rasak V](https://github.com/razinahmed)
- **Email**: Contact via GitHub profile

---

<div align="center">

### Made with ❤️ by Abdul Rasak V

⭐ If you found this project helpful, please consider giving it a star!

[Star on GitHub](https://github.com/razinahmed/ai-image-classifier) • [Report Issue](https://github.com/razinahmed/ai-image-classifier/issues) • [Suggest Feature](https://github.com/razinahmed/ai-image-classifier/issues/new)

</div>
