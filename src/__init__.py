import logging

from .app import app
from .endpoints.v1 import router as v1_router

logger = logging.getLogger("uvicorn.api").getChild(__name__)
logger.debug("Debug Mode Enabled")

app.include_router(v1_router, prefix="/v1")
