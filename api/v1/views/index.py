#!/usr/bin/python3
"""module named index"""
from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models import storage


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status", strict_slashes=False)
def status():
    """get data in json format"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def obj_counter():
    """retrieves the number of each objects by type"""
    my_dict = {}
    for k, v in my_classes.items():
        num_of_objs = storage.count(v)
        my_dict[k] = num_of_objs
    return jsonify(my_dict)
