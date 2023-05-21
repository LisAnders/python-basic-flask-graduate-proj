from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.database import db

class Opstatus(db.Model):
    
    id = Column(Integer, primary_key=True)
    id_top = Column(
        Integer,
        ForeignKey('typeop.id_top', name='fk_opstatus_id_top'),
        nullable=False,
        unique=False
    )
    status_code = Column(Integer, nullable=False, unique=False)
    status_name = Column(String(30), nullable=False, unique=False)
    
    typeop = relationship('Typeop', back_populates='opstatus')
