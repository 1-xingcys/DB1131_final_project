# Library
from flask import jsonify, request, Blueprint
from databaseInit import connect_to_database
from databaseUtils import execute_select_query

CustomerApi_bp = Blueprint('customerApi', __name__)

""""
API Interface for Customer
"""

@CustomerApi_bp.route('/restaurant/info/regular', methods=['GET'])
def Rest_reg_info():
  result = select_restaurant_reg_info()
  return jsonify(result)

@CustomerApi_bp.route('/customer/cname', methods=['POST'])
def GetCName() :
  data = request.json
  c_id = data.get('username')
  name = getCName(c_id)
  
  if name :
    return jsonify({"name": name}), 200
  else :
    return jsonify({"error": "Customer name does not exist"}), 401


""""
Internal Function
"""

def getCName(c_id) :
  psql_conn = connect_to_database()
  cur = psql_conn.cursor()

  query = '''
  SELECT c_name
  FROM CUSTOMER
  WHERE c_id = %s
  '''
  cur.execute(query, (c_id,))

  # get the res
  result = cur.fetchone()

  cur.close()
  psql_conn.close()
  
  if result:
      return result[0]
  else:
      return None
    
def submit_order(order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, c_id, r_id, meal_items: list) -> None:
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        # Insert into ORDER table
        order_query = """
        INSERT INTO "ORDER" (order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, c_id, r_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING o_id
        """
        data =  (order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, c_id, r_id)

        cur.execute(order_query,data)
        o_id = cur.fetchone()[0]

        # Insert meal items into INCLUDE_MEAL_IN_ORDER table
        meal_item_query = """
        INSERT INTO INCLUDE_MEAL_IN_ORDER (name, o_id, r_id, number) VALUES (%s, %s, %s, %s)
        """
        for meal in meal_items:
            cur.execute(meal_item_query, (meal['name'], o_id, r_id, meal['number']))

        conn.commit()
        print("Order submitted successfully")

    except Exception as e:
        conn.rollback()
        print(f"Failed to submit order: {e}")
    finally:
        cur.close()
        conn.close()
        
def select_meal_item(r_id) -> list:
    query = """
    SELECT * FROM MEAL_ITEM WHERE r_id = %s
    """
    return execute_select_query(query, (r_id,))
  
def select_restaurant_reg_info() -> list:
  query = """
  SELECT r.r_id, r.r_name, r.location, ro.day, ro.open_time, ro.close_time
  FROM RESTAURANT r
  LEFT JOIN REGULAR_OPEN_TIME ro ON r.r_id = ro.r_id
  """
  rows = execute_select_query(query)
  restaurant_info = {}
  for row in rows:
      r_id, name, location, day, open_time, close_time = row
      if r_id not in restaurant_info:
          restaurant_info[r_id] = {
              'id': r_id,
              'name': name,
              'location': location,
              'mon': '', 'tue': '', 'wed': '', 'thu': '', 'fri': '', 'sat': '', 'sun': ''
          }
      if day:
          restaurant_info[r_id][day.lower()] = f"{open_time}~{close_time}"
  return list(restaurant_info.values())