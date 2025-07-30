# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AuthRefreshTokenResponse"]


class AuthRefreshTokenResponse(BaseModel):
    access_token: Optional[str] = None
    """JWT access token"""

    expires_in: Optional[int] = None
    """Token expiration time in seconds"""

    token_type: Optional[str] = None
