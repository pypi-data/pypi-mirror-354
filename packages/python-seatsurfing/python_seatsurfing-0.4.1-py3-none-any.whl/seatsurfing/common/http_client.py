import logging
from typing import Optional
import httpx

from seatsurfing.models.authentication import Jwt, PasswordLoginRequest

logger = logging.getLogger(__name__)


class SeatsurfingHttpClient:
    """Common methods to interact with the Seatsurfing API. This class should only be used by specific endpoint implementations."""

    def __init__(
        self,
        base_url: str,
        *,
        organization_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.__base_url = base_url
        self.__organization_id = organization_id
        self.__jwt: Jwt = None
        self.__client = httpx.Client(follow_redirects=True, base_url=base_url)

        # login if username/password provided.
        if organization_id and username and password:
            self._password_login(username, password, organization_id)

    def __del__(self):
        self.__client.close()

    def _is_logged_in(self) -> bool:
        "Check if the client is logged in. This should be used for autnenticated endpoints."
        # We can't check if it's actually a real URL, but we can check if it's empty at least.
        if not self.__base_url:
            return False

        if not self.__jwt:
            return False

        if not self.__client.headers.get("Authorization"):
            return False

        return True

    def _get(
        self, path: str, *, params: dict = None, headers: dict = None
    ) -> httpx.Response | None:
        if not self.__base_url:
            return None

        r = self.__client.get(path, headers=headers, params=params)
        r.raise_for_status()
        return r

    def _post(
        self, path: str, *, data: dict = None, params: dict = None, headers: dict = None
    ) -> httpx.Response | None:
        if not self.__base_url:
            return None

        r = self.__client.post(path, json=data, headers=headers, params=params)
        r.raise_for_status()
        return r

    def _put(
        self, path: str, *, data: dict = None, params: dict = None, headers: dict = None
    ) -> httpx.Response | None:
        if not self.__base_url:
            return None

        r = self.__client.put(path, json=data, headers=headers, params=params)
        r.raise_for_status()
        return r

    def _delete(
        self, path: str, *, params: dict = None, headers: dict = None
    ) -> httpx.Response | None:
        if not self.__base_url:
            return None

        r = self.__client.delete(path, headers=headers, params=params)
        r.raise_for_status()
        return r

    def _password_login(
        self, username: str, password: str, organization_id: str
    ) -> Jwt:
        """Authenticate using username and password, and update class http client with new bearer token."""
        logger.debug(
            "Logging in to organization %s using username/password: %s | %s",
            organization_id,
            username,
            password,
        )

        data = PasswordLoginRequest(
            email=username,
            password=password,
            organization_id=organization_id,
        )

        r = self._post(
            path="/auth/login",
            data=data.model_dump(by_alias=True),
        )
        jwt = Jwt.model_validate(r.json())

        logger.debug("Successfully retrieved JWT: %s", jwt)

        headers = {"Authorization": f"Bearer {jwt.access_token}"}
        self.__client.headers.update(headers)
        self.__jwt = jwt

        return jwt
