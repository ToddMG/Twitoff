"""Minimal flask app"""

from flask import Flask, render_template

# Make the application
app = Flask(__name__)


# Make the route
@app.route("/")
# Define a function
def hello():
    return render_template('home.html')


# Creating a second route
@app.route("/about")
# Second route function
def preds():
    return render_template('about.html')
