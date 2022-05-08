#!/usr/bin/env python3


from wtforms import BooleanField, StringField, SubmitField
from wtforms import PasswordField, validators
from .models import User
from wtforms.validators import DataRequired
from wtforms.validators import Length, Email, EqualTo, email_validator
from wtforms.validators import Email, ValidationError

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


    """Username is taken"""  # 4
    def validate_username(self, username):  # 4
        register_user = User.query.filter_by(username=username.data).first()  # 4
        if register_user:  # 4
            raise ValidationError('Username is taken')  # 4

    """Email taken"""  # 4
    def validate_email(self, email):  # 4
        register_user = User.query.filter_by(email=email.data).first()  # 4
        if register_user:  # 4
            raise ValidationError('Email is taken')  # 4



class LoginForm(FlaskForm):  # 4


    """empty string in this StringField, used my own on html"""
    email = StringField('', [validators.Length(min=6, max=35),
                                          validators.Email()])  # 4

    """empty string in this PasswordField, used my own in html"""
    password = PasswordField('', [validators.DataRequired()])  # 4

    remember = BooleanField('Remember Me')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
