import json
import os
from pathlib import Path

# Optional MongoDB import
try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

def load_json(filepath):
    """Load a JSON file and return its data."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_student_data(filepath_or_collection):
    """
    Load student data either from JSON file or MongoDB collection.
    """
    if os.getenv("USE_MONGO", "false").lower() == "true":
        return load_from_mongo(collection_name=filepath_or_collection)
    else:
        return load_json(filepath_or_collection)

def load_all_students(student_sources):
    """
    Load multiple students' data.
    If using Mongo, student_sources should be a collection name (str).
    If using files, student_sources should be a list of JSON file paths.
    Returns a list of (student_id, student_data) tuples.
    """
    if os.getenv("USE_MONGO", "false").lower() == "true":
        data = load_from_mongo(collection_name=student_sources)
        return [(doc.get("student_id", f"student_{i+1}"), doc) for i, doc in enumerate(data)]
    else:
        students = []
        for filepath in student_sources:
            data = load_json(filepath)
            # Try to get student_id from data if available
            student_id = None
            if isinstance(data, list) and len(data) > 0 and "student_id" in data[0]:
                student_id = data[0]["student_id"]
            if not student_id:
                student_id = Path(filepath).stem
            students.append((student_id, data))
        return students

def load_scoring_map(filepath_or_collection):
    """
    Load SAT scoring map for Math & Reading/Writing.
    """
    if os.getenv("USE_MONGO", "false").lower() == "true":
        data = load_from_mongo(collection_name=filepath_or_collection)
    else:
        data = load_json(filepath_or_collection)
    return {entry["key"]: entry["map"] for entry in data}

def load_from_mongo(collection_name):
    """
    Fetch all documents from a given MongoDB collection.
    Requires: pymongo, running MongoDB, USE_MONGO=true
    """
    if MongoClient is None:
        raise ImportError("pymongo is required for MongoDB loading. Install with `pip install pymongo`.")
    
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "sat_analysis")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    return list(collection.find({}, {"_id": 0}))
