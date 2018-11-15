from ..models.UserModels import Order, User_model
from validate_email import validate_email
from flask_restful import Resource
from flask import make_response, jsonify, request, abort
from email.utils import parseaddr

class DataParcel(Resource):
	"""Utilizes data from an order by either getting all 
	data or posting new data"""
	def post(self):
		"""Create an order"""
		data = request.get_json() or {}

		if 'destination_address' not in data or 'pickup_address'\
			not in data or data['destination_address'].isalpha()==False\
		 	or data['pickup_address'].isalpha()==False:
			abort(make_response(jsonify(message=\
			"ensure to provide the addresses in correct format"),400))
		


		if 'recipient_name' not in data or 'recipient_id' not in data\
		or data['recipient_name'].isalpha()==False:
			abort(make_response(jsonify(message=\
		"recipient_name or recipient_id missing or wrong data format"),400))

		if 'item_type' not in data or 'weight' not in data or\
		data['item_type'] != 'parcel' and data['item_type'] != 'envelope':
			abort(make_response(jsonify(message=\
			"item_type/weight missing or data type wrong format"),400))

		if len(data)==0:
			abort(make_response(jsonify(message="Fill in the fields"),400))

		par = Order()
		par.create_order(data)

		payload = {
			"Status":"created",
			
		}
		result= make_response(jsonify(payload), 201)
		result.content_type = 'application/json;charset=utf-8'
		return result	

	def get(self):
		"""gets all orders made"""
		par = Order()
		all_orders = par.get_all()
		
		result= make_response(jsonify({
			"Status":"Ok",
			"Orders": all_orders
		}),200)
		result.content_type = 'application/json;charset=utf-8'
		return result
		
class SingleParcel(Resource):
	"""gets a single order"""
	def get(self, order_id):

		try:
			order_id = int(order_id)
		except Exception:
			return make_response(jsonify({
				"Message":"Provide a valid order id",
				"Status": "bad request"
			}),400)
		par = Order()
		one_order = par.get_one_order(order_id)
		if one_order is not None:
			return make_response(jsonify(
				{
					"Status":"Ok",
					"Orders": one_order
				}))
		return make_response(jsonify({
                "Status": "Not Found"
		}),404)
		
		
class CancelOrder(Resource):
	def put(self, order_id):
		"""cancels an order that exists"""
		data = request.get_json()
		try:
			order_id = int(order_id)
		except Exception:
			return make_response(jsonify({
				"Message":"Provide a valid order id",
				"Status": "bad request"
			}),400)
		if order_id is not None:
			order_id = str(order_id)
			print(data['order_id'])
			if order_id == data['order_id']:
				order_1 = Order()
				order_1.cancel_order(order_id)
				return make_response(jsonify({'Status': \
				'order has been canceled'}),201)
			
		return make_response(jsonify({"Status": \
		"Order doesn't exist"}),400)

class RegisterUser(Resource):
	"""This class creates a new user"""
	def post(self):		
			
		data = request.get_json() or {}

		if 'username'not in data or 'email' not in data or\
					 'password' not in data\
		 or 'con_password' not in data or 'role' not in data:
			abort(make_response(jsonify(message=\
			"Some or all fields are missing"),400))

		if data['role'] != 'Admin' and data['role'] != 'User':
			abort(make_response(jsonify({"Message":\
			"Roles can be either Admin or User"}),400))

		if data['password'] != data['con_password']:
			abort(make_response(jsonify(message=\
			"Password and confirm password not matching"),400))

		if not validate_email(data['email']):
			abort(make_response(jsonify(message=\
			"wrong email format"),400))

			
		if len(data)==0:
			abort(make_response(jsonify(message=\
			"Fill in the fields"),400))
		
		user_1 = User_model()
		user_1.create_user(data)

		payload = {
			"Status":"User created",
			
		}
		result= make_response(jsonify(payload), 201)
		result.content_type = 'application/json;charset=utf-8'
		return result

class UserLogin(Resource):
	"""Logs in an existing user"""
	def post(self):
		data = request.get_json()
		if 'email' not in data:
			abort(make_response(jsonify(message=\
			"Email missing"),400))
		if 'password' not in data:
			abort(make_response(jsonify(message=\
			"Password missing"),400))
		if 'role' not in data:
			abort(make_response(jsonify(message=\
			"Please check a role"),400))
		if len(data)==0:
			abort(make_response(jsonify(message=\
			"Fill in the fields"),400))

		user_1 = User_model()
		user_1.login_user(
			data["email"],
			data["password"],
			data["role"]
			)

		payload = {
			"Status":"User Logged in",
			
		}
		result= make_response(jsonify(payload), 201)
		result.content_type = 'application/json;charset=utf-8'
		return result


