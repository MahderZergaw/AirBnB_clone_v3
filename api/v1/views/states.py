#!/usr/bin/python3
"""State Objects module"""
from flask import Flask, jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**request.json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
