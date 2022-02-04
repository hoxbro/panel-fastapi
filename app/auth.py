from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager

from app.settings import GLOBAL_CONTEXT, SECRET_KEY, templates

auth_router = APIRouter()


class NotAuthenticatedException(Exception):
    pass


auth_manager = LoginManager(
    SECRET_KEY,
    token_url="/auth/login",
    use_cookie=True,
    custom_exception=NotAuthenticatedException,  # type:ignore[arg-type]
)
auth_manager.auto_error = False


async def redirect_login(request: Request, exc: NotAuthenticatedException):
    path = request.url.components.path
    return RedirectResponse(url=f"/login?next={path}")


auth_exception = (NotAuthenticatedException, redirect_login)


@auth_manager.user_loader()  # type:ignore[operator]
async def load_user(username: str) -> dict[str, str] | None:
    # This could (should) be made much more advanced
    DB = {"test": {"username": "test", "password": "test"}}
    user = DB.get(username)
    return user


async def get_current_user(request: Request) -> str | None:
    try:
        payload = await auth_manager.get_current_user(request.cookies["access-token"])
        return payload["username"]
    except Exception:
        return None


@auth_router.get("/login")
async def login(request: Request):
    bad_login = request.cookies.get("bad_login")

    response = templates.TemplateResponse(
        "login.html",
        {"request": request, "bad_login": bad_login, **GLOBAL_CONTEXT},
    )
    response.delete_cookie(key="bad_login")
    return response


@auth_router.post("/auth/login")
async def auth_login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = await load_user(username)
    if not user or password != user["password"]:
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        response.set_cookie("bad_login", True)
        return response

    access_token = auth_manager.create_access_token(data={"sub": username})
    url = request.query_params.get("next", "/")
    response = RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    auth_manager.set_cookie(response, access_token)
    return response


@auth_router.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse(
        "logout.html", {"request": request, **GLOBAL_CONTEXT}
    )
    response.delete_cookie(key="access-token")
    return response
