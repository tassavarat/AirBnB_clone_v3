#!/usr/bin/python3
"""
Amenities view module
"""

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """Returns a JSON string"""
    li = []
    dic_t = storage.all('Amenity').values()
    for i in dic_t:
        js = i.to_dict()
        li.append(js)
    return jsonify(li), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_id(amenity_id):
    """Returns a Amenity object based on: amenity_id"""
    d = storage.get("Amenity", amenity_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity_id(amenity_id):
    """Deletes a Amenity object"""
    d = storage.get("Amenity", amenity_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def create_amenities():
    """Creates an Amenity object"""
    dic_t = request.get_json()
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'name' not in dic_t:
        abort(400, {"Missing name"})
    new_amenity = Amenity(**dic_t)
    storage.new(new_amenity)
    storage.save()
    d = new_amenity.to_dict()
    return jsonify(d), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenities(amenity_id):
    """Updates a Amenity object"""
    dic_t = request.get_json()
    d = storage.get("Amenity", amenity_id)
    if not d:
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'name' in dic_t:
        for k, v in dic_t.items():
            setattr(d, k, v)
        storage.save()
    to_d = d.to_dict()
    return jsonify(to_d), 200
