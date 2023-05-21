from http import HTTPStatus
from flask import Blueprint, request, render_template, redirect, url_for
from models import db, Warehouse
from .wms.forms import WsForm

warehouse_app = Blueprint(
    'warehouse_app',
    __name__,
    url_prefix='/warehouse'
)

@warehouse_app.get('/', endpoint='list')
def get_warehouse_list():
    warehouse = Warehouse.query.order_by(Warehouse.id_ws).all()
    
    return render_template('wms/warehouse/list.html', warehouse=warehouse)


@warehouse_app.route('/create/', methods=['GET', 'POST'], endpoint='create')
def create_warehouse():
    form = WsForm()
    if request.method == 'GET':
        return render_template('wms/warehouse/create.html', form=form)
    if not form.validate_on_submit():
        return (render_template('wms/warehouse/create.html', form=form), HTTPStatus.BAD_REQUEST)
    
    warehouse = Warehouse(name=form.data['name'])
    db.session.add(warehouse)
    db.session.commit()
    return redirect(url_for('warehouse_app.list'))