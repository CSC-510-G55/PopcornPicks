"""
Copyright (c) 2023 Nathan Kohen, Nicholas Foster, Brandon Walia, Robert Kenney
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=import-error
import datetime
import logging
import smtplib
import bcrypt
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import jsonify
from bson.objectid import ObjectId
import json
import pandas as pd
import os


def create_colored_tags(genres):
    """
    Utitilty function to create colored tags for different
    movie genres
    """
    # Define colors for specific genres
    genre_colors = {
        "Musical": "#FF1493",  # DeepPink
        "Sci-Fi": "#00CED1",  # DarkTurquoise
        "Mystery": "#8A2BE2",  # BlueViolet
        "Thriller": "#FF6347",  # Tomato
        "Horror": "#FF4500",  # OrangeRed
        "Documentary": "#228B22",  # ForestGreen
        "Fantasy": "#FFA500",  # Orange
        "Adventure": "#FFD700",  # Gold
        "Children": "#32CD32",  # LimeGreen
        "Film-Noir": "#2F4F4F",  # DarkSlateGray
        "Comedy": "#FFB500",  # VividYellow
        "Crime": "#8B0000",  # DarkRed
        "Drama": "#8B008B",  # DarkMagenta
        "Western": "#FF8C00",  # DarkOrange
        "IMAX": "#20B2AA",  # LightSeaGreen
        "Action": "#FF0000",  # Red
        "War": "#B22222",  # FireBrick
        "(no genres listed)": "#A9A9A9",  # DarkGray
        "Romance": "#FF69B4",  # HotPink
        "Animation": "#4B0082",  # Indigo
    }
    tags = []
    for genre in genres:
        color = genre_colors.get(genre, "#CCCCCC")  # Default color if not found
        tag = f'<span style="background-color: {color}; color: #FFFFFF; \
            padding: 5px; border-radius: 5px;">{genre}</span>'
        tags.append(tag)
    return " ".join(tags)


def beautify_feedback_data(data):
    """
    Utility function to beautify the feedback json containing predicted movies for sending in email
    """
    # Create empty lists for each category
    yet_to_watch = []
    like = []
    dislike = []

    # Iterate through the data and categorize movies
    for movie, status in data.items():
        if status == "Yet to watch":
            yet_to_watch.append(movie)
        elif status == "Like":
            like.append(movie)
        elif status == "Dislike":
            dislike.append(movie)

    # Create a category-dictionary of liked, disliked and yet to watch movies
    categorized_data_dict = {
        "Liked": like,
        "Disliked": dislike,
        "Yet to Watch": yet_to_watch,
    }

    return categorized_data_dict


def create_movie_genres(movie_genre_df):
    """
    Utility function for creating a dictionary for movie-genres mapping
    """
    # Create a dictionary to map movies to their genres
    movie_to_genres = {}

    # Iterating on all movies to create the map
    for row in movie_genre_df.iterrows():
        movie = row[1]["title"]
        genres = row[1]["genres"].split("|")
        movie_to_genres[movie] = genres
    return movie_to_genres


def send_email_to_user(recipient_email, categorized_data):
    """
    Utility function to send movie recommendations to user over email
    """

    email_html_content = """
                        <html>
                        <head></head>
                        <body>
                            <h1 style="color: #333333;">Movie Recommendations from PopcornPicks</h1>
                            <p style="color: #555555;">Dear Movie Enthusiast,</p>
                            <p style="color: #555555;">We hope you're having a fantastic day!</p>
                            <div style="padding: 10px; border: 1px solid #cccccc; border-radius: 5px; background-color: #f9f9f9;">
                            <h2>Your Movie Recommendations:</h2>
                            <h3>Movies Liked:</h3>
                            <ul style="color: #555555;">
                                {}
                            </ul>
                            <h3>Movies Disliked:</h3>
                            <ul style="color: #555555;">
                                {}
                            </ul>
                            <h3>Movies Yet to Watch:</h3>
                            <ul style="color: #555555;">
                                {}
                            </ul>
                            </div>
                            <p style="color: #555555;">Enjoy your movie time with PopcornPicks!</p>
                            <p style="color: #555555;">Best regards,<br>PopcornPicks Team 🍿</p>
                        </body>
                        </html>
                        """

    # Email configuration
    smtp_server = "smtp.gmail.com"
    # Port for TLS
    smtp_port = 587
    sender_email = "popcornpicks777@gmail.com"

    # Use an app password since 2-factor authentication is enabled
    sender_password = " "
    subject = "Your movie recommendation from PopcornPicks"

    # Create the email message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    # Load the CSV file into a DataFrame
    movie_genre_df = pd.read_csv("../../data/movies.csv")
    # Creating movie-genres map
    movie_to_genres = create_movie_genres(movie_genre_df)
    # Create the email message with HTML content
    html_content = email_html_content.format(
        "\n".join(
            f'<li>{movie} \
            {create_colored_tags(movie_to_genres.get(movie, ["Unknown Genre"]))}</li><br>'
            for movie in categorized_data["Liked"]
        ),
        "\n".join(
            f'<li>{movie} \
            {create_colored_tags(movie_to_genres.get(movie, ["Unknown Genre"]))}</li><br>'
            for movie in categorized_data["Disliked"]
        ),
        "\n".join(
            f'<li>{movie} \
            {create_colored_tags(movie_to_genres.get(movie, ["Unknown Genre"]))}</li><br>'
            for movie in categorized_data["Yet to Watch"]
        ),
    )

    # Attach the HTML email body
    message.attach(MIMEText(html_content, "html"))

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        # Start TLS encryption
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        logging.info("Email sent successfully!")

    except SMTPException as e:
        # Handle SMTP-related exceptions
        logging.error("SMTP error while sending email: %s", str(e))

    finally:
        server.quit()


def create_account(client, email, username, password):
    """Utility function for creating an account"""
    try:
        db = client.PopcornPicksDB
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "friends": [],
            "created_at": datetime.datetime.utcnow(),
        }
        db.users.insert_one(user_data)
        return True
    except Exception as e:
        print(f"Error creating account: {str(e)}")
        return False


def add_friend(client, user, username):
    """
    Utility function for adding a friend
    """
    client.PopcornPicksDB.users.update_one(
        {"_id": ObjectId(user[1])}, {"$addToSet": {"friends": username}}
    )


def login_to_account(client, username, password):
    """
    Utility function for logging in to an account
    """
    try:
        db = client.PopcornPicksDB
        user = db.users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return str(user["_id"])
        return None
    except Exception as e:
        print(f"Error logging in: {str(e)}")
        return None


def submit_review(client, user, movie, score, review):
    """
    Utility function for creating a dictionary for submitting a review
    """
    try:
        db = client.PopcornPicksDB

        movie_doc = db.movies.find_one({"name": movie})

        if not movie_doc:
            csv_path = os.path.join(os.path.dirname(__file__), "../../data/movies.csv")
            df = pd.read_csv(csv_path)
            print(df.head())
            movie_row = df[df["title"] == movie]
            print(movie, movie_row)

            if movie_row.empty:
                raise Exception("Movie not found in CSV")

            movie_doc = {
                "_id": int(movie_row.iloc[0]["movieId"]),
                "name": movie,
                "imdb_id": movie_row.iloc[0]["imdb_id"],
            }

            db.movies.insert_one(movie_doc)

        if not movie_doc:
            raise Exception("Movie not found in database or CSV")

        review_doc = {
            "user_id": ObjectId(user[1]),
            "movie_id": movie_doc["_id"],
            "score": score,
            "review": review,
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }

        db.ratings.insert_one(review_doc)

    except Exception as e:
        print(f"Error submitting review: {str(e)}")
        raise


def get_wall_posts(client):
    """
    Utility function to get wall posts from the MongoDB database,
    joining data from Users, Ratings, and Movies collections.
    """
    db = client.PopcornPicksDB

    posts = list(
        db.ratings.aggregate(
            [
                {
                    "$lookup": {
                        "from": "movies",
                        "localField": "movie_id",
                        "foreignField": "_id",
                        "as": "movie_info",
                    }
                },
                {"$unwind": "$movie_info"},
                {
                    "$project": {
                        "_id": 0,
                        "name": "$movie_info.name",
                        "imdb_id": "$movie_info.imdb_id",
                        "review": "$review",
                        "score": "$score",
                        "time": "$time",
                    }
                },
                {"$sort": {"time": -1}},
                {"$limit": 50},
            ]
        )
    )
    print(posts)
    return jsonify(posts)


def get_user_ratings(client):
    """
    Utility function to get wall posts from the MongoDB database,
    joining data from Users, Ratings, and Movies collections.
    """
    db = client.PopcornPicksDB

    posts = list(
        db.ratings.aggregate(
            [
                {
                    "$lookup": {
                        "from": "movies",
                        "localField": "movie_id",
                        "foreignField": "_id",
                        "as": "movie_info",
                    }
                },
                {"$unwind": "$movie_info"},
                {
                    "$project": {
                        "_id": 0,
                        "user_id": "$user_id",
                        "name": "$movie_info.name",
                        "imdb_id": "$movie_info.imdb_id",
                        "movie_id": "$movie_id",
                        "review": "$review",
                        "score": "$score",
                        "time": "$time",
                    }
                },
                {"$sort": {"time": -1}},
                {"$limit": 50},
            ]
        )
    )
    print(posts)
    return posts


def get_recent_movies(client, user_id):
    """
    Utility function for getting recent movies reviewed by a user
    """
    try:
        db = client.PopcornPicksDB
        pipeline = [
            {"$match": {"user_id": str(user_id)}},
            {"$sort": {"time": -1}},
            {"$limit": 5},
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "movie_id",
                    "foreignField": "_id",
                    "as": "movie",
                }
            },
            {"$unwind": "$movie"},
            {"$project": {"_id": 0, "name": "$movie.name", "score": "$score"}},
        ]

        results = list(db.ratings.aggregate(pipeline))
        return jsonify(results)

    except Exception as e:
        print(f"Error getting recent movies: {str(e)}")
        return jsonify([])


def get_username(client, user):
    """
    Utility function for getting the current users username
    """
    user_data = client.PopcornPicksDB.users.find_one({"_id": ObjectId(user[1])})
    return user_data["username"] if user_data else ""


def get_recent_friend_movies(client, username):
    """
    Utility function for getting recent movies from user's friends
    """
    try:
        db = client.PopcornPicksDB

        user = db.users.find_one({"username": username})
        if not user:
            return jsonify([])

        friends = user.get("friends", [])[1]
        if not friends:
            return jsonify([])

        pipeline = [
            {"$match": {"user_id": {"$in": friends}}},
            {"$sort": {"time": -1}},
            {"$limit": 5},
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "movie_id",
                    "foreignField": "_id",
                    "as": "movie",
                }
            },
            {"$unwind": "$movie"},
            {"$project": {"_id": 0, "name": "$movie.name", "score": "$score"}},
        ]

        results = list(db.ratings.aggregate(pipeline))
        return jsonify(results)

    except Exception as e:
        print(f"Error getting friend movies: {str(e)}")
        return jsonify([])


def get_friends(client, user):
    """
    Utility function for getting the current users friends
    """
    user_data = client.PopcornPicksDB.users.find_one({"_id": ObjectId(user[1])})
    return json.dumps(user_data.get("friends", []))


def get_user_history(client, user_id):
    """
    Retrieves the current user's movie ratings from the database for recommendation.
    """
    try:
        db = client.PopcornPicksDB
        user_history = []

        user_ratings = db.ratings.find({"user_id": ObjectId(user_id)})

        for rating in user_ratings:
            user_history.append((rating["movie_id"], rating["score"]))

        return user_history

    except Exception as e:
        print(f"Error retrieving user history: {str(e)}")
        raise
