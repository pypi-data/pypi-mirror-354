__version__ = "0.1.0"

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080) 