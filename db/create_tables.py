import psycopg2
from psycopg2 import Error
import os
db_url = os.getenv('DATABASE_URL')


class DatabaseConnection:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(db_url)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Could not connect with database", error)

    def create_tables(self):
        create_table_orders = """CREATE TABLE IF NOT EXISTS orders_table (
            order_id serial PRIMARY KEY,
            destination_addr  VARCHAR (256) NOT NULL,
            pickup_addr  VARCHAR (256) NOT NULL,
            recipient_name  VARCHAR (256) NOT NULL,
            recipient_id  INT NOT NULL,
            item_type VARCHAR (256) NOT NULL DEFAULT 'parcel',
            weight INT NOT NULL,
            order_status VARCHAR (50) NOT NULL DEFAULT 'In-Transit',
            payment_status VARCHAR (50) NOT NULL DEFAULT 'Not paid')
            """
        create_table_users = """ CREATE TABLE IF NOT EXISTS users_tables(
            user_id serial PRIMARY KEY,
            username VARCHAR(250) NOT NULL,
            email VARCHAR(96) UNIQUE,
            password VARCHAR(48) NOT NULL,
            con_password VARCHAR(48) NOT NULL,
            role VARCHAR(48) NOT NULL DEFAULT 'Admin')
            """

        self.cursor.execute(create_table_orders)
        self.cursor.execute(create_table_users)

if __name__ == '__main__':
    database_connection = DatabaseConnection()
    database_connection.create_tables()
