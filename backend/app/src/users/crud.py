from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from fastapi import HTTPException, status

from ..users.model import Users

# read a single user by id
def get_user_query_by_id(db: Session, id: int):
    query_details = db.query(Users).filter(Users.user_id == id).first()
    db.close()
    return query_details

def create_query(db: Session, user: Users):

    new_user = Users(
        # questionnaire_id = user.questionnaire_id,
        query   = user.query
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
