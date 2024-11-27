"""
Copyright (c) 2023 Srimadh V Rao, Akul G Devali, Manav D Shah
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=import-error
import json
import datetime
import logging
import smtplib
import bcrypt
from dotenv import load_dotenv
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo.errors import PyMongoError
from bson.errors import InvalidId
from bson.objectid import ObjectId
import pandas as pd
import os
import requests
import string
import secrets

app_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(app_dir)
project_dir = os.path.dirname(code_dir)

load_dotenv()


def load_movies():
    """Load movies data from CSV."""
    return pd.read_csv(os.path.join("data", "movies.csv"))


def generate_random_string(length: int) -> str:
    characters = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


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
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "popcornpicks.ofc@gmail.com"
    sender_password = os.getenv("APP_PASSWORD")

    # Verify that environment variables are set
    if not sender_email or not sender_password:
        logging.error("Email credentials not found in environment variables")
        raise ValueError("Email credentials not properly configured")

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

    # Create the email message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Your movie recommendation from PopcornPicks"

    try:
        # Load the CSV file into a DataFrame
        movie_genre_df = pd.read_csv("data/movies.csv")
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
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            logging.info("Email sent successfully!")

    except FileNotFoundError:
        logging.error("Movies CSV file not found")
        raise
    except SMTPException as e:
        logging.error("SMTP error while sending email: %s", str(e))
        raise


def create_account(db, email, username, password):
    """Utility function for creating an account"""
    try:
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
    except PyMongoError as e:
        print(f"Error creating account: {str(e)}")
        return False


def add_friend(db, user, username):
    """
    Utility function for adding a friend
    """
    db.users.update_one(
        {"_id": ObjectId(user[1])}, {"$addToSet": {"friends": username}}
    )
    return True


def login_to_account(db, username, password):
    """
    Utility function for logging in to an account
    """
    try:
        user = db.users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return str(user["_id"])
        return None
    except PyMongoError as e:
        print(f"Error logging in: {str(e)}")
        return None


def submit_review(db, user, movie, score, review):
    """
    Utility function for creating a dictionary for submitting a review
    """
    movie_doc = db.movies.find_one({"name": movie})

    if not movie_doc:
        csv_path = os.path.join("data/movies.csv")
        df = pd.read_csv(csv_path)
        movie_row = df[df["title"] == movie]

        movie_doc = {
            "_id": int(movie_row.iloc[0]["movieId"]),
            "name": movie,
            "imdb_id": movie_row.iloc[0]["imdb_id"],
        }

        db.movies.insert_one(movie_doc)

    review_doc = {
        "user_id": ObjectId(user[1]),
        "movie_id": movie_doc["_id"],
        "score": score,
        "review": review,
        "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

    db.ratings.insert_one(review_doc)


def add_list_to_db(db, user, list_name, movie_list):
    """
    Utility function for adding a list to the database
    """

    slug = list_name + "--" + generate_random_string(10)
    user_id = ObjectId(user[1])

    movies = []

    for movie_name in movie_list:
        movie_doc = db.movies.find_one({"title": movie_name})

        if not movie_doc:
            csv_path = os.path.join("data/movies.csv")
            df = pd.read_csv(csv_path)
            movie_row = df[df["title"] == movie_name]

            movie_row = movie_row.to_dict(orient="records")[0]
            movie_row["name"] = movie_row["title"]

            db.movies.update_one(
                {"movieId": movie_row["movieId"]},
                {
                    "$setOnInsert": movie_row
                },  # Only insert the record if it doesn't exist
                upsert=True,
            )

        movies.append(db.movies.find_one({"name": movie_name})["_id"])

    db.lists.insert_one(
        {
            "name": list_name,
            "slug": slug,
            "movies": list(movies),
            "user_id": user_id,
        }
    )

    return slug


def get_list_from_db(db, slug):
    """
    Utility function for getting a list from the database
    """
    list_data = db.lists.find_one({"slug": slug}, {"_id": False, "user_id": False})
    movie_ids = list_data["movies"]

    movies = list(
        db.movies.find({"_id": {"$in": movie_ids}}, {"_id": False, "user_id": False})
    )  # Exclude '_id' field

    list_data["movies"] = movies

    return list_data


def get_wall_posts(db):
    """
    Utility function to get wall posts from the MongoDB database,
    joining data from Users, Ratings, and Movies collections.
    """

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
                        "user_id": "$user_id",
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

    def get_username_from_user_id(db, user):
        """
        Utility function for getting the current users username
        """
        user_data = db.users.find_one({"_id": ObjectId(user)})
        return user_data["username"] if user_data else ""

    print(posts)
    posts = [
        {**post, "username": get_username_from_user_id(db, str(post["user_id"]))}
        for post in posts
    ]

    # Remove the 'user_id' field if you don't want it in the final output
    posts = [{k: v for k, v in post.items() if k != "user_id"} for post in posts]
    return posts


def get_user_ratings(db):
    """
    Utility function to get wall posts from the MongoDB database,
    joining data from Users, Ratings, and Movies collections.
    """
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
                        "movie_id": "$movie_info.movieId",
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


def get_recent_movies(db, user_id, movies_df):
    """
    Gets the recent movies of the active user with their names and ratings.
    """
    user_id = ObjectId(user_id)
    movies = list(db.ratings.find({"user_id": user_id}).sort("_id", -1))
    print(movies)
    if not movies:
        return json.dumps([])
    movie_data = [
        {"movie_id": movie["movie_id"], "score": movie["score"]} for movie in movies
    ]
    ratings_df = pd.DataFrame(movie_data)
    merged_df = pd.merge(
        ratings_df, movies_df, how="left", left_on="movie_id", right_on="movieId"
    )
    recent_movies_list = merged_df[["title", "score"]].to_dict(orient="records")
    return json.dumps(recent_movies_list)


def get_username(db, user):
    """
    Utility function for getting the current users username
    """
    user_data = db.users.find_one({"_id": ObjectId(user[1])})
    return user_data["username"] if user_data else ""


def get_friends(db, user_id):
    """
    Utility function to get a user's friends list with their user IDs and usernames.
    """
    user_data = db.users.find_one({"_id": ObjectId(user_id)})

    friend_usernames = user_data.get("friends", [])

    friends_info = list(
        db.users.find(
            {"username": {"$in": friend_usernames}, "_id": {"$ne": ObjectId(user_id)}},
            {"_id": 1, "username": 1},
        )
    )

    return [
        {"_id": str(friend["_id"]), "username": friend["username"]}
        for friend in friends_info
    ]


def get_user_history(db, user_id):
    """
    Retrieves the current user's movie ratings from the database for recommendation.
    """
    try:
        user_history = []

        user_ratings = db.ratings.find({"user_id": ObjectId(user_id)})

        for rating in user_ratings:
            user_history.append((rating["movie_id"], rating["score"]))

        return user_history

    except InvalidId as e:
        print(f"Invalid user ID format: {str(e)}")
        raise


def get_genre_count(db, user):
    """
    Utility function to get movies from the MongoDB database, and calculate the count of
    genres of the movies which the user has watched.
    """
    results = db.ratings.find({"user_id": ObjectId(user[1])}, {"movie_id": 1, "_id": 0})

    # Extract movie_ids from the results
    movie_ids = [result["movie_id"] for result in results]

    # Read the movies CSV file into a DataFrame
    movies_df = load_movies()

    # Filter rows where the movie_id is in the provided movie_ids list and get the 'genres' column
    filtered_genres = movies_df[movies_df["movieId"].isin(movie_ids)]["genres"]

    # Initialize an empty dictionary to store genre counts
    genre_count = {}

    # Loop through each row in the genres column
    for genres in filtered_genres:
        # Split by '|' and strip any whitespace around each genre
        genre_list = [genre.strip() for genre in genres.split("|")]
        print(genre_list, end="\n")
        # Count each genre
        for genre in genre_list:
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1
    return genre_count


def fetch_streaming_link(imdb_id):
    """
    Fetches the streaming links of movies.
    """

    url = f"https://api.watchmode.com/v1/title/{imdb_id}/sources/"
    api_key = os.getenv("WATCHMODE_API_KEY")

    headers = {"Authorization": f"Bearer {api_key}"}

    params = {"apiKey": api_key, "regions": "US"}

    response = requests.get(url, headers=headers, params=params, timeout=4)
    sources = {
        item["name"]: {"platform": item["name"], "url": item["web_url"]}
        for item in response.json()
    }
    res = sorted(sources.values(), key=lambda x: x["platform"])

    if res:
        return res[0]["url"]  # Returns the first URL
    return None
