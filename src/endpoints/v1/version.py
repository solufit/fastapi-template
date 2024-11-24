"""This module defines the version endpoint for the FastAPI application."""

from logging import getLogger

from fastapi import APIRouter

from src.app import app
from src.scheme.version import VersionResponse

router = APIRouter()

logger = getLogger("uvicorn.api.v1").getChild(__name__)


@router.get("/")
async def get_version() -> VersionResponse:
    """Retrieve the current version of the application."""
    version: str = app.version
    logger.info("Version Function was called.")
    return VersionResponse(version=version)
