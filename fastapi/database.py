from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends

sqlite_file_name= "sql.db"
sqlite_url = f"sql:///../{sqlite_file_name}"

engine = create_engine(sqlite_url,connect_args={"check_same_thread": False})

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_depends = Annotated[Session, Depends(get_session)]