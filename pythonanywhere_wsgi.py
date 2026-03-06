# WSGI configuration for PythonAnywhere
import sys
import os

# Add your project directory to the sys.path
path = '/home/sofoy14/paloma-valencia'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['PYTHONUNBUFFERED'] = '1'

# Import your Flask app
from app import app as application
