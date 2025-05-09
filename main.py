import os
import uuid
import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="Image Processing App")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Available filters
FILTERS = {
    "grayscale": "Grayscale",
    "gaussian_blur": "Gaussian Blur",
    "sepia": "Sepia",
    "brightness": "Brightness",
    "contrast": "Contrast",
    "threshold": "Threshold",
    "invert": "Invert",
    "pixelate": "Pixelate"
}

def process_grayscale(image):
    """Convert image to grayscale"""
    return cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

def process_gaussian_blur(image, ksize=5):
    """Apply Gaussian blur to image"""
    # Ensure kernel size is odd
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def process_sepia(image):
    """Apply sepia filter to image"""
    kernel = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])
    result = cv2.transform(image, kernel)
    return np.clip(result, 0, 255).astype(np.uint8)

def process_brightness(image, factor=1.5):
    """Adjust image brightness"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(pil_img)
    pil_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def process_contrast(image, factor=1.5):
    """Adjust image contrast"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def process_threshold(image, threshold=127):
    """Apply binary threshold to image"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def process_invert(image):
    """Invert image colors"""
    return cv2.bitwise_not(image)

def process_pixelate(image, factor=10):
    """Pixelate the image"""
    height, width = image.shape[:2]
    # Resize down
    small = cv2.resize(image, (width // factor, height // factor), 
                       interpolation=cv2.INTER_LINEAR)
    # Resize up with nearest-neighbor interpolation for pixelated effect
    return cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)

def apply_filter(image_data, filter_type, params=None):
    """Apply the selected filter to the image"""
    # Ensure params exists
    if params is None:
        params = {}
    
    # Convert PIL Image to OpenCV format (numpy array)
    image = cv2.cvtColor(np.array(image_data), cv2.COLOR_RGB2BGR)
    
    # Apply selected filter
    if filter_type == "grayscale":
        result = process_grayscale(image)
    elif filter_type == "gaussian_blur":
        # Make sure ksize is an integer
        ksize = int(params.get("ksize", 5))
        result = process_gaussian_blur(image, ksize)
    elif filter_type == "sepia":
        result = process_sepia(image)
    elif filter_type == "brightness":
        # Make sure factor is a float
        factor = float(params.get("factor", 1.5))
        result = process_brightness(image, factor)
    elif filter_type == "contrast":
        # Make sure factor is a float
        factor = float(params.get("factor", 1.5))
        result = process_contrast(image, factor)
    elif filter_type == "threshold":
        # Make sure threshold is an integer
        threshold = int(params.get("threshold", 127))
        result = process_threshold(image, threshold)
    elif filter_type == "invert":
        result = process_invert(image)
    elif filter_type == "pixelate":
        # Make sure factor is an integer
        factor = int(params.get("factor", 10))
        result = process_pixelate(image, factor)
    else:
        # Return original image if filter not recognized
        result = image
    
    # Convert back to PIL Image
    return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with the upload form"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "filters": FILTERS}
    )

@app.post("/process/")
async def process_image(
    file: UploadFile = File(...),
    filter_type: str = Form(...),
    brightness_factor: float = Form(1.5),
    contrast_factor: float = Form(1.5),
    blur_ksize: int = Form(5),
    threshold_value: int = Form(127),
    pixelate_factor: int = Form(10)
):
    """Process the uploaded image with the selected filter"""
    try:
        # Read the file content
        contents = await file.read()
        
        # Open the image with PIL
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Set parameters for the filter - explicitly using strings as keys to avoid typing issues
        filter_params = {}
        
        # Add appropriate parameters based on filter type
        filter_params["ksize"] = blur_ksize
        filter_params["threshold"] = threshold_value
        
        # Add factor parameters with appropriate type conversion
        if filter_type == "brightness":
            filter_params["factor"] = float(brightness_factor)
        elif filter_type == "contrast":
            filter_params["factor"] = float(contrast_factor)
        elif filter_type == "pixelate":
            filter_params["factor"] = int(pixelate_factor)
        
        # Apply the selected filter
        processed_image = apply_filter(image, filter_type, filter_params)
        
        # Convert the processed image to base64 for display
        buffered = io.BytesIO()
        processed_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Convert the original image to base64 for display
        buffered_original = io.BytesIO()
        image.save(buffered_original, format="JPEG")
        original_img_str = base64.b64encode(buffered_original.getvalue()).decode()
        
        # Return response
        return {
            "original_filename": file.filename,
            "filter_applied": FILTERS.get(filter_type, "Unknown"),
            "original_image": f"data:image/jpeg;base64,{original_img_str}",
            "processed_image": f"data:image/jpeg;base64,{img_str}"
        }
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# For local development and Replit
if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Image Processing App")
    logger.info("Access the web interface at http://0.0.0.0:8080")
    
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=8080)