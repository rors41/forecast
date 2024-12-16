from fastapi import Depends, HTTPException, status
from forecast.config import CONFIG
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    if (
        credentials.scheme != "Bearer"
        or credentials.credentials != CONFIG.app_api_key.get_secret_value()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )
