from ..models.AdminModels import UserOrders
from ..models.UserModels import Order
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity, get_raw_jwt, jwt_required)
from validate_email import validate_email
from flask_restful import Resource
from flask import make_response, jsonify, request, abort
from email.utils import parseaddr


class OrderParcels(Resource):
    """Utilizes data from an order by getting all
    data"""
    @jwt_required
    def get(self):
        """get all orders in the database"""
        user = get_jwt_identity()
        if user[1]['role'] != "Admin":
            return "Not Authorized!"
        par = UserOrders()

        all_orders = par.get_all_orders()

        payload = {
            "Status": "Ok",
            "Data": all_orders
        }

        return payload, 200


class SingleOrder(Resource):
    """gets a single order with id"""
    @jwt_required
    def get(self, order_id):
        user = get_jwt_identity()
        print(user)
        if user[1]['role'] != "Admin":
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
                    "Status": "Order found",
                    "Orders": one_order
                }))
        return make_response(jsonify({
            "Status": "Not Found"
        }), 404)


class UsersOrders(Resource):

    @jwt_required
    def get(self, user_id):
        """gets all orders for certain user"""
        user = get_jwt_identity()
        print(user)
        if user[1]['role'] != "Admin":
            return "Not Authorized!"
        try:
            user_id = int(user_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        par = UserOrders()

        all_orders = par.get_all(user_id)
        if all_orders:

            return {"Status": "Found user " + str(user_id) + " orders",
                    "Orders": all_orders
                    }, 200

        return {
            "Status": "Not Found"
        }, 404


class UpdateOrder(Resource):

    @jwt_required
    def put(self, order_id):

        user = get_jwt_identity()
        if user[1]['role'] != "Admin":
            return "Not Authorized!"
        data = request.get_json()

        if data["order_status"] != 'Delivered' and data['order_status'] != 'Canceled'\
                and data['order_status'] != 'In-Transit':
            return {"Status": "Status can be 'Canceled', 'Delivered' or 'In-Transit'"}, 400

        order_stat = data['order_status']

        try:
            order_id = int(order_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        order = Order()
        order.get_one_order(order_id)

        if order is None:
            return {"Status": "Order doesn't exist"}, 404

        par = UserOrders()
        update_order = par.update_order_status(order_id, order_stat)
        if update_order:

            return {"Status": "Order " + order_stat
                    }, 200

        return {
            "Status": "Not Found"
        }, 404


class Update_location(Resource):

    @jwt_required
    def put(self, order_id):

        user = get_jwt_identity()
        if user[1]['role'] != "Admin":
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
        print(update_loc)
        if update_loc:

            return {"Status": "Current Location is " + data['current_location']
                    }, 200

        return {
            "Status": "Order Not found"
        }, 404


class Update_destination(Resource):

    @jwt_required
    def put(self, order_id):

        user = get_jwt_identity()
        if user[1]['role'] != "User":
            return {"Status": "Not Authorized!"}

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

            return {"Status": "Destination updated to " + data["destination_address"]
                    }, 200

        return {
            "Status": "Order Not found"
        }, 404
