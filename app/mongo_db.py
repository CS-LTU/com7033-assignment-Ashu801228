from flask import current_app
from pymongo import MongoClient

_client = None
_patients_collection = None


def get_mongo_client():
    
    #create and cache a MongoClient using the Flask app config.

    global _client
    if _client is None:
        uri = current_app.config["MONGO_URI"]
        _client = MongoClient(uri)
    return _client


def get_patients_collection():

    #Return the MongoDB 'patients' collection.

    #Database name is taken from the URI (e.g. stroke_app),
    #collection name is fixed as 'patients'.
    
    global _patients_collection
    if _patients_collection is None:
        client = get_mongo_client()
        db = client.get_default_database()
        _patients_collection = db["patients"]
    return _patients_collection
