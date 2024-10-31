import unittest
import warnings
from src.recommenderapp.client import client
from bson import ObjectId
from datetime import datetime

warnings.filterwarnings("ignore")


class TestMongoDB(unittest.TestCase):
    """
    Unit tests for MongoDB operations related to users, movies, and ratings.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test database and create necessary indexes for the collections.
        This method is called once before all tests are run.
        """
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
        """
        Reset the state of the database before each test by clearing out the users, movies, and ratings collections.
        Also, populate the movies collection with sample data.
        """
        self.db.users.delete_many({})
        self.db.movies.delete_many({})
        self.db.ratings.delete_many({})
        self.db.movies.insert_many(self.sample_movies)

    def test_user_creation(self):
        """
        Test user creation in the database. Ensure that a user can be created and that duplicate usernames are not allowed.
        """
        user = {
            "username": "svrao",
            "email": "svrao@ncsu.edu",
            "password": "Binary.createFromBase64('hash_here')",
            "friends": [],
            "created_at": datetime.now(),
        }
        result = self.db.users.insert_one(user)
        self.assertTrue(result.inserted_id)

        # Test for duplicate username insertion (should raise an exception)
        duplicate_user = user.copy()
        duplicate_user["email"] = "different@ncsu.edu"
        with self.assertRaises(Exception):
            self.db.users.insert_one(duplicate_user)

    def test_movie_rating(self):
        """
        Test that a user can rate a movie and that the rating is correctly saved in the database.
        """
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

        # Verify that the rating was saved correctly
        saved_rating = self.db.ratings.find_one({"_id": rating_id})
        self.assertEqual(saved_rating["score"], 5)

    def test_friend_relationship(self):
        """
        Test that users can add each other as friends and that the relationship is correctly stored in the database.
        """
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

        # Add friend relationships between users
        self.db.users.update_one({"_id": user1}, {"$push": {"friends": "Hey"}})
        self.db.users.update_one({"_id": user2}, {"$push": {"friends": "Hey"}})

        # Verify that the friend relationship was added correctly
        updated_user = self.db.users.find_one({"_id": user1})
        self.assertIn("Hey", updated_user["friends"])

    def test_get_user_movies(self):
        """
        Test that a user's rated movies can be retrieved from the database along with their ratings.
        """
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

        # Insert a rating for the movie by the user
        self.db.ratings.insert_one(
            {
                "user_id": user_id,
                "movie_id": movie["_id"],
                "score": 5,
                "created_at": datetime.now(),
            }
        )

        # Retrieve all ratings by this user
        user_ratings = list(self.db.ratings.find({"user_id": user_id}))

        # Verify that the correct number of ratings and score are returned
        self.assertEqual(len(user_ratings), 1)
        self.assertEqual(user_ratings[0]["score"], 5)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests have run by deleting all documents from users, movies, and ratings collections.
        Drop the entire test database to ensure no leftover data.
        """
        cls.db.users.delete_many({})
        cls.db.movies.delete_many({})
        cls.db.ratings.delete_many({})
        client.drop_database("testDB")


if __name__ == "__main__":
    unittest.main()
