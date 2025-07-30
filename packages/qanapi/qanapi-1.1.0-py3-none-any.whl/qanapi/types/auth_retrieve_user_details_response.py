# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["AuthRetrieveUserDetailsResponse"]


class AuthRetrieveUserDetailsResponse(BaseModel):
    id: Optional[int] = None

    email: Optional[str] = None

    email_verified_at: Optional[datetime] = None

    first_login: Optional[int] = None

    gravatar_url: Optional[str] = None

    name: Optional[str] = None

    roles: Optional[List[str]] = None
