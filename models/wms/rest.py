from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from models.database import db


class Rest(db.Model):
    
    rest_id = Column(Integer, primary_key=True,)
    id_ws = Column(
        Integer,
        ForeignKey('warehouse.id_ws', name='fk_id_ws'),
        nullable=False,
        unique=False,
    )
    id_art = Column(
        Integer,
        ForeignKey('article.id_art', name='fk_id_art'),
        nullable=False,
        unique=False,
    )
    quantity = Column(
        Float,
        nullable=False,
        default=0
    )
    lastdate = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    
    warehouse = relationship('Warehouse', back_populates='rest')
    article = relationship('Article', back_populates='rest')