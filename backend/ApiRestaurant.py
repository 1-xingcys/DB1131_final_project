from flask import jsonify, request, Blueprint
from databaseInit import connect_to_database

RestaurantApi_bp = Blueprint('restaurantApi', __name__)

""""
API Interface for Restaurant
"""

""""
Internal Function
"""

def set_regular_open_time(hours):
    query = """
    INSERT INTO REGULAR_OPEN_TIME (r_id, day, open_time, close_time) VALUES (%s, %s, %s, %s)
    ON CONFLICT (r_id, day) DO UPDATE SET open_time = EXCLUDED.open_time, close_time = EXCLUDED.close_time
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.executemany(query, hours)
        conn.commit()
        print(f"{len(hours)} regular open time set successfully")
    except Exception as e:
        conn.rollback()
        print(f"Failed to set regular open times: {e}")
    finally:
        cur.close()
        conn.close()
        
def add_meal_items(meal_items):
    query = """
    INSERT INTO MEAL_ITEM (name, r_id, price, processing_time) VALUES (%s, %s, %s, %s)
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.executemany(query, meal_items)
        conn.commit()
        print(f"{len(meal_items)} meal items added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Failed to add meal items: {e}")
    finally:
        cur.close()
        conn.close()