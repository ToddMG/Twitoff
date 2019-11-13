"""Prediction of Users based on Tweet embeddings."""
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


def predict_user(user1_name, user2_name, tweet_text, cache=None):
    """
    Determine and return which user is more likely to say something
    :param user1_name: First user to compare
    :param user2_name: Second user to compare
    :param tweet_text: Tweet to be used in prediction
    :param cache:
    :return:
    """
    user_set = pickle.dumps((user1_name, user2_name))

    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))
    else:
        # GET users
        user1 = User.query.filter(User.name == user1_name).one()
        user2 = User.query.filter(User.name == user2_name).one()
        # GET user embeddings
        user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
        user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
        # Split into array
        embeddings = np.vstack([user1_embeddings, user2_embeddings])
        labels = np.concatenate([np.ones(len(user1.tweets)),
                                 np.zeros(len(user2.tweets))])
        # Fit the Logistic Regression model
        log_reg = LogisticRegression().fit(embeddings, labels)
        cache and cache.set(user_set, pickle.dumps(log_reg))

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
