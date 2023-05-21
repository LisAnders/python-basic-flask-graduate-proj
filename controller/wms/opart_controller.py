from sqlalchemy.orm import aliased
from models import db, Operation, Article, Opart


def get_operation_article_by_id_op(id_op:int):
    op = aliased(Operation)
    art = aliased(Article)
    opart = Opart.query.join(
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
        ).all()
    return opart


def get_opart_detail(id_opart:int):
    opart = Opart.query.get(id_opart)
    return opart


def wms_create_opart(id_op:int, id_art:int, quantity:float, price:float):
    opart = Opart(
        id_op = id_op,
        id_art = id_art,
        quantity = quantity,
        price = price,
        opsum = price * quantity,
    )
    db.session.add(opart)
    db.session.commit()
    return opart


def wms_update_opart(id_opart:int, old_quantity:float, new_quantity:float, price:float):
    opart = get_opart_detail(id_opart)
    opart.price = price
    opart.quantity = new_quantity
    opart.opsum = new_quantity * price
    db.session.add(opart)
    db.session.commit
    new_quantity-=old_quantity
    return new_quantity

def wms_delete_opart(id_opart:int):
    opart = get_opart_detail(id_opart)
    db.session.delete(opart)
    db.session.commit()
    old_quantity = -opart.quantity
    return old_quantity