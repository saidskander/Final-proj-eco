#!/usr/bin/env python3

from flask import render_template, redirect, url_for  # 1
from flask import request, session  # 1
from pet_shop import app, db  # 1
from pet_shop import bcrypt  # 3
from flask import flash  # 2
from .forms import RegistrationForm  # 2
from .forms import LoginForm
from .models import User  # 3
import os  # 3


@app.route("/favicon.ico", methods=['GET', 'POST'])
def favicon():
    return "", 200


@app.route('/')
@app.route('/admin', methods=['GET', 'POST'])  # 1
def home():  # 1
    """simple return string"""
    """return"Welcom to my new pet store"  # 1"""
    return render_template("home.html", title="Admin Dashbord")


@app.route('/login', methods=['GET', 'POST'])  # 1
def login():  # 1
    """login"""
    form = LoginForm(request.form)  # 4
    if request.method == 'POST' and form.validate():  # 4
        user = User.query.filter_by(email = form.email.data).first()  # 4
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # 4
            session["email"] = form.email.data
            flash(f'Welcom {form.email.data}',"success")  # 4
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash("wrong password", "danger")
    return render_template("login.html", form=form, title="login")  # 1


@app.route('/register', methods=['GET', 'POST'])  # 2
def register():  # 2
    """registration forms"""
    form = RegistrationForm(request.form)  # 2
    if request.method == 'POST' and form.validate():  # 2
        hash_password = bcrypt.generate_password_hash(form.
                                                      password.
                                                      data)  # 3
        user = User(username=form.username.data,
                    name=form.name.data,
                    email=form.email.data,
                    password=hash_password)  #  "",2,3
        db.session.add(user)  #  "",2,3
        db.session.commit()  # 3
        flash(f'Welcom {form.name.data}, your account has been created',"success")  # 2
        return redirect(url_for('home'))  # 2
    return render_template('register.html', form=form, title="Register")  # 2

