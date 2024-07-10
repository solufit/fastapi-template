from fastapi import APIRouter

from .version import router as version_router

router = APIRouter()

# Add your API routes here

router.include_router(version_router)

