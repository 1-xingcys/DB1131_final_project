# This the main file of backend

# Library
from flask import Flask
from flask_cors import CORS

# import api file
from authentication import authentication_bp
from customerApi import CustomerApi_bp

# import customized library
from database import db_init

app = Flask(__name__)
app.register_blueprint(authentication_bp)
app.register_blueprint(CustomerApi_bp)
CORS(app)

if __name__ == '__main__':
    db_init()
    app.run(host="0.0.0.0", port=5000)
