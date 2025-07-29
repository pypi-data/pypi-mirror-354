import logging
from seatsurfing.common.http_client import SeatsurfingHttpClient
from seatsurfing.models.booking import Space

logger = logging.getLogger(__name__)


# TODO: this whole thing needs a lot of docs and hints still.


class Spaces(SeatsurfingHttpClient):
    """
    Location and space related methods.

    Documentation: https://seatsurfing.io/docs/rest-api#spaces
    """

    def get_spaces_for_location(self, location_id: str):
        """Get all spaces in a location `list[Space]`"""
        r = self._get(f"/location/{location_id}/space/")
        if not r:
            return r
        return [Space(**x) for x in r.json()]
