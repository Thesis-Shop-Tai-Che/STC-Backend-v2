from typing import Optional, Union

from sqladmin import Admin
from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqladmin.authentication import AuthenticationBackend, login_required
from starlette.responses import RedirectResponse
from auth.utils import (create_access_token, decode_and_verify_access_token,
    decode_and_verify_refresh_token, verify_password)
from database import get_db
from starlette.routing import URLPath

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        
        if not username or not password:
            return False
        
        if username == "admin" and password == "admin":
            return True
        
        return False

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        cookies = request.cookies
    
        access_token = cookies.get("access_token")
        if access_token is None:
            response = RedirectResponse("/admin/login", status_code=302)
            return response
        
        decoded_access_token = decode_and_verify_access_token(access_token)

        if decoded_access_token is None:
            refresh_token = cookies.get("refresh_token")
            decoded_refresh_token = decode_and_verify_refresh_token(refresh_token)

            if decoded_refresh_token is None:
                response = RedirectResponse("/admin/login", status_code=302)
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")
                return response
            
            new_access_token = create_access_token(decoded_refresh_token['sub'], decoded_refresh_token['user_id'])
            response = RedirectResponse(request.url, status_code=302)
            response.set_cookie("access_token", new_access_token)
            return response

        return True
