#!/usr/bin/python3
"""objects that handles all default RESTFul API actions"""

from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object:"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in request.json:
        abort(400, 'Missing name')
    place_data = request.json
    place_data['city_id'] = city_id
    new_place = Place(**place_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object:"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
