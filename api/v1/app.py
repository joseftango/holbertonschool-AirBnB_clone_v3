#!/usr/bin/python3
"""module named app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True)
