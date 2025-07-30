# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["ScopeListResponse", "ScopeListResponseItem"]


class ScopeListResponseItem(BaseModel):
    id: Optional[int] = None

    created_at: Optional[datetime] = None

    name: Optional[str] = None

    route: Optional[str] = None

    updated_at: Optional[datetime] = None


ScopeListResponse: TypeAlias = List[ScopeListResponseItem]
