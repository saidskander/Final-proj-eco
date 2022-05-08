#!/usr/bin/env python3

from flask import render_template, redirect, url_for  # 1
from flask import request, session  # 1
from pet_shop import app, db  # 1
from pet_shop import bcrypt, mail  # 3
from flask import flash  # 2
from .forms import RegistrationForm, ResetPasswordForm, RequestResetForm
from .forms import LoginForm
from .models import User  # 3
#from pet_shop.products.models import BrandName
from flask_login import current_user, logout_user, login_user
from flask_mail import Message
import os


@app.route("/favicon.ico", methods=['GET', 'POST'])
def favicon():
    return "", 200


@app.route('/')
@app.route('/AdminHome', methods=['GET', 'POST'])  # 1
def AdminHome():  # 1
    """simple return string"""
    """return Welcom to your admin page"""
    """form = LoginForm(request.form)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
    """
    return render_template("admin.html", title="Admin")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('AdminHome'))


@app.route('/AdminLogin', methods=['GET', 'POST'])  # 1
def AdminLogin():  # 1
    """login"""
    if current_user.is_authenticated:
        return redirect(url_for('AdminHome'))
    form = LoginForm(request.form)  # 4
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()  # 4
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('AdminHome'))
            flash(f'Welcom {form.email.data}',"success")  # 4
        else:
            flash("wrong password", "danger")
    return render_template("AdminLogin.html", form=form, title="login")  # 1


@app.route('/AdminRegister', methods=['GET', 'POST'])  # 2
def AdminRegister():  # 2
    """registration forms"""
    if current_user.is_authenticated:
        return redirect(url_for('AdminHome'))
    form = RegistrationForm(request.form)  # 2
    if request.method == 'POST' and form.validate():  # 2
        hash_password = bcrypt.generate_password_hash(form.
                                                      password.
                                                      data).decode("utf-8")  # 3
        user = User(username=form.username.data,
                    name=form.name.data,
                    email=form.email.data,
                    password=hash_password)  #  "",2,3
        db.session.add(user)  #  "",2,3
        db.session.commit()  # 3
        flash(f'Welcom {form.name.data}, your account has been created',"success")  # 2
        return redirect(url_for('AdminLogin'))  # 2
    return render_template('AdminRegister.html', form=form, title="Register")  # 2

# Password Reset

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@skander.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply you dont have to do anything and plz ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('AdminHome'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('AdminLogin'))
    return render_template('admin_email/reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('AdminHome'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can log in now!', 'success')
        return redirect(url_for('AdminLogin'))
    return render_template('admin_email/reset_token.html', title='Reset Password', form=form)
