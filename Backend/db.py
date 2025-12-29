from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
from dotenv import load_dotenv
load_dotenv()



# DATABASE_URL = os.getenv("DATABASE_URL")
DEV_DATABASE_URL = os.getenv("DEV_DATABASE_URL")
engine = create_engine(DEV_DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
        