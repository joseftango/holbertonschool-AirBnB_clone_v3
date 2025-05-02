#!/usr/bin/python3
''' main file of our api application '''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def not_found(execption):
    """close the storage instance"""
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        Host = getenv('HBNB_API_HOST')
    else:
        Host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        Port = getenv('HBNB_API_PORT')
    else:
        Port = 5000

    app.run(host=Host, port=Port, threaded=True) 
