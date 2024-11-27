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


@CustomerApi_bp.route('/customer/past_orders', methods=['POST'])
def Get_past_orders():
    data = request.json
    c_id = data.get('c_id')
    # 呼叫select_past_order
    past_orders = select_past_order(c_id)
    if past_orders:
        return jsonify({"past_orders": past_orders}), 200
    else:
        return jsonify({"error": "No past orders found for this customer"}), 404


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


def select_past_order(c_id) -> list:
    query = """
    SELECT o.o_id, o.order_time, o.expected_time, o.pick_up_time, o.eating_utensil, o.plastic_bag, o.note, o.r_id, imo.name, imo.number
    FROM "ORDER" o
    LEFT JOIN INCLUDE_MEAL_IN_ORDER imo ON o.o_id = imo.o_id
    WHERE o.c_id = %s
    ORDER BY o.order_time DESC
    """
    rows = execute_select_query(query, (c_id,))
    past_orders = {}
    for row in rows:
        (o_id, order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, r_id, meal_name, meal_number) = row
        if o_id not in past_orders:
            query = f"SELECT r_id FROM restaurant AS r WHERE r = {r_id}"
            r_name = execute_select_query(query)
            past_orders[o_id] = {
                'order_id': o_id,
                'order_time': order_time,
                'expected_time': expected_time,
                'pick_up_time': pick_up_time,
                'eating_utensil': eating_utensil,
                'plastic_bag': plastic_bag,
                'note': note,
                'restaurant_name': r_name,
                'meals': []
            }
        if meal_name:
            past_orders[o_id]['meals'].append({'name': meal_name, 'number': meal_number})
    return list(past_orders.values())