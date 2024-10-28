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
from src.prediction_scripts.item_based import recommend_for_new_user

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
        recommendations, _, _ = recommend_for_new_user(ts,user_id,client)
        self.assertEqual(recommendations, [])

if __name__ == "__main__":
    unittest.main()
