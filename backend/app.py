""""
Main File Of Backend
"""

from flask import Flask
from flask_cors import CORS

# import api file
from ApiAuthentication import authentication_bp
from ApiCustomer import CustomerApi_bp
from ApiAdmin import AdminApi_bp
from ApiRestaurant import RestaurantApi_bp

# import customized library
from databaseInit import db_init

app = Flask(__name__)
app.register_blueprint(authentication_bp)
app.register_blueprint(CustomerApi_bp)
app.register_blueprint(AdminApi_bp)
app.register_blueprint(RestaurantApi_bp)
CORS(app)

if __name__ == '__main__':
    # db_init()
    app.run(host="0.0.0.0", port=5000)
