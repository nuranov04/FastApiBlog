from fastapi import APIRouter

from apps.users.routers import router as users

router = APIRouter()

router.include_router(prefix="/users", router=users)
