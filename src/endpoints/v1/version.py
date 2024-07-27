from logging import getLogger

from fastapi import APIRouter

from src.app import app
from src.scheme.version import VersionResponse

router = APIRouter()

logger = getLogger("uvicorn.api.v1").getChild(__name__)


@router.get("/")
async def get_version() -> VersionResponse:
    version: str = app.version
    logger.info("Version Function was called.")
    return VersionResponse(version=version)
