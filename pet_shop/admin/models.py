#!/usr/bin/env python3
from pet_shop import db  # 3
"""https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/"""
class User(db.Model):  # 3
    id = db.Column(db.Integer, primary_key=True)  # 3
    name = db.Column(db.String(30), unique=False, nullable=False)  # 3
    username = db.Column(db.String(30), unique=True, nullable=False)  # 3
    email = db.Column(db.String(120), unique=True, nullable=False)  # 3
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="default.png")  # 3
    password = db.Column(db.String(60), unique=False, nullable=False)  # 3

    def __repr__(self):  # 3
        """ return '<User %r>' % self.username  # 3 """
        return f"User(username='{self.username}',Email='{self.email}', image_file='{self.image_file}', password='{self.password})"


db.create_all()
