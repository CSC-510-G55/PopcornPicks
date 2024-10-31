import unittest
from src.recommenderapp.client import client
from bson import ObjectId
from unittest.mock import patch, MagicMock
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
    get_recent_friend_movies,
    add_friend,
    get_friends,
    get_user_history,
    fetch_streaming_link
)
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import requests

class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = client
        cls.db = client.testDB

        cls.sample_movies = [
            {"_id": ObjectId(), "name": "Toy Story", "imdb_id": "tt0114709", "year": 1995},
            {"_id": ObjectId(), "name": "Interstellar", "imdb_id": "tt0816692", "year": 2014}
        ]

        cls.db.movies.insert_many(cls.sample_movies)

    def test_create_colored_tags(self):
        genres = ["Musical", "Sci-Fi"]
        result = create_colored_tags(genres)
        expected_result = (
            '<span style="background-color: #FF1493; color: #FFFFFF; padding: 5px; border-radius: 5px;">Musical</span> '
            '<span style="background-color: #00CED1; color: #FFFFFF; padding: 5px; border-radius: 5px;">Sci-Fi</span>'
        )
        self.assertEqual(result, expected_result)

    def test_beautify_feedback_data(self):
        data = {"Movie 1": "Yet to watch", "Movie 2": "Like", "Movie 3": "Dislike"}
        result = beautify_feedback_data(data)
        expected_result = {
            "Liked": ["Movie 2"],
            "Disliked": ["Movie 3"],
            "Yet to Watch": ["Movie 1"]
        }
        self.assertEqual(result, expected_result)

    def test_create_movie_genres(self):
        data = [
            ["862", "Toy Story (1995)", "Animation|Comedy|Family"],
            ["8844", "Jumanji (1995)", "Adventure|Fantasy|Family"]
        ]
        movie_genre_df = pd.DataFrame(data, columns=["movieId", "title", "genres"])
        result = create_movie_genres(movie_genre_df)
        expected_result = {
            "Toy Story (1995)": ["Animation", "Comedy", "Family"],
            "Jumanji (1995)": ["Adventure", "Fantasy", "Family"]
        }
        self.assertEqual(result, expected_result)

    @patch("smtplib.SMTP")
    def test_send_email_to_user(self, mock_smtp):
        categorized_data = {
            "Liked": ["Toy Story"],
            "Disliked": ["Cutthroat Island"],
            "Yet to Watch": ["Assassins"]
        }
        
        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance
        
        send_email_to_user("test@example.com", categorized_data)
        
        mock_server_instance.sendmail.assert_called_once()

    def test_create_account(self):
        result = create_account(self.client, email="test@example.com", username="testUser", password="password123")
        self.assertTrue(result)

    def test_login_to_account(self):
        create_account(self.client, email="test@example.com", username="testUserLogin", password="password123")
        
        user_id = login_to_account(self.client, username="testUserLogin", password="password123")
        
        self.assertIsNotNone(user_id)
        
        wrong_login_attempt = login_to_account(self.client, username="testUserLogin", password="wrongPassword")
        
        self.assertIsNone(wrong_login_attempt)

    def test_submit_review(self):
        user_id = login_to_account(self.client, username="testUserLogin", password="password123")
        
        submit_review(self.client, user=user_id, movie="Toy Story", score=5, review="Great movie!")
        
        review_doc = self.db.ratings.find_one({"user_id": ObjectId(user_id)})
        
        self.assertIsNotNone(review_doc)
        self.assertEqual(review_doc["score"], 5)

    def test_get_wall_posts(self):
        user_id = login_to_account(self.client, username="testUserLogin", password="password123")
        
        submit_review(self.client, user=user_id, movie="Toy Story", score=5, review="Great movie!")
        
        posts = get_wall_posts(self.client)
        
        self.assertGreater(len(posts.json), 0)

    def test_get_recent_movies(self):
        user_id = login_to_account(self.client, username="testUserLogin", password="password123")
        
        submit_review(self.client, user=user_id, movie="Toy Story", score=5, review="Great movie!")
        
        recent_movies = get_recent_movies(self.client, user_id)
        
        self.assertGreater(len(recent_movies.json), 0)

    def test_get_username(self):
        user_id = login_to_account(self.client, username="testUserLogin", password="password123")
        
        username = get_username(self.client, user=[None, user_id])
        
        self.assertEqual(username, "testUserLogin")

    def test_add_friend_and_get_friends(self):
        user_id_1 = login_to_account(self.client, username="testUserLogin1", password="password123")
        print(user_id_1)
        add_friend(self.client, [None, user_id_1], username="Friend1")
        
        friends_list = get_friends(self.client, [None, user_id_1])
        
        self.assertIn("Friend1", friends_list)

    def test_get_user_history(self):
        user_id_1 = login_to_account(self.client, username="testUserLogin1", password="password123")
        
        submit_review(self.client, user=user_id_1, movie="Toy Story", score=4, review="")
        
        history = get_user_history(self.client, user_id_1)
        
        self.assertGreater(len(history), 0)

    @patch("requests.get")
    def test_fetch_streaming_link(self, mock_get):
       mock_response = MagicMock()
       mock_response.json.return_value = [{"name": "Netflix", "web_url": "https://netflix.com"}]
       mock_get.return_value = mock_response

       url = fetch_streaming_link("tt0114709")

       self.assertEqual(url, 'https://netflix.com')

if __name__ == "__main__":
    unittest.main()