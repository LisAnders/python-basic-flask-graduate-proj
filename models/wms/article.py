from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, func
from sqlalchemy.orm import relationship
from flask_sqlalchemy.query import Query
from models.database import db


class Article(db.Model):
    id_art = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False, default='', server_default='')
    is_online = Column(Boolean, nullable=False, default=False)
    lastdate = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    price_buy = Column(Float, nullable=True)
    price_sale = Column(Float, nullable=True)
    
    rest = relationship('Rest', back_populates='article')
    opart = relationship('Opart', back_populates='article')
    artbarcode = relationship('ArtBarcode', back_populates='article')

    if TYPE_CHECKING:
        query: Query
        