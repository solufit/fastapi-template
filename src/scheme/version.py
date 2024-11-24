from pydantic import BaseModel


class VersionResponse(BaseModel):
    """Model representing a version response."""

    version: str
