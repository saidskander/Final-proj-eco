#!/usr/bin/env python3
from pet_shop import db, app  # 4
from datetime import datetime
from pet_shop.admin.models import User


"""Numeric"""
class NewProduct(db.Model):
    __tablename__ = 'newproduct'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_1 = db.Column(db.String(150), nullable=False, default='default.png')
    image_2 = db.Column(db.String(150), nullable=False, default='default.png')
    image_3 = db.Column(db.String(150), nullable=False, default='default.png')
    price = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None), nullable=False)
    #price = db.Column(db.Numeric(10.2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False, default="gjkgkj")
    desc = db.Column(db.Text, nullable=False, default="ghjgk")
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('CategoryName',backref=db.backref('categories', lazy=True))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('BrandName',backref=db.backref('brands', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')

    def __repr__(self):
        # return '<NewProduct %r>' % self.name
        return f"NewProduct('{self.name}', '{self.image_1}', '{self.price}', '{self.discount}','{self.stock}', '{self.colors}', '{self.pub_date}', '{self.brand_id}', '{self.brand}', '{self.category}')"


class BrandName(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return '<BrandName %r>' % self.name


class CategoryName(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return '<CategoryName %r>' % self.name
        

db.create_all()
db.session.commit()
