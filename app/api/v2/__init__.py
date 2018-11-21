from flask import Blueprint
from flask_restful import Api, Resource
from .views.UserViews import DataParcel, SingleParcel, UsersOrders, RegisterUser, UserLogin

version2 = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(version2)

api.add_resource(DataParcel, '/parcels')
api.add_resource(SingleParcel, '/parcels/<order_id>')
api.add_resource(UsersOrders, '/parcels/<user_id>/orders')
api.add_resource(RegisterUser, '/register')
api.add_resource(UserLogin, '/login')
