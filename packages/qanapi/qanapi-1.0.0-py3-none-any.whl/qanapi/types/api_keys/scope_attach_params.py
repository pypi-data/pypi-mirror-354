# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["ScopeAttachParams"]


class ScopeAttachParams(TypedDict, total=False):
    scope_ids: Required[Iterable[int]]
    """List of scope IDs to attach"""
