from src.endpoints.v1 import router as v1_router
from .app import app

app.include_router(v1_router, prefix="/v1")