from flask import Blueprint
from flask_restful import Api, Resource
from .views.UserViews import DataParcel, SingleUsersParcels,  RegisterUser, UserLogin, SingleUsersParcel
from .views.AdminViews import OrderParcels, SingleOrder, UsersOrders, UpdateOrder, Update_location, Update_destination

version2 = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(version2)

api.add_resource(DataParcel, '/parcels')
api.add_resource(SingleUsersParcels, '/parcels/<int:user_id>')
api.add_resource(SingleUsersParcel, '/parcels/<int:user_id>/<int:order_id>')
api.add_resource(UsersOrders, '/parcels/<int:user_id>/orders')
api.add_resource(RegisterUser, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(OrderParcels, '/orders')
api.add_resource(SingleOrder, '/orders/<int:order_id>')
api.add_resource(UpdateOrder, '/parcel/<int:order_id>/orders')
api.add_resource(Update_location, '/parcels/<int:order_id>/presentLocation')
api.add_resource(Update_destination, '/parcels/<int:order_id>/destination')
