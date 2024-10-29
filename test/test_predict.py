"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import sys
import unittest
import warnings
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
# pylint: disable=wrong-import-position
from src.recommenderapp.item_based import recommend_for_new_user

# pylint: enable=wrong-import-position
warnings.filterwarnings("ignore")

from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://svrao3:popcorn1234@popcorn.xujnm.mongodb.net/?retryWrites=true&w=majority&appName=PopCorn"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

user = {1: None}
user[1] = "671b289a193d2a9361ebf39a"  # Hardcoded user id for testing purposes
user_id = user[1]


class Tests(unittest.TestCase):
    """
    Test cases for recommender system
    """

    def test_empty_input(self):
        ts = []
        recommendations, _, _ = recommend_for_new_user(ts, user_id, client)
        self.assertEqual(recommendations, [])

    def test_no_matching_movie(self):
        ts = [{"title": "Unknown Movie (2025)", "rating": 10.0}]
        recommendations, _, _ = recommend_for_new_user(ts, user_id, client)
        self.assertEqual(recommendations, [])

    def test_duplicate_movies(self):
        ts = [
            {"title": "Toy Story (1995)", "rating": 10.0},
            {"title": "Toy Story (1995)", "rating": 10.0},
        ]
        recommendations, _, _ = recommend_for_new_user(ts, user_id, client)
        self.assertTrue(len(recommendations) > 0)

    def test_genre_similarity_calculation(self):
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        recommendations, genres, _ = recommend_for_new_user(ts, user_id, client)
        self.assertTrue(len(recommendations) > 0)
        genres_set = set(genre for sublist in genres for genre in sublist.split("|"))
        self.assertTrue("Animation" in genres_set)

    def test_runtime_similarity_calculation(self):
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        recommendations, _, _ = recommend_for_new_user(ts, user_id, client)
        self.assertTrue(len(recommendations) > 0)

    def test_large_history_input(self):
        ts = [{"title": f"Movie {i}", "rating": 10.0} for i in range(500)]
        recommendations, _, _ = recommend_for_new_user(ts, user_id, client)
        self.assertTrue(len(recommendations) <= 10)

    def test_genre_diversity_in_recommendations(self):
        ts = [
            {"title": "Mortal Kombat (1995)", "rating": 8.0},
            {"title": "Les Miserables (1995)", "rating": 7.0},
            {"title": "Jurassic Park (1993)", "rating": 9.0},
        ]
        _, genres, _ = recommend_for_new_user(ts, user_id, client)
        unique_genres = set(g for genre in genres for g in genre.split("|"))
        self.assertTrue(
            {"Action", "History", "Science Fiction"}.issubset(unique_genres)
        )


if __name__ == "__main__":
    unittest.main()
