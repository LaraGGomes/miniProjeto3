import uuid
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Field, Session, create_engine


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(default=None)
    username: str = Field(default=None, unique=True)
    password: str
    profile_image: str | None = Field(default=None, nullable=True)


class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    author: uuid.UUID = Field(foreign_key="user.id")
    like_count: int = Field(default=0)


class LikedPost(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="post.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")


class UserRegister(SQLModel):
    name: str
    username: str
    password: str


class CreateUpdatePost(SQLModel):
    content: str


engine = create_engine("sqlite:///fuckerberg.db", echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


session_deps = Annotated[Session, Depends(get_session)]
