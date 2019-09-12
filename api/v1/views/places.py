#!/usr/bin/python3
"""
places view module
"""

from models import storage
from models.place import Place
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """Returns all Place objects based on Place"""
    li = []
    d = storage.all("Places").values()
    if not storage.get("City", city_id):
        abort(404)
    for place in d:
        if place.to_dict()["city_id"] == city_id:
            li.append(place.to_dict())
    return jsonify(li), 200


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place_id(place_id):
    """Returns a Place object based on: place_id"""
    d = storage.get("Place", place_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place_id(place_id):
    """Deletes a Place object"""
    d = storage.get("Place", place_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates a Place object"""
    dic_t = request.get_json()
    if not storage.get("City", city_id):
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'user_id' not in dic_t:
        abort(400, {"Missing user_id"})
    if not storage.get("User", dic_t["user_id"]):
        abort(404)
    if 'name' not in dic_t:
        abort(400, {"Missing name"})
    dic_t["city_id"] = city_id
    new_place = Place(**dic_t)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_places(place_id):
    """Updates a Place object"""
    dic_t = request.get_json()
    d = storage.get("Place", place_id)
    if not d:
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    for k, v in dic_t.items():
        if k == 'name' or k == 'description' or \
                k == 'number _rooms' or k == 'number_bathrooms' or \
                k == 'max_guest' or k == 'price_by_night':
            setattr(d, k, v)
            storage.save()
    to_d = d.to_dict()
    return jsonify(to_d), 200
