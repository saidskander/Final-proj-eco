#!/usr/bin/env python3

from flask import url_for, redirect, render_template  # 4
from flask import flash, request, session
from pet_shop import db, app, photos  # 4
from pet_shop.admin.models import BrandName, CategoryName, NewProduct  # 4
from pet_shop.admin.models import User
from .forms import NewProduct_forms, Brand_Forms, Category_Forms
from flask_login import current_user
import secrets
import os




def brands():
    brands = BrandName.query.join(NewProduct, (BrandName.id == NewProduct.brand_id)).all()
    return brands

def categories():
    categories = CategoryName.query.join(NewProduct,(CategoryName.id == NewProduct.category_id)).all()
    return categories

def products():
    products = NewProduct.query.join(User,(NewProduct.id == User.newproduct_id)).all()
    return products


# @app.route('/')
@app.route('/AdminProducts', methods=['GET', 'POST'])
def AdminProducts():
    """products """
    """products = NewProduct.query.all()"""
    products = NewProduct.query.filter_by(user=current_user)\
        .order_by(NewProduct.pub_date.desc()).all()
    """products = current_user.newproducts"""
    return render_template('products.html', products=products)

@app.route("/NewProduct", methods=['GET','POST'])
def New_Product():
    brands = BrandName.query.all()
    categories = CategoryName.query.all()
    form = NewProduct_forms(request.form)
    if request.method=="POST" and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        product = NewProduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(product)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('New_Product'))
    return render_template('newproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)  # 4
# title='Add a Product', brands=brands,categories=categories


@app.route("/newcateg", methods=['GET','POST'])
def New_Category():
    categories = CategoryName.query.all()
    form = Category_Forms(request.form)
    """add categories withs spesific form"""
    if request.method == 'POST' and form.validate():
        category = CategoryName(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f"your {form.name.data} has been aded","success")
    else:
        flash("plz add the forms")
    category = request.form.get('category')
    return render_template('newcategory.html', Category_Forms="Category_Forms", form=form, categories=categories)  # 4



@app.route("/newbrand", methods=['GET','POST'])
def New_Brand():
    brands = BrandName.query.all()
    form = Brand_Forms(request.form)
    """add categories withs spesific form"""
    if request.method == 'POST' and form.validate():
        brand = BrandName(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f"your {form.name.data} has been aded","success")
        brand = request.form.get('brand')
    else:
        flash("plz add the forms")
    return render_template('newbrand.html',  Brand_Forms="Brand_Forms", form=form, brands=brands)
