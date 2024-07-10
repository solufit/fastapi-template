from fastapi import FastAPI, APIRouter

from ...scheme.version import VersionResponse
from ...app import app

router = APIRouter()

@router.get("/")
async def get_version():
    version: str = app.version
    return VersionResponse(version=version)