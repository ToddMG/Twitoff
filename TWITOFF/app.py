from flask import Flask
from .models import DB


# Make app factory
def create_app():
    app = Flask(__name__)

    # Add config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # Make database aware of app
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff'

    return app
