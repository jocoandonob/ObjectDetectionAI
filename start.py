import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Image Processing App")
    logger.info("Access the web interface at http://0.0.0.0:5000")
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)