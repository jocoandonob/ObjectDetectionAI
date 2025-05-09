# Object Detection AI

A FastAPI-based web application for object detection and image processing.

## Features

- Image upload and processing
- Object detection capabilities
- Static file serving
- Modern web interface

## Prerequisites

- Python 3.7+
- OpenCV (cv2)
- NumPy
- Pillow (PIL)
- FastAPI
- Jinja2

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ObjectDetectionAI
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
ObjectDetectionAI/
├── uploads/         # Directory for uploaded images
├── static/          # Static files (CSS, JS, images)
├── run.py          # Test script to verify dependencies
└── start.py        # Main application entry point
```

## Usage

1. Run the test script to verify all dependencies are installed correctly:
```bash
python run.py
```

2. Start the application:
```bash
python start.py
```

3. Open your web browser and navigate to `http://localhost:8000`

## Development

The application uses:
- FastAPI for the web framework
- OpenCV and PIL for image processing
- Jinja2 for templating
- Static file serving for assets

## License

[Add your license information here] 