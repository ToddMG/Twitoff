"""Minimal flask app"""

from flask import Flask

# Make the application
app = Flask(__name__)

# Make the route
@app.route("/")

# Define a function
def hello():
    return "Hello beautiful world!"


