from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField
from wtforms.validators import DataRequired,EqualTo,Email

class RegisterForm(FlaskForm):
    email = StringField('البريد الالكتروني',validators=[DataRequired(),Email(message="بريد الكتروني غير مقبول")])
    password = PasswordField('كلمة المرور',validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة المرور',validators=[DataRequired(),EqualTo('password','كلمة المرور غير متساوية')])
    submit = SubmitField('تسجيل')


class LoginForm(FlaskForm):
    email = StringField('البريد الالكتروني',validators=[DataRequired(),Email()])
    password = PasswordField('كلمة المرور',validators=[DataRequired()])
    submit = SubmitField('دخول')

class UplodForm(FlaskForm):
    file_ = FileField('اختر ملف',validators=[DataRequired()])