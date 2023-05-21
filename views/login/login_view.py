from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, User
from .forms.login_forms import LoginForm, RegistrForm

login_app = Blueprint(
    'login_app',
    __name__,
    url_prefix='/login'
)

@login_app.route('/', methods=['GET', 'POST'], endpoint='login')
def login_page():
    form = LoginForm()
        
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль')
        
    # else:
    #     flash('Введите логин и пароль')
    
    return render_template('login/login.html', form=form)


@login_app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register_page():
    form=RegistrForm()
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password_retype')
    
    if request.method == 'POST':
        if not (username or password or password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(username=username, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_app.login')) 
    
    return render_template('login/register.html', form=form)


@login_app.route('/logout', methods=['GET', 'POST'], endpoint='logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('index')) 




