from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main import util

s, config = util.load_config()

if s:
    SQLALCHEMY_DATABASE_URI = config["SQLALCHEMY_DATABASE_URI"]
    SECRET_KEY = config["SECRET_KEY"]

else:
    print("沒有設定檔或設定檔異常")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = "請先登入"
login_manager.login_message_category = "info"

from main import routes