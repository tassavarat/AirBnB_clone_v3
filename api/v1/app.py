#!/usr/bin/python3
"""
The app module
"""

from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """calls storage.close() method"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"),
            threaded=True)
