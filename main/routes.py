from main import app
from flask import render_template, redirect, url_for, flash
from main.models import User, Inbody, BodyFatMachine, StepCount, SportAndOthers, SportType
from main.forms import RegisterForm, LoginForm, EditStudentIdForm, EditHeightForm, EditGroupNumForm, InbodyForm, StepForm, PersonalizationForm
from main import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


# @login_required is telling us this page is only allow login user to access,
# if we go to __init__ to check out login_manager.login_view that we set,
# it means once the route has @login_required decorator , it take us to login page.
# the following def will be executed once we login.
@app.route('/main')
@login_required
def main_page():

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = User.query.filter(User.username == cur_user)
    except NameError:
        raise

    return render_template('main.html', user=user)


@app.route('/edit_student_id', methods=['GET', 'POST'])
@login_required
def edit_student_id_page():
    form = EditStudentIdForm()

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = User.query.filter(User.username == cur_user)
    except NameError:
        raise

    if form.validate_on_submit():
        User.query.filter_by(username=cur_user).update(dict(student_id=form.student_id.data))
        db.session.commit()
        flash('成功修改學生編號!', category='success')
        return redirect(url_for('main_page'))
    else:
        flash('一旦按下「確認修改」，即不得更改!', category='warning')

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'修改格式不符: {err_msg}', category='danger')

    return render_template('edit_student_id.html', user=user, form=form)


@app.route('/edit_height', methods=['GET', 'POST'])
@login_required
def edit_height_page():
    form = EditHeightForm()

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = User.query.filter(User.username == cur_user)
    except NameError:
        raise

    if user[0].height is None:
        flash('一旦按下「確認修改」，即不得更改!', category='warning')

    if form.validate_on_submit():
        User.query.filter_by(username=cur_user).update(dict(height=form.height.data))
        db.session.commit()
        flash('成功修改身高!', category='success')
        return redirect(url_for('main_page'))
    else:
        flash('一旦按下「確認修改」，即不得更改!', category='warning')

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'修改格式不符: {err_msg}', category='danger')

    return render_template('edit_height.html', user=user, form=form)


@app.route('/edit_group_num', methods=['GET', 'POST'])
@login_required
def edit_group_num_page():
    form = EditGroupNumForm()

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = User.query.filter(User.username == cur_user)
    except NameError:
        raise

    if form.validate_on_submit():
        User.query.filter_by(username=cur_user).update(dict(group_num=form.group_num.data))
        db.session.commit()
        flash('成功修改組別!', category='success')
        return redirect(url_for('main_page'))
    else:
        flash('一旦按下「確認修改」，即不得更改!', category='warning')

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'修改格式不符: {err_msg}', category='danger')

    return render_template('edit_group_num.html', user=user, form=form)


@app.route('/inbody', methods=['GET', 'POST'])
@login_required
def inbody_page():
    form = InbodyForm()

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = Inbody.query.filter(Inbody.username == cur_user)
        user_count = Inbody.query.filter(Inbody.username == cur_user).count()
    except NameError:
        raise

    if form.validate_on_submit():
        date_to_check = datetime.strptime(form.inspection_date.data, "%Y-%m-%d")

        try:  # 利用這個方法去限制他們輸入的前後測不能比上一次更早
            max_date = max([i.inspection_date for i in user[0:]])
        except ValueError:
            max_date = datetime.min

        if date_to_check >= max_date:

            inbody_to_create = Inbody(inspection_date=form.inspection_date.data,
                                      weight=form.weight.data,
                                      fat_weight=form.fat_weight.data,
                                      fat_percent=form.fat_percent.data,
                                      muscle_weight=form.muscle_weight.data,
                                      body_water_weight=form.body_water_weight.data,
                                      score=form.score.data,
                                      username=cur_user
                                      )
            db.session.add(inbody_to_create)
            db.session.commit()
            flash('資料上傳成功!', category='success')
            return redirect(url_for('inbody_page'))

        else:
            flash('請勿選擇比先前更早的日期!', category='danger')



    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'資料上傳出錯: {err_msg}', category='danger')

    return render_template('inbody.h'
                           'tml', user=user, user_count=user_count, form=form)


@app.route('/fat_machine', methods=['GET', 'POST'])
@login_required
def fat_machine_page():
    form = InbodyForm()  # 表單上傳一模一樣所以直接套來用

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = BodyFatMachine.query.filter(BodyFatMachine.username == cur_user)
        user_count = BodyFatMachine.query.filter(BodyFatMachine.username == cur_user).count()
    except NameError:
        raise

    if form.validate_on_submit():
        date_to_check = datetime.strptime(form.inspection_date.data, "%Y-%m-%d")

        try:  # 利用這個方法去限制他們輸入的不能比上一次更早
            max_date = max([i.inspection_date for i in user[0:]])
        except ValueError:
            max_date = datetime.min

        if date_to_check >= max_date:
            fat_machine_to_create = BodyFatMachine(inspection_date=form.inspection_date.data,
                                                   weight=form.weight.data,
                                                   fat_weight=form.fat_weight.data,
                                                   fat_percent=form.fat_percent.data,
                                                   muscle_weight=form.muscle_weight.data,
                                                   body_water_weight=form.body_water_weight.data,
                                                   score=form.score.data,
                                                   username=cur_user
                                                   )
            db.session.add(fat_machine_to_create)
            db.session.commit()
            flash('資料上傳成功!', category='success')
            return redirect(url_for('fat_machine_page'))

        else:
            flash('請勿選擇比先前更早的日期!', category='danger')

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'資料上傳出錯: {err_msg}', category='danger')

    return render_template('fat_machine.html', user=user, user_count=user_count, form=form)


@app.route('/step', methods=['GET', 'POST'])
@login_required
def step_page():
    form = StepForm()  # 表單上傳一模一樣所以直接套來用

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = StepCount.query.filter(StepCount.username == cur_user)
    except NameError:
        raise

    if form.validate_on_submit():
        date_to_check = datetime.strptime(form.walking_date.data, "%Y-%m-%d")

        if date_to_check not in [i.walking_date for i in user]:  # 如果那一天沒有資料
            step_to_create = StepCount(walking_date=date_to_check,
                                       step=form.step.data,
                                       username=cur_user
                                       )
            db.session.add(step_to_create)
            db.session.commit()
            flash('資料上傳成功!', category='success')
            return redirect(url_for('step_page'))

        else:
            flash('所選日期已有資料，請勿重覆上傳!', category='danger')

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='danger')

    return render_template('step.html', user=user, form=form)


@app.route('/personalization', methods=['GET', 'POST'])
@login_required
def personalization_page():
    form = PersonalizationForm()

    if current_user.is_active:
        cur_user = current_user.username
    try:
        user = db.session.query(SportAndOthers.sporting_date,
                                SportAndOthers.description,
                                SportType.sport_type,
                                SportAndOthers.sport_duration).\
                join(SportType, SportAndOthers.sport_code == SportType.id, isouter=True).\
                filter(SportAndOthers.username == cur_user)
    except NameError:
        raise

    if form.validate_on_submit():
        sport_to_create = SportAndOthers(sporting_date=form.sporting_date.data,
                                         sport_code=form.sport_code.data,
                                         sport_duration=form.sport_duration.data,
                                         username=cur_user,
                                         description=form.description.data
                                         )
        db.session.add(sport_to_create)
        db.session.commit()
        flash('資料上傳成功!', category='success')
        return redirect(url_for('personalization_page'))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'資料上傳出錯: {err_msg}', category='danger')

    return render_template('personalization.html', user=user, form=form)


# =======================================註冊、登入、登出=======================================


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              name=form.name.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'帳號創建成功! 請先完善個人資料。', category='success')
        return redirect(url_for('main_page'))

    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'帳號創建出錯: {err_msg}', category='danger')

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
            flash(f'登入成功! 你正在以 {attempted_user.username} 的身份進行操作。', category='success')
            return redirect(url_for('home_page'))

        else:
            flash('帳號密碼有誤! 請再嘗試。', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("你已成功登出", category='info')
    return redirect(url_for('home_page'))
