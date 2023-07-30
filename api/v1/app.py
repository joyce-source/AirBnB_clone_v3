#!/usr/bin/python3
"""api Flask application"""
from flask import Flask, jsonify
from models import storage
from os import environ
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_DB(error):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 page, a Not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Main Function"""
    host: str = environ.get("HBNB_API_HOST", "0.0.0.0")
    port: int = int(environ.get("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True)
