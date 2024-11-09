# This file is an api file

# Library
from flask import jsonify, request, Blueprint
import time

# import customized library
from utils import dataBase_connect

search_bp = Blueprint('search', __name__)

# function with some paremeters
@search_bp.route('/api/search', methods=['POST'])
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