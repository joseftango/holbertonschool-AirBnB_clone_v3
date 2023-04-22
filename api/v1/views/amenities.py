#!/usr/bin/python3
"""model named amenities"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False, methods=["GET", "POST"])
def get_amenities():
	"""retrive list of all Amenity objects"""
	if request.method == "GET":
		list_ams = []
		all_ams = storage.all(Amenity)
		for v in all_ams.values():
			list_ams.append(v.to_dict())
		return jsonify(list_ams)

	else:
		data_am = request.get_json()
		if not data_am:
			abort(400, "Not a JSON")
		if not data_am.get('name'):
			abort(400, "Missing name")
		new_am = Amenity()
		for k, v in data_am.items():
			setattr(new_am, k, v)
		new_am.save()
		return jsonify(new_am.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["GET", "DELETE"])
def get_amenity_by_id(amenity_id=None):
	"""retrive a specific Amenity object"""
	my_amenity = storage.get(Amenity, amenity_id)
	if not my_amenity:
		abort(404)
	if request.method == "GET":
		return jsonify(my_amenity.to_dict())

	storage.delete(my_amenity)
	storage.save()
	return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id=None):
	"""update Amenity object"""
	data_am = request.get_json()
	if not data_am:
		abort(404, "Not a JSON")
	my_amenity = storage.get(Amenity, amenity_id)
	if not my_amenity:
		abort(404)
	for k, v in data_am.items():
		if k in ["id", "created_at", "updated_at"]:
			continue
		setattr(my_amenity, k, v)
	storage.save()
	return jsonify(my_amenity.to_dict()), 200
