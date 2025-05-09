"""
WSGI entry point
"""
from main import app as application

# This file is a WSGI entry point
# The 'application' object is what WSGI servers (like gunicorn) expect