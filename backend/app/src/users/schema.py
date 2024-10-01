from pydantic import BaseModel
from datetime import date

class Query(BaseModel):
    user_input : str
    chatbot_response : str

class ChatMessage(BaseModel):
    message : str

class Users(BaseModel):

    username : str
    password : str
    address  : str
    dob  : date
    number : str
    email  : str


class Accounts(BaseModel):

 
    user_id : int
    account_type : str
    balance : float
    overseas_limit : float
    #transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'))

class Transactions(BaseModel):

    account_id : int
    transaction_type : str
    amount : float
    date_of_transaction : date
    description : str
    location : str
