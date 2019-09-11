#!/usr/bin/python3
"""
states view module
"""

from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify


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
    '''Returns a State object based on: state_id'''
    d = storage.get("State", state_id)
    return jsonify(d.to_dict())
