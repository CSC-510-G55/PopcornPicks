import os
import unittest
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_mongo_uri = os.getenv("MONGO_URI")

    def test_negative_mongo_connection(self):
        WRONG_MONGO_URI = "mongodb://invalid_user:invalid_pass@invalid_host:27017/test"
        os.environ["MONGO_URI"] = WRONG_MONGO_URI

        try:
            from src.recommenderapp.client import client
        except Exception as mongo_e:
            self.assertIn("bad database name", str(mongo_e).lower())

        os.environ["MONGO_URI"] = self.original_mongo_uri
        from src.recommenderapp.client import client

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
