#!/usr/bin/python3

from flask import Flask  # 1
from flask_sqlalchemy import SQLAlchemy  # 1

"""
Start sqlalchemy
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
"""
app = Flask(__name__)  # 1
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_shop.db'  # 1
db = SQLAlchemy(app)  # 1

from pet_shop import routes  # noqa: E402 # 1
