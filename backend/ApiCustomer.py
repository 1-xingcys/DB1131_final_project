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
    coupon_id = data.get('coupon_id', None)  # 默認為 None
    print(type(meal_items))
    print(meal_items, flush=True)
    
    # 向資料庫更新訂單相關資訊，並回傳折價券資訊給前端
    try :
        issued_discount_rate, start_date, due_date = submit_order(order_time, expected_time, pick_up_time, \
                 eating_utensil, plastic_bag, note, c_id, r_id, meal_items, coupon_id)
        result = {"getCoupon" : bool(issued_discount_rate), 
                    "discount_rate" : issued_discount_rate, 
                    "start_date" : start_date, 
                    "due_date" : due_date}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error" : str(e)}), 401
    
    

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

@CustomerApi_bp.route('/customer/submit/order/validate/coupon',methods=['POST'])
def Validate_coupon():
    try:
        data = request.json
        c_id = data.get("c_id")
        discount_rate = data.get("discount_rate")
        valid_coupon_id = validate_coupon(c_id, discount_rate)
        if valid_coupon_id is not None:
            return jsonify(valid_coupon_id), 200
        else:
            return jsonify({"error": "no coupon"}), 401
    except Exception as e:
        print(f"Unexpected error in Validate_coupon: {e}", flush=True)
        return jsonify({"error": "Validate_coupon內部錯誤"}), 500

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
  
  
# meal_items : [{'name' : name, 'number' : number}, {}, ...]
# coupon_id 可以為空(none)
def submit_order(order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, c_id, r_id, meal_items: list, coupon_id = None) -> None:
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        # 若有傳入 coupon_id，檢查其有效性
        if coupon_id:
            available_coupons = select_available_coupons(c_id)
            valid_coupon = next((coupon for coupon in available_coupons if coupon['coupon_id'] == coupon_id), None)
            print(f"折價券存在！")
            if not valid_coupon:
                print(f"折價券 {coupon_id} 不可用或不存在", flush=True)
                raise ValueError("無效的折價券")

        ###########################################
        # 重要 Transection 開始：確認餐點數量 & 更新餐點數量
        ###########################################

        # 確認供應數量足夠
        check_supply_query = """
        SELECT "name", remaining_num
        FROM serve_meal
        WHERE r_id = %s AND "name" = ANY(%s)
        FOR UPDATE
        """
        name_list = [item['name'] for item in meal_items]
        cur.execute(check_supply_query, (r_id, name_list))
        rows = cur.fetchall()
        
        remaining_nums = {row[0]: row[1] for row in rows}
        for meal_item in meal_items :
            if meal_item['number'] > remaining_nums[ meal_item['name'] ] :
                raise ValueError(f"{meal_item['name']} remain {remaining_nums[ meal_item['name'] ]} > {meal_item['number']}")
        
        # 更新供應（剩餘）數量
        update_remaining_num_query = """
        UPDATE serve_meal
        SET remaining_num = remaining_num - %s
        WHERE r_id = %s AND name = %s
        """
        update_meal_items = [(meal_item['number'], r_id, meal_item['name']) for meal_item in meal_items]
        cur.executemany(update_remaining_num_query, update_meal_items)
        
        conn.commit()
        
        ###########################################
        # 重要 Transection 結束
        ###########################################
        
        
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
            
        # 計算折價前的總金額
        total_price = calculate_order_total(meal_items,r_id)
        print(f"訂單編號{o_id}的折價前總金額為：{total_price}元。",flush=True)

        # 更新折價券的使用情況
        if coupon_id:
            discount_rate = valid_coupon['discount_rate']
            total_price *= discount_rate
            total_price = round(total_price)  # 四捨五入確保為整數
            coupon_update_query = """
            UPDATE COUPON
            SET used_on_id = %s WHERE coup_id = %s
            """
            cur.execute(coupon_update_query, (o_id, coupon_id))
            print(f"使用折價券 {coupon_id} ，折扣後總金額為：{total_price} 元。", flush=True)
        else:
            total_price = round(total_price)  # 確保金額為整數

        conn.commit()
        
        # 檢查折價後（如果有）價格是否大於 200

        print("Order submitted successfully", flush=True)
        if(total_price >= 200):
            issued_discount_rate, start_date, due_date = issue_coupon(c_id, order_time)
            return issued_discount_rate, start_date, due_date
        
        return "", "", ""
        
    except Exception as e:
        conn.rollback()
        print(f"Failed to submit order: {e}", flush=True)
        raise ValueError(e)
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
    SELECT mi.name, mi.price, mi.processing_time, sm.remaining_num
    FROM MEAL_ITEM AS mi
	JOIN serve_meal AS sm ON mi.r_id = sm.r_id AND mi.name = sm.name
    WHERE mi.r_id = %s AND sm.date = now()::DATE AND sm.remaining_num > 0
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
            # 查詢餐廳名稱
            query1 = f"SELECT r_name FROM restaurant AS r WHERE r_id = '{r_id}'"
            print("query1 : ", query1)
            result = execute_select_query(query1)
            r_name = result[0][0]

            # 查詢是否有折價券
            coupon_query = "SELECT discount_rate FROM COUPON WHERE used_on_id = %s"
            coupon_result = execute_select_query(coupon_query, (o_id,))
            discount_rate = coupon_result[0][0] if coupon_result else None
            print(f"訂單 {o_id} 有dicount_rate {discount_rate}",flush = True)

            # 初始化訂單數據
            past_orders[o_id] = {
                'order_id': o_id,
                'order_time': order_time,
                'expected_time': expected_time,
                'pick_up_time': pick_up_time,
                'eating_utensil': eating_utensil,
                'plastic_bag': plastic_bag,
                'note': note,
                'restaurant_name': r_name,
                'meals': [],
                'discount_rate' : discount_rate if discount_rate else None,
                'total_price' : None,  # 初始化總金額
                'r_id' : r_id # 只是下面計算金額需要，前端會忽略他
            }
        # 添加餐點到訂單
        if meal_name:
            past_orders[o_id]['meals'].append({'name' : meal_name, 'number': meal_number})
            print(f"訂單編號{o_id}有餐點： {past_orders[o_id]['meals']}",flush=True)
    # 計算所有訂單的總金額
    for o_id, order in past_orders.items():
        meals_for_order = order['meals']
        print(meals_for_order,flush=True)
        total_price = calculate_order_total(meals_for_order, order['r_id'])
        print(f"訂單編號 {o_id} 得折扣前總金額為 {total_price} 元",flush=True)
        # 根據折扣率調整總金額
        if order['discount_rate']:
            total_price = round(total_price * order['discount_rate'])
        # 更新總金額
        past_orders[o_id]['total_price'] = total_price
        print(f"訂單編號 {o_id} 得最後最後最後折扣後總金額為 {total_price} 元",flush=True)
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

def issue_coupon(c_id: str, order_time: str) -> tuple:
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
        
        return discount_rate, start_date, due_date
    except Exception as e:
        print(f"Failed to issue coupon: {e}")

def validate_coupon(c_id, discount_rate: float) -> int:
    '''
    顧客會選擇他想使用的折扣率，這個函數會檢查該顧客有沒有這個折扣率的折價券，
    如果有就回傳符合的coupon_id 沒有的話就回傳none，並raise error
    '''
    query = """
    SELECT coup_id, due_date
    FROM COUPON
    WHERE owner_id = %s AND discount_rate = %s AND used_on_id IS NULL AND due_date >= CURRENT_DATE
    ORDER BY due_date ASC
    """

    try:
        # 執行查詢，獲取符合條件的折價券
        rows = execute_select_query(query, (c_id, discount_rate))
        if not rows:
            # 如果沒有找到符合條件的折價券，返回 None 並記錄錯誤
            print(f"這白癡沒有這種折價券是在耍什麼低能操 {c_id} 折扣率: {discount_rate}", flush=True)
            return None
        # 選擇 due_date 最近的折價券 (第一個結果)
        coupon_id = rows[0][0]  # 取出 coup_id
        print(f"找到符合條件的折價券: coupon_id {coupon_id}, discount_rate {discount_rate}", flush=True)
        return coupon_id

    except Exception as e:
        print(f"validate_coupon出包", flush=True)
        raise