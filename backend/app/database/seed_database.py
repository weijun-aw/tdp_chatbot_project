from sqlalchemy.orm import Session

from src.users.model import Users


from .database import SessionLocal


def is_database_seeded(db: Session):
    return db.query(Users).first() is not None


def add_dummy_query_history():
    db = SessionLocal()

    try:
        if is_database_seeded(db):
            print("Database is already seeded. Skip seeding.")
            return

        # Create a dummy QueryHistory Record
        dummy_query = Users(
            user_id=101,
            query= "What is Owala?"
        )

        db.add(dummy_query)
        db.commit()

        dummy_query_2 = Users(
            user_id=102,
            query="How much is an Owala?",
  
        )

        db.add(dummy_query_2)
        db.commit()


        print("Dummy QueryHistory records added successfully!")


    except Exception as e:
        print(f"Error: {e}")

    finally:
        db.close()
