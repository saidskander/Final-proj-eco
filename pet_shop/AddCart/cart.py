#!/usr/bin/python3

from crypt import methods
from tokenize import Number
from pet_shop.products.models import NewProduct
from flask import render_template, redirect, url_for  # 1
from flask import request, session, current_app
from pet_shop import app, db  # 1
from flask import flash

from pet_shop.products.routes import product


"""
link:1) https://favtutor.com/blogs/merge-dictionaries-python
link:2) https://stackoverflow.com/questions/25231989/how-to-check-if-a-variable-is-a-dictionary-in-python
"""
def merge_two_dicts(dictionary1, dictionary2):
    if isinstance(dictionary1, list) and isinstance(dictionary2,list):
        return dictionary1 + dictionary2
    elif isinstance(dictionary1, dict) and isinstance(dictionary2, dict):
        return dict(list(dictionary1.items()) + list(dictionary2.items()))
    return False


"""https://helperbyte.com/questions/12319/
how-you-can-implement-a-shopping-cart
-using-sessions-in-flask"""
""""""
"""
-IMPORTANT NOTE: this will works only in one POST form tag
-multi form tags will affect POST request from responding 
"""
@app.route("/addtocarts", methods=["POST"])
def AddToCarts():
    """add item to the cart"""
    try:
        CustomerProduct = NewProduct
        product_id = request.form.get("product_id")
        colors = request.form.get("colors")     
        quantity = request.form.get("quantity")

        product = CustomerProduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == "POST":
            DictionaryItems = {product_id:{"name": product.name, "price": product.price,"colors": product.colors, "discount": product.discount, "color":colors, "img":product.image_1, "quantity": quantity}}
            if "AddToCartx" in session:
                print(session["AddToCartx"])
                if product_id in session["AddToCartx"]:
                    print('Succesfully aded')
                else:
                    session["AddToCartx"] = merge_two_dicts(session["AddToCartx"], DictionaryItems)
                    return redirect(request.referrer)
            else:
                session["AddToCartx"] = DictionaryItems
                return redirect(request.referrer)   

    except Exception as x:
        print(x)
    finally:
        return redirect(request.referrer)


@app.route('/ItemCarts', methods=["POST", "GET"])
def ItemCarts():
    if "AddToCartx" not in session:
        return redirect(request.referrer)  
    subtotal = 0
    index = 0 # product index
    product_quantity = 0
    for key, product in session["AddToCartx"].items():
        index += 1 # product index
        product_quantity += int(product["quantity"])

        subtotal +=  ((int(product["quantity"]) * float(product["price"])) - (((int(product["quantity"]) * float(product["price"]))/100)* float(product["discount"]))) 




        GrandTotal = (( subtotal))

    return render_template('CustomerP/itemcarts.html',product_quantity=product_quantity,index=index, product=product, GrandTotal=GrandTotal, subtotal=subtotal)
