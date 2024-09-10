from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.database import get_db

from ..users.crud import get_user_query_by_id, create_query
from ..users.schema import (
    User
)


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses= {404: {"description": "Not found"}}
)

@user_router.get(
    "/{id}", response_model=User, status_code=status.HTTP_200_OK
)
def get_user_query(id: int, db: Session = Depends(get_db)):
    query_details = get_user_query_by_id(db, id=id)
    if query_details is None:
        raise HTTPException(
            status_code=404, details= "Query history not found in database"
        ) 
    return query_details

@user_router.post("/create_query/{id}", status_code=201 ,response_model=User)
async def create_response(user: User, db: Session = Depends(get_db)):

    new_user = create_query(db, user)

    return new_user