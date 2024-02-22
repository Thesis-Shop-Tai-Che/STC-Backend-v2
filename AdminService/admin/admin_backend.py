from sqladmin import Admin
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from auth.utils import create_access_token, create_refresh_token


class AdminBackend(Admin):
    async def login(self, request: Request) -> Response:
        assert self.authentication_backend is not None

        context = {"request": request, "error": ""}

        cookies = request.cookies
        refresh_token = cookies.get("refresh_token")
        if refresh_token is not None:
            return RedirectResponse(request.url_for("admin:index"), status_code=302)

        if request.method == "GET":
            return self.templates.TemplateResponse("login.html", context)

        ok = await self.authentication_backend.login(request)
        if not ok:
            context["error"] = "Invalid credentials."
            return self.templates.TemplateResponse(
                "login.html", context, status_code=400
            )
        
        access_token = create_access_token(username="admin", user_id=1)
        refresh_token = create_refresh_token(username="admin", user_id=1)
        
        res =  RedirectResponse(request.url_for("admin:index"), status_code=302)
        res.set_cookie(key="access_token", value=access_token)
        res.set_cookie(key="refresh_token", value=refresh_token)
        return res
    
    async def logout(self, request: Request) -> Response:
        assert self.authentication_backend is not None

        response = RedirectResponse("/admin/login", status_code=302)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
