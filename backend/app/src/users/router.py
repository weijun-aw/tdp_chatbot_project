from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.database import get_db

from ..users.crud import get_user_detail, create_user_detail, model_test, create_transaction, update_account_details,model_test_two, get_transaction_detail, get_user_balance, update_account_overseas_limit
from ..users.schema import (
    Query, Users, Accounts, Transactions, ChatMessage
)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses= {404: {"description": "Not found"}}
)

@user_router.post("/chat")
async def chatbot_logic(msg: ChatMessage):
    print(msg.message)
    response = model_test_two(msg)
    return {"response" : response}

@user_router.get(
    "/{id}", status_code=status.HTTP_200_OK
)
def get_user(id: int, db: Session = Depends(get_db)):
    user_details = get_user_detail(db, id=id)
    if user_details is None:
        raise HTTPException(
            status_code=404, details= "Query history not found in database"
        ) 
    return user_details

@user_router.post("/create_user/{id}", status_code=201 ,response_model=Users)
async def create_user(user: Users, db: Session = Depends(get_db)):

    new_user = create_user_detail(db, user)

    return new_user

@user_router.post("/create_bryan_response/{id}", status_code=201 ,response_model=Query)
async def create_bryan_response(query: Query, db: Session = Depends(get_db)):

    new_user = model_test(db, query)

    return new_user

@user_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_transaction(id: int, db: Session = Depends(get_db)):
    transaction_list = get_transaction_detail(db, id=id)
    if transaction_list is None:
        raise HTTPException(
            status_code=404, details= "Query history not found in database"
        ) 
    return transaction_list

@user_router.post("/create_transaction_record/{account_id}", status_code=201 ,response_model=Transactions)
async def create_transaction_record(transaction: Transactions, db: Session = Depends(get_db)):

    new_user = create_transaction(db, transaction)

    return new_user

@user_router.put("/update_transaction_record/{id}")
async def update_account(account_id: int, transaction_id : int, db: Session = Depends(get_db)):
    if account_id is None:
        raise HTTPException(status_code=404, detail="Account not found")

    updated_account = update_account_details(db, account_id, transaction_id)

    return updated_account

@user_router.put("/allow_overseas_transaction")
def update_overseas_limit(overseas_limit: float, account_id : int ,db: Session = Depends(get_db)):
    """
    Update the overseas transaction limit for the user.
    """
    # Query the database to get the user's current settings
    user_details = update_account_overseas_limit(db, account_id, overseas_limit)
    
    # If user is not found
    if user_details is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"Your overseas transaction limit has been updated to {overseas_limit}."}

@user_router.get("/balance/{id}", status_code=status.HTTP_200_OK)
def get_balance(id: int, db: Session = Depends(get_db)):
    balance_information = get_user_balance(db, id=id)
    if balance_information is None:
        raise HTTPException(
            status_code=404, details= "Query history not found in database"
        ) 
    return balance_information