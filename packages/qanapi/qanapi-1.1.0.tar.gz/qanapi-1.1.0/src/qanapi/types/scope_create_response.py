# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["ScopeCreateResponse"]


class ScopeCreateResponse(BaseModel):
    id: Optional[int] = None

    created_at: Optional[datetime] = None

    name: Optional[str] = None

    route: Optional[str] = None

    updated_at: Optional[datetime] = None
