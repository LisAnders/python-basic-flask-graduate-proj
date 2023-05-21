from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, DateTime, Float, func
from sqlalchemy.orm import relationship

from models.database import db


class User(db.Model, UserMixin):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False, server_default='')
    active = Column(Boolean, nullable=False, server_default='0')
    roles = relationship('Role', secondary='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)
    
    def __str__(self):
        return self.name
    


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))