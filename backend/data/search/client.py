# data/search/client.py

import os
from functools import lru_cache

from pymongo import MongoClient
from pymongo.server_api import ServerApi

@lru_cache()
def get_mongo_client() -> MongoClient:
    """
    Returns a cached MongoClient instance.
    """
    uri = os.getenv("MONGO_URI")
    return MongoClient(uri, server_api=ServerApi('1'))
