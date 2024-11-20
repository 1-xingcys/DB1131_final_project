# database.py
import psycopg2
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# TODO

def add_customer(c_id, name, pwd, phone_no):
    pass

def add_restaurant(r_id, name, pwd, location):
    pass

def select_restaurant() -> list:    
    pass

def select_meal_item(r_id) -> list:
    pass

def submit_order(order_time, expected_time, pick_up_time, eating_utensil, plastic_bag, note, c_id, r_id, meal_item : list) -> None:
    pass



def db_init() :
    create_tables(create_table_query)
    
    return 0 















# Connect to the database
def connect_to_database():
    for i in range(5):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            print("Database connected successfully")
            return conn
        except psycopg2.OperationalError:
            print("Database not ready, retrying in 3 seconds...")
            time.sleep(3)
    raise Exception("Database connection failed after retries")

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

# Insert data_to_insert using a SQL string
def insert_data(insert_query, data_to_insert):
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.executemany(insert_query, data_to_insert)
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert data_to_insert: {e}")
    finally:
        cur.close()
        conn.close()














# ========================= query strings =========================#
create_table_query = '''
-- 資料表 CUSTOMER
CREATE TABLE CUSTOMER (
    c_id BIGINT PRIMARY KEY NOT NULL,
    c_name VARCHAR(20) NOT NULL,
    c_password VARCHAR(10) NOT NULL,
    c_phone_number VARCHAR(10) UNIQUE NOT NULL
);
-- 資料表 RESTAURANT
CREATE TABLE RESTAURANT (
    r_id BIGINT PRIMARY KEY NOT NULL,
    r_name VARCHAR(20) UNIQUE NOT NULL,
    r_password VARCHAR(10) NOT NULL,
    location VARCHAR(10) UNIQUE NOT NULL
);

-- 資料表 REGULAR_OPEN_TIME
CREATE TABLE REGULAR_OPEN_TIME (
    r_id BIGINT NOT NULL,
    day CHAR(3) NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    PRIMARY KEY (r_id, day),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 ORDER
CREATE TABLE "ORDER" (
    o_id BIGINT PRIMARY KEY NOT NULL,
    order_time TIMESTAMP NOT NULL,
    expected_time TIMESTAMP NOT NULL,
    pick_up_time TIMESTAMP NOT NULL,
    eating_utensil BOOLEAN NOT NULL,
    plastic_bag BOOLEAN NOT NULL,
    note VARCHAR(100),
    c_id BIGINT NOT NULL,
    star_num INT,
    review VARCHAR(50),
    r_id BIGINT NOT NULL,
    FOREIGN KEY (c_id) REFERENCES CUSTOMER(c_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 COUPON
CREATE TABLE COUPON (
    coup_id BIGINT PRIMARY KEY NOT NULL,
    discount_rate FLOAT NOT NULL CHECK (discount_rate IN (0.7, 0.75, 0.8, 0.85, 0.9)),
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    used_on_id BIGINT UNIQUE,
    owner_id BIGINT NOT NULL,
    FOREIGN KEY (used_on_id) REFERENCES "ORDER"(o_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES CUSTOMER(c_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 BUSINESS_DAY
CREATE TABLE BUSINESS_DAY (
    date DATE PRIMARY KEY NOT NULL,
    is_holiday BOOLEAN NOT NULL
);

-- 資料表 MEAL_ITEM
CREATE TABLE MEAL_ITEM (
    name VARCHAR(10) NOT NULL,
    r_id BIGINT NOT NULL,
    price INT NOT NULL,
    processing_time INT,
    PRIMARY KEY (name, r_id),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 INCLUDE_MEAL_IN_ORDER
CREATE TABLE INCLUDE_MEAL_IN_ORDER (
    name VARCHAR(10) NOT NULL,
    o_id BIGINT NOT NULL,
    r_id BIGINT NOT NULL,
    number INT NOT NULL,
    PRIMARY KEY (name, o_id, r_id),
    FOREIGN KEY (name, r_id) REFERENCES MEAL_ITEM(name, r_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (o_id) REFERENCES "ORDER"(o_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 CLOCK_IN
CREATE TABLE CLOCK_IN (
    r_id BIGINT NOT NULL,
    date DATE NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    PRIMARY KEY (r_id, date),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (date) REFERENCES BUSINESS_DAY(date) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 資料表 SERVE_MEAL
CREATE TABLE SERVE_MEAL (
    r_id BIGINT NOT NULL,
    name VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    supply_num INT NOT NULL CHECK (supply_num >= 0),
    PRIMARY KEY (r_id, name, date),
    FOREIGN KEY (r_id) REFERENCES RESTAURANT(r_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (name, r_id) REFERENCES MEAL_ITEM(name, r_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (date) REFERENCES BUSINESS_DAY(date) ON DELETE CASCADE ON UPDATE CASCADE
);
'''
