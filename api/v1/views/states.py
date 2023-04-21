#!/usr/bin/python3
"""module named states"""
from models.state import State
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "POST"])
def get_states(state_id=None):
    """retrive list of all State objects"""
    state_objs = storage.all(State)
    if request.method == "GET":
        if state_id is None:
            my_states = []
            for v in state_objs.values():
                v = v.to_dict()
                my_states.append(v)
            return jsonify(my_states)
        else:
            for v in state_objs.values():
                if v.id == state_id:
                    return jsonify(v.to_dict())
            abort(404)

    if request.method == "DELETE":
        removed = storage.get(State, state_id)
        if removed:
            storage.delete(removed)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_obj():
    """method that add a new instance"""
    state_dict = request.get_json()
    if state_dict is None:
        abort(400, "Not a JSON")
    if state_dict.get('name') is None:
        abort(400, "Missing name")
    my_obj = State()
    my_obj.name = state_dict['name']
    storage.new(my_obj)
    storage.save()
    return jsonify(my_obj.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_obj(state_id=None):
    """method that modify an exiting
    object matching with state_id"""
    data_dict = request.get_json()
    if data_dict is None:
        abort(400, {"Not a JSON"})
    wanted_state = storage.get(State, state_id)
    if wanted_state:
        for k, v in data_dict.items():
            if k == 'id' or k == 'update_at' or k == 'updated_at':
                continue
            setattr(wanted_state, k, v)
        storage.save()
        return jsonify(wanted_state.to_dict()), 200
    else:
        abort(400)
