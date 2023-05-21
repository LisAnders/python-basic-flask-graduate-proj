from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required

from .forms.retail_forms import RetailOpartForm
from controller.wms.operation_controller import recalc_op_sum
from controller.retail.retail_controller import (
    create_retail_op, 
    get_retail_opart, 
    get_retail_operation_list, 
    set_op_status_sold,
    create_retail_opart_by_barcode,
    get_retail_op_sum,
    update_retail_opart_quantity,
    delete_retail_opart
)
from controller.login_controller import chek_roles


retail_app = Blueprint(
    'retail_app',
    __name__,
    url_prefix='/retail'
)



@retail_app.route('/', methods=['GET'], endpoint='retail_list')
@retail_app.route('/<int:page>', methods=['GET'], endpoint='retail_list')
@login_required
@chek_roles(['Admin', 'Seller'])
def retail_list(page:int=1):
    sales = get_retail_operation_list(page)
    return render_template('retail/retail_list.html', sales=sales, page=page)


@retail_app.route('/create_sale', methods=['GET'], endpoint='create_sale')
@login_required
@chek_roles(['Admin','Seller'])
def create_sale():
    op = create_retail_op()
    return redirect(url_for('retail_app.add_opart', id_op = op.id_op))


@retail_app.route('/<int:id_op>/add_opart', methods=['GET', 'POST'], endpoint='add_opart')
@login_required
@chek_roles(['Admin','Seller'])
def add_opart(id_op:int):
    form=RetailOpartForm()
    if request.method == 'GET':
        return render_template('retail/add_opart.html', form=form, id_op=id_op)
    opart = create_retail_opart_by_barcode(id_op=id_op, barcode=form.data['barcode'])
    return redirect(url_for('retail_app.add_opart', id_op = id_op))  


@retail_app.route('/<int:id_op>/show_opart', methods=['GET'], endpoint='show_opart')
@login_required
def show_opart(id_op:int):
    opart = get_retail_opart(id_op=id_op)
    opsum = get_retail_op_sum(id_op=id_op)
    return render_template('retail/show_opart.html', opart=opart, opsum=opsum) 


@retail_app.route('/<int:id_op>/retail_opart', methods=['GET'], endpoint='retail_opart')
@login_required
def retail_opart(id_op:int):
    opart = get_retail_opart(id_op=id_op)
    return render_template('retail/retail_opart.html', opart=opart) 


@retail_app.route('/<int:id_opart>/update_opart_quant', methods=['GET', 'POST'], endpoint='update_opart_quant')
@login_required
@chek_roles(['Admin','Seller'])
def update_opart_quant(id_opart):
    opart = update_retail_opart_quantity(id_opart, quantity=float(request.form['quantity']))
    return redirect(url_for('retail_app.add_opart', id_op = opart.id_op))


@retail_app.route('/<int:id_opart>/delete_opart', methods=['GET', 'POST'], endpoint='delete_opart')
@login_required
@chek_roles(['Admin','Seller'])
def delete_opart(id_opart:int):
    if request.method =='GET':
        return '<h1>ПОКА ТУТ ПУСТО!!!</h1>'
    opart = delete_retail_opart(id_opart=id_opart)
    return redirect(url_for('retail_app.add_opart', id_op = opart.id_op))


@retail_app.route('/<int:id_op>/confirm_sold', methods=['GET', 'POST'], endpoint='confirm_sold')
@login_required
@chek_roles(['Admin','Seller'])
def confirm_sold(id_op):
    set_op_status_sold(id_op)
    return redirect(url_for('retail_app.retail_list'))

