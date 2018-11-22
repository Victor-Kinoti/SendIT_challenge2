from flask import Blueprint
from flask_restful import Api, Resource
from .views.UserViews import DataParcel, SingleParcel,  RegisterUser, UserLogin
from .views.AdminViews import OrderParcels, SingleOrder, UsersOrders, UpdateOrder, Update_location, Update_destination

version2 = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(version2)

api.add_resource(DataParcel, '/parcels')
api.add_resource(SingleParcel, '/parcels/<order_id>')
api.add_resource(UsersOrders, '/parcels/<user_id>/orders')
api.add_resource(RegisterUser, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(OrderParcels, '/orders')
api.add_resource(SingleOrder, '/orders/<order_id>')
api.add_resource(UpdateOrder, '/parcels/orders/<order_id>')
api.add_resource(Update_location, '/parcels/<order_id>/location')
api.add_resource(Update_destination, '/parcels/<order_id>/destination')
