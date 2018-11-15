from flask import Blueprint
from flask_restful import Api, Resource
from .views.UserViews import DataParcel, SingleParcel, CancelOrder, RegisterUser, UserLogin
from .views.AdminView import Admin_all_Orders, Admin_user_all_Order, admin_update_order_status, admin_update_payment_status
version1 = Blueprint('v1', __name__,  url_prefix = '/api/v1')

api = Api(version1)

api.add_resource(DataParcel, '/parcels')
api.add_resource(SingleParcel, '/parcels/<order_id>')
api.add_resource(CancelOrder, '/parcels/<order_id>/cancel')
api.add_resource(RegisterUser, "/register")
api.add_resource(UserLogin, '/login')
api.add_resource(Admin_all_Orders, '/users/parcels')
api.add_resource(Admin_user_all_Order, '/users/<name>/parcels')
api.add_resource(admin_update_order_status, '/users/delivered/<user_id>')
api.add_resource(admin_update_payment_status, '/users/paid/<user_id>')
