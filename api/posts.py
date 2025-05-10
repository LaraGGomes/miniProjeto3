import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from database import CreateUpdatePost, session_deps, Post
from users import get_current_user

post_router = APIRouter()


@post_router.get("/feed")
async def get_feed(
        session: session_deps,
):
    statement = select(Post)
    posts = session.exec(statement).all()
    return posts


@post_router.post("/")
async def create_post(*, post: CreateUpdatePost, session: session_deps,
                      current_user: Annotated[uuid.UUID, Depends(get_current_user)]):
    try:
        post = Post(author=current_user, content=post.content)

        session.add(post)
        session.commit()
        session.refresh(post)

    except:
        raise HTTPException(status_code=500, detail="Couldn't create post")

    return post.id


@post_router.get("/")
async def get_my_posts(
        session: session_deps,
        current_user: Annotated[uuid.UUID, Depends(get_current_user)]
):
    statement = select(Post).where(Post.author == current_user)
    posts = session.exec(statement).all()
    return posts


@post_router.put("/{post_id}")
async def edit_post(
        session: session_deps,
        current_user: Annotated[uuid.UUID, Depends(get_current_user)],
        post: CreateUpdatePost,
        post_id: uuid.UUID,
):
    post_db = session.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_db.author != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")

    post_db.content = post.content
    session.add(post_db)
    session.commit()
    session.refresh()

    return post_db.id


@post_router.delete("/{post_id}")
async def edit_post(
        session: session_deps,
        current_user: Annotated[uuid.UUID, Depends(get_current_user)],
        post_id: uuid.UUID,
):
    post_db = session.get(Post, post_id)

    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_db.author != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    session.delete(post_db)
    session.commit()

    return post_db.id
