from flask import jsonify, request, Blueprint
from datetime import datetime, timezone
from pytz import timezone
from databaseInit import connect_to_database
from databaseUtils import execute_select_query

RestaurantApi_bp = Blueprint('restaurantApi', __name__)

""""
API Interface for Restaurant
"""

# 用給定的餐廳 id 取得餐廳名稱
@RestaurantApi_bp.route('/restaurant/name', methods=['POST'])
def GetRName() :
  data = request.json
  r_id = data.get('username')
  name = getRName(r_id)

  if name :
    return jsonify(name), 200
  else :
    return jsonify({"error": "Restaurant name does not exist"}), 401

# 取得所有訂單（包含已完成和處理中）
@RestaurantApi_bp.route('/restaurant/past/order', methods=['POST'])
def Rest_Past_Order():
    data = request.json
    r_id = data.get('r_id')
    if not r_id:
        return jsonify({"error": "Missing required parameter 'r_id'"}), 400
    result = select_past_order(r_id)
    return jsonify(result)


@RestaurantApi_bp.route('/restaurant/clock/in', methods=['POST'])
def Clock_In():
    data = request.json
    r_id = data.get('r_id')
    if not r_id:
        return jsonify({"error": "Missing required parameter 'r_id'"}), 400
    current = add_clock_in(r_id)
    return jsonify({"message": f"Clock In at {current}!"}), 200

@RestaurantApi_bp.route('/restaurant/clock/out', methods=['POST'])
def Clock_Out():
    data = request.json
    r_id = data.get('r_id')
    if not r_id:
        return jsonify({"error": "Missing required parameter 'r_id'"}), 400
    current = add_clock_out(r_id)
    return jsonify({"message": f"Clock Out at {current}!"}), 200

@RestaurantApi_bp.route('/restaurant/check/clock', methods=['POST'])
def check_clock_in_status():
    data = request.json
    r_id = data.get('r_id')

    if not r_id:
        return jsonify({"error": "Missing r_id"}), 400

    is_clocked_in = get_clock_in_status(r_id)
    if is_clocked_in:
        return jsonify({"message": "Restaurant has clocked in!"}), 200
    else:
        return jsonify({"error": "Restaurant hasn't clocked in><"}), 401

@RestaurantApi_bp.route('/restaurant/update/serve/meal', methods=['POST'])
def update_serve_meal():
    data = request.json
    r_id = data.get('r_id')
    name = data.get('name')
    supply_num = data.get('supply_num')

    if not r_id:
        return jsonify({"error": "Missing r_id"}), 400
    elif not name:
        return jsonify({"error": "Missing meal name"}), 400

    add_serve_meal(r_id, name, supply_num)
    return jsonify({"message": f"Update {name} successful!"}), 200 # Response(status=200)

@RestaurantApi_bp.route('/restaurant/complete/order', methods=['POST'])
def Complete_Order() :
    data = request.json
    o_id = data.get('o_id')
    complete_time = data.get('complete_time')
    result = complete_Order(o_id, complete_time)
    
    if result :
        return jsonify("successful"), 200
    else : 
        return jsonify({"error": "update order fail"}), 400

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
    
    rows = execute_select_query(query, (r_id, ))


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
        
        print("[select_past_order query_meals] : ", query_meals)

        meal_rows = execute_select_query(query_meals, (str(o_id),))
        print("[meal_rows] : ", meal_rows, flush=True)
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


def add_clock_in(r_id):
    query = """
    INSERT INTO CLOCK_IN (r_id, date, open_time, close_time) VALUES (%s, %s, %s, %s)
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        current_datetime = datetime.now(timezone('Asia/Taipei'))
        open_time = current_datetime.time().replace(microsecond=0).strftime("%H:%M:%S")
        date = current_datetime.date().strftime("%Y-%m-%d")
        cur.execute(query, (r_id, date, open_time, open_time))
        conn.commit()
        print(f"Successfully clock in {date} {open_time}!", flush=True)
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        conn.rollback()
        print(f"Failed to clock in: {e}", flush=True)
    finally:
        cur.close()
        conn.close()

def add_clock_out(r_id):
    query = """
    UPDATE CLOCK_IN 
    SET close_time = %s
    WHERE r_id = %s AND date = %s
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        current_datetime = datetime.now(timezone('Asia/Taipei'))
        close_time = current_datetime.time().replace(microsecond=0).strftime("%H:%M:%S")
        date = current_datetime.date().strftime("%Y-%m-%d")
        cur.execute(query, (close_time, r_id, date))
        conn.commit()
        print(f"Successfully set close time at {date} {close_time}!", flush=True)
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        conn.rollback()
        print(f"Failed to clock out: {e}", flush=True)
    finally:
        cur.close()
        conn.close()


def add_serve_meal(r_id, name, supply_num):
    query = """
    INSERT INTO SERVE_MEAL (r_id, name, date, supply_num) VALUES (%s, %s, %s, %s)
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        today = datetime.now(timezone('Asia/Taipei')).date()
        cur.execute(query, (r_id, name, today, supply_num))
        conn.commit()
        print(f"Successfully update {name}'s quantity to {supply_num} at {today}!", flush=True)
    except Exception as e:
        conn.rollback()
        print(f"Failed to update {name}'s quantity to {supply_num} at {today}", flush=True)
        cur.close()
        conn.close()


def get_clock_in_status(r_id):
    query = """
    SELECT EXISTS(
        SELECT *
        FROM CLOCK_IN
        WHERE r_id = %s AND date = %s
    );
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        today = datetime.now(timezone('Asia/Taipei')).date()
        cur.execute(query, (r_id, today))
        res = cur.fetchone()[0]
        if res:
            return True
        else:
            return False
    except Exception as e:
        conn.rollback()
        print(f"Failed to get clock in status: {e}", flush=True)
    finally:
        cur.close()
        conn.close()

def complete_Order(o_id, complete_time) -> bool :
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        # Insert into ORDER table
        query = f"""
        UPDATE "ORDER"
        SET pick_up_time = '{complete_time}'
        WHERE o_id = {o_id}
        """

        cur.execute(query)

        conn.commit()
        print("Order update successfully", flush=True)
        
        return True

    except Exception as e:
        conn.rollback()
        print(f"Failed to update order: {e}", flush=True)
    finally:
        cur.close()
        conn.close()