"""
Copyright (c) 2024 Srimadh Vasuki Rao, Manav Shah, Akul Devali
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import os
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

print(f"Connecting to MongoDB at {mongo_uri}", flush=True)

client = MongoClient(mongo_uri)

client.admin.command("ping")
print("Pinged your deployment. You successfully connected to MongoDB!", flush=True)
