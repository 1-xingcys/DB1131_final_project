
# databaseInit.py
from databaseUtils import connect_to_database
from fakeData import generate_fake_customers, generate_fake_restaurant, generate_and_insert_regular_open_time,generate_fake_holidays,generate_fake_clock_ins

# temp for initializing some fake data
from ApiRestaurant import set_regular_open_time, add_meal_items
from ApiAdmin import add_customers, add_restaurants

def db_init() :
    create_tables(create_table_query)
        # Example usage of add_customers
    customers = [
        ("B10303097", "張弘蒲", "B10303097", "0912345678"),
        ("B10705009", "邱一新", "B10705009", "0923456789"),
        ('B10302353', 'duoduo', 'duoduo1111', '0934567891')
    ]
    add_customers(customers)
    
    generate_fake_customers()
    generate_fake_restaurant()
    generate_and_insert_regular_open_time()
    generate_fake_holidays()
    generate_fake_clock_ins()
    # Example usage of add_restaurants
    restaurants = [
        ("Rwatergun", "大水缸", "password", "科技大樓站"),
        ("Rsilvfish", "銀魚", "password", "小福"),
        ("Rtwinsegg", 'Twins手工蛋餅', 'password', '活大')
    ]
    add_restaurants(restaurants)

    # Example usage of add_meal_items
    meal_items = [
        ("鍋燒意麵", restaurants[0][0], 100, 5),
        ("泡菜意麵", restaurants[0][0], 120, 5),
        ("滷味個人餐", restaurants[0][0], 50, 2),
        ('椒麻雞套餐', restaurants[1][0], 100, 1),
        ('咖哩雞套餐', restaurants[1][0], 100, 1),
        ('打拋豬套餐', restaurants[1][0], 100, 1),
        ('火腿蛋餅', restaurants[2][0], 45, 3),
        ('鮪魚蛋餅', restaurants[2][0], 50, 3),
        ('紅茶', restaurants[2][0], 25, 1),
        ('鮮奶茶', restaurants[2][0], 35, 1)
    ]
    add_meal_items(meal_items)

    # Example usage of set_regular_open_time
    regular_hours = [
    (restaurants[0][0], 'Mon', '11:00', '19:30'),
    (restaurants[0][0], 'Tue', '11:00', '19:30'),
    (restaurants[0][0], 'Wed', '11:00', '19:30'),
    (restaurants[0][0], 'Thu', '11:00', '19:30'),
    (restaurants[0][0], 'Fri', '11:00', '19:30'),
    (restaurants[0][0], 'Sat', '11:00', '15:00'),
    (restaurants[1][0], 'Mon', '07:00', '14:00'),
    (restaurants[1][0], 'Tue', '07:00', '14:00'),
    (restaurants[1][0], 'Wed', '07:00', '14:00'),
    (restaurants[1][0], 'Thu', '07:00', '14:00'),
    (restaurants[1][0], 'Fri', '07:00', '14:00'),
    (restaurants[1][0], 'Sat', '07:00', '14:00'),
    (restaurants[2][0], 'Mon', '07:00', '14:00'),
    (restaurants[2][0], 'Tue', '07:00', '14:00'),
    (restaurants[2][0], 'Wed', '07:00', '14:00'),
    (restaurants[2][0], 'Thu', '07:00', '14:00'),
    (restaurants[2][0], 'Fri', '07:00', '14:00'),
    (restaurants[2][0], 'Sat', '07:00', '14:00'),
    ]
    set_regular_open_time(regular_hours)


    # Example usage of select_restaurant_reg_info
    # restaurant_info = select_restaurant_reg_info()
    # print(restaurant_info)
        
    
    # # Example usage of select_meal_item
    # meal_items1 = select_meal_item("Rwatergun")
    # print("Meal items for 大水缸:", meal_items1)
    # meal_items2 = select_meal_item("Rsilvfish")
    # print("Meal items for 銀魚:", meal_items2)

    # # Example usage of submit_order
    # order_time = "2024-11-13 12:00:00"
    # expected_time = "2024-11-13 12:30:00"
    # pick_up_time = "2024-11-13 12:30:00"

    # # Creating meal_items list for orders, ensuring correct format
    # # Creating meal_items list for orders, ensuring correct format
    # meal_items_order1 = [{"name": meal[0], "number": 3} for meal in meal_items1]
    # meal_items_order2 = [{"name": meal[0], "number": 2} for meal in meal_items2]
    # meal_item_order3 = [{"name": "椒麻雞套餐","number": 2}]
    # submit_order(order_time, expected_time, pick_up_time, True, True, "蝦換肉", "B10303097", "Rwatergun", meal_items_order1)

    # submit_order(order_time, expected_time, pick_up_time, False, False, "三高", "B10705009", "Rsilvfish", meal_items_order2)
    # submit_order(order_time, expected_time, pick_up_time, False, False, "三高", "B10303097", "Rsilvfish", meal_item_order3)

    return 0 



# Create tables using a SQL string
def create_tables(create_table_query):
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.execute(create_table_query)
        conn.commit()
        print("Successfully created tables")
    except Exception as e:
        conn.rollback()
        print(f"Failed to create tables: {e}")
    finally:
        cur.close()
        conn.close()




# ========================= query strings =========================#
create_table_query = '''
-- 資料表 CUSTOMER
CREATE TABLE IF NOT EXISTS CUSTOMER (
    c_id VARCHAR(9) PRIMARY KEY NOT NULL,
    c_name VARCHAR(20) NOT NULL,
    c_password VARCHAR(10) NOT NULL,
    c_phone_number VARCHAR(10) UNIQUE NOT NULL
);
-- 資料表 RESTAURANT
CREATE TABLE IF NOT EXISTS RESTAURANT (
    r_id VARCHAR(10) PRIMARY KEY NOT NULL,
    r_name VARCHAR(20) UNIQUE NOT NULL,
    r_password VARCHAR(10) NOT NULL,
    location VARCHAR(10) UNIQUE NOT NULL
);

-- 資料表 REGULAR_OPEN_TIME
CREATE TABLE  IF NOT EXISTS REGULAR_OPEN_TIME (
    r_id VARCHAR(10) NOT NULL,
    day CHAR(3) NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    PRIMARY KEY (r_id, day),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 ORDER
CREATE TABLE  IF NOT EXISTS "ORDER" (
    o_id BIGSERIAL PRIMARY KEY, -- 使用 BIGSERIAL 自動生成 o_id
    order_time TIMESTAMP NOT NULL,
    expected_time TIMESTAMP NOT NULL,
    pick_up_time TIMESTAMP NOT NULL,
    eating_utensil BOOLEAN NOT NULL,
    plastic_bag BOOLEAN NOT NULL,
    note VARCHAR(100),
    c_id VARCHAR(9) NOT NULL,
    star_num INT,
    review VARCHAR(50),
    r_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (c_id) REFERENCES CUSTOMER(c_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 COUPON
CREATE TABLE IF NOT EXISTS COUPON (
    coup_id BIGSERIAL PRIMARY KEY NOT NULL,
    discount_rate FLOAT NOT NULL CHECK (discount_rate IN (0.7, 0.75, 0.8, 0.85, 0.9)),
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    used_on_id BIGINT UNIQUE,
    owner_id VARCHAR(9) NOT NULL,
    FOREIGN KEY (used_on_id) REFERENCES "ORDER"(o_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES CUSTOMER(c_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 HOLIDAY
CREATE TABLE IF NOT EXISTS HOLIDAY (
    date DATE PRIMARY KEY NOT NULL,
    description VARCHAR(255)
);

-- 資料表 MEAL_ITEM
CREATE TABLE IF NOT EXISTS MEAL_ITEM (
    name VARCHAR(10) NOT NULL,
    r_id VARCHAR(10) NOT NULL,
    price INT NOT NULL,
    processing_time INT,
    PRIMARY KEY (name, r_id),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 INCLUDE_MEAL_IN_ORDER
CREATE TABLE IF NOT EXISTS INCLUDE_MEAL_IN_ORDER (
    name VARCHAR(10) NOT NULL,
    o_id BIGSERIAL NOT NULL,
    r_id VARCHAR(10) NOT NULL,
    number INT NOT NULL,
    PRIMARY KEY (name, o_id, r_id),
    FOREIGN KEY (name, r_id) REFERENCES MEAL_ITEM(name, r_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (o_id) REFERENCES "ORDER"(o_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 CLOCK_IN
CREATE TABLE IF NOT EXISTS CLOCK_IN (
    r_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    PRIMARY KEY (r_id, date),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 SERVE_MEAL
CREATE TABLE IF NOT EXISTS SERVE_MEAL (
    r_id VARCHAR(10) NOT NULL,
    name VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    supply_num INT NOT NULL CHECK (supply_num >= 0),
    remaining_num INT NOT NULL CHECK (remaining_num >= 0),
    PRIMARY KEY (r_id, name, date),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (name, r_id) REFERENCES MEAL_ITEM(name, r_id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''


if __name__ == "__main__":
    psql_conn = connect_to_database()
    cur = psql_conn.cursor()
    db_init()
     # commit the change to database server
    psql_conn.commit()
    cur.close()
    psql_conn.close()