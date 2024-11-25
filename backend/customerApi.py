# Library
from flask import jsonify, request, Blueprint
from database import select_restaurant_reg_info, connect_to_database

CustomerApi_bp = Blueprint('restInfo', __name__)

""""
API Interface for Customer
"""

@CustomerApi_bp.route('/restaurant/info/regular', methods=['GET'])
def Rest_reg_info():
  result = select_restaurant_reg_info()
  return jsonify(result)

@CustomerApi_bp.route('/customer/cname', methods=['POST'])
def GetCName() :
  data = request.json
  c_id = data.get('username')
  name = getCName(c_id)
  
  if name :
    return jsonify({"name": name}), 200
  else :
    return jsonify({"error": "Customer name does not exist"}), 401


""""
Internal Function
"""

def getCName(c_id) :
  psql_conn = connect_to_database()
  cur = psql_conn.cursor()

  query = '''
  SELECT c_name
  FROM CUSTOMER
  WHERE c_id = %s
  '''
  cur.execute(query, (c_id,))

  # get the res
  result = cur.fetchone()

  cur.close()
  psql_conn.close()
  
  if result:
      return result[0]
  else:
      return None