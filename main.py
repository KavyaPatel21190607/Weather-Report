import os
import logging
from app import app

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Start the Flask app
    app.run(host="0.0.0.0", port=5001, debug=True)
