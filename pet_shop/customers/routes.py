#!/usr/bin/env python3

from crypt import methods
from itertools import product
import os
from warnings import catch_warnings
from flask import render_template, redirect, url_for  # 1
from flask import request, session  # 1
from pet_shop import app, db  # 1
from pet_shop import bcrypt, mail  # 3
from flask import flash

from pet_shop.products.routes import brand, category  # 2
from .forms import RegistrationForm, ResetPasswordForm, RequestResetForm
from .forms import LoginForm
from .models import CustomerUser  # 3
from pet_shop.products.models import NewProduct, BrandName, CategoryName
from flask_login import login_user, current_user
from flask_mail import Message

@app.route("/favicon.ico", methods=['GET', 'POST'])
def favicon_icon():
    return "", 200

"""
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('CustomerLanding'))
"""

@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def CustomerP():
    page = request.args.get("page", 1, type=int)
    CustomerProduct = NewProduct
    brands = BrandName.query.join(CustomerProduct, (BrandName.id == CustomerProduct.brand_id)).all()
    categories = CategoryName.query.join(CustomerProduct, (CategoryName.id == CustomerProduct.category_id)).all()
    products = CustomerProduct.query.filter(CustomerProduct.stock > 0).paginate(page=page, per_page=6)
    return render_template("CustomerP/CustomerProduct.html", title="Welcom", products=products, brands=brands, categories=categories)

@app.route("/get_brand/<int:id>")
def Display_brands(id):
    """get brand"""
    page = request.args.get("page", 1, type=int)
    """Model variable"""
    CustomerProduct = NewProduct
    """query filter by id (this query for pagination url_for)"""
    b = CategoryName.query.filter_by(id=id).first_or_404()
    """get and display brands in shop with pagination"""
    brand = CustomerProduct.query.filter_by(brand=b).paginate(page=page, per_page=6)
    """join statement for brands and categories"""
    brands = BrandName.query.join(CustomerProduct, (BrandName.id == CustomerProduct.brand_id)).all()
    categories = CategoryName.query.join(CustomerProduct, (CategoryName.id == CustomerProduct.category_id)).all()
    return render_template('CustomerP/CustomerProduct.html', page=page, brand=brand, brands=brands, categories=categories, CustomerProduct=CustomerProduct, b=b)


@app.route("/Product_detail/<int:id>")
def Product_detail(id):
    """Unique product detail"""
    category = NewProduct.query.get_or_404(id)
    brand = NewProduct.query.get_or_404(id)
    product = NewProduct.query.get_or_404(id)
    return render_template('CustomerP/product-details.html', product=product, brand=brand, category=category)


@app.route("/get_categories/<int:id>")
def Display_categories(id):
    page = request.args.get("page", 1, type=int)
    """get categories"""
    CustomerProduct = NewProduct
    """query filter by id (this query for pagination url_for)"""
    c = CategoryName.query.filter_by(id=id).first_or_404()
    """get and display categories in shop with pagination"""
    category = CustomerProduct.query.filter_by(category=c).paginate(page=page, per_page=6)
    """join statement for brands and categories"""
    brands = BrandName.query.join(CustomerProduct, (BrandName.id == CustomerProduct.brand_id)).all()
    categories = CategoryName.query.join(CustomerProduct, (CategoryName.id == CustomerProduct.category_id)).all()
    return render_template('CustomerP/CustomerProduct.html', page=page, category=category, brands=brands, categories=categories, c=c)


@app.route('/CustomerLanding', methods=['GET', 'POST'])
def CustomerLanding():
    """simple return string"""
    return render_template("CustomerLanding.html", title="Welcom")


@app.route('/CustomerLogin', methods=['GET', 'POST'])
def CustomerLogin():
    """login"""
    #if current_user.is_authenticated:
        #return redirect(url_for('CustomerLanding'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = CustomerUser.query.filter_by(email = form.email.data).first()  # 4
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # 4
            session["email"] = form.email.data
            flash(f'Welcom {form.email.data}',"success")
            return redirect(request.args.get('next') or url_for('CustomerLanding'))
        else:
            flash("wrong password", "danger")
    return render_template("CustomerLogin.html", form=form, title="login")  # 1


@app.route('/CustomerRegister', methods=['GET', 'POST'])
def CustomerRegister():
    """registration forms"""
    #if current_user.is_authenticated:
        #return redirect(url_for('CustomerLanding'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.
                                                      password.
                                                      data).decode("utf-8")
        user = CustomerUser(username=form.username.data,
                    name=form.name.data,
                    email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcom {form.name.data}, your account has been created',"success")  # 2
        return redirect(url_for('CustomerLogin'))
    return render_template('CustomerRegister.html', form=form, title="Register")  # 2

# Password Reset

def Customer_send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@skander.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply you dont have to do anything and plz ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/Customer_reset_password", methods=['GET', 'POST'])
def Customer_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('CustomerLanding'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = CustomerUser.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('CustomerLogin'))
    return render_template('customer_email/reset_request.html', title='Reset Password', form=form)


@app.route("/Customer_reset_password/<token>", methods=['GET', 'POST'])
def Customer_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('CustomerLanding'))
    user = CustomerUser.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can log in now!', 'success')
        return redirect(url_for('CustomerLogin'))
    return render_template('customer_email/reset_token.html', title='Reset Password', form=form)
