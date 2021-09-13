#!/usr/bin/env python3


from wtforms import Form, BooleanField, StringField  # 2
from wtforms import PasswordField, validators  # 2


class RegistrationForm(Form):  # 2
    name = StringField('Name', [validators.Length(min=4, max=25)])  # 2
    username = StringField('Username', [validators.Length(min=4, max=25)])  # 2
    email = StringField('Email Address', [validators.Length(min=6, max=35),
                                          validators.Email()])  # 2
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])  # 2
    confirm = PasswordField('Repeat Password')  # 2
