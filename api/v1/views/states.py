#!/usr/bin/python3
"""
states view module
"""

from models import storage
from models.state import State
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/states", methods=["GET"])
def get_states():
    """Returns a JSON string"""
    li = []
    dic_t = storage.all('State').values()
    for i in dic_t:
        js = i.to_dict()
        li.append(js)
    return jsonify(li), 200


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state_id(state_id):
    """Returns a State object based on: state_id"""
    d = storage.get("State", state_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state_id(state_id):
    """Deletes a State object"""
    d = storage.get("State", state_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"])
def create_states():
    """Creates a State object"""
    dic_t = request.get_json()
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'name' not in dic_t:
        abort(400, {"Missing name"})
    new_state = State(**dic_t)
    storage.new(new_state)
    storage.save()
    d = new_state.to_dict()
    return jsonify(d), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_states(state_id):
    """Updates a State object"""
    dic_t = request.get_json()
    d = storage.get("State", state_id)
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
