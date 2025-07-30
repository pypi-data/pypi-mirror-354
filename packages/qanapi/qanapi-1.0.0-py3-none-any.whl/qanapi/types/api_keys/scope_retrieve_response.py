# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["ScopeRetrieveResponse", "ScopeRetrieveResponseItem", "ScopeRetrieveResponseItemPivot"]


class ScopeRetrieveResponseItemPivot(BaseModel):
    api_key_id: Optional[int] = None

    scope_id: Optional[int] = None


class ScopeRetrieveResponseItem(BaseModel):
    id: Optional[int] = None

    created_at: Optional[datetime] = None

    name: Optional[str] = None

    pivot: Optional[ScopeRetrieveResponseItemPivot] = None

    route: Optional[str] = None

    updated_at: Optional[datetime] = None


ScopeRetrieveResponse: TypeAlias = List[ScopeRetrieveResponseItem]
