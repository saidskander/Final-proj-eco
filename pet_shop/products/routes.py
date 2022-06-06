#!/usr/bin/env python3

from email.policy import default
from flask import url_for, redirect, render_template  # 4
from flask import flash, request, session, abort, send_file
from pet_shop import db, app, photos  # 4
from pet_shop.admin.models import User
from .models import NewProduct, CategoryName, BrandName
from .forms import NewProduct_forms, Brand_Forms, Category_Forms
from flask_login import current_user
import secrets
import os
# need this for img update/del/add
from flask import current_app


# this is for testing purpse and future use
def brands():
    brands = BrandName.query.join(NewProduct, (BrandName.id == NewProduct.brand_id)).all()
    return brands

# this is for testing purpse and future use
def categories():
    categories = CategoryName.query.join(NewProduct,(CategoryName.id == NewProduct.category_id)).all()
    return categories


@app.route('/AdminProducts', methods=['GET', 'POST'])
def AdminProducts():
    products = NewProduct.query.filter_by(user_id=current_user.id)\
        .order_by(NewProduct.pub_date.desc()).all()
    return render_template('products.html', products=products)


"""https://pythonhosted.org/Flask-Uploads/"""
@app.route("/NewProduct", methods=['GET','POST'])
def New_Product():
    brands = BrandName.query.all()
    categories = CategoryName.query.all()
    form = NewProduct_forms()
    if request.method == 'POST' and form.validate_on_submit() and "image_1" in request.files:
        """
        Adding a new product, the form wasnt working because the form.validate
        have to be before 'image_1' in request.files.
        the img form validation err is different than
        other form err look template.
        """
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        user_id = current_user.id
        brand = request.form.get('brand')
        category = request.form.get('category')
        if request.files.get('image_1'):
            image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        else:
            image_1 = url_for('static', filename='images/product_img/default.png')


        if request.files.get('image_2'):
            image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        else:
            image_2 = url_for('static', filename='images/product_img/' + 'default.png')

        if request.files.get('image_3'):
            image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        else:
            image_3 = url_for('static', filename='images/product_img/' + 'default.png')


        product = NewProduct(name=name,price=price,discount=discount,stock=stock,colors=colors,
                             desc=desc,category_id=category,brand_id=brand,image_1=image_1,
                             image_2=image_2,image_3=image_3 ,user_id=user_id)
        db.session.add(product)
        db.session.commit()
        flash(f'The product "{form.name.data}" was added in database')
        return redirect(url_for('New_Product'))

    return render_template('newproduct.html', form=form, title='Add a Product', brands=brands, categories=categories)  # 4


@app.route("/product/<int:product_id>")
def product(product_id):
    """product id"""
    product = NewProduct.query.get_or_404(product_id)
    if product.user != current_user:
        abort(403)
    return render_template('Productid.html', product=product)


@app.route("/product/<int:product_id>/update", methods=['GET','POST'])
def Update_Product(product_id):
    product = NewProduct.query.get_or_404(product_id)

    brands = BrandName.query.all()
    categories = CategoryName.query.all()
    form = NewProduct_forms()

    if product.user != current_user:
        abort(403)

    brand = request.form.get('brands')
    category = request.form.get('categories')

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.desc = form.desc.data
        product.user_id = current_user.id


        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/product_img/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/product_img/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/product_img/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")


        db.session.commit()
        flash(f'Your product "{form.name.data}" has been successfully updated')
        return redirect(url_for("AdminProducts", product_id=product.id))

    elif request.method == "GET":
        form.name.data = product.name
        form.price.data = product.price
        form.discount.data = product.discount
        form.stock.data = product.stock
        form.colors.data = product.colors
        form.desc.data = product.desc
        product.image_3 = product.image_3
    return render_template('newproduct.html', form=form, brands=brands, brand=brand, categories=categories, category=category, product=product)



@app.route("/product/<int:product_id>/delete", methods=['POST'])
def Delete_Product(product_id):
    product = NewProduct.query.get_or_404(product_id)
    if product.user != current_user:
        abort(403)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/product_img/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/product_img/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/product_img/" + product.image_3))
        except Exception as x:
            print(x)
    db.session.delete(product)
    flash(f'Your brand "{product.name}" has been deleted!')
    db.session.commit()
    return redirect(url_for("AdminProducts", product_id=product.id))


"""
@app.route("/category/<int:category_id>/delete", methods=['POST'])
def Delete_Category(category_id):
    category = CategoryName.query.get_or_404(category_id)
    if category.user != current_user:
        abort(403)
    db.session.delete(category)
    flash(f'Your Category "{category.name}" has been deleted!')
    db.session.commit()
    return redirect(url_for("Categories"))
"""


"""
@app.route("/NewProduct", methods=['GET','POST'])
def New_Product():
    brands = BrandName.query.all()
    categories = CategoryName.query.all()
    form = NewProduct_forms(request.form)
    if  request.method=='POST' and form.validate():


        brand = request.form.get('brand')
        category = request.form.get('category')

        image_1 = photos.save(request.files.get('form.image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('form.image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('form.image_3'), name=secrets.token_hex(10) + ".")


        user_id = current_user.id
        product = NewProduct(name=form.name.data,
                             price=form.price.data,
                             discount=form.discount.data,
                             stock=form.stock.data,
                             colors=form.colors.data,
                             desc=form.desc.data,
                             image_1=image_1,
                             image_2=image_2,
                             image_3=image_3,
                             brand=brand,
                             category=category,
                             user_id=user_id)

        db.session.add(product)
        flash(f'The product {form.name.data} is successfuly added')
        db.session.commit()
        return redirect(url_for('New_Product'))
    return render_template('newproduct.html', form=form, title='Add a Product', brands=brands, categories=categories)
"""








@app.route("/newcateg", methods=['GET','POST'])
def New_Category():
    categories = CategoryName.query.all()
    form = Category_Forms(request.form)
    """add categorie, 'form.validate()' will validate the brand form"""
    if request.method == 'POST' and form.validate():
        user_id = current_user.id
        category = CategoryName(name=form.name.data, user_id=user_id)
        db.session.add(category)
        db.session.commit()
        flash(f'your category "{form.name.data}" has been aded')
    else:
        flash("Add new category")
    category = request.form.get('category')
    return render_template('newcategory.html', Category_Forms="Category_Forms", form=form, categories=categories)  # 4


"""Display categories"""





@app.route("/categories", methods=['GET','POST'])
def Categories():
    """brands = BrandName.query.all()"""
    """brands = BrandName.query.order_by(BrandName.id.desc()).all()"""

    categories = CategoryName.query.filter_by(user_id=current_user.id)\
        .order_by(CategoryName.pub_date.desc()).all()
    return render_template('Category.html', title="Categories", categories=categories )


@app.route("/category/<int:category_id>")
def category(category_id):
    """brandid"""
    category = CategoryName.query.get_or_404(category_id)
    if category.user != current_user:
        abort(403)
    return render_template('Categoryid.html', category=category)


@app.route("/category/<int:category_id>/update", methods=['GET','POST'])
def Update_Category(category_id):
    category = CategoryName.query.get_or_404(category_id)
    if category.user != current_user:
        abort(403)
    form = Category_Forms()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash(f'Your new category "{form.name.data}" has been successfully updated')
        return redirect(url_for("category", category_id=category.id))
    elif request.method == "GET":
        form.name.data = category.name
        flash("Update your category")
    return render_template('newcategory.html', category=category, form=form)


@app.route("/category/<int:category_id>/delete", methods=['POST'])
def Delete_Category(category_id):
    category = CategoryName.query.get_or_404(category_id)
    if category.user != current_user:
        abort(403)
    if db.session.delete(category):
        flash(f'Your Category "{category.name}" has been deleted!')
        db.session.commit()
    else:
        flash(f'warning category is active in a product! delete the product or edit category')

    return redirect(url_for("Categories", category_id=category.id))



@app.route("/brands", methods=['GET','POST'])
def Brands():
    brands = BrandName.query.filter_by(user_id=current_user.id)\
        .order_by(BrandName.pub_date.desc()).all()
    return render_template('Brand.html', title="Update brand", brands=brands, brand=brand)


@app.route("/newbrand", methods=['GET','POST'])
def New_Brand():
    brands = BrandName.query.all()
    form = Brand_Forms(request.form)
    """add brand, 'form.validate()' will validate the brand form"""
    if request.method == 'POST' and form.validate():
        user_id = current_user.id
        brand = BrandName(name=form.name.data, user_id=user_id)
        db.session.add(brand)
        db.session.commit()
        flash(f'Your Brand "{form.name.data}" has been aded')
    else:
        flash("Add new brand")
    brand = request.form.get('brand')
    return render_template('newbrand.html',  Brand_Forms="Brand_Forms", form=form, brands=brands)


@app.route("/brand/<int:brand_id>")
def brand(brand_id):
    """brandid"""
    brand = BrandName.query.get_or_404(brand_id)
    if brand.user != current_user:
        abort(403)
    return render_template('Brandid.html', brand=brand)



@app.route("/brand/<int:brand_id>/update", methods=['GET','POST'])
def Update_Brand(brand_id):
    brand = BrandName.query.get_or_404(brand_id)
    if brand.user != current_user:
        abort(403)
    form = Brand_Forms()
    if form.validate_on_submit():
        brand.name = form.name.data
        db.session.commit()
        flash(f'Your new brand "{form.name.data}" has been successfully updated')
        return redirect(url_for("brand", brand_id=brand.id))
    elif request.method == "GET":
        form.name.data = brand.name
        flash("Update your brand")
    return render_template('newbrand.html', brand=brand, form=form)



@app.route("/brand/<int:brand_id>/delete", methods=['POST'])
def Delete_Brand(brand_id):
    brand = BrandName.query.get_or_404(brand_id)
    if brand.user != current_user:
        abort(403)
    if db.session.delete(brand):
        flash(f'Your brand "{brand.name}" has been deleted!')
        db.session.commit()
    else:
        flash(f'warning brand is active in a product! delete the product or edit brand')
    return redirect(url_for("Brands", brand_id=brand.id))





