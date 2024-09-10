import os 

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    return f"{os.getenv('DB_ENGINE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def get_async_database_url() -> str:
    return f"{os.getenv('ASYNC_DB_ENGINE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


def get_secret() -> str:
    return os.getenv('SECRET')