#!/usr/bin/python3
"""
states view module
"""

from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request


@app_views.route("/states", methods=["GET"])
def get_states():
    """Returns a JSON string"""
    li = []
    dic_t = storage.all('State').values()
    for i in dic_t:
        js = i.to_dict()
        li.append(js)
    return jsonify(li)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state_id(state_id):
    """Returns a State object based on: state_id"""
    d = storage.get("State", state_id)
    if d:
        return jsonify(d.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state_id(state_id):
    """Deletes a State object"""
    d = storage.get("State", state_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({})
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/states", methods=["POST"])
def create_states():
    """Creates a State object"""
    print("####")
    obj = request.get_json()
    print("output type is", type(request.get_json))
    print(obj.get("name"))
    print("####")
