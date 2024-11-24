# This file define some function that would be shared to many api
# api files will import this file as customized library 

import psycopg2
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# check we can connect and interact with database
def db_init() :
    psql_conn = dataBase_connect()
    cur = psql_conn.cursor()

    # create a table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS simple_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );
    '''
    cur.execute(create_table_query)
    
    insert_query = '''
    INSERT INTO simple_table (name) VALUES (%s);
    '''
    # insert some data
    data_to_insert = [
        ('Alice',),
        ('Bob',),
        ('Charlie',)
    ]

    cur.executemany(insert_query, data_to_insert)
    
    # commit the change to database server
    psql_conn.commit()

    cur.close()
    psql_conn.close()
    return 0

def dataBase_connect() :
    for i in range(5) :
        try:
            conn = psycopg2.connect(DATABASE_URL)
            print("Database connected successfully")
            return conn
        except psycopg2.OperationalError:
            print("Database not ready, retrying in 3 seconds...")
            time.sleep(3)
    raise Exception("Database connection failed after retries")
