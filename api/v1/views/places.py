#!/usr/bin/python3
"""A view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    all_places = city.places
    list_places = [place.to_dict() for place in all_places]
    return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object associated with a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("city_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    for key, value in data.items():
        setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def search_places():
    """Retrieves all Place objects based on the JSON in the request body."""

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    states_ids = data.get('states', [])
    cities_ids = data.get('cities', [])
    amenities_ids = data.get('amenities', [])

    if not states_ids and not cities_ids and not amenities_ids:
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)

    list_places = []
    if states_ids:
        states = [storage.get(State, state_id) for state_id in states_ids]
        for state in states:
            if state:
                for city in state.cities:
                    if city and city.id not in cities_ids:
                        cities_ids.append(city.id)

    if cities_ids:
        cities = [storage.get(City, city_id) for city_id in cities_ids]
        for city in cities:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities_ids:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities = [
            storage.get(Amenity, amenity_id) for amenity_id in amenities_ids
        ]
        list_places = [
            place for place in list_places
            if all([amenity in place.amenities for amenity in amenities])
        ]

    places = []
    for place in list_places:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        places.append(place_dict)

    return jsonify(places)
