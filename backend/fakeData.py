from databaseUtils import connect_to_database, execute_select_query
from ApiRestaurant import set_regular_open_time, add_meal_items, add_clock_in,add_clock_out
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

            # 打印測試日誌
            print(f"Processing {r_id} on {current_date} ({current_day}): Open {open_time}, Close {close_time}")

            case = random.choices(
                ["準時上下班", "延遲開店", "提早關店", "延遲開店且提早關店", "當天不營業"],
                weights=[0.8, 0.05, 0.05, 0.05, 0.05],
            )[0]

            try:
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


def gen_fake_include_meal_in_order():
   pass

def genenerate_fake_serve_meals():
   pass