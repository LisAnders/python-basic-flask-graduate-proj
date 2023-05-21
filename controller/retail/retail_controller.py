from datetime import date, datetime
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from sqlalchemy.sql import and_, func
from models import db, Typeop, Operation, Opstatus, Warehouse, Opart, Article, ArtBarcode, Rest
from ..constants import TOP_SALE, WS_RETAIL, STATUS_SOLD, STATUS_HOLD, STATUS_CANCELED, STATUS_UNFORMED


ITEMS_PER_PAGE = 10


def get_typeop_for_retail():
    '''
        Получение типовой "Продажа"
    '''
    typeop = Typeop.query.filter(Typeop.name == TOP_SALE).one()
    return typeop


def get_ws_for_retail():
    '''
        Получение МХ "Торговый зал"
    '''
    ws = Warehouse.query.filter(Warehouse.name == WS_RETAIL).one()
    return ws


def get_retail_operation_list(page:int):
    '''
        Получение списка операций типа "Продажа"
    '''
    top = get_typeop_for_retail()
    operation_list = Operation.query.join(
        Opstatus,
        and_(Operation.status == Opstatus.status_code, Operation.id_top==Opstatus.id_top)
        ).filter(
        and_(Operation.opdate == date.today(), Operation.id_top==top.id_top)
        ).add_columns(
        Operation.id_op,
        Operation.opnumber,
        Operation.opdate,
        Operation.opsum,
        Opstatus.status_name
        ).order_by(
        desc(Operation.id_op)    
        ).paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    return operation_list


def get_retail_operation_detail(id_op):
    '''
        Получение данных по конкретной операции "Продажа"
    '''
    top = get_typeop_for_retail()
    operation_detail = Operation.query.filter(and_(Operation.id_op == id_op, Operation.id_top==top.id_top)).one()
    return operation_detail    


def get_retail_opart(id_op:int):
    '''
        Получение списко позиций по операции 
    '''
    op = aliased(Operation)
    art = aliased(Article)
    retail_opart = Opart.query.join(
        op,
        Opart.id_op==op.id_op
        ).join(
            art,
            Opart.id_art==art.id_art
        ).filter(
            Opart.id_op==id_op
        ).add_columns(
            Opart.id_opart,
            art.code,
            art.name,
            Opart.quantity,
            Opart.price,
            Opart.opsum
        ).order_by(
            Opart.id_opart
        ).all()
    return retail_opart

def get_retail_article_list():
    article = Article.query.all()
    return article


def get_retail_status_by_name(name=STATUS_UNFORMED):
    top = get_typeop_for_retail()
    opstatus = Opstatus.query.filter(and_(Opstatus.id_top==top.id_top,Opstatus.status_name==name)).one_or_none()
    return opstatus


def get_article_by_barcode(barcode:str):
    '''
        Получение товара по ШК
    '''
    article = Article.query.join(
        ArtBarcode,
        Article.id_art == ArtBarcode.id_art
    ).filter(ArtBarcode.barcode==barcode
    ).one_or_none()
    return article


def create_retail_op():
    '''
        Создание операции "Продажа"
    '''
    top = get_typeop_for_retail()
    status = get_retail_status_by_name()
    top.last_num += 1
    opnum = top.last_num
    ws = get_ws_for_retail()
    retail_op = Operation(
        id_top = top.id_top,
        id_wso = ws.id_ws,
        opnumber = opnum,
        status = status.status_code,
        opsum = 0.0
    )
    db.session.add(retail_op, top)
    db.session.commit()
    return retail_op


def create_retail_opart(id_op:int, id_art:int, quantity:float, price:float):
    '''
        Создание товарной позиции операции "Продажа" вариант - выбор ТП из справочника ТП
    '''
    retail_opart = Opart(
    id_op = id_op,
    id_art = id_art,
    quantity = quantity,
    price = price,
    opsum = price * quantity,
        )
    db.session.add(retail_opart)
    db.session.commit()
    return retail_opart


def recalc_retail_rest(id_art:int, quantity:float=1.0):
    '''
        Пересчет остатка ТП операций "Продажа"
    '''
    ws = get_ws_for_retail()
    rest = Rest.query.filter(and_(Rest.id_art==id_art, Rest.id_ws==ws.id_ws)).one()
    rest.quantity-=quantity
    rest.lastdate = datetime.utcnow()
    db.session.add(rest)
    db.session.commit()


def get_retail_op_sum(id_op:int):
    opsum = Opart.query.with_entities(func.coalesce(func.sum(Opart.opsum), 0)).filter(Opart.id_op == id_op).scalar()
    return opsum


def recalc_retail_op_sum(id_op:int):
    '''
        Пересчет суммы операции
    '''
    opsum = get_retail_op_sum(id_op=id_op)
    operation = Operation.query.get(id_op)
    operation.opsum = opsum
    db.session.add(operation)
    db.session.commit()

def create_retail_opart_by_barcode(id_op:int, barcode:str):
    '''
        Создание товарной позиции операции "Продажа". 
        Вариант - поиск ТП по ШК
    '''
    article = get_article_by_barcode(barcode=barcode)
    if article:
        opart = Opart.query.filter(and_(Opart.id_op==id_op, Opart.id_art==article.id_art)).one_or_none()
        if opart:
            opart.quantity += 1
            opart.opsum = opart.price*opart.quantity
            db.session.add(opart)
            db.session.commit()
        else:
            opart = Opart(id_op=id_op, id_art=article.id_art, quantity=1, price=article.price_sale)
            opart.opsum = opart.price*opart.quantity
            db.session.add(opart)
            db.session.commit()
        recalc_retail_op_sum(id_op=opart.id_op)
        recalc_retail_rest(id_art=opart.id_art)
        return opart


def update_retail_opart_quantity(id_opart:int, quantity:float):
    '''
        Изменение кол-ва по ТП операции на экране продаж
    '''
    opart = Opart.query.get(id_opart)
    old_quantity = opart.quantity
    opart.quantity = quantity
    opart.opsum = opart.price * quantity
    db.session.add(opart)
    db.session.commit()
    new_quantity = quantity-old_quantity 
    recalc_retail_op_sum(id_op=opart.id_op)
    recalc_retail_rest(id_art=opart.id_art, quantity=new_quantity)
    return opart


def delete_retail_opart(id_opart:int):
    opart = Opart.query.get(id_opart)
    db.session.delete(opart)
    db.session.commit()
    return opart


def set_op_status_sold(id_op):
    '''
        Изменение статуса операции на "Проведена"
    '''
    operation = Operation.query.filter(Operation.id_op==id_op).one_or_none()
    status = get_retail_status_by_name(STATUS_SOLD)
    operation.status = status.status_code
    db.session.add(operation)
    db.session.commit()
    