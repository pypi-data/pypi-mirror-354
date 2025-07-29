# Copyright (C) 2023-2024 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from aiocache import Cache
from jwcrypto.jws import InvalidJWSSignature
import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from swh.auth.starlette import backends
from swh.auth.tests.sample_data import DECODED_TOKEN, USER_INFO


@pytest.fixture
def app_with_auth_backend(keycloak_oidc):
    backend = backends.BearerTokenAuthBackend(
        server_url="https://example.com",
        realm_name="example",
        client_id="example",
        cache=Cache(),  # Dummy cache
    )
    backend.oidc_client = keycloak_oidc
    middleware = [
        Middleware(
            AuthenticationMiddleware,
            backend=backend,
        )
    ]

    def homepage(request):
        if request.user.is_authenticated:
            return PlainTextResponse("Hello " + request.user.username)
        return PlainTextResponse("Hello")

    app = Starlette(routes=[Route("/", homepage)], middleware=middleware)
    return app


@pytest.fixture
def client(app_with_auth_backend):
    return TestClient(app_with_auth_backend)


def test_anonymous_access(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello"


def test_invalid_auth_header(client):
    client.headers = {"Authorization": "invalid"}
    response = client.get("/")
    assert response.status_code == 400
    assert response.text == "Invalid auth header"


def test_invalid_auth_type(client):
    client.headers = {"Authorization": "Basic invalid"}
    response = client.get("/")
    assert response.status_code == 400
    assert response.text == "Invalid or unsupported authorization type"


def test_invalid_refresh_token(client, keycloak_oidc):
    keycloak_oidc.set_auth_success(False)
    client.headers = {"Authorization": "Bearer invalid-valid-token"}
    response = client.get("/")
    assert response.status_code == 400
    assert "Access token failed to be decoded" in response.text


@pytest.mark.parametrize("token_type", ["access_token", "refresh_token"])
def test_success_with_tokens(client, keycloak_oidc, mocker, token_type):
    oidc_profile = keycloak_oidc.login()
    if token_type == "refresh_token":
        # simulate invalid decoding of refresh token then valid decoding of
        # new access token as JWT validation is disabled in keycloak_oidc fixture
        # due to the use of expired tokens
        mocker.patch.object(
            keycloak_oidc,
            "decode_token",
            side_effect=[InvalidJWSSignature(), DECODED_TOKEN],
        )
    client.headers = {"Authorization": f"Bearer {oidc_profile[token_type]}"}
    response = client.get("/")

    assert response.status_code == 200
    assert response.text == f'Hello {USER_INFO["preferred_username"]}'
