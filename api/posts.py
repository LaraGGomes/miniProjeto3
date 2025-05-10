import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from database import CreatePost, session_deps, Post
from users import get_current_user

post_router = APIRouter()


@post_router.post("/")
async def create_post(*, post: CreatePost, session: session_deps,
                      current_user: Annotated[uuid.UUID, Depends(get_current_user)]):
    try:
        post_db = Post.model_validate(post)
        post_d = {
            "content": post_db.content,
            "author": current_user
        }
        
        session.add(post_d)
        session.commit()

    except:
        raise HTTPException(status_code=500, detail="Couldn't create post")

    return post_db.id
