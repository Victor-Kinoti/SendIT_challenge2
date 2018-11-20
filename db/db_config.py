import psycopg2
from psycopg2 import Error
import os
db_url = os.getenv('DATABASE_URL')


def connect_to_db():
    try:
        return psycopg2.connect(db_url)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Could not connect with database", error)


def connection():
    conn = connect_to_db()
    return conn


def close_connection(conn):
    conn.commit()
    conn.close()
