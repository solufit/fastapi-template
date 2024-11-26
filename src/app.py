"""This module initializes and configures the FastAPI application.

If you want to change the title, description, version, or URLs of the API documentation, you can do so by modifying
the values in the APIDetail class in the app_detail.py module.

"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.app_detail import APIDetail

app = FastAPI(
    title=APIDetail.API_TITLE,
    description=APIDetail.DESCRIPTION,
    version=APIDetail.VERSION,
    openapi_url=APIDetail.OPENAPI_URL,
    docs_url=APIDetail.DOCS_URL,
    redoc_url=APIDetail.REDOC_URL,
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
