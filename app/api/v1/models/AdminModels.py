import uuid
from .UserModels import Order
class UserOrders(object):

    def get_all_orders(self):
        return Order.orders

    def get_one_user_order(self, order_id):
        for item in Order.orders:
            if item["order_id"] == order_id:
                return item


    def update_order_status(self, order_id):
        for item in Order.orders:
            if item["order_id"] == order_id:
                item['order_status'] = 'Delivered'
                return True
    
    def update_order_payment(self, order_id):
        for item in Order.orders:
           
            if item["order_id"] == order_id:
                item["payment_status"] = 'Paid'
            return True
