from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user

load_dotenv()

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
    @app.route('/user', methods=['POST'])  # Uses form
    @app.route('/user/<name>', methods=['GET'])  # Requires parameter
    def user(name=None, message=''):
        name = name or request.values['user_name']  # Get existing username or pull from HTML form

        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    # Route for predictions
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to itself'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = "{} is more likely to be said by {} than by {}".format(
                request.values['tweet_text'], user1 if prediction else user2, user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    # Set route for resetting the Database
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
