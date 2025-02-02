#!/usr/bin/python3
"""api Flask application"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_DB_session(error):
    """close the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 page, a Not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Main Function"""
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000

    app.run(host=host, port=port, threaded=True, debug=False)
