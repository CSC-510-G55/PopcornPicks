import unittest
import warnings
from src.recommenderapp.client import client
from bson import ObjectId
from datetime import datetime

warnings.filterwarnings("ignore")


class TestMongoDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = client.testDB
        cls.db.users.create_index("username", unique=True)
        cls.db.users.create_index("email", unique=True)
        cls.db.movies.create_index("imdb_id", unique=True)

        cls.sample_movies = [
            {"name": "Toy Story", "imdb_id": "tt0114709", "year": 1995},
            {"name": "Interstellar", "imdb_id": "tt0816692", "year": 2014},
            {"name": "The Avengers", "imdb_id": "tt0848228", "year": 2012},
            {"name": "Les Misérables", "imdb_id": "tt1193683", "year": 1998},
        ]

    def setUp(self):
        self.db.users.delete_many({})
        self.db.movies.delete_many({})
        self.db.ratings.delete_many({})
        self.db.movies.insert_many(self.sample_movies)

    def test_user_creation(self):
        user = {
            "username": "svrao",
            "email": "svrao@ncsu.edu",
            "password": "Binary.createFromBase64('hash_here')",
            "friends": [],
            "created_at": datetime.now(),
        }
        result = self.db.users.insert_one(user)
        self.assertTrue(result.inserted_id)
        duplicate_user = user.copy()
        duplicate_user["email"] = "different@ncsu.edu"
        with self.assertRaises(Exception):
            self.db.users.insert_one(duplicate_user)

    def test_movie_rating(self):
        user = {
            "username": "svrao",
            "email": "svrao@ncsu.edu",
            "password": "Binary.createFromBase64('hash_here')",
            "friends": [],
            "created_at": datetime.now(),
        }
        user_id = self.db.users.insert_one(user).inserted_id
        movie = self.db.movies.find_one({"imdb_id": "tt0114709"})

        rating = {
            "user_id": user_id,
            "movie_id": movie["_id"],
            "score": 5,
            "created_at": datetime.now(),
        }
        rating_id = self.db.ratings.insert_one(rating).inserted_id
        saved_rating = self.db.ratings.find_one({"_id": rating_id})
        self.assertEqual(saved_rating["score"], 5)

    def test_friend_relationship(self):
        user1 = self.db.users.insert_one(
            {
                "username": "root",
                "email": "svrao@ncsu.edu",
                "password": "Binary.createFromBase64('hash_here')",
                "friends": [],
                "created_at": datetime.now(),
            }
        ).inserted_id

        user2 = self.db.users.insert_one(
            {
                "username": "Hey",
                "email": "hey@ncsu.edu",
                "password": "Binary.createFromBase64('hash_here')",
                "friends": [],
                "created_at": datetime.now(),
            }
        ).inserted_id

        self.db.users.update_one({"_id": user1}, {"$push": {"friends": "Hey"}})
        self.db.users.update_one({"_id": user2}, {"$push": {"friends": "Hey"}})

        updated_user = self.db.users.find_one({"_id": user1})
        self.assertIn("Hey", updated_user["friends"])

    def test_get_user_movies(self):
        user_id = self.db.users.insert_one(
            {
                "username": "svrao",
                "email": "svrao@ncsu.edu",
                "password": "Binary.createFromBase64('hash_here')",
                "friends": [],
                "created_at": datetime.now(),
            }
        ).inserted_id

        movie = self.db.movies.find_one({"imdb_id": "tt0114709"})
        self.db.ratings.insert_one(
            {
                "user_id": user_id,
                "movie_id": movie["_id"],
                "score": 5,
                "created_at": datetime.now(),
            }
        )

        user_ratings = list(self.db.ratings.find({"user_id": user_id}))
        self.assertEqual(len(user_ratings), 1)
        self.assertEqual(user_ratings[0]["score"], 5)

    @classmethod
    def tearDownClass(cls):
        cls.db.users.delete_many({})
        cls.db.movies.delete_many({})
        cls.db.ratings.delete_many({})
        client.drop_database("testDB")


if __name__ == "__main__":
    unittest.main()
