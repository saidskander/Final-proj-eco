#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, TextAreaField, StringField, SubmitField, FloatField
from wtforms import validators, form
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length, NoneOf
from .models import BrandName, CategoryName
import re
"""
fixed/read more:
https://stackoverflow.com/questions/19612186/
forms-contactform-object-has-no-attribute-hidden-tag
"""
from flask_wtf import FlaskForm  # 4
from flask_wtf.file import FileField, FileAllowed, FileRequired  # 5


class NewProduct_forms(FlaskForm):
    """empty string in this StringField, pref my own my own html placeholder"""
    name = StringField('', [validators.DataRequired(), validators.Length(min=2, max=15)])

    price = IntegerField('', [validators.DataRequired("This field is required, And only numbers allowed")])
    discount = IntegerField('', [validators.InputRequired("This field is required, And only numbers allowed"), validators.NumberRange(min=0,max=100)])
    stock = IntegerField('', [validators.InputRequired("This field is required, And only numbers allowed"), validators.NumberRange(min=0,max=100)])
    colors = StringField('', [validators.DataRequired("maximum letters 50"), validators.Length(max=50)])
    desc = TextAreaField('', [validators.DataRequired("maximum letters 300"), validators.Length(max=300)])

    image_1 = FileField(validators=[FileAllowed(['jpg','png','jpeg'])])
    image_2 = FileField(validators=[FileAllowed(['jpg','png','jpeg'])])
    image_3 = FileField(validators=[FileAllowed(['jpg','png','jpeg'])])

    submit = SubmitField("")


class Brand_Forms(FlaskForm):
    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.DataRequired(""), validators.Length(max=12)])
    submit = SubmitField("")
    def validate_name(self, field):  # 4
        brand = BrandName.query.filter_by(name=field.data).first()
        if brand:  # 4
            raise ValidationError('Brand exist')  # 4


class Category_Forms(FlaskForm):  # 4
    """empty string in this StringField, used my own on html"""
    name = StringField('', [validators.DataRequired(), validators.Length(max=12)])
    submit = SubmitField("")
    """
       Big note..!!! validate_name was not working
       because i used the data form in one class form while there is different
       model classes(calass:CategoryName, BrandName)

       i can use name validate_name(self, name) instead like class Brand_Forms*
       another big note and very strange .. if i change the
       def validate_name it will not gonna work
       will search for this later {because i have only name in the form pfff}
    """
    def validate_name(self, field):  # 4
        categ = CategoryName.query.filter_by(name=field.data).first()
        if categ:  # 4
            raise ValidationError('category exist')  # 4
