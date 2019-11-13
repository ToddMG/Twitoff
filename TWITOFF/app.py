from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user

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

    # Route for getting new users
    @app.route('/user', methods=['POST']) # Uses form
    @app.route('/user/<name>', methods=['GET']) # Requires parameter
    def user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets= User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)


    # Set route for resetting the Database
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
