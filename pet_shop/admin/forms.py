#!/usr/bin/env python3


from wtforms import BooleanField, StringField  # 2
from wtforms import PasswordField, validators  # 2
"""
fixed/read more:
https://stackoverflow.com/questions/19612186/
forms-contactform-object-has-no-attribute-hidden-tag
"""
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):  # 2

    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.Length(min=4, max=25)])  # 2

    """empty string in this StringField, used my own on html"""
    username = StringField('', [validators.Length(min=4, max=25)])  # 2

    """empty string in this StringField, used my own on html"""
    email = StringField('', [validators.Length(min=6, max=35),
                                          validators.Email()])  # 2

    """empty string in this PasswordField, used my own in html"""
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])  # 2

    """empty string in this PasswordField, used my own in html"""
    confirm = PasswordField('')  # 2
