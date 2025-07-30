from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Optional
from uuid import uuid4

from keycloak import KeycloakAuthenticationError, KeycloakGetError, KeycloakOpenID

from webtool.auth.models import AuthData, Payload
from webtool.auth.service import BaseJWTService


def _get_header_value(header: dict, name: bytes) -> bytes | None:
    """
    Extracts a specific header value from HTTP headers.

    Parameters:
        header: HTTP header dictionary
        name: Name of the header to find
        Header value or None
    """

    header = dict(header)
    val = header.get(name)

    if val is None:
        return val

    return val


def _get_cookie_value(cookie: bytes, name: bytes) -> str | None:
    """
    Extracts a specific cookie value from a cookie string.

    Parameters:
        cookie: Cookie string (e.g., "name1=value1; name2=value2")
        name: Name of the cookie to find
        Cookie value or None
    """

    cookie = dict(c.split(b"=") for c in cookie.split(b"; "))
    val = cookie.get(name)

    if val is None:
        return None

    return val.decode()


def _get_authorization_scheme_param(authorization_header_value: Optional[bytes]) -> tuple[bytes, bytes]:
    """
    Separates scheme and token from Authorization header.

    Parameters:
        authorization_header_value: Authorization header value

    Return:
        tuple: scheme and token
    """

    if not authorization_header_value:
        return b"", b""
    scheme, _, param = authorization_header_value.partition(b" ")

    return scheme, param


def _get_access_token(scope: dict):
    """
    Extracts JWT from request scope.

    Parameters:
        scope: ASGI request scope

    Returns:
        (scheme, token) tuple or None
    """

    headers = scope.get("headers")
    if headers is None:
        raise ValueError("Cannot extract JWT from scope")

    authorization_value = _get_header_value(headers, b"authorization")
    if authorization_value is None:
        raise ValueError("Cannot extract JWT from scope")

    scheme, param = _get_authorization_scheme_param(authorization_value)
    if scheme.lower() != b"bearer" or not param:
        raise ValueError("Cannot extract JWT from scope")

    return scheme, param


class BaseBackend(ABC):
    """
    Abstract base class for authentication backends.
    All authentication backends must inherit from this class.
    """

    @abstractmethod
    async def authenticate(self, scope: dict) -> AuthData:
        """
        Performs authentication using the request scope.

        Parameters:
            scope: ASGI request scope

        Returns:
            Payload: Authentication data or None
        """

        raise NotImplementedError


class BaseAnnoBackend(BaseBackend):
    """
    Base backend class for handling anonymous users
    The implementation of BaseAnnoBackend should include a function to identify unauthenticated users
    """

    @abstractmethod
    def verify_identity(self, *args, **kwargs) -> Any:
        """
        Method to verify the identity of anonymous users
        """

        raise NotImplementedError


class IPBackend(BaseBackend):
    """
    Authentication backend based on IP address
    """

    async def authenticate(self, scope: dict) -> AuthData:
        """
        Performs authentication using the client's IP address.

        Parameters:
            scope: ASGI request scope

        Returns:
            AuthData: IP address or None
        """

        client = scope.get("client")
        if client is None:
            raise ValueError("Authentication Failed")

        return AuthData(identifier=client[0])


class SessionBackend(BaseBackend):
    """
    Session-based authentication backend
    """

    def __init__(self, session_name: str):
        """
        Parameters:
            session_name: Name of the session cookie
        """

        self.session_name = session_name

    def get_session(self, scope: dict) -> str | None:
        """
        Extracts session information from request scope.

        Parameters:
            scope: ASGI request scope

        Returns:
            Session string or None
        """

        headers = scope.get("headers")
        if headers is None:
            return None

        cookie = _get_header_value(headers, b"cookie")
        if cookie is None:
            return None

        session = _get_cookie_value(cookie, self.session_name.encode())
        if session is None:
            return None

        return session

    async def authenticate(self, scope: dict) -> AuthData:
        """
        Performs authentication using session information.

        Parameters:
            scope: ASGI request scope

        Returns:
            AuthData: session
        """

        session = self.get_session(scope)
        if not session:
            raise ValueError("Authentication Failed")

        return AuthData(identifier=session)


class AnnoSessionBackend(SessionBackend, BaseAnnoBackend):
    """
    Session backend for anonymous users.
    Automatically creates and assigns new sessions.
    """

    def __init__(
        self,
        session_name: str,
        max_age: int = 1209600,
        secure: bool = True,
        same_site: Literal["lax", "strict", "none"] | None = "lax",
        session_factory: Optional[Callable] = uuid4,
    ):
        """
        Parameters:
            session_name: Name of the session cookie
            max_age: Session expiration time (seconds)
            secure: HTTPS only flag
            same_site: SameSite cookie policy: lax, strict, none
            session_factory: Session ID generation function
        """

        super().__init__(session_name)

        self.session_factory = session_factory
        self.security_flags = f"httponly; samesite={same_site}; Max-Age={max_age};"
        if secure:
            self.security_flags += " secure;"

    async def verify_identity(self, scope: dict, send: Callable):
        """
        Assigns new session to anonymous users and redirects.

        Parameters:
            scope: ASGI request scope
            send: ASGI send function
        """

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.get("headers", [])

                cookie = _get_header_value(headers, b"cookie")
                if cookie is not None:
                    session = _get_cookie_value(cookie, self.session_name.encode())
                    if session is not None:
                        return await send(message)

                headers.append(
                    (
                        b"set-cookie",
                        f"{self.session_name}={self.session_factory().hex}; path=/; {self.security_flags}".encode(),
                    )
                )

                message["headers"] = headers

            await send(message)

        return send_wrapper


class JWTBackend(BaseBackend):
    """
    JWT (JSON Web Token) based authentication backend
    """

    def __init__(self, jwt_service: "BaseJWTService"):
        """
        Parameters:
            jwt_service: Service object for JWT processing
        """

        self.jwt_service = jwt_service

    async def validate_token(self, token: str) -> Payload:
        """
        Validates JWT.

        Parameters:
            token: JWT string

        Returns:
            Validated token data or None
        """

        validated_token = await self.jwt_service.validate_access_token(token)

        if validated_token is None or validated_token.get("sub") is None:
            raise ValueError("Authentication Failed")

        return validated_token

    async def authenticate(self, scope: dict) -> AuthData:
        """
        Performs authentication using JWT.

        Parameters:
            scope: ASGI request scope

        Returns:
            Validated token data or None
        """

        scheme, param = _get_access_token(scope)
        validated_token = await self.validate_token(param.decode())

        return AuthData(identifier=validated_token.pop("sub"), data=validated_token)


class KeycloakBackend(BaseBackend):
    def __init__(self, keycloak_connection: KeycloakOpenID):
        self.keycloak_connection = keycloak_connection

    async def authenticate(self, scope: dict) -> AuthData:
        scheme, param = _get_access_token(scope)

        try:
            tokeninfo = await self.keycloak_connection.a_introspect(param.decode())
        except (KeycloakAuthenticationError, KeycloakGetError):
            raise ValueError("Authentication Failed")

        if not tokeninfo or not tokeninfo.get("sub"):
            raise ValueError("Authentication Failed")

        tokeninfo.setdefault("access_token", param.decode())

        return AuthData(identifier=tokeninfo.get("sub"), data=tokeninfo)
