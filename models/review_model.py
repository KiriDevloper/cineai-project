from database.mongodb import db
from datetime import datetime

reviews_collection = db["reviews"]

def save_review(username, review, sentiment, score, movie_id=0):  # ← thêm movie_id
    doc = {
        "username":   username,
        "review":     review,
        "sentiment":  sentiment,
        "score":      score,
        "movie_id":   movie_id,                                    # ← thêm
        "created_at": datetime.utcnow().isoformat()
    }
    result = reviews_collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

def get_all_reviews():
    reviews = list(
        reviews_collection
        .find({})
        .sort("created_at", -1)
    )
    for review in reviews:
        review["_id"] = str(review["_id"])
    return reviews

def get_reviews_by_movie(movie_id):                                # ← hàm mới
    reviews = list(
        reviews_collection
        .find({"movie_id": movie_id})
        .sort("created_at", -1)
    )
    for review in reviews:
        review["_id"] = str(review["_id"])
    return reviews