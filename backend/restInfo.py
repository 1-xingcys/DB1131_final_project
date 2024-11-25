# Library
from flask import jsonify, Blueprint
from database import select_restaurant_reg_info

resInfo_bp = Blueprint('restInfo', __name__)

# function with no paremeter
@resInfo_bp.route('/restaurant/info/regular', methods=['GET'])
def Rest_reg_info():
  result = select_restaurant_reg_info()
  return jsonify(result)