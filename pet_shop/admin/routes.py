#!/usr/bin/env python3

from flask import render_template, redirect, url_for  # 1
from flask import request, session  # 1
from pet_shop import app, db  # 1
from flask import flash  # 2
from .forms import RegistrationForm  # 2


@app.route('/')  # 1
def PStore():  # 1
    """simple return string"""
    return"Welcom to my new pet store"  # 1


@app.route('/login', methods=['GET', 'POST'])  # 1
def login():  # 1
    """login"""
    return render_template("login.html", title="login")  # 1


@app.route('/register', methods=['GET', 'POST'])  # 2
def register():  # 2
    """registration forms"""
    form = RegistrationForm(request.form)  # 2
    if request.method == 'POST' and form.validate():  # 2
        """user = User(form.username.data, form.email.data,
                    form.password.data)  # 2
        db_session.add(user)  # 2"""
        flash('Thanks for registering')  # 2
        return redirect(url_for('login'))  # 2
    return render_template('register.html', form=form, title="Register")  # 2
