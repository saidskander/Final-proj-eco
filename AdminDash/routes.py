#!/usr/bin/env python3

from flask import url_for, redirect, render_template  # 4
from flask import flash, request  # 4
from pet_shop import db, app  # 4
from .models import BrandName, CategoryName  # 4
from .forms import Category_Form, Brand_Forms  # 4
import secrets
import os  # 4



@app.route("/newbrand", methods=['GET','POST'])  # 4
def NewBrand():  # 4
    form = Brand_Forms(request.form)  # 4
    """add categories withs spesific form"""
    if request.method == 'POST' and form.validate():  # 4
        brand = BrandName(name=form.name.data)  #  4
        db.session.add(brand)  # 4
        db.session.commit()
        flash(f"your {form.name.data} has been aded","success")  # 4
    else:  # 4
        flash("plz add the forms")  # 4
    return render_template('AutoAdd.html', brand_form="brand_form", form=form)  # 4



"""
@app.route("/newbrand", methods=['GET','POST'])  # 4
def NewBrand():  # 4
    form = Brand_Forms(request.form)  # 4
    if request.method == 'POST' and form.validate():  # 4
        get_new_brand = request.form.get("brand_name")  # 4
        new_brand = BrandName(name=get_new_brand)  # 4
        db.session.add(new_brand)  # 4
        db.session.commit()
        flash(f"your {get_new_brand} has been aded","success")  # 4
    else:  # 4
        flash("plz add the forms")  # 4
    return render_template('AutoAdd.html', brand_form="brand_form", form=form)  # 4

"""
@app.route("/")
@app.route("/newcateg", methods=['GET','POST'])
def NewCategory():  # 4
    form = Category_Form(request.form)  # 4
    if request.method == 'POST' and form.validate():  # 4
        categ = CategoryName(name=form.name.data)  #  4
        db.session.add(categ)  # 4
        db.session.commit()
        flash(f"your {form.name.data} has been aded")  # 4
    else:  # 4
        flash("You can add new Category")  # 4
    return render_template('AutoAdd.html', form=form, categ="categ")  # 4


"""

@app.route("/newcateg", methods=['GET','POST'])  # 4
def NewCategory():  # 4
    form = Category_Forms(request.form)  # 4
    if request.method == 'POST':  # 4
        get_new_categ = request.form.get("categ_name")  # 4
        new_categ = CategoryName(name=get_new_categ)  # 4
        db.session.add(new_categ)  # 4
        db.session.commit()
        return redirect(url_for('newbrand'))
        flash(f"your {get_new_categ} has been aded")  # 4
    else:  # 4
        flash("plz add the forms")  # 4
    return render_template('AutoAdd.html', title="newcateg", form=form)  # 4


"""
