"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty

This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import unittest
import warnings

from backend.recommenderapp.client import client
from backend.recommenderapp.item_based import recommend_for_new_user

warnings.filterwarnings("ignore")


user = {1: None}
user[1] = "673e820d3f9e32b77366db00"  # Hardcoded user id for testing purposes
USER_ID = user[1]

db = client.PopcornPicksDB


class Tests(unittest.TestCase):
    """
    Test cases for recommender system
    """

    def test_empty_input(self):
        """Test with empty input."""
        ts = []
        recommendations, _, _, _ = recommend_for_new_user(ts, USER_ID, db)
        self.assertEqual(recommendations, [])

    def test_no_matching_movie(self):
        """Test with no matching movie."""
        ts = [{"title": "Unknown Movie (2025)", "rating": 10.0}]
        recommendations, _, _, _ = recommend_for_new_user(ts, USER_ID, db)
        self.assertEqual(recommendations, [])

    def test_duplicate_movies(self):
        """Test with duplicate movies."""
        ts = [
            {"title": "Toy Story (1995)", "rating": 10.0},
            {"title": "Toy Story (1995)", "rating": 10.0},
        ]
        recommendations, _, _, _ = recommend_for_new_user(ts, USER_ID, db)
        self.assertTrue(len(recommendations) > 0)

    def test_genre_similarity_calculation(self):
        """Test genre similarity calculation."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        recommendations, genres, _, _ = recommend_for_new_user(ts, USER_ID, db)
        self.assertTrue(len(recommendations) > 0)
        genres_set = set(genre for sublist in genres for genre in sublist.split("|"))
        self.assertTrue("Animation" in genres_set)

    def test_runtime_similarity_calculation(self):
        """Test runtime similarity calculation."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        recommendations, _, _, _ = recommend_for_new_user(ts, USER_ID, db)
        self.assertTrue(len(recommendations) > 0)

    def test_large_history_input(self):
        """Test with large history input."""
        ts = [{"title": f"Movie {i}", "rating": 10.0} for i in range(500)]
        recommendations, _, _, _ = recommend_for_new_user(ts, USER_ID, db)
        self.assertTrue(len(recommendations) <= 10)

    def test_genre_diversity_in_recommendations(self):
        """Test genre diversity in recommendations."""
        ts = [
            {"title": "Mortal Kombat (1995)", "rating": 8.0},
            {"title": "Les Miserables (1995)", "rating": 7.0},
            {"title": "Jurassic Park (1993)", "rating": 9.0},
        ]
        _, genres, _, _ = recommend_for_new_user(ts, USER_ID, db)
        unique_genres = set(g for genre in genres for g in genre.split("|"))
        self.assertTrue(
            {"Action", "History", "Science Fiction"}.issubset(unique_genres)
        )

    def test_rating_type_filtering_g(self):
        """Test rating type filtering for G."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "G")
        self.assertTrue(all([rating == "G" for rating in ratings]))

    def test_rating_type_filtering_pg(self):
        """Test rating type filtering for PG."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "PG")
        self.assertTrue(all([rating == "PG" for rating in ratings]))

    def test_rating_type_filtering_pg13(self):
        """Test rating type filtering for PG-13."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "PG-13")
        self.assertTrue(all([rating == "PG-13" for rating in ratings]))

    def test_rating_type_filtering_r(self):
        """Test rating type filtering for R."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "R")
        self.assertTrue(all([rating == "R" for rating in ratings]))

    def test_rating_type_filtering_nc17(self):
        """Test rating type filtering for NC-17."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "NC-17")
        self.assertTrue(all([rating == "NC-17" for rating in ratings]))

    def test_rating_type_filtering_tv_y(self):
        """Test rating type filtering for TV-Y."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "TV-Y")
        self.assertTrue(all([rating == "TV-Y" for rating in ratings]))

    def test_rating_type_filtering_tv_pg(self):
        """Test rating type filtering for TV-PG."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "TV-PG")
        self.assertTrue(all([rating == "TV-PG" for rating in ratings]))

    def test_rating_type_filtering_tv_14(self):
        """Test rating type filtering for TV-14."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "TV-14")
        self.assertTrue(all([rating == "TV-14" for rating in ratings]))

    def test_rating_type_filtering_tv_ma(self):
        """Test rating type filtering for TV-MA."""
        ts = [{"title": "Toy Story (1995)", "rating": 10.0}]
        _, _, _, ratings = recommend_for_new_user(ts, USER_ID, db, "TV-MA")
        self.assertTrue(all([rating == "TV-MA" for rating in ratings]))


if __name__ == "__main__":
    unittest.main()
