import uuid
from .UserModels import Order
from db.db_config import connection, close_connection
from flask import make_response, jsonify


class UserOrders(object):

    def get_all_orders(self):

        conn = connection()
        with conn as cursor:
            cursor.execute("SELECT * FROM orders_table")
            orders = cursor.fetchall()

            orders_list = []
            for order in orders:
                orders_item = {
                    "order_id": order[0],
                    "destination_addr": order[1],
                    "pickup_addr": order[2],
                    "recipient_name": order[3],
                    "recipient_id": order[4],
                    "item_type": order[5],
                    "weight": order[6],
                    "order_status": [7],
                    "payment_status": [8]
                }
                orders_list.append(orders_item)

            return make_response(jsonify({
                "Message": "Success",
                "orders": orders_list
            }), 200)



    def get_one_user_order(self, user_id):
        """gets a specific order"""
        conn = connection()
        with conn as cursor:
            cursor.execute("SELECT * FROM orders_table WHERE user_id = %s", (user_id,))
            order_found = cursor.fetchone()

            return order_found

    def update_order_status(self, order_id):
        """update order status"""
        conn = connection()
        with conn as cursor:
            cursor.execute("""UPDATE orders_table SET order_status = %s
             WHERE order_id=%s RETURNING True""", ('Delivered', order_id))

    def update_order_payment(self, order_id):
        """update order payment"""
        conn = connection()
        with conn as cursor:
            cursor.execute("""UPDATE orders_table SET payment_status = %s
             WHERE order_id=%s RETURNING True""", ('Paid', order_id))
