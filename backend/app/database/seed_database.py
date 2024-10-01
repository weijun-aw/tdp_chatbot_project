from sqlalchemy.orm import Session

from src.users.model import Users, Accounts, Transactions
from datetime import date


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
            username = "Alisson Becker",
            password = "goalkeeper",
            address = "100 Anfield Road",
            dob = date(1992,10,2),
            number = "99933322",
            email = "alissonbecker@gmail.com"
            
        )

        db.add(dummy_query)
        db.commit()

        dummy_query_2 = Users(
            user_id=102,
            username = "Joe Gomez",
            password = "centreback",
            address = "200 Anfield Road",
            dob = date(1997,5,23),
            number = "99933333",
            email = "joegomez@gmail.com"
  
        )

        db.add(dummy_query_2)
        db.commit()

        dummy_query_3 = Accounts(
            account_id = 10001,
            user_id = 101,
            account_type = "Savings",
            balance = 2000000.94
        )

        db.add(dummy_query_3)
        db.commit()

        dummy_query_4 = Accounts(
            account_id = 10002,
            user_id = 102,
            account_type = "Savings",
            balance = 1854326.94
        )

        db.add(dummy_query_4)
        db.commit()

        dummy_query_5 = Transactions(
            transaction_id = 100001,
            account_id = 10001,
            transaction_type = "Transfer",
            amount = 60000,
            date_of_transaction = date(2024,9,26),
            description = "Weekly Wages",
            location = "Liverpool, United Kingdom"
        )

        db.add(dummy_query_5)
        db.commit()


        print("Dummy QueryHistory records added successfully!")


    except Exception as e:
        print(f"Error: {e}")

    finally:
        db.close()
