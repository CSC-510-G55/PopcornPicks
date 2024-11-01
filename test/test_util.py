"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks

Test suite for search feature
"""

import unittest
from unittest.mock import patch, MagicMock
from smtplib import SMTPException
import pandas as pd
from bson import ObjectId
from bson.errors import InvalidId
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
    get_genre_count,
)


class TestPopcornPicks(unittest.TestCase):
    """Test suite for PopcornPicks functionalities"""

    @classmethod
    def setUpClass(cls):
        """Set up the test database and sample data"""
        cls.movies_df = pd.read_csv("data/movies.csv")
        cls.client = client
        cls.db = client.testDB
        cls.db.users.create_index([("username", 1)])
        cls.db.users.create_index([("email", 1)])
        cls.db.movies.create_index([("imdb_id", 1)])
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

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database after all tests"""
        client.drop_database("testDB")

    # Utility Functions
    def test_create_colored_tags(self):
        genres = ["Musical", "Sci-Fi"]
        result = create_colored_tags(genres)
        expected_result = (
            '<span style="background-color: #FF1493; color: #FFFFFF;             '
            'padding: 5px; border-radius: 5px;">Musical</span> <s'
            'pan style="background-color: #00CED1; color: #FFFFFF;             '
            'padding: 5px; border-radius: 5px;">Sci-Fi</span>'
        )
        self.assertEqual(result, expected_result)

    def test_beautify_feedback_data(self):
        data = {"Movie 1": "Yet to watch", "Movie 2": "Like", "Movie 3": "Dislike"}
        result = beautify_feedback_data(data)
        expected_result = {
            "Liked": ["Movie 2"],
            "Disliked": ["Movie 3"],
            "Yet to Watch": ["Movie 1"],
        }
        self.assertEqual(result, expected_result)

    def test_create_movie_genres(self):
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

    # Email Functionality
    @patch("smtplib.SMTP")
    def test_send_email_to_user(self, mock_smtp):
        categorized_data = {
            "The Crimson Permanent Assurance (1983)": "Like",
            "Romancing the Stone (1984)": "Yet to watch",
            "Downtown (1990)": "Dislike",
        }
        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance
        send_email_to_user("test@example.com", beautify_feedback_data(categorized_data))
        mock_server_instance.sendmail.assert_called_once()

    # User Management
    def test_create_account(self):
        result = create_account(
            self.db,
            email="test@example.com",
            username="testUser",
            password="password123",
        )
        self.assertTrue(result)

    def test_login_to_account(self):
        user_id = login_to_account(self.db, username="testUserLogin", password="password123")
        self.assertIsNotNone(user_id)

        wrong_login_attempt = login_to_account(
            self.db, username="testUserLogin", password="wrongPassword"
        )
        self.assertIsNone(wrong_login_attempt)

    # Review and Rating
    def test_submit_review(self):
        user_id = login_to_account(self.db, username="testUserLogin", password="password123")
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

    # Movie Features
    def test_get_recent_movies(self):
        user_id = login_to_account(self.db, username="testUserLogin", password="password123")
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
        self.assertGreater(len(recent_movies), 0)

    @patch("requests.get")
    def test_fetch_streaming_link(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"name": "Netflix", "web_url": "https://netflix.com"}]
        mock_get.return_value = mock_response
        url = fetch_streaming_link("tt0114709")
        self.assertEqual(url, "https://netflix.com")

    @patch("pandas.read_csv")
    def test_get_genre_count(self, mock_read_csv):
        user_id = login_to_account(self.db, username="testUserLogin", password="password123")
        mock_movie_results = [{"movie_id": 1}, {"movie_id": 2}, {"movie_id": 3}]
        mock_db = MagicMock()
        mock_db.ratings.find.return_value = mock_movie_results
        mock_movies_data = {
            "movieId": [1, 2, 3],
            "genres": ["Action|Adventure", "Comedy|Drama", "Action|Sci-Fi"],
        }
        mock_df = pd.DataFrame(mock_movies_data)
        mock_read_csv.return_value = mock_df
        genre_counts = get_genre_count(mock_db, [None, str(user_id)])
        expected_counts = {
            "Action": 2,
            "Adventure": 1,
            "Comedy": 1,
            "Drama": 1,
            "Sci-Fi": 1,
        }
        self.assertEqual(genre_counts, expected_counts)
        mock_db.ratings.find.assert_called_once()
        mock_read_csv.assert_called_once()


if __name__ == "__main__":
    unittest.main()
