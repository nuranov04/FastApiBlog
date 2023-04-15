from fastapi import APIRouter

from apps.users.routers import router as users
from apps.posts.routers import routers as posts
from apps.likes.routers import router as likes

router = APIRouter()

router.include_router(prefix="/users", router=users)
router.include_router(prefix="/posts", router=posts)
router.include_router(prefix="/likes", router=likes)
