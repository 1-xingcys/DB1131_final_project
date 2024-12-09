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