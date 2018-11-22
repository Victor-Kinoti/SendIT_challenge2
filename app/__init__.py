from flask import Flask, Blueprint, make_response, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from .api.v1 import version1 as v1
from .api.v2 import version2 as v2
from db.create_tables import DatabaseConnection


def page_not_found(e):
    """Methods handles urls that don't exist"""
    return make_response(jsonify({
        'Status': 'Not Found',
        'Message': "URL doesn't exist"
    }), 404)


def create_app():
    """Intialize app"""
    app = Flask(__name__)
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = 'thisissecret'
    conn = DatabaseConnection()
    conn.create_tables()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    app.register_error_handler(404, page_not_found)
    return app
