from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status

from api.model import Post
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)
class PostBase(BaseModel):
    content : str
    user_id : int
class PostCreate(PostBase):
    pass 

@router.get('/')
def get_post(db: db_dependency, user: user_dependency, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()
@router.get('/posts')
def get_posts(db: db_dependency, user: user_dependency):
    return db.query(Post).all()
@router.post("/", status_code=status.HTTP_201_CREATED)
def creat_post(db: db_dependency, user: user_dependency, post: PostCreate):
    db_posts = Post(**post.model_dump,user_id= user.get('id'))
    db.add(db_posts)
    db.commit()
    db.refresh(db_posts)
    return db_posts

@router.delete("/")
def delete_post(db: db_dependency, user: user_dependency, post_id: int):
    db_posts = db.query(Post).filter(Post.id == post_id).first()
    if db_posts:
        db.delete(db_posts)
        db.commit()
    return db_posts
