#!/usr/bin/env python3
from pet_shop import db  # 3
"""https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/"""
from pet_shop import login_manager, app
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

"""
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
"""


"""takes user id as an argumment"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
product_members = db.Table('product_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('newproduct_id', db.Integer, db.ForeignKey('newproduct.id'))
)
"""


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="default.png")  # 3
    password = db.Column(db.String(60), unique=False, nullable=False)

    newproducts = db.relationship('NewProduct', backref='user', lazy="joined")
    brandnames = db.relationship('BrandName', backref='user', lazy=True)
    categorynames = db.relationship('CategoryName', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):  # 3
        """ return '<User %r>' % self.username  # 3 """
        return f"User(username='{self.username}',Email='{self.email}', image_file='{self.image_file}', password='{self.password})"



db.create_all()
db.session.commit()
