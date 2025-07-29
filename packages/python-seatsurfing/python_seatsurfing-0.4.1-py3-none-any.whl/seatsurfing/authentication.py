from datetime import datetime
import logging
from seatsurfing.common.http_client import SeatsurfingHttpClient
from seatsurfing.models.authentication import SingleOrg

logger = logging.getLogger(__name__)


class Authentication(SeatsurfingHttpClient):
    """
    Authentication related methods.

    Documentation: https://seatsurfing.io/docs/rest-api#authentication
    """

    def get_singleorg(self):
        """Check if instance hosts one organization only, and returns that organization's information"""
        r = self._get("/auth/singleorg")
        return SingleOrg(**(r.json()))
