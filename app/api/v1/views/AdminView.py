from ..models.AdminModels import UserOrders
from ..models.UserModels import Order
from flask_restful import Resource
from flask import make_response, jsonify, request, abort


class Admin_all_Orders(Resource):
	def get(self):
		"""gets all orders made"""
		order_1 = UserOrders()
		all_orders = order_1.get_all_orders()
		

		payload = {
			"Status":"Ok",
			"Orders": all_orders
		}
		result= make_response(jsonify(payload),200)
		result.content_type = 'application/json;charset=utf-8'
		return result

class Admin_user_all_Order(Resource):
	"""Gets all orders of a certain user
	param name
	return:jsonified response of the order
	"""	
	def get(self, name):
		try:
			name = str(name)
		except Exception:
			return make_response(jsonify({
					"Message": "provide users name string format",
					"Status":"Bad request"
				}),400)
		par = Order()
		user_orders = par.get_user_orders(name)
		if len(user_orders)>0:
			payload = {
				"Status": "OK",
				"orders": user_orders
			}

			result = make_response(jsonify(payload),200)
			result.content_type = 'application/json;charset=utf-8'
			return result
		return make_response(jsonify({
			'Message':"Resource not available!",
			'Status': 'Not Found'
		}),400)

class admin_update_order_status(Resource):
	"""updates an status of an order"""
	def put(self, user_id):
		try:
			user_id = str(user_id)
		except Exception:
			return make_response(jsonify({
				'Status':'Bad request'
			}),400)
		order_1 = UserOrders()
		order_1.update_order_status(user_id)
		if order_1:
			return make_response(jsonify({'message':\
			 'order has been delivered!'}),200)
		return make_response(jsonify({
			'Status':'Not Found'
		}))

class admin_update_payment_status(Resource):
	"""updates payment status of an order"""
	def put(self, user_id):
		try:
			user_id = str(user_id)
		except Exception:
			return make_response(jsonify({
				'Status':'Bad request'
			}),400)
		order_1 = UserOrders()
		order_1.update_order_payment(user_id)
		if order_1:
			return make_response(jsonify({"message": "order paid!"}),200)
		return make_response(jsonify({
			'Status':'Not Found'
		}),400)