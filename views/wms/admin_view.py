from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required

from models import db, User, Role
from .forms.admin_form import UserForm
from controller.wms.admin_controller import get_users
from controller.login_controller import chek_roles


admin_app = Blueprint(
    'admin_app',
    __name__,
    url_prefix='/admin'
)


@admin_app.route('/', methods=['GET'], endpoint='admin_list')
@login_required
@chek_roles(['Admin'])
def admin_list():
    users = get_users()
    return render_template('/wms/admin/admin_list.html', users=users)


@admin_app.route('/<int:user_id>/update_user', methods=['GET', 'POST'], endpoint='update_user')
@login_required
@chek_roles(['Admin'])
def update_user(user_id):
    user = User.query.get(user_id)
    form = UserForm(data={"roles":user.roles})
    form.roles.query = Role.query.all()
    if request.method == 'GET':
        return render_template('/wms/admin/update_user.html', form=form, user=user)
    print(form.roles.data)
    user.roles.clear()
    user.roles.extend(form.roles.data)
    db.session.commit()
    return redirect(url_for('wms_app.admin_app.admin_list'))
