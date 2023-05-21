from functools import wraps
from flask import render_template, redirect, request, flash
from flask_login import current_user
from sqlalchemy.sql import and_

from models import db, User, Role, UserRoles


def chek_roles(role:list[str]):
    def wrapper(view_function):

        @wraps(view_function)
        def decorator(*args, **kwargs):
            user = User.query.join(
                UserRoles,
                User.id == UserRoles.user_id
                ).join(
                Role,
                Role.id==UserRoles.role_id     
                ).filter(
                and_(Role.name.in_(role), User.id == int(current_user.get_id()))
                ).all()
            if user:
                return view_function(*args, **kwargs)
            
            # print(request.referrer)
            str_role = ', '.join(str(r) for r in role)
            flash(f'Доступ к данной странице/действию есть только у пользоватерелй с ролями {str_role}! Обратитесь к администратору.')
            # return render_template('/login/wrong_role.html', roles=str(role))
            return redirect(request.referrer)
            
            
        return decorator

    return wrapper