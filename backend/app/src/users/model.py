#from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, ForeignKey, Column, String, DATE, DateTime, FLOAT

from database.database import Base


class Query(Base):
    __tablename__ = "query"
    query_id = Column(Integer, primary_key=True)
    user_input = Column(String)
    chatbot_response = Column(String)

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String) #Not best practice, will change later
    address = Column(String)
    dob = Column(DATE)
    number = Column(String)
    email =  Column(String)
    #account_id = Column(Integer, ForeignKey('accounts.account_id')) # May need to contest this
    #query = Column(String)


class Accounts(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.user_id))
    account_type = Column(String)
    balance = Column(FLOAT)
    overseas_limit = Column(FLOAT)
    #transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'))

class Transactions(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey(Accounts.account_id))
    transaction_type = Column(String)
    amount = Column(FLOAT)
    date_of_transaction = Column(DATE)
    description = Column(String)
    location = Column(String)


