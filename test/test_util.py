"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks

Test suit for search feature
"""

import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from bson import ObjectId

from src.recommenderapp.client import client
from src.recommenderapp.utils import (
    create_colored_tags,
    beautify_feedback_data,
    create_movie_genres,
    send_email_to_user,
    create_account,
    login_to_account,
    submit_review,
    get_wall_posts,
    get_recent_movies,
    get_username,
    add_friend,
    get_friends,
    get_user_history,
    fetch_streaming_link,
)


class TestUtils(unittest.TestCase):
    """
    Unit tests for utility functions related to movie recommendation app.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test database and insert sample movie data before running the tests.
        This method is called once before any tests are executed.
        """
        cls.movies_df = pd.read_csv("data/movies.csv")

        cls.client = client
        cls.db = client.testDB

        cls.db.users.create_index([("username", 1)], unique=True)
        cls.db.users.create_index([("email", 1)], unique=True)
        cls.db.movies.create_index([("imdb_id", 1)], unique=True)
        cls.db.movies.create_index([("name", 1)])
        cls.db.ratings.create_index([("user_id", 1), ("time", -1)])
        cls.db.ratings.create_index([("movie_id", 1)])

        cls.sample_movies = [
            {
                "_id": ObjectId(),
                "name": "Toy Story (1995)",
                "imdb_id": "tt0114709",
                "movie_id": 862,
                "year": 1995,
            },
            {
                "_id": ObjectId(),
                "name": "Interstellar (2014)",
                "imdb_id": "tt0816692",
                "year": 2014,
                "movie_id": 862,
            },
        ]

        create_account(
            cls.db,
            email="test1@example.com",
            username="testUserLogin",
            password="password123",
        )
        cls.db.movies.insert_many(cls.sample_movies)

    def test_create_colored_tags(self):
        """
        Test the function that generates HTML
        tags with specific colors for movie genres.
        """
        genres = ["Musical", "Sci-Fi"]
        result = create_colored_tags(genres)
        print(result)
        expected_result = '<span style="background-color: #FF1493; color: #FFFFFF; \
            padding: 5px; border-radius: 5px;">Musical</span> \
            <span style="background-color: #00CED1; color: #FFFFFF; \
            padding: 5px; border-radius: 5px;">Sci-Fi</span>'
        self.assertEqual(result, expected_result)

    def test_beautify_feedback_data(self):
        """
        Test the function that organizes feedback data
        into categories such as 'Liked', 'Disliked', and 'Yet to Watch'.
        """
        data = {"Movie 1": "Yet to watch", "Movie 2": "Like", "Movie 3": "Dislike"}
        result = beautify_feedback_data(data)
        expected_result = {
            "Liked": ["Movie 2"],
            "Disliked": ["Movie 3"],
            "Yet to Watch": ["Movie 1"],
        }
        self.assertEqual(result, expected_result)

    def test_create_movie_genres(self):
        """
        Test the function that creates a dictionary of movie titles
        and their associated genres from a DataFrame.
        """
        data = [
            ["862", "Toy Story (1995)", "Animation|Comedy|Family"],
            ["8844", "Jumanji (1995)", "Adventure|Fantasy|Family"],
        ]
        movie_genre_df = pd.DataFrame(data, columns=["movieId", "title", "genres"])
        result = create_movie_genres(movie_genre_df)
        expected_result = {
            "Toy Story (1995)": ["Animation", "Comedy", "Family"],
            "Jumanji (1995)": ["Adventure", "Fantasy", "Family"],
        }
        self.assertEqual(result, expected_result)

    @patch("smtplib.SMTP")
    def test_send_email_to_user(self, mock_smtp):
        """
        Test the function that sends an email to a user with categorized movie feedback.
        Mock the SMTP server to avoid sending real emails during testing.
        """
        categorized_data = {
            "The Crimson Permanent Assurance (1983)": "Like",
            "Romancing the Stone (1984)": "Yet to watch",
            "Downtown (1990)": "Dislike",
            "City Slickers (1991)": "Yet to watch",
            "The Return of the Musketeers (1989)": "Like",
            "Gurren Lagann The Movie: Childhood's End (2008)": "Yet to watch",
            "The Machine Girl (2008)": "Dislike",
            "The Myth (2005)": "Yet to watch",
            "Gurren Lagann The Movie: The Lights in the \
                                Sky Are Stars (2009)": "Like",
            "Journey to the Center of the Earth (2008)": "Yet to watch",
        }

        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance

        send_email_to_user(
            "shrimadh332001@gmail.com", beautify_feedback_data(categorized_data)
        )

        mock_server_instance.sendmail.assert_called_once()

    def test_create_account(self):
        """
        Test the function that creates a new user account in the database.
        Ensure that account creation is successful.
        """
        result = create_account(
            self.db,
            email="test@example.com",
            username="testUser",
            password="password123",
        )
        self.assertTrue(result)

    def test_login_to_account(self):
        """
        Test the function that logs in a user by checking their credentials.

         - Ensure successful login with correct credentials.
         - Ensure login fails with incorrect credentials.
        """

        # Test successful login
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        self.assertIsNotNone(user_id)

        # Test failed login with incorrect password
        wrong_login_attempt = login_to_account(
            self.db, username="testUserLogin", password="wrongPassword"
        )
        self.assertIsNone(wrong_login_attempt)

    def test_submit_review(self):
        """
        Test the function that allows users to submit reviews for movies.
        Ensure that the review is saved correctly in the database.
        """
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        self.db.ratings.delete_many({})
        submit_review(
            self.db,
            user=[None, user_id],
            movie="Toy Story (1995)",
            score=5,
            review="Great movie!",
        )

        review_doc = self.db.ratings.find_one({"user_id": ObjectId(user_id)})

        self.assertIsNotNone(review_doc)
        self.assertEqual(review_doc["score"], 5)

    def test_get_wall_posts(self):
        """
        Test the function that retrieves wall posts (reviews) from all users.
        Ensure that wall posts are returned after a review is submitted.
        """
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        self.db.ratings.delete_many({})
        submit_review(
            self.db,
            user=[None, user_id],
            movie="Toy Story (1995)",
            score=5,
            review="Great movie!",
        )

        posts = get_wall_posts(self.db)
        print(posts)
        self.assertGreater(len(posts), 0)

    def test_get_recent_movies(self):
        """
        Test the function that retrieves recent movies reviewed by a specific user.
        Ensure that recent movies are returned after submitting a review.
        """
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        self.db.ratings.delete_many({})
        self.db.movies.delete_many({})
        submit_review(
            self.db,
            user=[None, user_id],
            movie="Toy Story (1995)",
            score=10,
            review="Great movie!",
        )

        recent_movies = get_recent_movies(self.db, user_id, self.movies_df)
        print("test_utils", recent_movies)
        self.assertGreater(len(recent_movies), 0)

    def test_get_username(self):
        """
        Test the function that retrieves a user's username based on their ID.
        Ensure that the correct username is returned for a given user ID.
        """
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )

        username = get_username(self.db, user=[None, user_id])

        self.assertEqual(username, "testUserLogin")

    def test_add_friend_and_get_friends(self):
        """
        Test adding a friend and retrieving the list of friends for a user.
        Ensure that friends are correctly added and retrieved from the database.
        """
        create_account(
            self.db,
            email="test2@example.com",
            username="Friend1",
            password="password123",
        )
        user_id_1 = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        print(user_id_1)
        add_friend(self.db, [None, user_id_1], username="Friend1")

        friends_list = get_friends(self.db, user_id_1)
        print(friends_list)
        friends_list = [friend["username"] for friend in friends_list]

        self.assertIn("Friend1", friends_list)

    def test_get_user_history(self):
        """
        Test retrieving a user's history of reviews and ratings.
        Ensure that reviews submitted by a user are correctly retrieved from their history.
        """
        user_id_1 = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )

        submit_review(
            self.db,
            user=[None, user_id_1],
            movie="Toy Story (1995)",
            score=4,
            review="",
        )

        history = get_user_history(self.db, user_id_1)

        self.assertGreater(len(history), 0)

    @patch("requests.get")
    def test_fetch_streaming_link(self, mock_get):
        """
        Test fetching streaming links for movies using an external API.
        Mock the requests.get method to simulate API responses without making real HTTP requests.
        Ensure that the correct streaming URL is returned based on the API response.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "Netflix", "web_url": "https://netflix.com"}
        ]
        mock_get.return_value = mock_response

        url = fetch_streaming_link("tt0114709")

        self.assertEqual(url, "https://netflix.com")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests have run by deleting all
        documents from users, movies, and ratings collections.
        Drop the entire test database to ensure no leftover data.
        """
        cls.db.users.delete_many({})
        cls.db.movies.delete_many({})
        cls.db.ratings.delete_many({})
        client.drop_database("testDB")


if __name__ == "__main__":
    unittest.main()
