from databaseUtils import connect_to_database, execute_select_query
from ApiRestaurant import set_regular_open_time, add_meal_items
from ApiAdmin import add_customers, add_restaurants
from faker import Faker
import pandas as pd
from pytz import timezone
from datetime import datetime, timedelta
import random



def generate_fake_customers() :
    # 隨機生成繁體中文資料
    fake = Faker("zh_TW")
    unique_ids = set()  # 用來跟蹤唯一學號
    n = 50
    customers = []
    for _ in range(n):
      # 屆數
      for grade in [13, 12, 11] :
        # 學院
        for institute in [1,2,3,4,5,6,7,8,9,'A','B'] :
          # 科系
          for department in [1,2,3,4,5] :
            # 生成以 B 開頭的 8 位數學號
            while True:  # 保證學號唯一
              # 生成學號
              c_id = f"B{grade}{institute}0{department}0{fake.random_number(digits=2, fix_len=True)}"
              if c_id not in unique_ids:  # 確認唯一性
                  unique_ids.add(c_id)  # 標記學號已使用
                  break
            c_name = fake.name()
            # c_password = fake.password(special_chars=False, length=10)
            c_password = c_id
            c_phone_number = f"09{fake.unique.random_number(digits=8, fix_len=True)}"
            customers.append((c_id, c_name, c_password, c_phone_number))
    add_customers(customers)
    
def generate_fake_restaurant() :
  r_id_set = set()  # 確保 r_id 唯一
  restaurants_data = []
  meal_items = []
  fake = Faker("zh_TW")
  for restaurant in restaurant_data:
    # 生成唯一的 r_id
    while True:
        r_id = f"R{fake.unique.random_number(digits=6, fix_len=True)}"
        if r_id not in r_id_set:
            r_id_set.add(r_id)
            break
    # 餐廳名稱和地點來自文件
    r_name = restaurant[0]
    location = f"{restaurant[1]}"

    # 生成密碼（10個字符，不包含特殊字符）
    r_password = fake.password(length=10, special_chars=False)
    
    # 添加到列表
    restaurants_data.append((r_id, r_name, r_password, location))
    
    # 新增餐點
    for item in meal_templates[r_name] :
      price = random.choice([50, 75, 100, 125, 150])
      processing_time = random.choice(range(1, 6))
      meal_items.append((item, r_id, price, processing_time))
  add_restaurants(restaurants_data)
  add_meal_items(meal_items)


def generate_and_insert_regular_open_time():
    """
    從資料庫中選取所有 r_id，生成模擬的 REGULAR_OPEN_TIME 資料（包含工作日區間），並插入到資料庫。
    """
    fake = Faker()
    
    # 預定義工作時間區間
    predefined_shifts = [
        ('08:00:00', '13:00:00'),  # 早上到中午
        ('12:00:00', '19:00:00'),  # 中午到傍晚
        ('08:00:00', '17:00:00'),  # 早上到傍晚
        ('12:00:00', '21:00:00')   # 中午到晚上
    ]
    
    # 預定義工作日區間
    predefined_days = [
        (['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 0.6),  # 週一到週五（權重最大）
        (['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 0.2),  # 週一到週日
        (['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 0.2)  # 週一公休
    ]
    
    hours = []
    
    # 從資料庫中獲取所有 r_id
    query = "SELECT r_id FROM RESTAURANT"
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.execute(query)
        r_ids = [row[0] for row in cur.fetchall()]  # 獲取所有 r_id
        if not r_ids:
            print("No r_ids found in the database. Exiting...")
            return
        
        # 生成 REGULAR_OPEN_TIME 的資料
        for r_id in r_ids:
            # 根據權重隨機選擇一個工作日區間
            days, _ = random.choices(predefined_days, weights=[w[1] for w in predefined_days])[0]
            for day in days:
                # 隨機選擇一個預定義區間
                open_time, close_time = random.choice(predefined_shifts)
                
                hours.append((r_id, day, open_time, close_time))
        
        # 插入到資料庫
        set_regular_open_time(hours)
        print(f"Inserted regular open times for {len(r_ids)} restaurants.")
    
    except Exception as e:
        print(f"Failed to fetch r_ids or insert regular open times: {e}")
    finally:
        cur.close()
        conn.close()

def generate_fake_orders():
  fake = Faker("zh_TW")
  c_ids = execute_select_query("SELECT c_id FROM CUSTOMER")
  rs = execute_select_query("SELECT r_id, r_name FROM RESTAURANT")
  
  conn = connect_to_database()
  cur = conn.cursor()
  
  for crow in c_ids :
    c_id = crow[0]
    for rrow in rs : 
      r_id, r_name = rrow[0], rrow[1]
      for _ in range(1) :
        order_time = fake.date_time_this_year()
        processing_time = fake.random_number(digits=1, fix_len=True)
        pick_time = fake.random_number(digits=1, fix_len=True)
        expected_time = order_time + timedelta(minutes=processing_time)
        pick_up_time = expected_time + timedelta(minutes=pick_time)
        eating_utensil = random.choice([True, False])
        plastic_bag = random.choice([True, False])
        note = random.choice(notes) if random.choice([True, False]) else None
        order_query = """
        INSERT INTO "ORDER" (order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, c_id, r_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING o_id
        """
        data =  (order_time.strftime('%Y-%m-%d %H:%M:%S'), expected_time.strftime('%Y-%m-%d %H:%M:%S'), pick_up_time.strftime('%Y-%m-%d %H:%M:%S'), eating_utensil, plastic_bag, note, c_id, r_id)
        cur.execute(order_query,data)
        o_id = cur.fetchone()[0]
        
        meal_item_query = """
        INSERT INTO INCLUDE_MEAL_IN_ORDER (name, o_id, r_id, number) VALUES (%s, %s, %s, %s)
        """
        for item in meal_templates[r_name] :
          if random.randint(0, 1) > 0.6 :
            cur.execute(meal_item_query, (item, o_id, r_id, random.choice(range(1,3))))
        
        # 加入折價券
        if random.randint(0, 1) > 0.6 :
          discount_rate = random.choice([0.7, 0.75, 0.8, 0.85, 0.9])
          cur.execute(
                  """
                  INSERT INTO COUPON (discount_rate, start_date, due_date, used_on_id, owner_id)
                  VALUES (%s, %s, %s, null, %s)
                  """,
                  (discount_rate, order_time.date(), order_time.date() + timedelta(days=7), c_id)
          )
          conn.commit()
        
            

def generate_fake_holidays():
    """
    将 2024 年的所有国定假日插入到 HOLIDAY 表中。
    """
    holidays = [
        ("2024-01-01", "元旦"),
        ("2024-02-08", "春節假期"),
        ("2024-02-09", "春節假期"),
        ("2024-02-10", "春節假期"),
        ("2024-02-11", "春節假期"),
        ("2024-02-12", "春節假期"),
        ("2024-02-13", "春節假期"),
        ("2024-02-14", "春節假期"),
        ("2024-02-28", "和平纪念日"),
        ("2024-04-04", "兒童節"),
        ("2024-04-05", "清明節"),
        ("2024-06-10", "端午節"),
        ("2024-09-17", "中秋節"),
        ("2024-10-10", "國慶日")
    ]

    query = """
    INSERT INTO HOLIDAY (date, description)
    VALUES (%s, %s)
    ON CONFLICT (date) DO NOTHING
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.executemany(query, holidays)
        conn.commit()
        print(f"{len(holidays)} holidays inserted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert holidays: {e}")
    finally:
        cur.close()
        conn.close()

def add_clock_in_with_time(r_id, current_date, open_time):
    """
    插入或更新開店時間，支持指定日期。
    """
    query = """
    INSERT INTO CLOCK_IN (r_id, date, open_time, close_time)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (r_id, date)
    DO UPDATE SET open_time = EXCLUDED.open_time
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.execute(query, (r_id, current_date, open_time, open_time))
        conn.commit()
        print(f"{r_id} Successfully clocked in on {current_date} at {open_time}!")
    except Exception as e:
        conn.rollback()
        print(f"{r_id} Failed to clock in on {current_date}: {e}")
    finally:
        cur.close()
        conn.close()

def add_clock_out_with_time(r_id, current_date, close_time):
    """
    插入或更新關店時間，支持指定日期。
    """
    query = """
    UPDATE CLOCK_IN 
    SET close_time = %s
    WHERE r_id = %s AND date = %s
    """
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        # open_time 可以用 close_time 作占位符
        cur.execute(query, (close_time, r_id, current_date))
        conn.commit()
        print(f"{r_id} Successfully set close time on {current_date} at {close_time}!")
    except Exception as e:
        conn.rollback()
        print(f"{r_id} Failed to clock out on {current_date}: {e}")
    finally:
        cur.close()
        conn.close()

def generate_fake_clock_ins():
    """
    為 2024 年12月前的每一天模擬每個 r_id 的上下班情況。
    """
    query_restaurants = "SELECT r_id FROM RESTAURANT"
    query_open_time = """
        SELECT r_id, day, open_time, close_time
        FROM REGULAR_OPEN_TIME
        WHERE r_id = %s
    """
    
    r_ids = execute_select_query(query_restaurants)
    if not r_ids:
        print("No restaurants found in the database.")
        return

    r_ids = [row[0] for row in r_ids]
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 11, 29)
    delta = timedelta(days=1)

    while start_date <= end_date:
        current_date = start_date.strftime("%Y-%m-%d")  # 當前日期格式化為 'YYYY-MM-DD'
        for r_id in r_ids:
            open_times = execute_select_query(query_open_time, (r_id,))
            current_day = start_date.strftime("%a")  # 當前日期的星期，格式為 'Mon', 'Tue' 等

            # 查找符合當前星期的營業時間
            matching_time = next(
                (ot for ot in open_times if ot[1] == current_day), None
            )
            if not matching_time:
                continue  # 如果當天沒有營業時間，跳過

            # 提取時間資訊
            r_id, day, open_time, close_time = matching_time
            open_time = str(open_time)
            close_time = str(close_time)

            print(f"Processing {r_id} on {current_date} ({current_day}): Open {open_time}, Close {close_time}")

            case = random.choices(
                ["準時上下班", "延遲開店", "提早關店", "延遲開店且提早關店", "當天不營業"],
                weights=[0.8, 0.05, 0.05, 0.05, 0.05],
            )[0]

            try:
                meal_item_query = """
                SELECT name FROM meal_item WHERE r_id = %s
                """
                result = execute_select_query(meal_item_query, (r_id,))
                meal_items = [row[0] for row in result]
                
                serve_meal_query = """
                INSERT INTO SERVE_MEAL (r_id, name, date, supply_num, remaining_num) VALUES (%s, %s, %s, %s, %s)
                """
                
                if case != "當天不營業":
                  conn = connect_to_database()
                  cur = conn.cursor()
                  for meal_item in meal_items :
                    supply_num = random.choice([50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200])
                    sale_rate = random.choice([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8])
                    remaining_num  = supply_num * sale_rate
                    cur.execute(serve_meal_query, (r_id, meal_item, current_date, supply_num, remaining_num))
                  conn.commit()
                  cur.close()
                  conn.close()

                if case == "準時上下班":
                    add_clock_in_with_time(r_id, current_date, open_time)
                    add_clock_out_with_time(r_id, current_date, close_time)
                elif case == "延遲開店":
                    delayed_open_time = (
                        datetime.strptime(open_time, "%H:%M:%S")
                        + timedelta(minutes=30)
                    ).strftime("%H:%M:%S")
                    add_clock_in_with_time(r_id, current_date, delayed_open_time)
                    add_clock_out_with_time(r_id, current_date, close_time)
                elif case == "提早關店":
                    early_close_time = (
                        datetime.strptime(close_time, "%H:%M:%S")
                        - timedelta(hours=2)
                    ).strftime("%H:%M:%S")
                    add_clock_in_with_time(r_id, current_date, open_time)
                    add_clock_out_with_time(r_id, current_date, early_close_time)
                elif case == "延遲開店且提早關店":
                    delayed_open_time = (
                        datetime.strptime(open_time, "%H:%M:%S")
                        + timedelta(minutes=30)
                    ).strftime("%H:%M:%S")
                    early_close_time = (
                        datetime.strptime(close_time, "%H:%M:%S")
                        - timedelta(hours=2)
                    ).strftime("%H:%M:%S")
                    add_clock_in_with_time(r_id, current_date, delayed_open_time)
                    add_clock_out_with_time(r_id, current_date, early_close_time)
                elif case == "當天不營業":
                    continue
            except Exception as e:
                print(f"Error processing {r_id} on {current_date}: {e}")

        start_date += delta
 
def generate_fake_coupon():
   pass


# 餐廳資料
restaurant_data = [
    ["摩斯漢堡", "小福樓1"],
    ["稻彥商號", "小福樓2"],
    ["麗宴精緻快餐", "小福樓3"],
    ["比司多", "小福樓4"],
    ["強尼兄弟", "小福樓5"],
    ["勝十蘭", "小福樓6"],
    ["銀魚泰式料理", "小福樓7"],
    ["炸雞大獅", "小福樓8"],
    ["可唐茶旅", "小福樓9"],
    ["重慶抄手", "禮賢樓(卓聯)1"],
    ["果果涼tea", "禮賢樓(卓聯)2"],
    ["品軒樓", "禮賢樓(卓聯)3"],
    ["小木屋鬆餅", "鹿鳴廣場"],
    ["SUBWAY", "二活"],
    ["稍飽燒肉", "醉月湖畔1"],
    ["TT 法國麵包", "醉月湖畔2"],
    ["穀果廚房", "社會科學院"],
    ["JM Cafe & Bistro", "次震宇宙館"],
    ["小農飯盒x茶茶小王子", "學新館"],
    ["蘇杭餐廳", "校友會館"],
]

meal_templates = {
  "摩斯漢堡": ["燒肉珍珠堡", "海洋珍珠堡", "摩斯雞塊"],
  "稻彥商號": ["稻無敵", "龍蝦花壽司", "豆皮壽司"],
  "麗宴精緻快餐": ["炒泡麵", "香腸飯", "日式烤肉飯"],
  "比司多": ["卡拉雞腿堡套餐", "蘿蔔糕加蛋", "鐵板麵套餐"],
  "強尼兄弟": ["油蔥雞肉飯", "精緻滷牛腱", "黑胡椒嫩煎雞胸"],
  "勝十蘭": ["北海道味噌拉麵", "京都醬油拉麵", "日式牛五花蓋飯"],
  "銀魚泰式料理": ["椒麻雞套餐", "咖哩雞套餐", "打拋豬套餐"],
  "炸雞大獅": ["炸雞薯條", "大師蓋飯", "虎咬雞"],
  "可唐茶旅": ["桑椹鮮果茶", "藍莓鮮果茶", "火龍鮮果茶"],
  "重慶抄手": ["抄手", "酸辣湯", "擔擔麵"],
  "果果涼tea": ["水果茶", "芋圓甜品", "椰奶凍"],
  "品軒樓": ["烤鴨便當", "清蒸魚便當", "麻婆豆腐便當"],
  "小木屋鬆餅": ["鮪魚沙拉蔬菜鬆餅", "葡萄奶酥鬆餅", "花生牛肉堡蔬菜鬆餅"],
  "SUBWAY": ["火雞火腿潛艇堡", "百味俱樂部潛艇堡", "牛肉丸潛艇堡"],
  "稍飽燒肉": ["牛肉套餐", "豬肉套餐"],
  "TT 法國麵包": ["可頌", "法棍", "拿鐵"],
  "穀果廚房": ["健康沙拉", "五穀飯", "綠茶"],
  "JM Cafe & Bistro": ["咖啡", "三明治", "千層蛋糕"],
  "小農飯盒x茶茶小王子": ["飯盒套餐", "烤雞腿", "果汁"],
  "蘇杭餐廳": ["東坡肉", "醉雞", "蝦仁炒飯"],
}

notes = [
    "加辣",
    "不要蔥",
    "不要香菜",
    "去冰",
    "醬料多一點",
    "要大份量",
    "請分開包裝",
    "餐點請快速製作",
    "要發票",
    "加一份餐具",
    "請幫我切成小塊",
    "請不要加糖",
    "我要全糖",
    "請附上餐巾紙",
    "請不要加花生",
    "冷熱分離",
    "請按時送達",
    "我要少鹽",
    "飲料不要太甜"
]

