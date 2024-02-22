import jwt
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from config import settings
from database import get_db


class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive=receive)
        try:
            authorization = request.headers.get("Authorization")
            if authorization:
                if authorization.lower().startswith("bearer"):
                    token = authorization.split(" ")[1]
                    try:
                        payload = jwt.decode(
                            token,
                            settings.JWT_SECRET_KEY,
                            algorithms=settings.JWT_ALGORITHM,
                        )
                        # user = (
                        #     get_db()
                        #     .query(User)
                        #     .filter(User.id == payload["user_id"])
                        #     .first()
                        # )
                        # if not user:
                        #     raise HTTPException(
                        #         status_code=404, detail="Invalid or expired token"
                        #     )
                        # request.state.user = user
                    except jwt.exceptions.PyJWTError:
                        raise HTTPException(
                            status_code=403, detail="Invalid or expired token"
                        )
                else:
                    raise HTTPException(
                        status_code=403, detail="Invalid authentication scheme"
                    )
            else:
                pass
        except (jwt.exceptions.PyJWTError, IndexError, KeyError):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        response = await self.app(request.scope, receive, send)
        return response
