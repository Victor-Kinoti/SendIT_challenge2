import uuid
from psycopg2.extras import RealDictCursor
from flask_jwt_extended import create_access_token, jwt_required
from db.db_config import connection, close_connection
from werkzeug.security import generate_password_hash, check_password_hash


class Order(object):
    """Creates an order"""

    # @jwt_required
    def create_order(self, data):
        print(data)
        destination_address = data['destination_address']
        pickup_address = data['pickup_address']
        recipient_name = data['recipient_name']
        recipient_id = data['recipient_id']
        item_type = data['item_type']
        weight = data['weight']
        user_id = data['user_id']
        current_location = data['current_location']
        order_status = data['order_status']
        payment_status = data['payment_status']

        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO orders_table(destination_address, pickup_address,
            recipient_name, recipient_id, item_type, weight, user_id, order_status, payment_status)
            VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(destination_address, pickup_address,
                                                                                    recipient_name, recipient_id, item_type, weight, user_id,
                                                                                    order_status, payment_status,))

            conn.commit()

    # @jwt_required
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

    # @jwt_required
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
            cursor.execute("""INSERT INTO users_tables(email, username,
            password, role)
            VALUES('{}', '{}', '{}', '{}');""".format(email, username, password, role))

            conn.commit()

    def login_user(self, email, password):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users_tables WHERE email = '%s'""" % email)
            res = cursor.fetchone()
        return res

    def get_user(self, email):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users_tables WHERE email = '%s'""" % email)
            res = cursor.fetchone()
        return res

    def get_pass(self, email):
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users_tables WHERE email = '%s'""" % email)

            passw = cursor.fetchone()

        return passw['password']
