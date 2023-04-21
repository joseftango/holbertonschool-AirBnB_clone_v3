#!/usr/bin/python3
"""module named cities"""
from models.state import State
from models.city import City
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET", "POST"])
def get_cities(state_id=None):
    """function that list all cities
    matched with state_id"""
    if request.method == "GET":
        my_state = storage.get(State, state_id)
        if not my_state:
            abort(404)
        else:
            my_citites = []
            for my_city in my_state.cities:
                my_citites.append(my_city.to_dict())
            return jsonify(my_citites)
    else:
        data_dict = request.get_json()
        if not data_dict:
            abort(400, {"Not a JSON"})
        if not data_dict.get('name'):
            abort(400, {"Missing name"})
        if not storage.get(State, state_id):
            abort(404)
        new_city = City()
        for k, v in data_dict.items():
            setattr(new_city, k, v)
        setattr(new_city, "state_id", state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_city_by_id(city_id=None):
    """retrive the city object
    that match with city_id"""
    my_city = storage.get(City, city_id)
    if not my_city:
        abort(404)
    if request.method == "GET":
        return jsonify(my_city.to_dict())
    if request.method == "DELETE":
        storage.delete(my_city)
        storage.save()
        return jsonify({}), 200
    else:
        data_dict = request.get_json()
        if not data_dict:
            abort(400, "Not a JSON")
        for k, v in data_dict.items():
            if k in ["id", "state_id", "created_at", "updated_at"]:
                continue
            setattr(my_city, k, v)
        storage.save()
        return jsonify(my_city.to_dict()), 200
