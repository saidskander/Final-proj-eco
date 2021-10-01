#!/usr/bin/env python3

from pet_shop import db  # 4

class BrandName(db.Model):  # 4
    name = db.Column(db.String(30), unique=True, nullable=False)  # 4
    id = db.Column(db.Integer, primary_key=True)  # 4

    def __repr__(self):  # 4
        return '<BrandName %r>' % self.name  # 4

class CategoryName(db.Model):  # 4
    name = db.Column(db.String(30), unique=True, nullable=False)  # 4
    id = db.Column(db.Integer, primary_key=True)  # 4

    def __repr__(self):  # 4
        return '<CategoryName %r>' % self.name  # 4

db.create_all()
