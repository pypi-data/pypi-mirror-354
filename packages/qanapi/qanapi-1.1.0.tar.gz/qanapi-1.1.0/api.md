# Auth

Types:

```python
from qanapi.types import (
    AuthLoginResponse,
    AuthLogoutResponse,
    AuthRefreshTokenResponse,
    AuthRetrieveUserDetailsResponse,
    AuthRevokeTokenResponse,
)
```

Methods:

- <code title="post /auth/login">client.auth.<a href="./src/qanapi/resources/auth.py">login</a>(\*\*<a href="src/qanapi/types/auth_login_params.py">params</a>) -> <a href="./src/qanapi/types/auth_login_response.py">AuthLoginResponse</a></code>
- <code title="post /auth/logout">client.auth.<a href="./src/qanapi/resources/auth.py">logout</a>() -> <a href="./src/qanapi/types/auth_logout_response.py">AuthLogoutResponse</a></code>
- <code title="post /auth/refresh">client.auth.<a href="./src/qanapi/resources/auth.py">refresh_token</a>() -> <a href="./src/qanapi/types/auth_refresh_token_response.py">AuthRefreshTokenResponse</a></code>
- <code title="get /auth/userdetails">client.auth.<a href="./src/qanapi/resources/auth.py">retrieve_user_details</a>() -> <a href="./src/qanapi/types/auth_retrieve_user_details_response.py">AuthRetrieveUserDetailsResponse</a></code>
- <code title="post /auth/revoke">client.auth.<a href="./src/qanapi/resources/auth.py">revoke_token</a>() -> <a href="./src/qanapi/types/auth_revoke_token_response.py">AuthRevokeTokenResponse</a></code>

# Encrypt

Types:

```python
from qanapi.types import EncryptEncryptDataResponse
```

Methods:

- <code title="post /encrypt">client.encrypt.<a href="./src/qanapi/resources/encrypt.py">encrypt_data</a>(\*\*<a href="src/qanapi/types/encrypt_encrypt_data_params.py">params</a>) -> <a href="./src/qanapi/types/encrypt_encrypt_data_response.py">EncryptEncryptDataResponse</a></code>

# Decrypt

Types:

```python
from qanapi.types import DecryptDecryptPayloadResponse
```

Methods:

- <code title="post /decrypt">client.decrypt.<a href="./src/qanapi/resources/decrypt.py">decrypt_payload</a>(\*\*<a href="src/qanapi/types/decrypt_decrypt_payload_params.py">params</a>) -> <a href="./src/qanapi/types/decrypt_decrypt_payload_response.py">DecryptDecryptPayloadResponse</a></code>

# APIKeys

Types:

```python
from qanapi.types import APIKeyRevokeResponse, APIKeyRotateResponse
```

Methods:

- <code title="patch /api-keys/{apiKey}/revoke">client.api_keys.<a href="./src/qanapi/resources/api_keys/api_keys.py">revoke</a>(api_key) -> <a href="./src/qanapi/types/api_key_revoke_response.py">APIKeyRevokeResponse</a></code>
- <code title="patch /api-keys/{apiKey}/rotate">client.api_keys.<a href="./src/qanapi/resources/api_keys/api_keys.py">rotate</a>(api_key) -> <a href="./src/qanapi/types/api_key_rotate_response.py">APIKeyRotateResponse</a></code>

## Scopes

Types:

```python
from qanapi.types.api_keys import (
    ScopeRetrieveResponse,
    ScopeAttachResponse,
    ScopeDetachResponse,
    ScopeSyncResponse,
)
```

Methods:

- <code title="get /api-keys/{apiKey}/scopes">client.api_keys.scopes.<a href="./src/qanapi/resources/api_keys/scopes.py">retrieve</a>(api_key) -> <a href="./src/qanapi/types/api_keys/scope_retrieve_response.py">ScopeRetrieveResponse</a></code>
- <code title="post /api-keys/{apiKey}/scopes/attach">client.api_keys.scopes.<a href="./src/qanapi/resources/api_keys/scopes.py">attach</a>(api_key, \*\*<a href="src/qanapi/types/api_keys/scope_attach_params.py">params</a>) -> <a href="./src/qanapi/types/api_keys/scope_attach_response.py">ScopeAttachResponse</a></code>
- <code title="post /api-keys/{apiKey}/scopes/detach">client.api_keys.scopes.<a href="./src/qanapi/resources/api_keys/scopes.py">detach</a>(api_key, \*\*<a href="src/qanapi/types/api_keys/scope_detach_params.py">params</a>) -> <a href="./src/qanapi/types/api_keys/scope_detach_response.py">ScopeDetachResponse</a></code>
- <code title="post /api-keys/{apiKey}/scopes/sync">client.api_keys.scopes.<a href="./src/qanapi/resources/api_keys/scopes.py">sync</a>(api_key, \*\*<a href="src/qanapi/types/api_keys/scope_sync_params.py">params</a>) -> <a href="./src/qanapi/types/api_keys/scope_sync_response.py">ScopeSyncResponse</a></code>

# Scopes

Types:

```python
from qanapi.types import (
    ScopeCreateResponse,
    ScopeRetrieveResponse,
    ScopeUpdateResponse,
    ScopeListResponse,
    ScopeDeleteResponse,
)
```

Methods:

- <code title="post /scopes">client.scopes.<a href="./src/qanapi/resources/scopes.py">create</a>(\*\*<a href="src/qanapi/types/scope_create_params.py">params</a>) -> <a href="./src/qanapi/types/scope_create_response.py">ScopeCreateResponse</a></code>
- <code title="get /scopes/{id}">client.scopes.<a href="./src/qanapi/resources/scopes.py">retrieve</a>(id) -> <a href="./src/qanapi/types/scope_retrieve_response.py">ScopeRetrieveResponse</a></code>
- <code title="put /scopes/{id}">client.scopes.<a href="./src/qanapi/resources/scopes.py">update</a>(id, \*\*<a href="src/qanapi/types/scope_update_params.py">params</a>) -> <a href="./src/qanapi/types/scope_update_response.py">ScopeUpdateResponse</a></code>
- <code title="get /scopes">client.scopes.<a href="./src/qanapi/resources/scopes.py">list</a>() -> <a href="./src/qanapi/types/scope_list_response.py">ScopeListResponse</a></code>
- <code title="delete /scopes/{id}">client.scopes.<a href="./src/qanapi/resources/scopes.py">delete</a>(id) -> <a href="./src/qanapi/types/scope_delete_response.py">ScopeDeleteResponse</a></code>
