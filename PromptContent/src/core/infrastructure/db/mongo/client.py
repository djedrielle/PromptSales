import os
from pymongo import MongoClient

_client = None

def _client_instance():
    global _client
    if _client is None:
        uri = os.environ.get("MONGODB_URI")
        if not uri:
            raise RuntimeError("MONGODB_URI not set")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return _client

def get_collection():
    db = os.environ.get("MONGODB_DB", "promptsales")
    col = os.environ.get("MONGODB_BRIEFS_COLLECTION", "briefs")
    return _client_instance()[db][col]
