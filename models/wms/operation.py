from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float, func
from sqlalchemy.orm import relationship
from models.database import db

class Operation(db.Model):
    
    id_op = Column(Integer, primary_key=True)
    id_top = Column(
        Integer,
        ForeignKey('typeop.id_top', name='fk_operation_id_top'),
        nullable=False,
        unique=False
    )
    id_wso = Column(
        Integer,
        ForeignKey('warehouse.id_ws', name='fk_operation_id_wso'),
        nullable=True,
        unique=False
    )
    id_wsi = Column(
        Integer,
        ForeignKey('warehouse.id_ws', name='fk_operation_id_wsi'),
        nullable=True,
        unique=False
    )
    opnumber = Column(String(20), nullable=False, unique=False)
    opdate = Column(Date, nullable=False, default=datetime.today)
    status = Column(
        Integer,
        nullable=False,
        unique=False
    )
    opsum = Column(Float, nullable=False, unique=False)
    lastdate = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    
    typeop = relationship('Typeop', back_populates='operation')
    opart = relationship('Opart', back_populates='operation')