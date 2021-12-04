from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# old db using
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# db using currently
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'

app.config['SECRET_KEY'] = 'f67789555f8dcd52a21eab1f'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes

