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


class SingleOrder(Resource):

    def get(self, order_id):
        try:
            order_id = int(order_id)
        except Exception:
            return {"Message": "Provide a valid order id",
                    "Status": "bad request"}, 400

        par = UserOrders()
        one_order = par.get_one_order(order_id)
        if one_order is not None:
            return make_response(jsonify(
                {
                    "Status": "Ok",
                    "Orders": one_order
                }))
        return make_response(jsonify({
            "Status": "Not Found"
        }), 404)


class UsersOrders(Resource):

    def get(self, user_id):
        """gets all orders for certain user"""
        try:
            user_id = int(user_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        par = UserOrders()

        all_orders = par.get_all(user_id)
        if all_orders:

            return {"Status": "Ok",
                    "Orders": all_orders
                    }, 200

        return {
            "Status": "Not Found"
        }, 404
