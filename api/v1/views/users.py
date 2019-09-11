#!/usr/bin/python3
"""
users view module
"""

from models import storage
from models.user import User
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/users", methods=["GET"])
def get_users():
    """Returns a JSON string"""
    li = []
    dic_t = storage.all('User').values()
    for i in dic_t:
        js = i.to_dict()
        li.append(js)
    return jsonify(li), 200


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user_id(user_id):
    """Returns a User object based on: state_id"""
    d = storage.get("User", user_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user_id(user_id):
    """Deletes a State object"""
    d = storage.get("User", user_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"])
def create_user():
    """Creates a User object"""
    dic_t = request.get_json()
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'email' not in dic_t:
        abort(400, {"Missing email"})
    if 'password' not in dic_t:
        abort(400, {"Missing password"})
    print(dic_t)
    new_user = User(**dic_t)
    storage.new(new_user)
    storage.save()
    d = new_user.to_dict()
    return jsonify(d), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a User object"""
    dic_t = request.get_json()
    d = storage.get("User", user_id)
    if not d:
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    if 'email' in dic_t and 'password' in dic_t:
        for k, v in dic_t.items():
            setattr(d, k, v)
        storage.save()
    to_d = d.to_dict()
    return jsonify(to_d), 200
