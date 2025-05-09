"""
Simple test script to verify our filters are working correctly
"""
import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from main import (
    process_grayscale,
    process_gaussian_blur,
    process_sepia,
    process_brightness,
    process_contrast,
    process_threshold,
    process_invert,
    process_pixelate
)

def generate_test_image():
    """Create a simple test image with colored shapes"""
    # Create a blank image
    img = np.ones((300, 400, 3), dtype=np.uint8) * 255
    
    # Add a red rectangle
    cv2.rectangle(img, (50, 50), (150, 150), (0, 0, 255), -1)
    
    # Add a green circle
    cv2.circle(img, (250, 100), 50, (0, 255, 0), -1)
    
    # Add a blue triangle
    pts = np.array([[200, 200], [300, 200], [250, 300]], np.int32)
    cv2.fillPoly(img, [pts], (255, 0, 0))
    
    # Add some text
    cv2.putText(img, "Test Image", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Save the image
    os.makedirs("tests", exist_ok=True)
    cv2.imwrite("tests/test_image.jpg", img)
    
    return img

def test_all_filters():
    """Test all implemented filters on the test image"""
    # Generate test image
    img = generate_test_image()
    print("Test image generated.")
    
    # Process with each filter
    grayscale = process_grayscale(img)
    blur = process_gaussian_blur(img, 7)
    sepia = process_sepia(img)
    bright = process_brightness(img, 1.8)
    contrast = process_contrast(img, 1.8)
    threshold = process_threshold(img, 127)
    invert = process_invert(img)
    pixelate = process_pixelate(img, 8)
    
    # Save results
    cv2.imwrite("tests/grayscale.jpg", grayscale)
    cv2.imwrite("tests/blur.jpg", blur)
    cv2.imwrite("tests/sepia.jpg", sepia)
    cv2.imwrite("tests/bright.jpg", bright)
    cv2.imwrite("tests/contrast.jpg", contrast)
    cv2.imwrite("tests/threshold.jpg", threshold)
    cv2.imwrite("tests/invert.jpg", invert)
    cv2.imwrite("tests/pixelate.jpg", pixelate)
    
    print("All filters tested and results saved to 'tests' directory.")

if __name__ == "__main__":
    test_all_filters()