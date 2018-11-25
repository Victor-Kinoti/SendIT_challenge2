from ..models.UserModels import Order, User
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity, get_raw_jwt, jwt_required)
from validate_email import validate_email
from flask_restful import Resource
from flask import make_response, jsonify, request, abort
from flask_jwt_extended import create_access_token
from email.utils import parseaddr


class DataParcel(Resource):
    """Utilizes data from an order by either getting all
    data or posting new data"""

    @jwt_required
    def post(self):
        """Create an order"""
        user = get_jwt_identity()

        if user[1]['role'] != "User":
            return {"Status": "Not Authorized!"}, 401

        parcel = User()
        user_i = parcel.get_userid(user[0])

        user_identity = user_i['user_id']

        data = request.get_json()
        if len(data) == 0:
            abort(make_response(jsonify(message="Fill in the fields"), 400))

        if 'destination_address' not in data or 'pickup_address'\
                not in data or data['destination_address'].isalpha() == False\
                or data['pickup_address'].isalpha() == False:
            return{"Status": "Ensure to provide the addresses in correct format"}

        if 'recipient_name' not in data or 'recipient_id' not in data\
                or data['recipient_name'].isalpha() == False:
            return {"Status": "Provide correct recipient data"}

        if 'current_location' not in data or data['current_location'].isalpha() == False:
            return {"Status": "Provide the current location in correct format"}

        parcels = Order()
        parcels.create_order(data, user_identity)

        payload = {
            "Status": "created"

        }
        return payload, 201

    @jwt_required
    def get(self):

        user = get_jwt_identity()
        if user[1]['role'] != "Admin":
            return {"Status": "Not Authorized!"}, 401

        """get all orders in the database"""
        par = Order()

        all_orders = par.get_all_orders()

        payload = {
            "Status": "Ok",
            "Data": all_orders
        }

        return payload, 200


class SingleUsersParcels(Resource):
    """gets a single order"""

    @jwt_required
    def get(self, user_id):
        user = get_jwt_identity()
        if user[1]['role'] != "User":
            return {"Status": "Not Authorized!"}, 401

        try:
            user_id = int(user_id)
        except Exception:
            return {"Status": "Provide a valid user id"}, 400

        par = Order()

        identity = User()
        verify = identity.get_userid(user[0])

        if verify['user_id'] != user_id:
            return {"Status": "Not Authorized"}, 401

        all_orders = par.get_one_users_order(user_id)
        if all_orders is not None:
            return {
                "Status": "Your Order History",
                "Orders": all_orders
            }, 200
        return {
            "Status": "Not Found"
        }, 404


class SingleUsersParcel(Resource):

    @jwt_required
    def get(self, user_id, order_id):
        user = get_jwt_identity()

        if user[1]['role'] != "User":
            return {"Status": "Not Authorized!"}, 401

        try:
            user_id = int(user_id)
        except Exception:
            return {"Message": "Provide a valid user id",
                    "Status": "bad request"}, 400

        par = Order()

        identity = User()
        verify = identity.get_userid(user[0])

        if verify['user_id'] != user_id:
            return {"Status": "Not Authorized"}, 401

        one_order = par.get_one_order_user(user_id, order_id)
        if one_order is not None:
            return {
                "Status": "Your Order",
                "Orders": one_order
            }, 200
        return {
            "Status": "Not Found"
        }, 404


class RegisterUser(Resource):
    """This class creates a new user"""

    def post(self):

        data = request.get_json() or {}
        print(data)

        if 'email' not in data or validate_email(data['email']) == False:
            return {"Status": "Email fields missing/ wrong email format"}, 400

        print(data)
        user_1 = User()
        user_found = user_1.get_user(data['email'])
        if user_found:
            return {"Status": "User with that email already exists"}, 400

        if len(data) == 0:
            abort(make_response(jsonify(message="Fill in the fields"), 400))

        if 'username'not in data or data['username'].isalpha() == False:
            return {"Status": "username fields missing or in wrong format"}, 400

        if 'password' not in data or 'con_password' not in data:
            return{"Status": "password/con-password fields missing"}, 400

        if 'email' not in data or validate_email(data['email']) == False:
            return {"Status": "Email fields missing"}, 400

        if 'role' not in data:
            return {"Status": "Please check a role"}, 400

        if data['role'] != 'Admin' and data['role'] != 'User':
            return{"Status": "Roles can be either Admin or User"}, 400

        if data['password'] != data['con_password']:
            return {"Status": "Password and confirm password not matching"}, 400

        if not validate_email(data['email']):
            return {"Status": "wrong email format"}, 400

        user_1.create_user(data)

        payload = {
            "Status": "User " + data['username'] + " created"

        }
        return payload, 201


class UserLogin(Resource):

    def post(self):
        data = request.get_json() or {}

        if validate_email(str(data['email'])) is False:
            return {"Status": "Wrong email format!"}, 400

        user = User()
        user_found = user.get_user(data['email'])
        if user_found:

            email = data['email']
            password = data['password']

            auth = user.login_user(email, password)

            if auth:
                pass_match = user.get_pass(data['email'])
                role = user.get_user_role(data['email'])
                if pass_match['password'] == str(password):
                    access_token = create_access_token(identity=[email, role])

                    payload = {
                        "Status": "User Logged in",
                        "token": access_token

                    }

                    return payload, 200
                return {"Status": "Email/password wrong"}, 400
        return {
            "Status": "Email/password wrong"
        }, 404
