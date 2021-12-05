from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# old db using
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# db using currently
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Admin_SAU:MyRootSQL2021@localhost/student_health_system?charset=utf8'

app.config['SECRET_KEY'] = 'f67789555f8dcd52a21eab1f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from main import routes

