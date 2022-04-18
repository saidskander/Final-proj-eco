#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField  # 4
from wtforms import PasswordField, validators  # 4
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length  # 4
from .models import CategoryName, BrandName  # 4
"""
fixed/read more:
https://stackoverflow.com/questions/19612186/
forms-contactform-object-has-no-attribute-hidden-tag
"""
from flask_wtf import FlaskForm  # 4


class Category_Form(FlaskForm):  # 4
    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.DataRequired(), validators.Length(min=3, max=12)])
    submit = SubmitField("")

    """
       Big note..!!! validate_name was not working
       because i used the data form in one class form while there is different
       model classes(calass:CategoryName, BrandName)

       i can use name validate_name(self, name) instead like class Brand_Forms
       another big note and very strange .. if i change the
       def validate_name it will not gonna work
       will search for this later
    """
    def validate_name(self, field):  # 4
        categ = CategoryName.query.filter_by(name=field.data).first()
        if categ:  # 4
            raise ValidationError('category exist')  # 4


class Brand_Forms(FlaskForm):  # 4
    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.DataRequired(), validators.Length(min=3, max=12)])
    submit = SubmitField("")

    def validate_name(self, name):  # 4y
        brand = BrandName.query.filter_by(name=name.data).first()
        if brand:  # 4
            raise ValidationError('Brand exist')  # 4
