"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks

Test suite for search feature
"""

# pylint: skip-file

import unittest
from unittest.mock import patch, MagicMock
from smtplib import SMTPException

import pandas as pd

from bson import ObjectId
from bson.errors import InvalidId

from backend.recommenderapp.client import client
from backend.recommenderapp.utils import (
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
    add_list_to_db,
    get_list_from_db,
)


class TestRecommenderApp(unittest.TestCase):
    """Test class for all recommender app functionality"""

    @classmethod
    def setUpClass(cls):
        """Common setup for all tests"""
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
        """Clean up after all tests"""
        cls.db.users.delete_many({})
        cls.db.movies.delete_many({})
        cls.db.ratings.delete_many({})
        client.drop_database("testDB")

    def test_create_colored_tags(self):
        """Test generating HTML tags with specific colors for movie genres."""
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
        """Test organizing feedback data into categories."""
        data = {"Movie 1": "Yet to watch", "Movie 2": "Like", "Movie 3": "Dislike"}
        result = beautify_feedback_data(data)
        expected_result = {
            "Liked": ["Movie 2"],
            "Disliked": ["Movie 3"],
            "Yet to Watch": ["Movie 1"],
        }
        self.assertEqual(result, expected_result)

    def test_create_movie_genres(self):
        """Test creating dictionary of movie titles and genres."""
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
        """Test sending email to user with categorized movie feedback."""
        categorized_data = {
            "The Crimson Permanent Assurance (1983)": "Like",
            "Romancing the Stone (1984)": "Yet to watch",
            "Downtown (1990)": "Dislike",
        }
        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance
        send_email_to_user("test@example.com", beautify_feedback_data(categorized_data))
        mock_server_instance.sendmail.assert_called_once()

    @patch("pandas.read_csv")
    def test_send_email_file_not_found(self, mock_read_csv):
        """Test handling of FileNotFoundError."""
        mock_read_csv.side_effect = FileNotFoundError
        categorized_data = {"Test Movie": "Like"}

        with self.assertRaises(FileNotFoundError):
            send_email_to_user(
                "test@example.com", beautify_feedback_data(categorized_data)
            )

    @patch("smtplib.SMTP")
    def test_send_email_smtp_error(self, mock_smtp):
        """Test handling of SMTPException."""
        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance
        mock_server_instance.sendmail.side_effect = SMTPException("SMTP Error")

        categorized_data = {"Test Movie": "Like"}

        with self.assertRaises(SMTPException):
            send_email_to_user(
                "test@example.com", beautify_feedback_data(categorized_data)
            )

    def test_create_account(self):
        """Test creating a new user account."""
        result = create_account(
            self.db,
            email="test@example.com",
            username="testUser",
            password="password123",
        )
        self.assertTrue(result)

    def test_login_to_account(self):
        """Test user login functionality."""
        # Test successful login
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        # self.assertIsNotNone(user_id)

        # Test failed login
        wrong_login_attempt = login_to_account(
            self.db, username="testUserLogin", password="wrongPassword"
        )
        # self.assertIsNone(wrong_login_attempt)

    def test_get_username(self):
        """Test retrieving username based on user ID."""
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        username = get_username(self.db, user=[None, user_id])
        # self.assertEqual(username, "testUserLogin")

    def test_add_friend_and_get_friends(self):
        """Test adding and retrieving friends."""
        create_account(
            self.db,
            email="test2@example.com",
            username="Friend1",
            password="password123",
        )
        user_id_1 = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        add_friend(self.db, [None, user_id_1], username="Friend1")

        friends_list = get_friends(self.db, user_id_1)
        friends_usernames = [friend["username"] for friend in friends_list]
        self.assertIn("Friend1", friends_usernames)

    def test_submit_review(self):
        """Test submitting movie reviews."""
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        self.db.ratings.delete_many({})
        submit_review(
            self.db,
            user=[None, user_id],
            movie="Jumanji (1995)",
            score=10,
            review="Great movie!",
        )

    def test_get_wall_posts(self):
        """Test retrieving wall posts."""
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
        self.assertGreater(len(posts), 0)

    def test_get_user_history(self):
        """Test retrieving user history."""
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        submit_review(
            self.db,
            user=[None, user_id],
            movie="Interstellar (2014)",
            score=8,
            review="Good movie",
        )
        history = get_user_history(self.db, user_id)
        self.assertGreater(len(history), 0)

    def test_get_user_history_invalid_id(self):
        """Test handling invalid user ID in history retrieval."""
        with self.assertRaises(InvalidId):
            get_user_history(self.db, "invalid_id_format")

    def test_get_recent_movies(self):
        """Test retrieving recent movies."""
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
        self.assertGreater(len(recent_movies), 0)

    def test_list_creation(self):
        """Test creating and retrieving movie lists."""
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        toy_story_collection = [
            "Toy Story (1995)",
            "Toy Story 2 (1999)",
            "Toy Story 3 (2010)",
        ]

        slug = add_list_to_db(
            self.db,
            user=[None, user_id],
            list_name="Toy Story Collection",
            movie_list=toy_story_collection,
        )

        retrieved_list = get_list_from_db(self.db, slug)

        self.assertEqual(
            [
                (movie["title"] if "title" in movie else movie["name"])
                for movie in retrieved_list["movies"]
            ],
            toy_story_collection,
        )

    def test_uniqueness_of_list_slug(self):
        """Test uniqueness of list slug."""
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )
        toy_story_collection = [
            "Toy Story (1995)",
            "Toy Story 2 (1999)",
            "Toy Story 3 (2010)",
        ]

        slug1 = add_list_to_db(
            self.db,
            user=[None, user_id],
            list_name="Toy Story Collection",
            movie_list=toy_story_collection,
        )

        slug2 = add_list_to_db(
            self.db,
            user=[None, user_id],
            list_name="Toy Story Collection",
            movie_list=toy_story_collection,
        )

        self.assertNotEqual(slug1, slug2)

    @patch("requests.get")
    def test_fetch_streaming_link(self, mock_get):
        """Test fetching streaming links."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "Netflix", "web_url": "https://netflix.com"}
        ]
        mock_get.return_value = mock_response

        url = fetch_streaming_link("tt0114709")
        self.assertEqual(url, "https://netflix.com")

    @patch("pandas.read_csv")
    def test_get_genre_count(self, mock_read_csv):
        """Test calculating genre counts."""
        user_id = login_to_account(
            self.db, username="testUserLogin", password="password123"
        )

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
