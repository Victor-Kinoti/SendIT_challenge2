import uuid
from .UserModels import Order
from db.db_config import connection, close_connection
from flask_jwt_extended import create_access_token, jwt_required


class UserOrders():

    def get_all_orders(self):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM orders_table;""")
            order = cursor.fetchall()
        return order

    def get_one_order(self, order_id):
        # for admins
        """Gets a specific order with order_id as arguments
        param:order_id
        :return:"""
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM orders_table WHERE order_id = %s""" % order_id)
            order = cursor.fetchone()
        return order

    def get_all(self, user_id):
        """Get all orders of specific user
        """
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM orders_table WHERE user_id = %s""" % user_id)
            order = cursor.fetchall()
        return order

    def update_order_status(self, order_id, order_status):
        conn = connection()
        try:
            conn = connection()
            cur = conn.cursor()
            cur.execute("""UPDATE orders_table SET order_status= '{}' WHERE order_id= {} """ .format(
                order_status, order_id))
            conn.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_location(self, order_id, current_location):
        conn = connection()
        try:
            conn = connection()
            cur = conn.cursor()
            cur.execute("""UPDATE orders_table SET current_location= '{}' WHERE order_id= {} """ .format(
                current_location, order_id))
            conn.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def Update_order_destination(self, order_id, destination_address):
        conn = connection()
        try:
            conn = connection()
            cur = conn.cursor()
            cur.execute("""UPDATE orders_table SET destination_address= '{}' WHERE order_id= {} """ .format(
                destination_address, order_id))
            conn.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
