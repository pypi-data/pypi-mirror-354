# Copyright (C) 2020-2025  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from datetime import datetime
import hashlib
from typing import Any, Dict, Optional

from django.core.cache import cache
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    ValidationError,
)
import sentry_sdk

from swh.auth.django.models import OIDCUser
from swh.auth.django.utils import (
    keycloak_oidc_client,
    oidc_profile_cache_key,
    oidc_user_from_decoded_token,
    oidc_user_from_profile,
)
from swh.auth.keycloak import (
    ExpiredSignatureError,
    KeycloakError,
    KeycloakOpenIDConnect,
    keycloak_error_message,
)


def _update_cached_oidc_profile(
    oidc_client: KeycloakOpenIDConnect, oidc_profile: Dict[str, Any], user: OIDCUser
) -> None:
    """
    Update cached OIDC profile associated to a user if needed: when the profile
    is not stored in cache or when the authentication tokens have changed.

    Args:
        oidc_client: KeycloakOpenID wrapper
        oidc_profile: OIDC profile used to authenticate a user
        user: django model representing the authenticated user
    """
    # put OIDC profile in cache or update it after token renewal
    cache_key = oidc_profile_cache_key(oidc_client, user.id)
    if (
        cache.get(cache_key) is None
        or user.access_token != oidc_profile["access_token"]
    ):
        # set cache key TTL as refresh token expiration time
        assert user.refresh_expires_at
        ttl = int(user.refresh_expires_at.timestamp() - timezone.now().timestamp())

        # save oidc_profile in cache
        cache.set(cache_key, user.oidc_profile, timeout=max(0, ttl))


class OIDCAuthorizationCodePKCEBackend:
    """
    Django authentication backend using Keycloak OpenID Connect authorization
    code flow with PKCE ("Proof Key for Code Exchange").

    To use that backend globally in your django application, proceed as follow:

        * add ``"swh.auth.django.backends.OIDCAuthorizationCodePKCEBackend"``
          to the ``AUTHENTICATION_BACKENDS`` django setting

        * configure Keycloak URL, realm and client by adding
          ``SWH_AUTH_SERVER_URL``, ``SWH_AUTH_REALM_NAME`` and ``SWH_AUTH_CLIENT_ID``
          in django settings

        * add ``swh.auth.django.views.urlpatterns`` to your django application URLs

        * add an HTML link targeting the ``"oidc-login"`` django view in your
          application views

        * once a user is logged in, add an HTML link targeting the ``"oidc-logout"``
          django view in your application views (a ``next`` query parameter
          can be used to redirect to a view of choice once the user is logged out)

    """

    def authenticate(
        self, request: HttpRequest, code: str, code_verifier: str, redirect_uri: str
    ) -> Optional[OIDCUser]:
        user = None
        try:
            oidc_client = keycloak_oidc_client()
            # try to authenticate user with OIDC PKCE authorization code flow
            oidc_profile = oidc_client.authorization_code(
                code, redirect_uri, code_verifier=code_verifier
            )

            # create Django user
            user = oidc_user_from_profile(oidc_client, oidc_profile)

            # update cached oidc profile if needed
            _update_cached_oidc_profile(oidc_client, oidc_profile, user)

        except Exception as e:
            sentry_sdk.capture_exception(e)

        return user

    def get_user(self, user_id: int) -> Optional[OIDCUser]:
        # get oidc profile from cache
        oidc_client = keycloak_oidc_client()
        cache_key = oidc_profile_cache_key(oidc_client, user_id)
        oidc_profile = cache.get(cache_key)
        if oidc_profile:
            try:
                user = oidc_user_from_profile(oidc_client, oidc_profile)
                # update cached oidc profile if needed
                _update_cached_oidc_profile(oidc_client, oidc_profile, user)
                # restore auth backend
                setattr(user, "backend", f"{__name__}.{self.__class__.__name__}")
                return user
            except KeycloakError as ke:
                error_msg = keycloak_error_message(ke)
                if error_msg == "invalid_grant: Session not active":
                    # user session no longer active, remove oidc profile from cache
                    cache.delete(cache_key)
                else:
                    sentry_sdk.capture_exception(ke)
                return None
            except Exception as e:
                sentry_sdk.capture_exception(e)
                return None
        else:
            return None


class OIDCBearerTokenAuthentication(BaseAuthentication):
    """
    Django REST Framework authentication backend using bearer tokens for
    Keycloak OpenID Connect.

    It enables to authenticate a Web API user by sending a long-lived
    OpenID Connect refresh token in HTTP Authorization headers.
    Long lived refresh tokens can be generated by opening an OpenID Connect
    session with the following scope: ``openid offline_access``.

    To use that backend globally in your DRF application, proceed as follow:

        * add ``"swh.auth.django.backends.OIDCBearerTokenAuthentication"``
          to the ``REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]``
          django setting.

        * configure Keycloak URL, realm and client by adding
          ``SWH_AUTH_SERVER_URL``, ``SWH_AUTH_REALM_NAME`` and ``SWH_AUTH_CLIENT_ID``
          in django settings

    Users will then be able to perform authenticated Web API calls by sending
    their refresh token in HTTP Authorization headers, for instance:
    ``curl -H "Authorization: Bearer ${TOKEN}" https://...``.

    """

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            return None

        try:
            auth_type, refresh_token = auth_header.split(" ", 1)
        except ValueError:
            raise AuthenticationFailed("Invalid HTTP authorization header format")

        if auth_type != "Bearer":
            raise AuthenticationFailed(
                (f"Invalid or unsupported HTTP authorization" f" type ({auth_type}).")
            )
        try:
            oidc_client = keycloak_oidc_client()

            # compute a cache key from the token that does not exceed
            # memcached key size limit
            hasher = hashlib.sha1()
            hasher.update(refresh_token.encode("ascii"))
            cache_key = f"api_token_{hasher.hexdigest()}"

            # check if an access token is cached
            access_token = cache.get(cache_key)

            if access_token is not None:
                # attempt to decode access token
                try:
                    decoded_token = oidc_client.decode_token(access_token)
                # access token has expired
                except ExpiredSignatureError:
                    decoded_token = None

            if access_token is None or decoded_token is None:
                # get a new access token from authentication provider
                access_token = oidc_client.refresh_token(refresh_token)["access_token"]
                # decode access token
                decoded_token = oidc_client.decode_token(access_token)
                # compute access token expiration
                exp = datetime.fromtimestamp(decoded_token["exp"])
                ttl = int(exp.timestamp() - timezone.now().timestamp())
                # save access token in cache while it is valid
                cache.set(cache_key, access_token, timeout=max(0, ttl))

            # create Django user
            user = oidc_user_from_decoded_token(decoded_token, oidc_client.client_id)
        except UnicodeEncodeError:
            raise ValidationError("Invalid bearer token")
        except KeycloakError as ke:
            error_msg = keycloak_error_message(ke)
            if error_msg in (
                "invalid_grant: Offline session not active",
                "invalid_grant: Offline user session not found",
            ):
                error_msg = (
                    "Bearer token expired after a long period of inactivity; "
                    "please generate a new one."
                )
            raise AuthenticationFailed(error_msg)
        except Exception as e:
            raise APIException(str(e))

        return user, None
