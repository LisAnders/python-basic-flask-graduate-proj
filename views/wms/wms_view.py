from flask import Blueprint, render_template
from flask_login import login_required

from .operation_view import operation_app
from .opart_view import opart_app
from .article_view import article_app
from .admin_view import admin_app
from controller.login_controller import chek_roles

wms_app = Blueprint(
    'wms_app',
    __name__,
    url_prefix='/wms'
)

wms_app.register_blueprint(operation_app)
wms_app.register_blueprint(opart_app)
wms_app.register_blueprint(article_app)
wms_app.register_blueprint(admin_app)


@wms_app.route('/', methods=['GET'], endpoint='index')
@login_required
@chek_roles(['Admin', 'Manager'])
def wms_index():
    return render_template('/wms/wms_index.html')