from models import db, User, Role, UserRoles
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import func, String



def get_users():
    users = User.query.join(
                UserRoles,
                User.id == UserRoles.user_id,
                isouter=True
                ).join(
                Role,
                Role.id==UserRoles.role_id,
                isouter=True     
                ).add_columns(
                User.id,
                User.username,
                func.array_agg(Role.name, type_=ARRAY(String)).label('role')    
                ).group_by(
                User.id
                ).all()
    return users