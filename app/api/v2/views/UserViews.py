from ..models.UserModels import Order, User
from validate_email import validate_email
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
        print(data['email'])

        if validate_email(str(data['email'])) is False:
            return {"Status": "Wrong email format!"}

        found = User()
        user_found = found.get_user(data['email'])
        if user_found:

            user = User()
            email = data['email']
            password = data['password']

            auth = user.login_user(email, password)

            if auth:
                passw = User()
                pass_match = passw.get_pass(data['email'])

                if pass_match:
                    access_token = create_access_token(identity=email)

                    payload = {
                        "Status": "User Logged in",
                        "token": access_token

                    }

                    return payload, 200
                return {"password mismatch"}, 400
        return {
            "Status": "User doesn't exist"
        }, 404
