#!/usr/bin/python3

from flask import Flask
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate


"""
Start sqlalchemy
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
"""
"""data_config"""
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'rzarzrzuaoiruzoprpuza'  #  when using template form.hidden and bcrypt package2-3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


"""search"""
msearch = Search()
msearch.init_app(app)

'''migrate'''
migrate = Migrate(app, db)


"""bcrypt"""
bcrypt = Bcrypt(app)


"""images_config"""
basedir = os.path.abspath(os.path.dirname(__file__)) # using this for images
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images/product_img')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
#app.config['UPLOADED_PHOTOS_ALLOW'] = set(['png', 'jpg', 'jpeg'])


"""Login Managers"""
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


"""mail_config"""
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

app.config['MAIL_USERNAME'] = 'test2022xyz@gmail.com'
app.config['MAIL_PASSWORD'] = 'kabvennepsoiijae'
# azerty123-
mail = Mail(app)




from pet_shop.admin import routes  # noqa: E402 # 1
# from pet_shop.AdminDash import routes  # noqa: E402 # 4
from pet_shop.products import routes  # noqa: E402 # 5
from pet_shop.customers import routes  # noqa: E402
from pet_shop.AddCart import cart  # noqa: E402