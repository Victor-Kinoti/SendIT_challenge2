import uuid
from .UserModels import Order
from db.db_config import connection, close_connection


class UserOrders(object):

    def get_all_orders(self):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM orders_table;""")
            order = cursor.fetchall()
        return order
