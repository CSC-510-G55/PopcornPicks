"""
Test cases for MongoDB connection.
"""

# pylint: skip-file
import os
import unittest
import logging
from dotenv import load_dotenv
from src.recommenderapp.client import client

logging.basicConfig(level=logging.DEBUG)
load_dotenv()


class TestDB(unittest.TestCase):
    """Test cases for MongoDB connection."""

    @classmethod
    def setUpClass(cls):
        """Set up MongoDB connection URI."""
        cls.original_mongo_uri = os.getenv("MONGO_URI")

    def test_negative_mongo_connection(self):
        """Test negative case for MongoDB connection."""
        invalid_mongo_uri = (
            "mongodb://invalid_user:invalid_pass@invalid_host:27017/test"
        )
        os.environ["MONGO_URI"] = invalid_mongo_uri

        with self.assertRaises(Exception) as context:
            from src.recommenderapp.client import client

        self.assertIn("bad database name", str(context.exception).lower())

        os.environ["MONGO_URI"] = self.original_mongo_uri


if __name__ == "__main__":
    unittest.main()
