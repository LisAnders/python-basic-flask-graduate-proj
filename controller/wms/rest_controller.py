from datetime import datetime
from models import db, Rest
from ..constants import TYPEIO_IN, TYPEIO_OUT, TYPEIO_MOVE

def recalc_rests(id_art:int, id_wsi:int, id_wso:int, quantity:float, typeio:int ): 
    '''
        Набросок логики пересчета остатков по позициям при добавлении ТП
    '''
    rest_wso = Rest.query.filter(Rest.id_art==id_art).filter(Rest.id_ws==id_wso).one_or_none()
    rest_wsi = Rest.query.filter(Rest.id_art==id_art).filter(Rest.id_ws==id_wsi).one_or_none()
    if typeio == TYPEIO_IN:
        if not rest_wsi:
            rest = Rest(id_ws=id_wsi, id_art=id_art, quantity=quantity)
            db.session.add(rest)
            db.session.commit()
        else:
            rest_wsi.quantity += quantity
            rest_wsi.lastdate = datetime.utcnow()
            db.session.add(rest_wsi)
            db.session.commit()
    
    if typeio == TYPEIO_OUT:
        if not rest_wso:
            rest = Rest(id_ws=id_wso, id_art=id_art, quantity=-quantity)
            db.session.add(rest)
            db.session.commit()
        else:
            rest_wso.quantity -= quantity
            rest_wso.lastdate = datetime.utcnow()
            db.session.add(rest_wso)
            db.session.commit()                     
    
    if typeio == TYPEIO_MOVE:
        if not rest_wsi:
            rest = Rest(id_ws=id_wsi, id_art=id_art, quantity=quantity)
            db.session.add(rest)
            db.session.commit()
        else:
            rest_wsi.quantity += quantity
            rest_wsi.lastdate = datetime.utcnow()
            db.session.add(rest_wsi)
            db.session.commit()            

        if not rest_wso:
            rest = Rest(id_ws=id_wso, id_art=id_art, quantity=-quantity)
            db.session.add(rest)
            db.session.commit()
        else:
            rest_wso.quantity -= quantity
            rest_wso.lastdate = datetime.utcnow()
            db.session.add(rest_wso)
            db.session.commit()     