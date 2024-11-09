from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import duckdb
import psycopg2
import time
import os

app = Flask(__name__)
CORS(app)
DATABASE_URL = os.getenv("DATABASE_URL")

# function with no paremeter
@app.route('/api/hello', methods=['GET'])
def hello():
    time.sleep(2)
    return jsonify(message="厲害👍")


# function with some paremeters
@app.route('/api/search', methods=['POST'])
def search():
    time.sleep(0.3)
    print("request is :", request, flush=True)
    data = request.json 
    print(data, flush=True)
    user_input = data.get("sqlinput") 
    conn = dataBase_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM simple_table;")
    rows = cur.fetchall()
    conn.close()
    cur.close()
    column = ["hi"] * len(rows[0])
    for row in rows:
        print(row, flush=True)
    return jsonify(table=rows, column=column)

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

if __name__ == '__main__':
    db_init()
    
    app.run(host="0.0.0.0", port=5000)
