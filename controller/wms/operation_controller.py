from sqlalchemy import func, desc
from sqlalchemy.orm import aliased
from sqlalchemy.sql import and_
from models import db, Operation, Warehouse, Typeop, Opstatus, Opart
from ..constants import TOP_INCOME, TOP_INVOCE, TOP_MOVEMENT, WS_STORAGE, WS_RETAIL, WS_ONLINE, WS_TRANSIT, STATUS_UNFORMED

ITEMS_PER_PAGE = 20


def get_wms_operation_list(page):
    '''
        функция отображения данных на странице списка операций
    '''
    wso = aliased(Warehouse)
    wsi = aliased(Warehouse)
    top = aliased(Typeop)
    status = aliased(Opstatus)
    operation = Operation.query.join(
            wsi, 
            Operation.id_wsi == wsi.id_ws, 
            isouter=True
        ).join(
            wso, 
            Operation.id_wso == wso.id_ws, 
            isouter=True
        ).join(
            top,
            Operation.id_top == top.id_top,
        ).join(
            status,
            Operation.status == status.status_code,
        ).filter(
            Operation.id_top == status.id_top    
        ).add_columns(
            Operation.id_op,
            top.name.label('top'),
            Operation.opnumber,
            Operation.opdate, 
            Operation.opsum,
            wsi.name.label('wsi'), 
            wso.name.label('wso'),
            status.status_name.label('status'),
        ).order_by(
            desc(Operation.id_op)    
        ).paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    
    return operation


def get_operation_by_id_op(id_op:int):
    operation = Operation.query.get(id_op)
    return operation


def get_wms_typeop_by_id_top(id_top):
    '''
        Получение данных по типовой по id
    '''
    typeop = Typeop.query.get(id_top)
    return typeop



def get_wms_typeop_for_create():
    '''
        Получение списка типовых, доступных для создания в WMS части приложения
    '''
    typeop = Typeop.query.filter(Typeop.name.in_([TOP_INCOME, TOP_INVOCE, TOP_MOVEMENT])).order_by(Typeop.name).all()
    return typeop


def get_wms_redirection_by_typeop(id_top:int):
    '''
        Определение "направления" создания операции в зависимости от типа
    '''
    typeop = get_wms_typeop_by_id_top(id_top)
    if typeop.name == TOP_INCOME:
        return 'create_arrival'
    if typeop.name == TOP_INVOCE:
        return 'create_consumption'
    if typeop.name == TOP_MOVEMENT:
        return 'create_movement'
    

def get_wms_warehouse_by_typeop(id_top:int):
    '''
        Получение списка доступных МХ для создания операций в зависимости от типа операции
    '''
    typeop = get_wms_typeop_by_id_top(id_top)
    if typeop.name == TOP_INCOME:
        ws_list = Warehouse.query.filter(Warehouse.name.in_([WS_STORAGE, WS_TRANSIT])).order_by(Warehouse.name).all()
        return ws_list
    if typeop.name == TOP_INVOCE:
        ws_list = Warehouse.query.filter(Warehouse.name.in_([WS_STORAGE])).order_by(Warehouse.name).all()
        return ws_list
    if typeop.name == TOP_MOVEMENT:
        ws_list = Warehouse.query.filter(Warehouse.name.in_([WS_STORAGE, WS_RETAIL, WS_ONLINE, WS_TRANSIT])).order_by(Warehouse.name).all()
        return ws_list


def get_wms_opstatus_for_create(id_top:int):
    '''
        Получение "низкого" статуса операции для создания операции
    '''
    status = Opstatus.query.filter(and_(Opstatus.id_top == id_top, Opstatus.status_name == STATUS_UNFORMED)).all()
    return status

    
def recalc_op_sum(id_op:int):
    '''
        Пересчет суммы операции
    '''
    opsum = Opart.query.with_entities(func.coalesce(func.sum(Opart.opsum), 0)).filter(Opart.id_op == id_op).scalar()
    operation = Operation.query.get(id_op)
    operation.opsum = opsum
    db.session.add(operation)
    db.session.commit()


def create_wms_operation(id_top:int, opnumber:str, opdate, status:int, id_wso:int=None, id_wsi:int=None):
    operation = Operation(
    id_top=id_top,
    id_wso = id_wso,
    id_wsi = id_wsi,
    opnumber = opnumber,
    opdate = opdate,
    status = status,
    opsum = 0.0,
    )
    db.session.add(operation)
    db.session.commit()
    return operation
    