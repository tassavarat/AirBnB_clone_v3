#!/usr/bin/python3
"""
states view module
"""

from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response


'''
d = storage.get("State", "421a55f4-7d82-47d9-b54c-a76916479546")
print("d is ", d)
if d:
    storage.delete(d)
    storage.save()
    print("empty dic")
else:
    print("Not found")
'''


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
    """Deletes a state object"""
    d = storage.get("State", state_id)
    if d:
        storage.delete(d)
        storage.save()
        return jsonify({})
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
