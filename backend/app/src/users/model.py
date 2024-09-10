#from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, ForeignKey, Column, String

from database.database import Base

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    query = Column(String)
