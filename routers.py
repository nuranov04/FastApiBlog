from fastapi import APIRouter

from apps.users.routers import router as users
from apps.posts import routers as posts

router = APIRouter()

router.include_router(prefix="/users", router=users)
router.include_router(prefix="/posts", router=posts)
