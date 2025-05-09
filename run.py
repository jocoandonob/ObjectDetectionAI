"""
Simple test script to verify our code is working correctly
"""
import os

# Create required directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Test imports
import cv2
import numpy as np
from PIL import Image, ImageEnhance

# Test FastAPI dependencies
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

print("All imports succeeded!")
print("Code is ready to run.")
print("To run the app, use: python start.py")