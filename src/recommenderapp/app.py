"""
Copyright (c) 2023 Nathan Kohen, Nicholas Foster, Brandon Walia, Robert Kenney
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=import-error
import json
from flask import Flask, jsonify, render_template, request
import pandas as pd
from flask_cors import CORS
from bson.objectid import ObjectId
from pymongo.errors import (
    OperationFailure,
    DuplicateKeyError,
)

from src.recommenderapp.search import Search

from src.recommenderapp.client import client
from src.recommenderapp.utils import (
    beautify_feedback_data,
    send_email_to_user,
    create_account,
    login_to_account,
    submit_review,
    get_wall_posts,
    get_username,
    add_friend,
    get_friends,
    get_recent_movies,
    get_recent_friend_movies,
    get_genre_count,
    fetch_streaming_link,
)

from src.recommenderapp.item_based import (
    recommend_for_new_user,
)

app = Flask(__name__)
app.secret_key = "secret key"

db = client.PopcornPicksDB

cors = CORS(app, resources={r"/*": {"origins": "*"}})
user = {1: None}
# user[1] = "671b289a193d2a9361ebf39a"  # Hardcoded user id for testing purposes

movies_df = pd.read_csv("data/movies.csv")


@app.route("/")
def login_page():
    """
    Renders the login page.
    """
    return render_template("login.html")


@app.route("/profile")
def profile_page():
    """
    Renders the login page.
    """
    get_genre_count(db, user)

    if user[1] is not None:
        return render_template("profile.html")
    return render_template("login.html")


@app.route("/wall")
def wall_page():
    """
    Renders the wall page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("wall.html")
    return render_template("login.html")


@app.route("/review")
def review_page():
    """
    Renders the review page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("review.html")
    return render_template("login.html")


@app.route("/landing")
def landing_page():
    """
    Renders the landing page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("landing_page.html")
    return render_template("login.html")


@app.route("/search_page")
def search_page():
    """
    Renders the search page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("search_page.html")
    return render_template("login.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    data1 = data["movie_list"]

    user_rating = [{"title": movie, "rating": 10.0} for movie in data1]

    recommendations, genres, imdb_id = recommend_for_new_user(user_rating, user[1], db)

    web_url = []
    for element in imdb_id:
        web_url.append(fetch_streaming_link(element))

    resp = {
        "recommendations": recommendations,
        "genres": genres,
        "imdb_id": imdb_id,
    }

    print(resp, end="\n")
    return resp


@app.route("/search", methods=["POST"])
def search():
    """
    Handles movie search requests.
    """
    term = request.form["q"]
    finder = Search()
    filtered_dict = finder.results_top_ten(term)
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp


@app.route("/", methods=["POST"])
def create_acc():
    """
    Handles creating a new account
    """
    data = json.loads(request.data)
    create_account(db, data["email"], data["username"], data["password"])
    return request.data


@app.route("/out", methods=["POST"])
def signout():
    """
    Handles signing out the active user
    """
    user[1] = None
    return request.data


@app.route("/log", methods=["POST"])
def login():
    """Handles user login."""
    data = json.loads(request.data)
    resp = login_to_account(db, data["username"], data["password"])
    user[1] = resp
    if not resp:
        return "Invalid credentials", 400
    user[1] = resp
    return request.data


@app.route("/friend", methods=["POST"])
def friend():
    """
    Handles adding a new friend
    """
    data = json.loads(request.data)
    add_friend(db, user, data["username"])
    return request.data


@app.route("/guest", methods=["POST"])
def guest():
    """
    Sets the user to be a guest user
    """
    data = json.loads(request.data)
    user[1] = data["guest"]
    return request.data


@app.route("/review", methods=["POST"])
def review():
    """
    Handles the submission of a movie review
    """
    data = json.loads(request.data)
    submit_review(db, user, data["movie"], data["score"], data["review"])
    return request.data


@app.route("/getWallData", methods=["GET"])
def wall_posts():
    """
    Gets the posts for the wall
    """
    return get_wall_posts(db)


@app.route("/getRecentMovies", methods=["GET"])
def recent_movies():
    """
    Gets the recent movies of the active user
    """
    return get_recent_movies(db, user[1], movies_df)


@app.route("/getRecentFriendMovies", methods=["POST"])
def recent_friend_movies():
    """
    Gets the recent movies of a certain friend
    """
    data = json.loads(request.data)
    user_id = ObjectId(data["friend_id"]["_id"])
    return get_recent_friend_movies(db, user_id, movies_df)


@app.route("/getUserName", methods=["GET"])
def username():
    """
    Gets the username of the active user
    """
    return get_username(db, user)


@app.route("/getFriends", methods=["GET"])
def get_friend():
    """
    Gets the friends of the active user
    """
    return get_friends(db, user[1])


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Handles user feedback submission and mails the results.
    """
    data = json.loads(request.data)
    return data


@app.route("/sendMail", methods=["POST"])
def send_mail():
    """
    Handles user feedback submission and mails the results.
    """
    data = json.loads(request.data)
    user_email = data["email"]
    send_email_to_user(user_email, beautify_feedback_data(data))
    return data


@app.route("/success")
def success():
    """
    Renders the success page.
    """
    return render_template("success.html")


def setup_mongodb_indexes():
    """
    Sets up the MongoDB indexes.
    """
    try:
        db.users.create_index([("username", 1)], unique=True)
        db.users.create_index([("email", 1)], unique=True)
        db.movies.create_index([("imdb_id", 1)], unique=True)
        db.movies.create_index([("name", 1)])
        db.ratings.create_index([("user_id", 1), ("time", -1)])
        db.ratings.create_index([("movie_id", 1)])

        print("Indexes created successfully")
    except DuplicateKeyError as e:
        print(f"Duplicate key error: {str(e)}")
    except OperationFailure as e:
        print(f"Operation failed: {str(e)}")


if __name__ == "__main__":
    setup_mongodb_indexes()
    app.run(port=5000)
