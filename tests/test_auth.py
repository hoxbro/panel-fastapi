from urllib.parse import urljoin

import pytest
import requests
from bokeh.util.token import generate_session_id

from app.auth import auth_manager
from app.settings import SECRET_KEY
from models import titles


@pytest.mark.parametrize("model", list(titles))
@pytest.mark.parametrize(
    "baseurl,env",
    [("http://0.0.0.0:5006", "local"), ("http://0.0.0.0:8080", "docker")],
)
def test_bokeh_auth(model, baseurl, env):
    # Check if live
    try:
        response = requests.get(baseurl)
    except requests.exceptions.ConnectionError:
        pytest.skip(f"{env} webpage is not live. Skipping.")

    url = urljoin(baseurl, f"panel/{model}")

    # Without permission
    response = requests.get(url)
    assert response.status_code == 403

    # With permission
    headers = {"bokeh-session-id": generate_session_id(SECRET_KEY, signed=True)}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


@pytest.mark.parametrize("model", list(titles))
@pytest.mark.parametrize(
    "baseurl,env",
    [("http://0.0.0.0:8000", "local"), ("http://0.0.0.0:8080", "docker")],
)
def test_fastapi_auth(model, baseurl, env):
    # Check if live
    try:
        response = requests.get(baseurl)
    except requests.exceptions.ConnectionError:
        pytest.skip(f"{env} webpage is not live. Skipping.")

    url = urljoin(baseurl, model)
    redirect_url = urljoin(baseurl, f"/login?next=/{model}")

    # Without permission
    response = requests.get(url)
    assert response.status_code == 200
    assert response.url == redirect_url

    # With permission
    cookies = {"access-token": auth_manager.create_access_token(data={"sub": "test"})}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert response.url == url
    assert "/autoload.js?bokeh-autoload-element" in response.text
