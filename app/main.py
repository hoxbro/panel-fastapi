from __future__ import annotations

import os
from urllib.parse import urljoin

import panel as pn
from bokeh.embed import server_document
from bokeh.util.token import generate_session_id
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles

from app.auth import auth_exception, auth_manager, auth_router, get_current_user
from app.settings import ALLOWED_HOSTS, GLOBAL_CONTEXT, SECRET_KEY, templates
from models import serving, titles

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.add_exception_handler(*auth_exception)


@app.get("/")
async def root(request: Request):
    username = await get_current_user(request)
    return templates.TemplateResponse(
        "root.html",
        {"request": request, "username": username, **GLOBAL_CONTEXT},
    )


@app.get("/{model}")
async def panel_model(request: Request, model: str, user=Depends(auth_manager)):
    if model not in titles:
        raise HTTPException(status_code=404, detail="Item not found")

    if os.getenv("DOCKERENV"):
        url = urljoin(request.headers["host"], f"panel/{model}")
    else:
        url = f"http://0.0.0.0:5006/panel/{model}"

    headers = {"bokeh-session-id": generate_session_id(SECRET_KEY, signed=True)}
    script = server_document(
        url=url, arguments=dict(request.query_params), headers=headers
    )

    return templates.TemplateResponse(
        "panel_model.html",
        {
            "request": request,
            "script": script,
            "username": user["username"],
            "title": titles[model],
            **GLOBAL_CONTEXT,
        },
    )


pn.serve(
    serving,
    port=5006,
    allow_websocket_origin=ALLOWED_HOSTS,
    address="0.0.0.0",
    show=False,
    sign_sessions=True,
    secret_key=SECRET_KEY,
    generate_session_ids=False,
    num_process=1 if os.name == "nt" else 2,
)
