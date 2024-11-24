# authentication
from flask import jsonify, request, Blueprint
from database import connect_to_database
authentication_bp = Blueprint('authentication',__name__)



# function with some paremeters
@authentication_bp.route('/authentication/customer', methods=['POST'])
def authentication_customer():
    # TODO
    pass


@authentication_bp.route('/authentication/restaurant', methods=['POST'])
def authentication_restaurant():
    # TODO
    pass



def check_customer(c_id, pwd) -> bool :
    # TODO
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
    result = cur.fetchone()

    cur.close()
    psql_conn.close()

    if result is not None:
        return True
    else:
        return False


def check_restaurant(r_id, pwd) -> bool :
    # TODO
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

    result = cur.fetchone()

    cur.close()
    psql_conn.close()

    if result is not None:
        return True
    else:
        return False
    




    

