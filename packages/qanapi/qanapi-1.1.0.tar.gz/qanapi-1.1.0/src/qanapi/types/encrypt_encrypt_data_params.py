# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EncryptEncryptDataParams", "Access", "Attributes"]


class EncryptEncryptDataParams(TypedDict, total=False):
    data: Required[Union[str, float, Dict[str, object], Iterable[object]]]
    """The actual data to encrypt.

    - Can be a scalar (string/number), object, or array.
    - If the value is an object or array, only the specified `sensitiveFields` are
      encrypted.
    """

    access: Access

    attributes: Attributes
    """Optional metadata describing the data's context."""

    sensitive_fields: Annotated[List[str], PropertyInfo(alias="sensitiveFields")]
    """Laravel-style dot-notated paths to fields that should be encrypted.

    Supports:

    - Dot notation for nested fields: `user.profile.ssn`
    - Wildcard `*` for arrays or dynamic keys: `users.*.token`

    Examples:

    - `password`
    - `user.credentials.secret`
    - `accounts.*.secret`
    - `teams.*.members.*.email`
    """


class Access(TypedDict, total=False):
    acl: List[str]
    """Access control list — list of user roles authorized to decrypt this data."""


class Attributes(TypedDict, total=False):
    classification: Literal["public", "internal", "confidential", "restricted"]

    owner: str

    tags: List[str]
