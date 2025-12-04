from flask import current_app
from pymongo import MongoClient, errors


def get_mongo_client():
    """
    Create and return a MongoClient.
    MongoDB must be available. If not, the app raises an error immediately.
    """
    uri = current_app.config["MONGO_URI"]

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        # Test connection
        client.admin.command("ping")
        return client
    except errors.PyMongoError as e:
        # Hard fail: MongoDB MUST be running
        current_app.logger.error(f"Cannot connect to MongoDB at {uri}: {e}")
        raise RuntimeError("MongoDB is required but not available.") from e


def get_patients_collection():
    """
    Return the MongoDB 'patients' collection.
    """
    client = get_mongo_client()
    db = client.get_default_database()
    return db["patients"]
