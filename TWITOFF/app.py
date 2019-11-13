from decouple import config
from flask import Flask, render_template, request
from .models import DB, User


# Make app factory
def create_app():
    app = Flask(__name__)

    # Add config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Make database aware of app
    DB.init_app(app)

    # Set route for root
    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    # Set route for resetting the Database
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
