from fastapi import APIRouter

from src.app import app
from src.scheme.version import VersionResponse

router = APIRouter()


@router.get("/")
async def get_version() -> VersionResponse:
    version: str = app.version
    return VersionResponse(version=version)
