"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty

This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import unittest
import warnings
from pymongo.mongo_client import MongoClient

from src.recommenderapp.item_based import recommend_for_new_user

warnings.filterwarnings("ignore")

MONGO_URI = "mongodb+srv://svrao3:popcorn1234@popcorn.xujnm.mongodb.net"
MONGO_OPTIONS = "/?retryWrites=true&w=majority&appName=PopCorn"
MONGO_URI += MONGO_OPTIONS

client = MongoClient(MONGO_URI)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

user = {1: None}
user[1] = "671b289a193d2a9361ebf39a"  # Hardcoded user id for testing purposes
USER_ID = user[1]

class Tests(unittest.TestCase):
    """
    Test cases for recommender system
    """

    def test_empty_input(self):
        """Test with empty input."""
        ts = []
        recommendations, _, _ = recommend_for_new_user(ts, USER_ID, client)
        self.assertEqual(recommendations, [])

    def test_no_matching_movie(self):
        """Test with no matching movie."""
        ts = [{"title": "Unknown Movie (2025)", "rating": 10.0}]
        recommendations, _, _ = recommend_for_new_user(ts, USER_ID, client)
        self.assertEqual(recommendations, [])

    def test_duplicate_movies(self):
        """Test with duplicate movies."""
        ts = [
            {"title": "Toy Story (1995)", "rating": 10.0},
            {"title": "Toy Story (1995)", "rating": 10.0},
        ]
        recommendations, _, _ = recommend_for_new_user(ts, USER_ID, client)
        self.assertTrue(len(recommendations) > 0)

    def test_genre_similarity_calculation(self):
        """Test genre similarity calculation."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        recommendations, genres, _ = recommend_for_new_user(ts, USER_ID, client)
        self.assertTrue(len(recommendations) > 0)
        genres_set = set(genre for sublist in genres for genre in sublist.split("|"))
        self.assertTrue("Animation" in genres_set)

    def test_runtime_similarity_calculation(self):
        """Test runtime similarity calculation."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        recommendations, _, _ = recommend_for_new_user(ts, USER_ID, client)
        self.assertTrue(len(recommendations) > 0)

    def test_large_history_input(self):
        """Test with large history input."""
        ts = [{"title": f"Movie {i}", "rating": 10.0} for i in range(500)]
        recommendations, _, _ = recommend_for_new_user(ts, USER_ID, client)
        self.assertTrue(len(recommendations) <= 10)

    def test_genre_diversity_in_recommendations(self):
        """Test genre diversity in recommendations."""
        ts = [
            {"title": "Mortal Kombat (1995)", "rating": 8.0},
            {"title": "Les Miserables (1995)", "rating": 7.0},
            {"title": "Jurassic Park (1993)", "rating": 9.0},
        ]
        _, genres, _ = recommend_for_new_user(ts, USER_ID, client)
        unique_genres = set(g for genre in genres for g in genre.split("|"))
        self.assertTrue({"Action", "History", "Science Fiction"}.issubset(unique_genres))

if __name__ == "__main__":
    unittest.main()
