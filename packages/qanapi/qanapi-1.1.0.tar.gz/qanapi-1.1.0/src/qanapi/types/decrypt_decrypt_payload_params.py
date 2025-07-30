# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DecryptDecryptPayloadParams"]


class DecryptDecryptPayloadParams(TypedDict, total=False):
    data: Required[Union[str, Dict[str, object], Iterable[object]]]
    """The encrypted payload to decrypt.

    - Can be a string or an object/array with encrypted fields.
    - Decryption is selective if `sensitiveFields` is provided.
    """

    sensitive_fields: Annotated[List[str], PropertyInfo(alias="sensitiveFields")]
    """Laravel-style dot-notated paths to fields to decrypt.

    - Same syntax and behavior as in EncryptRequest.
    - If omitted, all string values matching encryption prefix are attempted.

    Examples:

    - `user.ssn`
    - `employees.*.payroll.token`
    """
