from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


# @login_required is telling us this page is only allow login user to access,
# if we go to __init__ to check out login_manager.login_view that we set,
# it means once the route has @login_required decorator , it take us to login page.
# the following def will be executed once we login.
@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    # 如果有submit然後POST東西過來...
    if form.validate_on_submit():
        # form.username.data 為登入者所填的表單資料中的'用戶同稱'，
        # 找出它那一筆data的所有資料存成叫做 attempted_user
        attempted_user = User.query.filter_by(username=form.username.data).first()

        # 如果帳號跟所輸入的密碼與db中的匹配...
        # check_password_correction則是將db的密碼與登入者所嘗試的密碼做檢查的動作
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are Logged in as: {attempted_user.username}', category='success')

            return redirect(url_for('market_page'))

        else:
            flash('Username and password are not match! Please try again.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out.", category='info')
    return redirect(url_for('home_page'))
