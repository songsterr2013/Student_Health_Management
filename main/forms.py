from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from main.models import User
import string


class EditStudentIdForm(FlaskForm):

    def validate_student_id(self, student_id_to_check):
        a_to_z = [i for i in string.ascii_lowercase]
        zero_to_nine = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if student_id_to_check.data[0] not in a_to_z:
            print(student_id_to_check.data[0], a_to_z)
            raise ValidationError('學生編號請以小寫英文為首')
        for i in student_id_to_check.data[1:]:
            if i not in zero_to_nine:
                raise ValidationError('不符合格式')

    student_id = StringField(label='修改你的學生編號:(首字母需為小寫)', validators=[Length(min=7, max=15), DataRequired()])
    submit = SubmitField(label='確定修改')


class EditHeightForm(FlaskForm):

    def validate_height(self, height_to_check):
        try:
            int_height = int(height_to_check.data)
        except ValueError:
            raise ValidationError('請勿輸入數字以外的字符')
        if int_height > 200 or int_height < 100:
            raise ValidationError('請輸入100~200區間的數值')

    height = StringField(label='修改你的身高:(只需輸入數字)', validators=[DataRequired()])
    submit = SubmitField(label='確定修改')


class EditGroupNumForm(FlaskForm):

    def validate_group_num(self, group_num_to_check):
        group_list = list(map(str, [i for i in range(1, 21)]))
        if group_num_to_check.data not in group_list:
            raise ValidationError('請輸入1~20區間的數值')

    group_num = StringField(label='修改你的組別:(只需輸入數字)', validators=[DataRequired()])
    submit = SubmitField(label='確定修改')


class InbodyForm(FlaskForm):

    def validate_weight(self, weight_to_check):
        try:
            int_weight = float(weight_to_check.data)
        except ValueError:
            raise ValidationError('體重(Kg): 請勿輸入數字以外的字符')
        if int_weight > 200 or int_weight < 0:
            raise ValidationError('體重(Kg): 請輸入0~200區間的數值')

    def validate_fat_weight(self, fat_weight_to_check):
        try:
            int_fat = float(fat_weight_to_check.data)
        except ValueError:
            raise ValidationError('體脂肪重(Kg): 請勿輸入數字以外的字符')
        if int_fat > 200 or int_fat < 0:
            raise ValidationError('體脂肪重(Kg): 請輸入0~200區間的數值')

    def validate_fat_percent(self, fat_percent_to_check):
        try:
            int_fat = float(fat_percent_to_check.data)
        except ValueError:
            raise ValidationError('體脂肪率(%): 請勿輸入數字以外的字符')
        if int_fat > 100 or int_fat < 0:
            raise ValidationError('體脂肪率(%): 請輸入0~100區間的數值')

    def validate_muscle(self, muscle_to_check):
        try:
            int_muscle = float(muscle_to_check.data)
        except ValueError:
            raise ValidationError('骨骼肌重(Kg): 請勿輸入數字以外的字符')
        if int_muscle > 200 or int_muscle < 0:
            raise ValidationError('骨骼肌重(Kg): 請輸入0~200區間的數值')

    def validate_body_water_weight(self, body_water_weight_to_check):
        try:
            int_score = float(body_water_weight_to_check.data)
        except ValueError:
            raise ValidationError('身體總水重(L): 請勿輸入數字以外的字符')
        if int_score > 200 or int_score < 0:
            raise ValidationError('身體總水重(L): 請輸入0~200區間的數值')

    def validate_score(self, score_to_check):
        try:
            int_score = int(score_to_check.data)
        except ValueError:
            raise ValidationError('Inbody分數: 請勿輸入數字以外的字符')
        if int_score > 100 or int_score < 0:
            raise ValidationError('Inbody分數: 請輸入0~100區間的數值')

    inspection_date = StringField(label='測量日:', validators=[DataRequired()])
    weight = StringField(label='體重(Kg):', validators=[DataRequired()])
    fat_weight = StringField(label='體脂肪重(Kg):', validators=[DataRequired()])
    fat_percent = StringField(label='體脂肪率(%):', validators=[DataRequired()])
    muscle_weight = StringField(label='骨骼肌重(Kg):', validators=[DataRequired()])
    body_water_weight = StringField(label='身體總水重(L):', validators=[DataRequired()])
    score = StringField(label='Inbody分數:', validators=[DataRequired()])
    submit = SubmitField(label='確定上傳')

class RegisterForm(FlaskForm):

    # When you inherit a class,
    # FlaskForm will care all functions that you create and name prefix with 'validate',
    # after the '_' it is required to name with just the same as val as you create,
    # like 'username', once it found ,it will pass it into parameter and execute sth.

    def validate_username(self, username_to_check):
        a_to_z = [i for i in string.ascii_lowercase]
        zero_to_nine = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        if username_to_check.data[0] not in a_to_z:
            raise ValidationError('帳號請以小寫英文為首')
        for i in username_to_check.data[1:]:
            if i not in zero_to_nine:
                raise ValidationError('請按照格式輸入帳號')
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('此帳號已被使用，若帳號被佔用請聯絡學務處')

    username = StringField(label='帳號(請以你的學生編號+出生月日為帳號):', validators=[Length(min=10, max=15), DataRequired()])
    name = StringField(label='中文姓名:', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='設定密碼:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='密碼確認:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='創建帳號')


class LoginForm(FlaskForm):
    username = StringField(label='請輸入帳號:', validators=[DataRequired()])
    password = PasswordField(label='請輸入密碼:', validators=[DataRequired()])
    submit = SubmitField(label='登入')
