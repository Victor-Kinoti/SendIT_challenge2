from ..models.UserModels import Order
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
        result = make_response(jsonify(payload), 201)
        result.content_type = 'application/json;charset=utf-8'
        return result

    def get(self):
        data = request.get_json() or {}
        """gets all orders made"""
        par = Order()

        all_orders = par.get_all()

        result = make_response(jsonify({
            "Status": "Ok",
            "Orders": all_orders
        }), 200)
        result.content_type = 'application/json;charset=utf-8'
        return result


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


class CancelOrder(Resource):

    def put(self, order_id):
        """cancels an order that exists"""
        data = request.get_json()
        try:
            order_id = int(order_id)
        except Exception:
            return make_response(jsonify({
                "Message": "Provide a valid order id",
                "Status": "bad request"
            }), 400)
        # if order_id is not None:
        par = Order(data)
        par.cancel_order(order_id)


class RegisterUser(Resource):
    """This class creates a new user"""

    def post(self):

        data = request.get_json() or {}

        if 'username'not in data or 'email' not in data or\
                'password' not in data\
                or 'con_password' not in data or 'role' not in data:
            abort(make_response(jsonify(message="Some or all fields are missing"), 400))

        if data['role'] != 'Admin' and data['role'] != 'User':
            abort(make_response(jsonify({"Message":
                                         "Roles can be either Admin or User"}), 400))

        if data['password'] != data['con_password']:
            abort(make_response(
                jsonify(message="Password and confirm password not matching"), 400))

        if not validate_email(data['email']):
            abort(make_response(jsonify(message="wrong email format"), 400))

        if len(data) == 0:
            abort(make_response(jsonify(message="Fill in the fields"), 400))

        user_1 = User(data)

        user_1.create_user(data)

        payload = {
            "Status": "Use created",
            "data": data

        }
        result = make_response(jsonify(payload), 201)
        result.content_type = 'application/json;charset=utf-8'
        return result


class UserLogin(Resource):
    """Logs in an existing user"""

    def post(self):
        data = request.get_json()
        if 'email' not in data:
            abort(make_response(jsonify(message="Email missing"), 400))
        if 'password' not in data:
            abort(make_response(jsonify(message="Password missing"), 400))
        if 'role' not in data:
            abort(make_response(jsonify(message="Please check a role"), 400))
        if len(data) == 0:
            abort(make_response(jsonify(message="Fill in the fields"), 400))

        user_1 = User(data)
        user_1.get_user(data['email'])
        if not user_1:
            return make_response(jsonify({"message": "User doesn't exists"}), 404)

        access_token = create_access_token(identity=data['email'])

        payload = {
            "Status": "User Logged in",
            "token": access_token

        }

        result = make_response(jsonify(payload), 201)
        result.content_type = 'application/json;charset=utf-8'
        return result
