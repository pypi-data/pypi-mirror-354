# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AuthLoginResponse"]


class AuthLoginResponse(BaseModel):
    access_token: Optional[str] = None
    """JWT Bearer token"""

    expires_in: Optional[int] = None
    """Token expiration in seconds"""

    token_type: Optional[str] = None
    """Token Type"""
