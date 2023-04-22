#!/usr/bin/python3
"""model named places"""
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=["GET", "POST"])
def get_places(city_id=None):
    """retrive list of all places objects
    linked with a specific City instance"""
    my_city = storage.get(City, city_id)
    if not my_city:
        abort(404)
    if request.method == "GET":
        li_places = []
        my_places = storage.all(Place)
        for v in my_places.values():
            if v.city_id == city_id:
                li_places.append(v.to_dict())
        return jsonify(li_places)

    data_place = request.get_json()
    if not data_place:
        abort(400, "Not a JSON")
    user_id = data_place.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")
    if not data_place.get('name'):
        abort(400, "Missing name")
    my_user = storage.get(User, user_id)
    if not my_user:
        abort(404)
    new_place = Place()
    for k, v in data_place.items():
        setattr(new_place, k, v)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_place_by_id(place_id=None):
    """retrive a Place object matching with id"""
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    if request.method == "GET":
        return jsonify(my_place.to_dict())
    if request.method == "DELETE":
        storage.delete(my_place)
        storage.save()
        return jsonify({}), 200

    data_place = request.get_json()
    if not data_place:
        abort(404, "Not a JSON")
    for k, v in data_place.items():
        if k in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(my_place, k, v)
    storage.save()
    return jsonify(my_place.to_dict()), 200
