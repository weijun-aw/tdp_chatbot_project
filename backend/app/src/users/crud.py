from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import DATE


from fastapi import HTTPException, status

from ..users.model import  Query, Users, Accounts, Transactions

from ..algorithm.chat import bryan_chatbot

# read a single user by id
def get_user_detail(db: Session, id: int):
    user_info = db.query(Users).filter(Users.user_id == id).first()
    db.close()
    return user_info

def create_user_detail(db: Session, user: Users):

    new_user = Users(
        # questionnaire_id = user.questionnaire_id,
        username = user.username,
        password = user.password,
        address = user.address,
        dob = user.dob,
        number = user.number,
        email = user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def model_test(db: Session, query_information:Query):

    input = query_information.user_input

    response = bryan_chatbot(input)

    print(response)

    db.add(query_information)
    db.commit()
    db.refresh(query_information)
    return query_information

def model_test_two(msg:str):

    response = bryan_chatbot(msg)

    return response
   
def create_transaction(db: Session, transaction: Transactions):

    new_transaction_record = Transactions(

        account_id = transaction.account_id,
        transaction_type = transaction.transaction_type,
        amount = transaction.amount,
        date_of_transaction = transaction.date_of_transaction,
        description = transaction.description,
        location = transaction.location
    )

    db.add(new_transaction_record)
    db.commit()
    db.refresh(new_transaction_record)
    return new_transaction_record

def update_account_details(db: Session, account_id : int, transaction_id : int):

    # Retrieve account info
    account_information = db.query(Accounts).filter(Accounts.account_id == account_id).first()
    current_amount = account_information.balance

    # Retrieve transaction info
    transaction_information = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
    transaction_amount = transaction_information.amount
    transaction_type = transaction_information.transaction_type

    if transaction_type == 'Transfer':
        new_amount = current_amount + transaction_amount
        print(new_amount)
        account_information.balance = new_amount

        #account_information.balance = new_amount
        db.commit()
        db.refresh(account_information)

    return account_information

# Haven't Test this
def get_transaction_detail(db: Session, account_id : int, transaction_id : int, date_transaction : DATE):
    transaction_info = db.query(Transactions).filter(Transactions.account_id == account_id, Transactions.date_of_transaction == date_transaction ).all()
    db.close()
    return transaction_info

def get_user_balance(db: Session, id: int):
    user_balance_info = db.query(Accounts).filter(Accounts.account_id == id).first()
    balance = user_balance_info.balance
    db.close()
    return balance

def update_account_overseas_limit(db: Session, account_id : int, new_overseas_limit : float):

    # Retrieve account info
    account_information = db.query(Accounts).filter(Accounts.account_id == account_id).first()
    account_information.overseas_limit = new_overseas_limit

    db.commit()
    db.refresh(account_information)

    return account_information

