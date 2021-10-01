#!/usr/bin/python3

from flask import Flask  # 1
from flask_sqlalchemy import SQLAlchemy  # 1
from flask_bcrypt import Bcrypt

"""
Start sqlalchemy
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
"""
app = Flask(__name__)  # 1
bcrypt = Bcrypt(app)  # 3
app.config['SECRET_KEY'] = 'rzarzrzuaoiruzoprpuza'  #  when using template form.hidden and bcrypt package2-3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_shop.db'  # 1
db = SQLAlchemy(app)  # 1

from pet_shop.admin import routes  # noqa: E402 # 1
from pet_shop.AdminDash import routes  # noqa: E402 # 4
