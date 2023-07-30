#!/usr/bin/python3
"""Index"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """An endpoint that returns a status JSON response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """An endpoint that retrieves the number of each objects by type"""
    stats_data = {
        'Amenity': storage.count('Amenity'),
        'Place': storage.count('Place'),
        'Review': storage.count('Review'),
        'State': storage.count('State'),
        'City': storage.count('City'),
        'User': storage.count('User')
    }

    return jsonify(stats_data)
