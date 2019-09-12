#!/usr/bin/python3
"""
City view module
"""

from models import storage
from models.city import City
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_city(state_id):
    """Returns all City objects based on State"""
    li = []
    d = storage.all("City").values()
    if not storage.get("State", state_id):
        abort(404)
    for city in d:
        if city.to_dict()["state_id"] == state_id:
            li.append(city.to_dict())
    return jsonify(li), 200


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city_id(city_id):
    """Returns a City object based on: city_id"""
    d = storage.get("City", city_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city_id(city_id):
    """Deletes a City object"""
    d = storage.get("City", city_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Creates a City object"""
    dic_t = request.get_json()
    dic_t["state_id"] = state_id
    if not storage.get("State", state_id):
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'name' not in dic_t:
        abort(400, {"Missing name"})
    new_city = City(**dic_t)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_cities(city_id):
    """Updates a City object"""
    dic_t = request.get_json()
    d = storage.get("City", city_id)
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
