#!/usr/bin/env python3
from pet_shop import db
"""https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/"""
from pet_shop import login_manager, app
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class CustomerUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="default.png")  # 3
    password = db.Column(db.String(60), unique=False, nullable=False)

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
        return CustomerUser.query.get(user_id)

    def __repr__(self):
        """ return '<CustomerUser %r>' % self.username  # 3 """
        return f"CustomerUser(username='{self.username}',Email='{self.email}', image_file='{self.image_file}', password='{self.password})"


db.create_all()
