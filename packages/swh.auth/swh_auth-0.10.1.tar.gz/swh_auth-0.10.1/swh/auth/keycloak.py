# Copyright (C) 2020-2024  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import json
from typing import Any, Dict
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

# add ExpiredSignatureError alias to avoid leaking jwcrypto import
# in swh-auth client code
from jwcrypto.jwt import JWTExpired as ExpiredSignatureError  # noqa
from keycloak import KeycloakOpenID

# add KeycloakError alias to avoid leaking keycloak import
# in swh-auth client code
from keycloak.exceptions import KeycloakError  # noqa

from swh.core.config import load_from_envvar


class KeycloakOpenIDConnect:
    """
    Wrapper class around python-keycloak to ease the interaction with Keycloak
    for managing authentication and user permissions with OpenID Connect.
    """

    def __init__(
        self,
        server_url: str,
        realm_name: str,
        client_id: str,
        realm_public_key: str = "",
    ):
        """
        Args:
            server_url: URL of the Keycloak server
            realm_name: The realm name
            client_id: The OpenID Connect client identifier
            realm_public_key: The realm public key (will be dynamically
                retrieved if not provided)
        """
        self._keycloak = KeycloakOpenID(
            server_url=server_url,
            client_id=client_id,
            realm_name=realm_name,
        )
        self.server_url = server_url
        self.realm_public_key = realm_public_key

    @property
    def realm_name(self):
        return self._keycloak.realm_name

    @realm_name.setter
    def realm_name(self, value):
        self._keycloak.realm_name = value

    @property
    def client_id(self):
        return self._keycloak.client_id

    @client_id.setter
    def client_id(self, value):
        self._keycloak.client_id = value

    def well_known(self) -> Dict[str, Any]:
        """
        Retrieve the OpenID Connect Well-Known URI registry from Keycloak.

        Returns:
            A dictionary filled with OpenID Connect URIS.
        """

        return self._keycloak.well_known()

    def authorization_url(self, redirect_uri: str, **extra_params: str) -> str:
        """
        Get OpenID Connect authorization URL to authenticate users.

        Args:
            redirect_uri: URI to redirect to once a user is authenticated
            extra_params: Extra query parameters to add to the
                authorization URL
        """
        auth_url = self._keycloak.auth_url(redirect_uri)
        # scope and state query parameters are now handled by auth_url method
        # since python-keycloak 1.8.1,
        # code below ensures those will be overridden if provided in extra_params
        # TODO: remove that code and pass scope and state params to auth_url method
        # once we use python-keycloak >= 1.8.1 in production
        parsed_auth_url = urlparse(auth_url)
        auth_url_qs = parse_qs(parsed_auth_url.query)
        auth_url_qs.update({k: [v] for k, v in extra_params.items()})
        auth_url = urlunparse(
            parsed_auth_url._replace(query=urlencode(auth_url_qs, doseq=True))
        )
        return auth_url

    def authorization_code(
        self, code: str, redirect_uri: str, **extra_params
    ) -> Dict[str, Any]:
        """
        Get OpenID Connect authentication tokens using Authorization
        Code flow.

        Raises:
            KeycloakError in case of authentication failures

        Args:
            code: Authorization code provided by Keycloak
            redirect_uri: URI to redirect to once a user is authenticated
                (must be the same as the one provided to authorization_url):
            extra_params: Extra parameters to add in the authorization request
                payload.
        """
        return self._keycloak.token(
            grant_type="authorization_code",
            code=code,
            redirect_uri=redirect_uri,
            **extra_params,
        )

    def login(
        self, username: str, password: str, scope: str = "openid", **extra_params
    ) -> Dict[str, Any]:
        """
        Get OpenID Connect authentication tokens using Direct Access Grant flow.

        Raises:
            KeycloakError in case of authentication failures

        Args:
            username: an existing username in the realm
            password: password associated to username
            extra_params: Extra parameters to add in the authorization request
                payload.
        """
        return self._keycloak.token(
            grant_type="password",
            scope=scope,
            username=username,
            password=password,
            **extra_params,
        )

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Request a new access token from Keycloak using a refresh token.

        Args:
            refresh_token: a refresh token provided by Keycloak

        Returns:
            a dictionary filled with tokens info
        """
        return self._keycloak.refresh_token(refresh_token)

    def decode_token(
        self, token: str, validate: bool = True, **kwargs
    ) -> Dict[str, Any]:
        """
        Try to decode a JWT token.

        Args:
            token: a JWT token to decode
            validate: whether to validate the token
            kwargs: additional keyword arguments for jwcrypto's JWT object

        Returns:
            a dictionary filled with decoded token content
        """
        return self._keycloak.decode_token(token, validate=validate, **kwargs)

    def logout(self, refresh_token: str) -> None:
        """
        Logout a user by closing its authenticated session.

        Args:
            refresh_token: a refresh token provided by Keycloak
        """
        self._keycloak.logout(refresh_token)

    def userinfo(self, access_token: str) -> Dict[str, Any]:
        """
        Return user information from its access token.

        Args:
            access_token: an access token provided by Keycloak

        Returns:
            a dictionary filled with user information
        """
        return self._keycloak.userinfo(access_token)

    @classmethod
    def from_config(cls, **kwargs: Any) -> "KeycloakOpenIDConnect":
        """Instantiate a KeycloakOpenIDConnect class from a configuration dict.

        Args:

            kwargs: configuration dict for the instance, with one keycloak key, whose
                value is a Dict with the following keys:
                - server_url: URL of the Keycloak server
                - realm_name: The realm name
                - client_id: The OpenID Connect client identifier

        Returns:
            the KeycloakOpenIDConnect instance

        """
        cfg = kwargs["keycloak"]
        return cls(
            server_url=cfg["server_url"],
            realm_name=cfg["realm_name"],
            client_id=cfg["client_id"],
        )

    @classmethod
    def from_configfile(cls, **kwargs: Any) -> "KeycloakOpenIDConnect":
        """Instantiate a KeycloakOpenIDConnect class from the configuration loaded from the
        SWH_CONFIG_FILENAME envvar, with potential extra keyword arguments if their
        value is not None.

        Args:
            kwargs: kwargs passed to instantiation call

        Returns:
            the KeycloakOpenIDConnect instance
        """
        config = dict(load_from_envvar()).get("keycloak", {})
        config.update({k: v for k, v in kwargs.items() if v is not None})
        return cls.from_config(keycloak=config)


def keycloak_error_message(keycloak_error: KeycloakError) -> str:
    """Transform a keycloak exception into an error message."""
    try:
        # keycloak error wrapped in a JSON document
        msg_dict = json.loads(keycloak_error.error_message)
        error_msg = msg_dict["error"]
        error_desc = msg_dict.get("error_description")
        if error_desc:
            error_msg = f"{error_msg}: {error_desc}"
        return error_msg
    except Exception:
        # fallback: return error message string
        return keycloak_error.error_message
