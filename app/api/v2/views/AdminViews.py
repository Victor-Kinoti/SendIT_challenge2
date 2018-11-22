from ..models.AdminModels import UserOrders
from flask_jwt_extended import create_access_token
from validate_email import validate_email
from flask_restful import Resource
from flask import make_response, jsonify, request, abort
from email.utils import parseaddr


class OrderParcels(Resource):
    """Utilizes data from an order by either getting all
    data or posting new data"""

    def get(self):
        """get all orders in the database"""
        par = UserOrders()

        all_orders = par.get_all_orders()

        payload = {
            "Status": "Ok",
            "Data": all_orders
        }

        return payload, 200
