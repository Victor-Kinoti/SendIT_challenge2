from ..models.UserModels import Order, User
from flask_jwt_extended import create_access_token
from validate_email import validate_email
from flask_restful import Resource
from flask import make_response, jsonify, request, abort
from flask_jwt_extended import create_access_token
from email.utils import parseaddr


class DataParcel(Resource):
    """Utilizes data from an order by either getting all
    data or posting new data"""

    def post(self):
        """Create an order"""
        data = request.get_json()

        par = Order()
        par.create_order(data)

        payload = {
            "Status": "created",
            "Data": data

        }
        return payload, 201

    def get(self):
        """get all orders in the database"""
        par = Order()

        all_orders = par.get_all_orders()

        payload = {
            "Status": "Ok",
            "Data": all_orders
        }

        return payload, 200


class SingleParcel(Resource):
    """gets a single order"""

    def get(self, order_id):
        try:
            order_id = int(order_id)
        except Exception:
            return {"Message": "Provide a valid order id",
                    "Status": "bad request"}, 400

        par = Order()
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
        par = Order()

        all_orders = par.get_all(user_id)

        payload = {
            "Status": "Ok",
            "Data": all_orders
        }

        return payload, 200


class RegisterUser(Resource):
    """This class creates a new user"""

    def post(self):

        data = request.get_json() or {}

        user_1 = User()

        user_1.create_user(data)

        payload = {
            "Status": "User created",
            "data": data

        }
        return payload, 201


class UserLogin(Resource):

    def post(self):
        data = request.get_json() or {}

        user = User()

        login_user = user.login_user(data['email'], data['password'])

        my_id = [data['email']]

        token = create_access_token(identity=my_id)

        payload = {
            "Status": "User Logged in"
        }
