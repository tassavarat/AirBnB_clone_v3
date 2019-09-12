#!/usr/bin/python3
"""
reviews view module
"""

from models import storage
from models.review import Review
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/reviews", methods=["GET"])
def get_reviews():
    """Returns a JSON string"""
    li = []
    dic_t = storage.all('Review').values()
    for i in dic_t:
        js = i.to_dict()
        li.append(js)
    return jsonify(li), 200


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews_by_places(place_id):
    """Returns all Review objects based on Place"""
    li = []
    if not storage.get("Place", place_id):
        abort(404)
    for rev in storage.all("Review").values():
        if rev.to_dict()["place_id"] == place_id:
            li.append(rev.to_dict())
    return jsonify(li), 200


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review_id(review_id):
    """Returns a Review object based on: review_id"""
    d = storage.get("Review", review_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review_id(review_id):
    """Deletes a Review object"""
    d = storage.get("Review", review_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Creates a Review object"""
    dic_t = request.get_json()
    if not storage.get("Place", place_id):
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'user_id' not in dic_t:
        abort(400, {"Missing user_id"})
    if not storage.get("User", dic_t["user_id"]):
        abort(404)
    if 'text' not in dic_t:
        abort(400, {"Missing text"})
    dic_t["place_id"] = place_id
    new_rev = Review(**dic_t)
    storage.new(new_rev)
    storage.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_reviews(review_id):
    """Updates a Review object"""
    dic_t = request.get_json()
    d = storage.get("Review", review_id)
    if not d:
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    for k, v in dic_t.items():
        if k == 'text':
            setattr(d, k, v)
            storage.save()
    to_d = d.to_dict()
    return jsonify(to_d), 200
