# authentication
from flask import jsonify, request, Blueprint
from database import connect_to_database
authentication_bp = Blueprint('authentication',__name__)



""""
API Interface for Authentication
"""

@authentication_bp.route('/authentication/customer', methods=['POST'])
def authentication_customer():
    #####################################################
    # Using Flask.request to get paremeters from frontend
    data = request.json
    c_id = data.get('username')
    pwd = data.get('password')
    #####################################################

    if not c_id or not pwd:
        return jsonify({"error": "Missing c_id or password"}), 400

    is_valid = check_customer(c_id, pwd)
    if is_valid:
        return jsonify({"message": "Customer authenticated successfully"}), 200
    else:
        return jsonify({"error": "Invalid customer credentials"}), 401


@authentication_bp.route('/authentication/restaurant', methods=['POST'])
def authentication_restaurant():
    data = request.json
    r_id = data.get('username')
    pwd = data.get('password')

    if not r_id or not pwd:
        return jsonify({"error": "Missing r_id or password"}), 400

    is_valid = check_restaurant(r_id, pwd)
    if is_valid:
        return jsonify({"message": "Restaurant authenticated successfully"}), 200
    else:
        return jsonify({"error": "Invalid restaurant credentials"}), 401



""""
Internal Function
"""

def check_customer(c_id, pwd) -> bool :
    psql_conn = connect_to_database()
    cur = psql_conn.cursor()

     # add a customer
    add_customer_query = '''
    SELECT EXISTS(
        SELECT *
        FROM CUSTOMER
        WHERE c_id = %s AND c_password = %s
    );
    '''
    cur.execute(add_customer_query, (c_id, pwd))

    # get the res
    result = cur.fetchone()[0]

    cur.close()
    psql_conn.close()
    
    if result:
        return True
    else:
        return False


def check_restaurant(r_id, pwd) -> bool :
    psql_conn = connect_to_database()
    cur = psql_conn.cursor()

     # add a customer
    check_restaurant_query = '''
    SELECT EXISTS(
        SELECT *
        FROM RESTAURANT
        WHERE r_id = %s AND r_password = %s
    );
    '''
    cur.execute(check_restaurant_query, (r_id, pwd))

    result = cur.fetchone()[0]

    cur.close()
    psql_conn.close()

    if result:
        return True
    else:
        return False
    




    

