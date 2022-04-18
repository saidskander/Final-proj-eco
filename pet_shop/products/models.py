"""
#!/usr/bin/env python3
from pet_shop import db  # 4
from datetime import datetime
#from pet_shop.admin.models import User
"""

"""
class NewProduct(db.Model):
    __tablename__ = 'New_Product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')
    price = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None), nullable=False)

#    price = db.Column(db.Numeric(10.2), nullable=False)
    discount = db.Column(db.Integer, default=0)

    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('CategoryName',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('BrandName',backref=db.backref('brands', lazy=True))

#   product_id = db.Column(db.ForeignKey('product.id'),nullable=False)
# product = db.relationship('User', backref=db.backref("products", lazy=True))


    def __repr__(self):
        # return '<NewProduct %r>' % self.name
        return f"NewProduct('{self.name}', '{self.image_1}', '{self.price}', '{self.discount}', '{self.stock}', '{self.colors}', '{self.pub_date}', '{self.brand_id}')"

class BrandName(db.Model):  # 4
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)  # 4
    name = db.Column(db.String(30), unique=True, nullable=False)  # 4

    def __repr__(self):  # 4
        return '<BrandName %r>' % self.name  # 4

class CategoryName(db.Model):  # 4
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)  # 4
    name = db.Column(db.String(30), unique=True, nullable=False)  # 4

    def __repr__(self):  # 4
        return '<CategoryName %r>' % self.name  # 4


db.create_all()

"""
