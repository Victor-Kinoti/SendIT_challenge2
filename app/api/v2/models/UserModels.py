import uuid
from psycopg2.extras import RealDictCursor
from db.db_config import connection, close_connection
from werkzeug.security import generate_password_hash, check_password_hash


class Order(object):
    """Model that creates an order"""

    def create_order(self, data):
        print(data)
        destination_address = data['destination_address']
        pickup_address = data['pickup_address']
        recipient_name = data['recipient_name']
        recipient_id = data['recipient_id']
        item_type = data['item_type']
        weight = data['weight']
        user_id = data['user_id']
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
