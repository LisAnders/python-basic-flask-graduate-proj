from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from models.database import db


class Warehouse(db.Model):
    id_ws = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    lastdate = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    rest = relationship('Rest', back_populates='warehouse')