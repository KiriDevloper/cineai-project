from flask import Blueprint, request, jsonify, session
from models.review_model import save_review, get_reviews_by_movie
from ai.predict import predict_sentiment
from models.review_model import reviews_collection
from bson import ObjectId

review_bp = Blueprint("review", __name__)

# ── GET /reviews?movie_id=X ──
@review_bp.route("/reviews", methods=["GET"])
def reviews():
    movie_id = request.args.get("movie_id", type=int)
    data = get_reviews_by_movie(movie_id) if movie_id is not None else []
    return jsonify(data)

# ── DELETE /delete-review/<id> ──
@review_bp.route("/delete-review/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    review = reviews_collection.find_one({"_id": ObjectId(review_id)})

    if not review:
        return jsonify({"error": "Review not found"}), 404

    if review["username"] != session["user"]:
        return jsonify({"error": "Forbidden"}), 403

    reviews_collection.delete_one({"_id": ObjectId(review_id)})
    return jsonify({"message": "Deleted"})

# ── POST /predict ──
@review_bp.route("/predict", methods=["POST"])
def predict():
    body     = request.get_json()
    text     = body.get("review", "")
    movie_id = body.get("movie_id", 0)        # ← thêm
    username = session.get("user", "Anonymous")

    sentiment, score = predict_sentiment(text)
    print(f"DEBUG movie_id nhận được: {movie_id}")  # ← thêm dòng này
    save_review(username, text, sentiment, score, movie_id)  # ← thêm movie_id

    return jsonify({
        "sentiment": sentiment,
        "score":     score
    })