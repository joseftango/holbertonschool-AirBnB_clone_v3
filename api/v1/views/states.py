#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    '''retrives states'''
    if request.method == 'GET':
        states = []
        for v in storage.all(State).values():
            states.append(v.to_dict())
        return jsonify(states)


@app_views.route('/states/', methods=['POST'])
def post_states():
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'message': 'Missing name'}), 400
    d = request.get_json()
    new_state = State(**d)
    new_state.save()
    return jsonify(new_state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def one_state(state_id):
    '''retrive a state based from state_id argument'''
    my_state = storage.get(State, state_id)
    if not my_state:
        abort(404)
    if request.method == 'GET':
        return jsonify(my_state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(my_state)
        storage.save()
        return jsonify({}), 200
    else:
        if not request.get_json():
            return jsonify({'message': 'Not a JSON'}), 400

        data = request.get_json()
        my_state = storage.get(State, state_id)

        if my_state:
            for k, v in data.items():
                if k in ['id', 'created_at', 'updated_at']:
                    continue
                else:
                    setattr(my_state, k, v)
            storage.save()
            return jsonify(my_state.to_dict()), 200
        else:
            abort(404)
