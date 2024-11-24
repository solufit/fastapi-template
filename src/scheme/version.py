"""This module defines the VersionResponse model."""

from pydantic import BaseModel


class VersionResponse(BaseModel):
    """Model representing a version response."""

    version: str
