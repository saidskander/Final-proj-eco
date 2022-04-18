#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, TextAreaField, StringField, SubmitField, FloatField
from wtforms import validators, form
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length, NoneOf
from pet_shop.admin.models import BrandName, CategoryName
import re
"""
fixed/read more:
https://stackoverflow.com/questions/19612186/
forms-contactform-object-has-no-attribute-hidden-tag
"""
from flask_wtf import FlaskForm  # 4
from flask_wtf.file import FileField, FileAllowed, FileRequired  # 5


class NewProduct_forms(FlaskForm):  # 4
    """empty string in this StringField, pref my own my own on html"""
    name = StringField('name', [validators.DataRequired(), validators.Length(min=2, max=15)])

    price = IntegerField('price', [validators.DataRequired()])
    discount = IntegerField('', [validators.DataRequired()])
    stock = IntegerField('', [validators.DataRequired()])

    colors = TextAreaField('', [validators.DataRequired()])
    discription = TextAreaField('', [validators.DataRequired()])

    image_1 = FileField('img 1', validators=[FileRequired(), FileAllowed(["png"])])
    image_2 = FileField('img 2', validators=[FileRequired(), FileAllowed(["png"])])
    image_3 = FileField('img 3', validators=[FileRequired(), FileAllowed(["png"])])


    submit = SubmitField("")


class Brand_Forms(FlaskForm):  # 4
    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.DataRequired(), validators.Length(min=3, max=12)])
    submit = SubmitField("")

    def validate_name(self, field):  # 4y
        brand = BrandName.query.filter_by(name=field.data).first()
        if brand:  # 4
            raise ValidationError('Brand exist')  # 4


class Category_Forms(FlaskForm):  # 4
    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.DataRequired(), validators.Length(min=3, max=12)])
    submit = SubmitField("")
    """
       Big note..!!! validate_name was not working
       because i used the data form in one class form while there is different       model classes(calass:CategoryName, BrandName)

       i can use name validate_name(self, name) instead like class Brand_Forms       another big note and very strange .. if i change the
       def validate_name it will not gonna work
       will search for this later
    """
    def validate_name(self, field):  # 4
        categ = CategoryName.query.filter_by(name=field.data).first()
        if categ:  # 4
            raise ValidationError('category exist')  # 4
