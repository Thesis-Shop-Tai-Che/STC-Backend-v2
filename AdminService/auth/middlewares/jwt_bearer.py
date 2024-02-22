import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings
from database import get_db


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme"
                )
            # token = credentials.credentials
            # try:
            #     payload = jwt.decode(
            #         token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            #     )
            #     user = (
            #         get_db().query(User).filter(User.id == payload["user_id"]).first()
            #     )
            #     if not user:
            #         raise HTTPException(
            #             status_code=404, detail="Invalid or expired token"
            #         )
            #     return user

            # except jwt.exceptions.PyJWTError:
            #     raise HTTPException(status_code=403, detail="Invalid or expired token")
        else:
            raise HTTPException(status_code=403, detail="Invalid or expired token")
