"""This module contains the APIDetail class which provides metadata and configuration for the API."""


class APIDetail:
    """APIDetail class contains metadata and configuration for the FastAPI Template API.

    Attributes:
        API_TITLE (str): The title of the API.
        DESCRIPTION (str): A brief description of the API.
        VERSION (str): The version of the API.
        OPENAPI_URL (str): The URL path for the OpenAPI schema.
        DOCS_URL (str): The URL path for the interactive API documentation (Swagger UI).
        REDOC_URL (str): The URL path for the ReDoc documentation.
    """

    API_TITLE = "FastAPI Template API"
    DESCRIPTION = """
        FastAPI Template API is a template for creating a FastAPI project.
    """
    VERSION = "1.0.0"
    OPENAPI_URL = "/openapi.json"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
