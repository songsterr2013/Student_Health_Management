from main import db, login_manager
from main import bcrypt
from flask_login import UserMixin


# 看似是一個讓程式記得登入者資訊的設定
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 學生基本資料
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    student_id = db.Column(db.String(length=30), nullable=True)
    height = db.Column(db.Integer(), nullable=True)
    group_num = db.Column(db.Integer(), nullable=True)
    created_date = db.Column(db.DateTime, default=db.func.now())

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


# Inbody測量數據
class Inbody(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    weight = db.Column(db.String(length=15), nullable=False)
    fat_weight = db.Column(db.String(length=15), nullable=False)
    fat_percent = db.Column(db.String(length=15), nullable=False)
    muscle_weight = db.Column(db.String(length=15), nullable=False)
    body_water_weight = db.Column(db.String(length=15), nullable=False)
    score = db.Column(db.Integer(), nullable=False)
    inspection_date = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())


# 體脂計測量數據
class BodyFatMachine(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    weight = db.Column(db.String(length=15), nullable=False)
    fat_weight = db.Column(db.String(length=15), nullable=False)
    fat_percent = db.Column(db.String(length=15), nullable=False)
    muscle_weight = db.Column(db.String(length=15), nullable=False)
    body_water_weight = db.Column(db.String(length=15), nullable=False)
    score = db.Column(db.Integer(), nullable=False)
    inspection_date = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())


# 個人運動數據記錄
class StepCount(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    step = db.Column(db.String(length=15), nullable=False)
    walking_date = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())


# 個人運動數據記錄
class SportAndOthers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sport_code = db.Column(db.Integer(), nullable=False)
    sport_duration = db.Column(db.String(length=15), nullable=False)
    sporting_date = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())
    description = db.Column(db.String(length=30), nullable=True)


# 運動種類
class SportType(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sport_type = db.Column(db.String(length=30), nullable=False)