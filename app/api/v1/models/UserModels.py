import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class Order(object):
	"""Model that creates an order"""
	orders = []
	def create_order(self, data):
		self.destination_addr = data['destination_address']
		self.pickup_addr = data['pickup_address']
		self.recipient_name = data['recipient_name']
		self.recipient_id = data['recipient_id']
		self.item_type = data['item_type']
		self.weight = data['weight']
		self.name = data['name']

		payload  ={
		"order_id": uuid.uuid4().int >> 64,
		"destination_address":self.destination_addr,
		"pickup_address":self.pickup_addr,
		"recipient_name":self.recipient_name,
		"recipient_id":self.recipient_id,
		"item_type":self.item_type,
		"weight":self.weight,
		"order_status":"In transit",
		"payment_status":"Not Paid",
		"name":self.name
		}
		print(type(payload['order_id']))

		Order.orders.append(payload)
		return True
	def get_all(self):
		"""Get all orders
		return: """
		return Order.orders

	def get_one_order(self,order_id):
		"""Gets a specific order with order_id as arguments
		param:order_id
		:return:"""
		
		for item in Order.orders:
			if item["order_id"] == order_id:
				return item

	def get_one_user_orders(self, name):
		"""Model to get all orders of a certain user"""
		for order in Order.orders:
			if order['name'] == name:
				return order
			return "No such order"

	def cancel_order(self, order_id):
		"""Model to cancel an order that exists"""
		for order in Order.orders:
			if order["order_id"] == order_id:
				order['order_status'] = 'canceled'
				return True

	def get_user_orders(self, name):
		"""Model to get all orders of a certain user"""
		orders = [order for order in Order.orders
                   if order['name'] == name]
		return orders	

class User_model(object):
	fields = []
	def create_user(self, data):
		"""Model to create new user"""
		self.email = data['email']
		self.username = data['username'] 
		self.password = data['password']
		self.con_password = data['con_password']
		self.role = data['role']


		payload={
			"user_id": str(uuid.uuid4().int),
			"email":self.email,
			"username":self.username,
			"password":self.password,
			"con_password":self.con_password,
			"role":self.role
		}
		User_model.fields.append(payload)
		return True

	def login_user(self, email, password, role):
		"""Model that allow registered user to login"""
		self.email = email
		self.password = password,
		self.role = role

		payload={
			"user_id":str(uuid.uuid4().int),
			"email":self.email,
			"password":self.password,
			"role":self.role
		}
		User_model.fields.append(payload)
		return True

	
	