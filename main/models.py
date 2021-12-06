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
    #items = db.relationship('Item', backref='owned_user', lazy=True)

    '''@property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"'''

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
    fat = db.Column(db.String(length=15), nullable=False)
    muscle = db.Column(db.String(length=15), nullable=False)
    inspection_date = db.Column(db.DateTime(), nullable=False)
    score = db.Column(db.Integer(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)


'''# 個人記錄測量數據
class Records(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    weight = db.Column(db.String(length=15), nullable=True)
    fat = db.Column(db.String(length=15), nullable=True)
    muscle = db.Column(db.String(length=15), nullable=True)
    inspection_date = db.Column(db.DateTime(), nullable=True)
    step_count = db.Column(db.Integer(), nullable=True)
    username = db.Column(db.String(length=30), nullable=True)'''
