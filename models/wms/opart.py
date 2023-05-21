from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func, UniqueConstraint
from sqlalchemy.orm import relationship
from models.database import db

class Opart(db.Model):
    id_opart = Column(Integer, primary_key=True)
    id_op = Column(
        Integer,
        ForeignKey('operation.id_op', name='fk_opart_id_op'),
        nullable=False,
        unique=False
    )
    id_art = Column(
        Integer,
        ForeignKey('article.id_art', name='fk_opart_id_art'),
        unique=False,
        nullable=False
    )
    quantity = Column(Float, unique=False, nullable=False)
    price = Column(Float, unique=False, nullable=False)
    opsum = Column(Float, unique=False, nullable=False)
    lastdate = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    UniqueConstraint(id_op, id_art, name='unique_id_op_id_art')
    
    operation = relationship('Operation', back_populates='opart')
    article = relationship('Article', back_populates='opart')