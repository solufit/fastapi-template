from fastapi import APIRouter

from .version import router as version_router
from .user import router as user_router

router = APIRouter()

# Add your API routes here

router.include_router(version_router)
router.include_router(user_router)
