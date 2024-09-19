from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from database.database import Base, engine
from database.seed_database import add_dummy_query_history
from src.users import model 
from src.users.router import user_router
from src.algorithm import chat

Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["http://127.0.0.1:3000", "http://localhost:3000", "http://localhost:4173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

add_dummy_query_history()

app.get("/")
def home_ping():
    return "success"