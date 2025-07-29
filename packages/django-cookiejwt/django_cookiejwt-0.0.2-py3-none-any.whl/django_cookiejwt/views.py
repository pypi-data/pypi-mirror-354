from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenBlacklistView, TokenViewBase

from . import conf
from .serializers import (
    CustomTokenObtainPairSerializer,
    ResponseCustomTokenObtainPairSerializer,
    TokenBlacklistSerializer,
)
from .services import (
    set_access_token_cookie,
    set_refresh_token_cookie,
    set_session_cookie,
)


@extend_schema_view(
    post=extend_schema(
        summary="Get JWT tokens",
        description="Returns a pair of JWT tokens to authenticate the user and sets them in a cookie",
        tags=["Authentication"],
        request=CustomTokenObtainPairSerializer,
        responses={
            status.HTTP_200_OK: ResponseCustomTokenObtainPairSerializer,
        },
    )
)
class CookieTokenObtainPairView(TokenViewBase):
    """Returns a pair of JSON web tokens for user authentication."""

    serializer_class = CustomTokenObtainPairSerializer  # type: ignore[assignment]

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        # We receive access and refresh tokens
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")

        # Setting cookies for tokens
        set_access_token_cookie(response, access_token)
        set_refresh_token_cookie(response, refresh_token)

        # Setting a session cookie
        if conf.COOKIEJWT_SET_SESSION_COOKIE:
            set_session_cookie(response, request)

        # Optionally remove tokens from the response body
        response.data.pop("access", None)
        response.data.pop("refresh", None)

        return response


@extend_schema_view(
    post=extend_schema(
        summary="Add token to blacklist",
        description="Adds a refresh token to the blacklist, which logs the user out",
        tags=["Authentication"],
        request=TokenBlacklistSerializer,
        responses={
            status.HTTP_200_OK: {},
            status.HTTP_400_BAD_REQUEST: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },
        },
    )
)
class CookieTokenBlacklistView(TokenBlacklistView):
    """Places refresh token on blacklist."""

    def post(self, request: Request, *args, **kwargs) -> Response:
        # Getting a refresh token from a cookie
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"error": "Refresh token not provided"}, status=400)

        # The parent TokenBlacklistView expects the token in the request data.
        # Create a dictionary with the token to pass to the serializer
        data = {"refresh": refresh_token}

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # If validation is successful, the token is blacklisted.
        # Now, create a response and delete the authentication cookies.
        response = Response(status=status.HTTP_200_OK)
        set_access_token_cookie(response, "access_token", delete=True)
        set_refresh_token_cookie(response, "refresh_token", delete=True)
        setattr(response, "is_blacklisted", True)

        return response
