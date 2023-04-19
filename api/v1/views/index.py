#!/usr/bin/python3
"""module named index"""
from api.v1.views import app_views
from flask import jsonify
from models import city, state, place, user, amenity, review, storage


my_classes= {'cities': city.City, 'states': state.State, 
            'places': place.Place, 'users': user.User,
            'amenities': amenity.Amenity, 'reviews': review.Review
            }


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
