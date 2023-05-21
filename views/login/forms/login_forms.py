from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, FloatField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        label="Логин:",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Введите логин'},
    )
    password = PasswordField(
        label="Пароль:",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Введите пароль'},
    )
    
    
class RegistrForm(FlaskForm):
    username = StringField(
        label="Логин:",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Введите логин'},
    )
    password = PasswordField(
        label="Пароль:",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Введите пароль'},
    )
    password_retype = PasswordField(
        label="Подтверждение пароля:",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Подтвердите пароль'},
    )
    