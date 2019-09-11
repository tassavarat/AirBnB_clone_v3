#!/usr/bin/python3
"""
states view module
"""

from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify

"""
li = []
dic = storage.all('State').values()
for i in dic:
    for k, v in i.to_dict().items():
        print(k, v)
        print("########")
        print(jsonify({k: v}))

print("#########################")
li = []
dic = storage.all('State').values()
for i in dic:
    js = i.to_dict()
    li.append(js)
print(li)
"""


@app_views.route("/states", methods=["GET"])
def status():
    """Returns a JSON string"""
    li = []
    dic = storage.all('State').values()
    for i in dic:
        js = i.to_dict()
        li.append(js)
    return li
