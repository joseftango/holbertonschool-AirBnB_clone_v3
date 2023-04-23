#!/usr/bin/python3
"""model named reviews"""
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET", "POST"])
def get_reviews(place_id=None):
    """Retrieves the list of all
    Review objects of a Place"""
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    if request.method == "GET":
        li_places = []
        my_reviews = storage.all(Review)
        for rev in my_reviews.values():
            if rev.place_id == place_id:
                li_places.append(rev.to_dict())
        return jsonify(li_places)

    data_reviews = request.get_json()
    if not data_reviews:
        abort(400, "Not a JSON")
    user_id = data_reviews.get("user_id")
    if not user_id:
        abort(404, "Missing user_id")
    if not data_reviews.get("text"):
        abort(400, "Missing text")
    my_user = storage.get(User, user_id)
    if not my_user:
        abort(404)
    new_rev = Review()
    setattr(new_rev, 'place_id', place_id)
    for k, v in data_reviews.items():
        setattr(new_rev, k, v)
    new_rev.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def get_review_by_id(review_id):
    """retrive the specific review
    match with review_id"""
    my_review = storage.get(Review, review_id)
    if not my_review:
        abort(404)
    if request.method == "GET":
        return jsonify(my_review.to_dict())
    storage.delete(my_review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """Updates a Review object mentioned by it id"""
    my_rev = storage.get(Review, review_id)
    if not my_rev:
        abort(404)
    data_review = request.get_json()
    if not data_review:
        abort(400, "Not a JSON")
    for k, v in data_review.items():
        if k in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(my_rev, k, v)
    storage.save()
    return jsonify(my_rev.to_dict()), 200
