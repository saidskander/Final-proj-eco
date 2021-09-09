#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////eco.db'
db = SQLAlchemy(app)

if True:  # noqa: E402
    from pet_shop import routes
    ...
