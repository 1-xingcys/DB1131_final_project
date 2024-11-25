from flask import jsonify, request, Blueprint
from databaseInit import connect_to_database

AdminApi_bp = Blueprint('adminApi', __name__)

""""
API Interface for Admin
"""

""""
Internal Function
"""

def add_customers(customers):
    """
    Insert multiple customers into the CUSTOMER table.

    :param customers: A list of tuples, where each tuple contains (c_id, name, pwd, phone_no)
    """
    query = """
    INSERT INTO CUSTOMER (c_id, c_name, c_password, c_phone_number) VALUES (%s, %s, %s, %s)
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.executemany(query, customers)
        conn.commit()
        print(f"{len(customers)} customers added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Failed to add customers: {e}")
    finally:
        cur.close()
        conn.close()


def add_restaurants(restaurants):
    query = """
    INSERT INTO RESTAURANT (r_id, r_name, r_password, location) VALUES (%s, %s, %s, %s)
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.executemany(query, restaurants)
        conn.commit()
        print(f"{len(restaurants)} restaurants added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Failed to add restaurants: {e}")
    finally:
        cur.close()
        conn.close()