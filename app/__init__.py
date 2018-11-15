from flask import Flask, Blueprint, make_response, jsonify
from .api.v1 import version1 as v1

def page_not_found(e):
    """Methods handles urls that don't exist"""
    return make_response(jsonify({
        'Status':'Not found',
        'Message':"URL doesn't exist"
    }),404)


def create_app():
    """Intialize app"""
    app = Flask(__name__)
    app.register_blueprint(v1)
    app.register_error_handler(404, page_not_found)
    return app