from flask import jsonify, request, Blueprint
from databaseInit import connect_to_database
from databaseUtils import execute_select_query

RestaurantApi_bp = Blueprint('restaurantApi', __name__)

""""
API Interface for Restaurant
"""

@RestaurantApi_bp.route('/restaurant/name', methods=['POST'])
def GetRName() :
  data = request.json
  r_id = data.get('username')
  name = getRName(r_id)

  if name :
    return jsonify({"name": name}), 200
  else :
    return jsonify({"error": "Restaurant name does not exist"}), 401

@RestaurantApi_bp.route('/restaurant/past/order', methods=['POST'])
def Rest_Past_Order():
    data = request.json
    r_id = data.get('r_id')
    if not r_id:
        return jsonify({"error": "Missing required parameter 'r_id'"}), 400
    result = select_past_order(r_id)
    return jsonify(result)


""""
Internal Function
"""

def getRName(r_id) :
  psql_conn = connect_to_database()
  cur = psql_conn.cursor()

  query = '''
  SELECT r_name
  FROM RESTAURANT
  WHERE r_id = %s
  '''
  cur.execute(query, (r_id,))

  # get the res
  result = cur.fetchone()

  cur.close()
  psql_conn.close()
  
  if result:
      return result[0]
  else:
      return None

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


def select_past_order(r_id):
    query = """
    SELECT *
    FROM "ORDER"
    WHERE r_id = %s
    ORDER BY o_id
    """
    rows = execute_select_query(query, str(r_id))

    # 查詢每筆訂單的餐點資訊
    query_meals = """
    SELECT o_id, "name", "number"
    FROM INCLUDE_MEAL_IN_ORDER
    WHERE o_id = %s
    """

    past_order = {}
    for row in rows:
        o_id, order_time, expected_time, pick_up_time, \
        eating_utensil, plastic_bag, note, c_id, starnum, review, r_id = row

        meal_rows = execute_select_query(query_meals, str(o_id))
        meals = [{"name": name, "number": number} for _, name, number in meal_rows]

        past_order[o_id] = {
            'id': o_id,
            'order_time': order_time,
            'expected_time': expected_time, 
            'finish_time': pick_up_time,
            'eating_utensil': eating_utensil,
            'plastic_bag': plastic_bag,
            'note': note,
            'c_id': c_id,
            'starnum': starnum,
            'review': review,
            'meals': meals 
        }
    return list(past_order.values())