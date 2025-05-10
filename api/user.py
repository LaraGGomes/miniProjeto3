from fastapi import APIRouter, HTTPException
from sqlmodel import select

from database import UserRegister, User, session_deps

user_router = APIRouter()


@user_router.post("/register")
def create_user(*, user: UserRegister, session: session_deps):
    user_db = User.model_validate(user)

    statement = select(User).where(User.name == user_db.name)
    results = session.exec(statement).first()

    if results:
        raise HTTPException(status_code=409, detail="Username already taken")

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db.id
