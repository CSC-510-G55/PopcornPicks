"""
Copyright (c) 2024 Srimadh Vasuki Rao, Manav Shah, Akul Devali
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import os
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_OPTIONS = "/?retryWrites=true&w=majority&appName=PopCorn"
MONGO_URI += MONGO_OPTIONS

client = MongoClient(MONGO_URI)

client.admin.command("ping")
print("Pinged your deployment. You successfully connected to MongoDB!", flush=True)
