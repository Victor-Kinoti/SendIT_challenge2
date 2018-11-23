from ..models.AdminModels import UserOrders
from ..models.UserModels import Order
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity, get_raw_jwt, jwt_required)
from validate_email import validate_email
from flask_restful import Resource
from flask import make_response, jsonify, request, abort
from email.utils import parseaddr


class OrderParcels(Resource):
    """Utilizes data from an order by either getting all
    data or posting new data"""
    @jwt_required
    def get(self):
        user = get_jwt_identity()
        if user[1] != "Admin":
            return "Not Authorized!"
        """get all orders in the database"""
        par = UserOrders()

        all_orders = par.get_all_orders()

        payload = {
            "Status": "Ok",
            "Data": all_orders
        }

        return payload, 200


class SingleOrder(Resource):
    """gets a single order with id"""

    def get(self, order_id):
        user = get_jwt_identity()
        if user[1] != "Admin":
            return "Not Authorized!"
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
        user = get_jwt_identity()
        if user[1] != "Admin":
            return "Not Authorized!"
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


class UpdateOrder(Resource):

    def put(self, order_id):

        user = get_jwt_identity()
        if user[1] != "Admin":
            return "Not Authorized!"
        data = request.get_json()

        order_stat = data['order_status']

        try:
            order_id = int(order_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        order = Order()
        order.get_one_order(order_id)

        if order is None:
            return {"Status": "Order doesn't exist"}

        par = UserOrders()
        update_order = par.update_order_status(order_id, order_stat)
        if update_order:

            return {"Status": "Delivered"
                    }, 200

        return {
            "Status": "Not Found"
        }, 404


class Update_location(Resource):

    def put(self, order_id):

        user = get_jwt_identity()
        if user[1] != "Admin":
            return "Not Authorized!"
        data = request.get_json()

        current_loc = data["current_location"]
        try:
            order_id = int(order_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        par = UserOrders()

        update_loc = par.update_location(order_id, current_loc)
        if update_loc:

            return {"Status": "location updated"
                    }, 200

        return {
            "Status": "Order Not found"
        }, 404


class Update_destination(Resource):

    def put(self, order_id):

        user = get_jwt_identity()
        if user[1] != "User":
            return "Not Authorized!"

        data = request.get_json()
        dest_adrr = data["destination_address"]
        try:
            order_id = int(order_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        par = UserOrders()

        update_des = par.Update_order_destination(order_id, dest_adrr)
        if update_des:

            return {"Status": "destination updated"
                    }, 200

        return {
            "Status": "Order Not found"
        }, 404
