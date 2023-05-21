from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from models.database import db

class Typeop(db.Model):
    
    id_top = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    num_mask = Column(String(10), unique=True, nullable=False)
    last_num = Column(Integer, unique=False, nullable=False)
    typeio = Column(Integer, unique=False, nullable=False)
    lastdate = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    
    opstatus = relationship('Opstatus', back_populates='typeop')
    operation = relationship('Operation', back_populates='typeop')