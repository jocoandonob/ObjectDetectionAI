"""
Direct runner script for the Image Processing App in Replit
"""
import os
import sys
import logging
import uvicorn

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_directories():
    """Create necessary directories for the application"""
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)

def run_server():
    """Run the FastAPI server"""
    try:
        logger.info("Starting Image Processing App")
        logger.info("Access the web interface at http://0.0.0.0:5000")
        uvicorn.run("main:app", host="0.0.0.0", port=5000)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return 1
    return 0

if __name__ == "__main__":
    # Create necessary directories
    create_directories()
    
    # Run the server
    sys.exit(run_server())