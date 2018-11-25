import uuid
from psycopg2.extras import RealDictCursor
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity, get_raw_jwt, jwt_required)
from db.db_config import connection, close_connection
from werkzeug.security import generate_password_hash, check_password_hash


class Order(object):
    """Creates an order"""

    def create_order(self, data, user_identity):

        destination_address = data['destination_address']
        pickup_address = data['pickup_address']
        recipient_name = data['recipient_name']
        recipient_id = int(data['recipient_id'])
        weight = data['weight']
        user_id = user_identity
        current_location = data['current_location']
        order_status = "In-Transit"
        payment_status = "Not Paid"

        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO orders_table(destination_address, pickup_address,
            recipient_name, recipient_id, weight, user_id, order_status, payment_status)
            VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(destination_address, pickup_address,
                                                                              recipient_name, recipient_id, weight, user_id,
                                                                              order_status, payment_status))

            conn.commit()

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

    def get_one_users_order(self, user_id):

        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM orders_table WHERE user_id = %s""" % user_id)
            order = cursor.fetchall()
        return order

    def get_one_order_user(self, user_id, order_id):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM orders_table WHERE user_id = %s AND order_id = %s""" % (user_id, order_id))
            order = cursor.fetchone()
        return order

    def get_all_orders(self):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM orders_table;""")
            order = cursor.fetchall()
        return order


class User(object):

    def create_user(self, data):
        """Model to create new user"""
        email = data['email']
        username = data['username']
        password = data['password']
        con_password = data['con_password']
        role = data['role']

        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO users_table(email, username,
            password, role)
            VALUES('{}', '{}', '{}', '{}');""".format(email, username, password, role))

            conn.commit()

    def login_user(self, email, password):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users_table WHERE email = '%s'""" % email)
            res = cursor.fetchone()
        return res

    def get_user(self, email):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users_table WHERE email = '%s'""" % email)
            res = cursor.fetchone()
        return res

    def get_user_role(self, email):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT role FROM users_table WHERE email = '%s'""" % email)
            res = cursor.fetchone()
        return res

    def get_pass(self, email):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT password FROM users_table WHERE email = '%s'""" % email)

            passw = cursor.fetchone()

        return passw

    def get_userid(self, email):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT user_id FROM users_table WHERE email = '%s'""" % email)

            userid = cursor.fetchone()

        return userid
