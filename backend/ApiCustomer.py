from flask import jsonify, request, Blueprint
from databaseInit import connect_to_database
from databaseUtils import execute_select_query,execute_query

import random
from datetime import datetime, timedelta

CustomerApi_bp = Blueprint('customerApi', __name__)

""""
API Interface for Customer
"""

@CustomerApi_bp.route('/restaurant/info/regular', methods=['GET'])
def Rest_reg_info():
  result = select_restaurant_reg_info()
  return jsonify(result)

@CustomerApi_bp.route('/customer/name', methods=['POST'])
def GetCName() :
  data = request.json
  c_id = data.get('username')
  name = getCName(c_id)

  if name :
    return jsonify(name), 200
  else :
    return jsonify({"error": "Customer name does not exist"}), 401

@CustomerApi_bp.route('/restaurant/name/regular', methods=['GET'])
def Rest_name() :
    result = select_restaurant_name()
    return jsonify(result)


@CustomerApi_bp.route('/restaurant/meal_item/regular', methods=['POST'])
def A_rest_meal_item() :
    data = request.json
    r_id = data.get('id')
    result = select_restaurant_meal_item(r_id)
    return jsonify(result)

@CustomerApi_bp.route('/restaurant/name/opening', methods=['GET'])
def Opening_rest_name() :
    result = select_opening_restaurant_name()
    return jsonify(result)


@CustomerApi_bp.route('/restaurant/meal_item/available', methods=['POST'])
def A_opening_rest_meal_item() :
    data = request.json
    r_id = data.get('id')
    result = select_opening_restaurant_meal_item(r_id)
    return jsonify(result)

@CustomerApi_bp.route('/customer/submit/order', methods=['POST'])
def Submit_order() :
    data = request.json
    order_time = data.get('order_time')
    expected_time = data.get('expected_time')
    pick_up_time = data.get('pick_up_time')
    eating_utensil = bool(data.get('eating_utensil'))
    plastic_bag = bool(data.get('plastic_bag'))
    note = data.get('note')
    c_id = data.get('c_id')
    r_id = data.get('r_id')
    meal_items = data.get('meal_items')
    print(type(meal_items))
    print(meal_items, flush=True)
    
    submit_order(order_time, expected_time, pick_up_time, \
                 eating_utensil, plastic_bag, note, c_id, r_id, meal_items)
    
    return jsonify({"result" : "success"}), 200
    

@CustomerApi_bp.route('/customer/past_orders', methods=['POST'])
def Get_past_orders():
    data = request.json
    c_id = data.get('c_id')
    # 呼叫select_past_order
    past_orders = select_past_order(c_id)
    if past_orders:
        return jsonify(past_orders), 200
    else:
        return jsonify({"error": "No past orders found for this customer"}), 404
    
@CustomerApi_bp.route('/customer/available_coupons',methods=['POST'])
def Get_available_coupons():
    data = request.json
    c_id = data.get('c_id')
    # 呼叫select_available_coupons
    available_coupons = select_available_coupons(c_id)
    if available_coupons:
        return jsonify(available_coupons), 200
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
  
  
# meal_item : [{'name' : name, 'number' : number}, {}, ...]
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
        total_price = calculate_order_total(meal_items,r_id)
        print(f"訂單編號{o_id}的總金額為：{total_price}元。")
        if(total_price >= 200):
            issue_coupon(c_id, order_time)
        conn.commit()
        print("Order submitted successfully", flush=True)

    except Exception as e:
        conn.rollback()
        print(f"Failed to submit order: {e}", flush=True)
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

def select_restaurant_name() -> list :
    query = """
    SELECT r_id, r_name
    FROM RESTAURANT
    """
    rows = execute_select_query(query)
    res = {}
    for row in rows :
        r_id, r_name = row
        res[r_id] = {
            'id' : r_id,
            'name' : r_name
        }
    return list(res.values())

def select_restaurant_meal_item(r_id) -> list :
    query = """
    SELECT name, price, processing_time
    FROM MEAL_ITEM WHERE r_id = %s
    """
    rows = execute_select_query(query, (r_id,))
    res = {}
    for row in rows :
        name, price, processing_time = row
        res[name] = {
            'name' : name,
            'price' : price,
            'processing_time' : processing_time
        }
    return list(res.values())

def select_opening_restaurant_name() :
    query = """
    SELECT r.r_id, r.r_name
    FROM RESTAURANT AS r 
        JOIN CLOCK_IN AS ci ON r.r_id = ci.r_id
    WHERE ci.date = now()::DATE  AND ci.open_time = ci.close_time
    """
    rows = execute_select_query(query)
    res = {}
    for row in rows :
        r_id, r_name = row
        res[r_id] = {
            'id' : r_id,
            'name' : r_name
        }
    return list(res.values())

def select_opening_restaurant_meal_item(r_id) :
    query = """
    SELECT mi.name, mi.price, mi.processing_time, sm.supply_num
    FROM MEAL_ITEM AS mi
	JOIN serve_meal AS sm ON mi.r_id = sm.r_id AND mi.name = sm.name
    WHERE mi.r_id = %s AND sm.date = now()::DATE AND sm.supply_num > 0
    """
    rows = execute_select_query(query, (r_id,))
    res = {}
    for row in rows :
        name, price, processing_time, supply_num = row
        res[name] = {
            'name' : name,
            'price' : price,
            'processing_time' : processing_time,
            'supply_num' : supply_num
        }
    return list(res.values())



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
            query1 = f"SELECT r_name FROM restaurant AS r WHERE r_id = '{r_id}'"
            print("query1 : ", query1)
            result = execute_select_query(query1)
            print("result : ", result, flush=True)
            r_name = result[0][0]
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

# 顯示顧客目前尚未使用且還沒過期的折價券
def select_available_coupons(c_id) -> list:

    query = """
    SELECT c.coup_id, c.discount_rate, c.start_date, c.due_date
    FROM COUPON c
    WHERE c.owner_id = %s AND c.used_on_id IS NULL AND c.due_date >= CURRENT_DATE
    ORDER BY c.due_date ASC
    """
    rows = execute_select_query(query, (c_id,))
    available_coupons = []

    for row in rows:
        (coup_id, discount_rate, start_date, due_date) = row
        available_coupons.append({
            'coupon_id': coup_id,
            'discount_rate': discount_rate,
            'start_date': start_date,
            'due_date': due_date
        })
        print(f"coupon_id {coup_id} 的 開始時間為 {start_date} , 結束時間為 {due_date}",flush=True )
    print("SUCCESSFULLY select available coupon 水喔",flush=True)
    return available_coupons

# meal_item : [{'name' : name, 'number' : number}, {}, ...]
def calculate_order_total(meal_items: list, r_id) -> float:
    """
    被submit_order呼叫，給定餐點計算該訂單總金額。
    """
    query = """
    SELECT price FROM MEAL_ITEM
    WHERE r_id = %s AND name = %s
    """
    total_price = 0.0
    try:
        for meal in meal_items:
            meal_name = meal['name']
            meal_quantity = meal['number']
            # 查詢餐點價格
            result = execute_select_query(query, (r_id, meal_name))
            if result:
                price_per_item = result[0][0]  # 取第一行第一列的價格
                total_price += price_per_item * meal_quantity
            else:
                print(f"Meal item '{meal_name}' not found in restaurant {r_id}.")
        return total_price
    except Exception as e:
        print(f"Failed to calculate order total: {e}")
        return 0.0

import random
from datetime import datetime, timedelta

def issue_coupon(c_id: str, order_time: str) -> None:
    """
    在 submit_order 中被呼叫。呼叫條件是如果前面 calculate_order_total 的金額大於等於 200。
    這個函數會拿訂單的資訊去資料庫插入一筆折價券資料，開始日期是下單時間（只取 order_time 中的日期部分），
    結束日期是開始日期 + 7。折扣率是從 {0.7, 0.75, 0.8, 0.85, 0.9} 隨機抽出。
    """
    try:
        # 從折扣率池中隨機選擇一個折扣率
        discount_rate = random.choice([0.7, 0.75, 0.8, 0.85, 0.9])
        
        # 提取開始日期（只取日期部分）
        start_date = datetime.strptime(order_time.split(" ")[0], "%Y-%m-%d").date()
        
        # 計算結束日期
        due_date = start_date + timedelta(days=7)

        # 插入折價券的 SQL 查詢
        query = """
        INSERT INTO COUPON (discount_rate, start_date, due_date, used_on_id, owner_id)
        VALUES (%s, %s, %s, null, %s)
        """
        # 執行插入操作
        data = (discount_rate, start_date, due_date, c_id)
        execute_query(query, data)

        print(f"Coupon issued successfully for customer {c_id} with discount rate {discount_rate}")
        print(f"下單時間為 {order_time} , 發放折價券時間為 {start_date} , 截止日期為 {due_date}")
    except Exception as e:
        print(f"Failed to issue coupon: {e}")
