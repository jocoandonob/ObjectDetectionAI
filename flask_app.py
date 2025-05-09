"""
Flask application that serves as a proxy to our FastAPI app
"""
import os
import subprocess
import threading
import time
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Store the uvicorn process
uvicorn_process = None

def start_uvicorn():
    """Start the uvicorn server for FastAPI app"""
    global uvicorn_process
    
    # Use subprocess to start uvicorn without blocking
    cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
    uvicorn_process = subprocess.Popen(cmd)
    
    # Give the server time to start
    time.sleep(2)

@app.route('/')
def index():
    """Redirect to the FastAPI app"""
    return redirect('http://0.0.0.0:5000/')

@app.route('/start_server')
def start_server():
    """Start the uvicorn server"""
    global uvicorn_process
    
    if uvicorn_process is None:
        # Start the server in a separate thread to not block this request
        thread = threading.Thread(target=start_uvicorn)
        thread.daemon = True
        thread.start()
        return "Starting server... Please wait a moment and then go to <a href='/'>homepage</a>."
    else:
        return "Server is already running. Go to <a href='/'>homepage</a>."

@app.route('/stop_server')
def stop_server():
    """Stop the uvicorn server"""
    global uvicorn_process
    
    if uvicorn_process is not None:
        uvicorn_process.terminate()
        uvicorn_process = None
        return "Server stopped."
    else:
        return "Server is not running."

if __name__ == '__main__':
    # Start uvicorn automatically when this script runs
    start_uvicorn()
    
    # Start Flask on a different port
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)