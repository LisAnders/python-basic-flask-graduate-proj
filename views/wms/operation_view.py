from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from .forms import OperationForm
from controller.constants import TOP_INCOME, TOP_INVOCE, TOP_MOVEMENT
from controller.wms.operation_controller import (
    get_wms_operation_list, 
    get_wms_typeop_for_create, 
    get_wms_redirection_by_typeop,
    get_wms_typeop_by_id_top,
    get_wms_warehouse_by_typeop,
    create_wms_operation,
    get_wms_opstatus_for_create
    )
from controller.login_controller import chek_roles

operation_app = Blueprint(
    'operation_app',
    __name__,
    url_prefix='/operation'
)


def prepare_operation_form(id_top:int):
    '''
        Подготовка формы операции в зависимости от типа операции
    '''
    typeop = get_wms_typeop_by_id_top(id_top)
    form = OperationForm()
    choises_ws = [(w.id_ws, w.name) for w in get_wms_warehouse_by_typeop(id_top)]
    if typeop.name == TOP_INCOME:
        form.wsi.choices = choises_ws
    if typeop.name == TOP_INVOCE:
        form.wso.choices = choises_ws
    if typeop.name == TOP_MOVEMENT:
        form.wsi.choices = choises_ws
        form.wso.choices = choises_ws
    form.status.choices = [(ops.status_code, ops.status_name) for ops in get_wms_opstatus_for_create(id_top)]
    return form


@operation_app.route('/', methods=['GET'], endpoint='list')
@operation_app.route('/<int:page>', methods=['GET'], endpoint='list')
@login_required
@chek_roles(['Admin','Manager'])
def operation_list(page:int=1):
    operation = get_wms_operation_list(page)
    return render_template('wms/operation/list.html', operation=operation, page=page)


@operation_app.route('/<int:id_top>/create_consumption', methods=['GET', 'POST'], endpoint='create_consumption')
@login_required
@chek_roles(['Admin','Manager'])
def create_consumption(id_top:int):
    '''
        Создание расходных операций
    '''
    typeop = get_wms_typeop_by_id_top(id_top)
    form = prepare_operation_form(id_top)
    if request.method == 'GET':
        return render_template('wms/operation/create/create_consumption.html', form=form, typeop=typeop)
    operation = create_wms_operation(
        id_top=id_top,
        id_wso=form.data['wso'],
        opnumber=form.data['opnumber'],
        opdate=form.data['opdate'],
        status=form.data['status'],
    )
    return redirect(url_for('wms_app.opart_app.create_opart', id_op=operation.id_op))

    
@operation_app.route('/<int:id_top>/create_arrival', methods=['GET', 'POST'], endpoint='create_arrival')
@login_required
@chek_roles(['Admin','Manager'])
def create_arrival(id_top:int):
    '''
        Создание операции прихода товара
    '''
    typeop = get_wms_typeop_by_id_top(id_top)
    form = prepare_operation_form(id_top)
    if request.method == 'GET':
        return render_template('wms/operation/create/create_arrival.html', form=form, typeop=typeop)
    operation = create_wms_operation(
        id_top=id_top,
        id_wsi=form.data['wsi'],
        opnumber=form.data['opnumber'],
        opdate=form.data['opdate'],
        status=form.data['status'],
    )
    return redirect(url_for('wms_app.opart_app.create_opart', id_op=operation.id_op))


@operation_app.route('/<int:id_top>/create_movement', methods=['GET', 'POST'], endpoint='create_movement')
@login_required
@chek_roles(['Admin','Manager'])
def create_movement(id_top:int):
    '''
        Создание операций перемещения по МХ
    '''
    typeop = get_wms_typeop_by_id_top(id_top)
    form = prepare_operation_form(id_top)
    if request.method == 'GET':
        return render_template('wms/operation/create/create_movement.html', form=form, typeop=typeop)
    operation = create_wms_operation(
        id_top=id_top,
        id_wso = form.data['wso'],
        id_wsi=form.data['wsi'],
        opnumber=form.data['opnumber'],
        opdate=form.data['opdate'],
        status=form.data['status'],
    )
    return redirect(url_for('wms_app.opart_app.create_opart', id_op=operation.id_op))


@operation_app.route('/create', methods=['GET'], endpoint='create')
@login_required
@chek_roles(['Admin','Manager'])
def create_operation_list():
    '''
        Страница с доступными для создания типами операций
    '''
    typeop = get_wms_typeop_for_create()
    return render_template('wms/operation/create/create.html', typeop=typeop)
    

@operation_app.route('/<int:id_top>/redirect_to_create', methods=['GET'], endpoint='redirect')
@login_required
@chek_roles(['Admin','Manager'])
def redirect_to_create(id_top:int):
    '''
    Перенаправление на создание операций в зависимости от выбранного типа операции
    '''
    redirection = get_wms_redirection_by_typeop(id_top)
    return redirect(url_for(f'wms_app.operation_app.{redirection}', id_top = id_top))
