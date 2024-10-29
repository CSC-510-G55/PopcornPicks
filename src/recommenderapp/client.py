from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

MONGO_URI = "mongodb+srv://svrao3:popcorn1234@popcorn.xujnm.mongodb.net"
MONGO_OPTIONS = "/?retryWrites=true&w=majority&appName=PopCorn"
MONGO_URI += MONGO_OPTIONS

client = MongoClient(MONGO_URI)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except (ConnectionFailure, ServerSelectionTimeoutError) as mongo_e:
    print(f"Could not connect to MongoDB: {mongo_e}")
