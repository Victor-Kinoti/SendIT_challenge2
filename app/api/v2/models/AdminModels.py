import uuid
from .UserModels import Order
from db.db_config import connection, close_connection
from flask_jwt_extended import create_access_token, jwt_required


class UserOrders(object):

    @jwt_required
    def get_all_orders(self):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM orders_table;""")
            order = cursor.fetchall()
        return order

    @jwt_required
    def get_one_order(self, order_id):
        """Gets a specific order with order_id as arguments
        param:order_id
        :return:"""
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM orders_table WHERE order_id = %s""" % order_id)
            order = cursor.fetchone()
        return order

    @jwt_required
    def get_all(self, user_id):
        """Get all orders of specific user
        """
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM orders_table WHERE user_id = %s""" % user_id)
            order = cursor.fetchall()
        return order

    @jwt_required
    def update_order_status(self, order_id):
        conn = connection()
        try:
            conn = connection()
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute("""UPDATE orders_table SET order_status= '{}' WHERE order_id= {} """ .format(
                'Delivered', order_id))
            conn.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @jwt_required
    def update_location(self, order_id):
        conn = connection()
        try:
            conn = connection()
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute("""UPDATE orders_table SET current_location= '{}' WHERE order_id= {} """ .format(
                'Nairobi', order_id))
            conn.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @jwt_required
    def Update_order_destination(self, order_id):
        conn = connection()
        try:
            conn = connection()
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute("""UPDATE orders_table SET destination_address= '{}' WHERE order_id= {} """ .format(
                'Meru', order_id))
            conn.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
