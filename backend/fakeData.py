from databaseUtils import connect_to_database
from ApiRestaurant import set_regular_open_time, add_meal_items
from ApiAdmin import add_customers, add_restaurants
from faker import Faker
import pandas as pd


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
  file_path = './restaurants.csv'
  restaurants_df = pd.read_csv(file_path)
  r_id_set = set()  # 確保 r_id 唯一
  restaurants_data = []
  fake = Faker("zh_TW")
  for index, row in restaurants_df.iterrows():
    # 生成唯一的 r_id
    while True:
        r_id = f"R{fake.unique.random_number(digits=6, fix_len=True)}"
        if r_id not in r_id_set:
            r_id_set.add(r_id)
            break
    # 餐廳名稱和地點來自文件
    r_name = row['name']
    location = f"{row['location']}{index}"

    # 生成密碼（10個字符，不包含特殊字符）
    r_password = fake.password(length=10, special_chars=False)
    
    # 添加到列表
    restaurants_data.append((r_id, r_name, r_password, location))
  add_restaurants(restaurants_data)

from faker import Faker
from ApiRestaurant import set_regular_open_time
from databaseUtils import connect_to_database
import random

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

def generate_fake_meal_items():
   pass

def generate_fake_orders():
   # 某些超過200元的訂單會去生成 coupon
   pass

def generate_fake_holidays():
   pass

def generate_fake_clock_ins():
   pass

def gen_fake_include_meal_in_order():
   pass

def genenerate_fake_serve_meals():
   pass