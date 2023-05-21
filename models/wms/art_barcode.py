from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, DateTime, Float, func
from sqlalchemy.orm import relationship
from models.database import db

class ArtBarcode(db.Model):
    barcode_id = Column(Integer, primary_key=True)
    id_art = Column(
        Integer,
        ForeignKey('article.id_art', name='fk_art_barcode_id_art'),
        nullable=False,
        unique=False,
    )
    barcode = Column(String, nullable=False, unique=True)
    
    article = relationship('Article', back_populates='artbarcode')