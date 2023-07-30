#!/usr/bin/python3
"""A view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrive all Amenity objects"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrive all Amenity objects by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a State object by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete(amenity)
    amenity.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    for key, value in data.items():
        setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
