from typing import Optional
from seatsurfing.authentication import Authentication
from seatsurfing.booking import Bookings
from seatsurfing.space import Spaces


class Client:
    """Client to interact with Seatsurfing."""

    def __init__(
        self,
        base_url: str,
        organization_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.base_url = base_url

        self.organization_id = organization_id
        self.username = username
        self.password = password

        # Unauthenticated endpoints, doesn't require any credentials
        self.authentication = Authentication(base_url=self.base_url)

        # Authenticated endpoints, require credentials to use them
        self.booking = Bookings(
            base_url=self.base_url,
            organization_id=self.organization_id,
            username=self.username,
            password=self.password,
        )

        self.spaces = Spaces(
            base_url=self.base_url,
            organization_id=self.organization_id,
            username=self.username,
            password=self.password,
        )

    def login(
        self,
        organization_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Log in to the seatsurfing instance using credentials.
        Set `organization_id`, `username`, and `password` class variables.
        """
        # Support for both passing in variables, and using saved class variables.
        # if something is not passed in, then we use the class variable.
        _organization_id = organization_id if organization_id else self.organization_id
        _username = username if username else self.username
        _password = password if password else self.password

        # all these variables must be set, otherwise we can't authnenticate.
        if not _organization_id:
            raise ValueError("Organization ID not set")
        if not _username:
            raise ValueError("Username not set")
        if not _password:
            raise ValueError("Password not set")

        self.booking = Bookings(
            base_url=self.base_url,
            organization_id=_organization_id,
            username=_username,
            password=_password,
        )

        self.spaces = Spaces(
            base_url=self.base_url,
            organization_id=_organization_id,
            username=_username,
            password=_password,
        )
