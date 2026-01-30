from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str | None = Security(api_key_header)) -> None:
    """
    Verify API key from X-API-Key header.

    If no API keys are configured (empty api_keys setting), authentication is disabled.
    If API keys are configured, requests must provide a valid key.

    Args:
        api_key: API key from X-API-Key header

    Raises:
        HTTPException: 401 if authentication is required but key is missing or invalid
    """
    valid_keys = settings.get_api_keys_list()

    # If no keys configured, authentication is disabled
    if not valid_keys:
        return

    # If keys are configured, require authentication
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
