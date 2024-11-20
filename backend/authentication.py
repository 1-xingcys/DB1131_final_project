# authentication
from flask import jsonify, request, Blueprint

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
    pass


def check_restaurant(r_id, pwd) -> bool :
    # TODO
    pass
    



    

