# This file is an api file

# Library
from flask import jsonify, Blueprint
import time

hello_bp = Blueprint('hello', __name__)

# function with no paremeter
@hello_bp.route('/api/hello', methods=['GET'])
def hello():
    time.sleep(2)
    return jsonify(message="厲害👍")