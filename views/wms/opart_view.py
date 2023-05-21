from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from models import db, Article
from .forms import  OpartForm
from controller.wms.operation_controller import recalc_op_sum, get_operation_by_id_op
from controller.wms.rest_controller import recalc_rests
from controller.wms.opart_controller import (
    get_operation_article_by_id_op,
    get_opart_detail,
    wms_create_opart,
    wms_update_opart,
    wms_delete_opart,
)
from controller.login_controller import chek_roles


opart_app = Blueprint(
    'opart_app',
    __name__,
    url_prefix='/opart'
)


@opart_app.route('/<int:id_op>', methods=['GET'], endpoint='list')
@login_required
@chek_roles(['Admin','Manager'])
def get_operation_opart(id_op:int):
    '''
        Получение списка товарных позиций операции
    '''
    opinfo = get_operation_by_id_op(id_op)
    opart = get_operation_article_by_id_op(id_op)
    return render_template('wms/opart/list.html', opart=opart, opinfo=opinfo)

    
@opart_app.route('/<int:id_op>/create_opart', methods=['GET', 'POST'], endpoint='create_opart')
@login_required
@chek_roles(['Admin','Manager'])
def create_opart(id_op:int):
    '''
        Добавление товарной позиции к операции
    '''
    op = get_operation_by_id_op(id_op)
    form = OpartForm()
    form.id_art.choices = [(ar.id_art, ar.name) for ar in Article.query.all()]
    if request.method == 'GET':
        return render_template('wms/opart/create_opart.html', form=form, operation=op)
    opart = wms_create_opart(id_op=id_op, id_art=int(form.data['id_art']), quantity=float(form.data['quantity']), price=float(form.data['price']))
    recalc_op_sum(id_op=opart.id_op)
    recalc_rests(id_art = opart.id_art, id_wsi=op.id_wsi, id_wso=op.id_wso, quantity=opart.quantity, typeio=op.typeop.typeio)
    return redirect(url_for('wms_app.operation_app.list'))


@opart_app.route('/<int:id_opart>/update_opart', methods=['GET', 'POST'], endpoint='update_opart')
@login_required
@chek_roles(['Admin','Manager'])
def update_opart(id_opart):
    '''
        Изменение товарной позиции операции
    '''
    opart = get_opart_detail(id_opart)
    form = OpartForm()
    if request.method == 'GET':
        return render_template('wms/opart/update_opart.html', form=form, opart=opart)
    new_quantity=wms_update_opart(
        id_opart=id_opart, 
        old_quantity=opart.quantity , 
        new_quantity=float(form.data['quantity']), 
        price=float(form.data['price'])
    )
    recalc_op_sum(id_op=opart.id_op)
    recalc_rests(id_art = opart.id_art, id_wsi=opart.operation.id_wsi, id_wso=opart.operation.id_wso, quantity=new_quantity, typeio=opart.operation.typeop.typeio)
    return redirect(url_for('wms_app.operation_app.list'))


@opart_app.route('/<int:id_opart>/delete_opart', methods=['GET', 'POST'], endpoint='delete_opart')
@login_required
@chek_roles(['Admin','Manager'])
def delete_opart(id_opart):
    '''
        Удаление товарной позиции операции
    '''
    opart = get_opart_detail(id_opart)
    op_wsi=opart.operation.id_wsi
    op_wso= opart.operation.id_wso
    op_typeio = opart.operation.typeop.typeio
    if request.method == 'GET':
        return render_template('wms/opart/delete_opart.html', opart=opart)
    old_quantity = wms_delete_opart(id_opart=id_opart) 
    recalc_op_sum(id_op=opart.id_op)
    recalc_rests(id_art = opart.id_art, id_wsi=op_wsi, id_wso=op_wso, quantity=old_quantity, typeio=op_typeio)
    return redirect(url_for('wms_app.operation_app.list'))
