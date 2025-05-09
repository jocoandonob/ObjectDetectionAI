"""
Gunicorn application entry point for Replit deployment
"""
from main import app

# This file is used by gunicorn as the entry point
# It imports the FastAPI app from main.py