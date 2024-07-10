from .app import app
from .endpoints.v1 import router as v1_router

app.include_router(v1_router, prefix="/v1")
