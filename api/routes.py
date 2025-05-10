from fastapi import APIRouter

from interactions import interactions_router
from posts import post_router
from users import user_router

router = APIRouter()

router.include_router(router=user_router, prefix="/users", tags=["users"])
router.include_router(router=post_router, prefix="/posts", tags=["posts"])
router.include_router(router=interactions_router, prefix="/posts/i", tags=["interactions"])
