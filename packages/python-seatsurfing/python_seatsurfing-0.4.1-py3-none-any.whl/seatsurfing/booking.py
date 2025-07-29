from datetime import datetime
import logging
from seatsurfing.common.http_client import SeatsurfingHttpClient
from seatsurfing.models.booking import Booking, BookingCreateOrUpdateDTO

logger = logging.getLogger(__name__)


# TODO: this whole thing needs a lot of docs and hints still.


class Bookings(SeatsurfingHttpClient):
    """
    Booking related methods.

    Documentation: https://seatsurfing.io/docs/rest-api#bookings
    """

    def _convert_datetime_to_str(self, time: datetime) -> str:
        """Helper function to return the correct format of a datetime."""
        return time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_bookings(self):
        """Get all bookings as `list[Booking]`"""
        r = self._get("/booking/")
        if not r:
            return r
        return [Booking(**x) for x in r.json()]

    def get_booking(self, booking_id: str):
        """Get a single booking by ID. Returns a `Booking` object."""
        r = self._get(f"/booking/{booking_id}")
        if not r:
            return r
        return Booking(**(r.json()))

    def get_filtered_org_bookings(
        self, from_date: datetime, to_date: datetime
    ) -> list[Booking]:
        """
        Get bookings using filters. Currently supports time period.
        """
        data = {
            "start": self._convert_datetime_to_str(from_date),
            "end": self._convert_datetime_to_str(to_date),
        }
        r = self._get("/booking/filter/", params=data)
        if not r:
            return []
        return [Booking(**x) for x in r.json()]

    def create_booking(
        self,
        enter: datetime,
        leave: datetime,
        space_id: str,
        subject: str,
        user_email: str = "",
    ):
        """
        Create a new booking. If `user_email` is empty, it will create a booking for your logged in user.

        `user_email` should only be filled out if you are an admin, and can create bookings on behalf of others.
        """
        data = BookingCreateOrUpdateDTO(
            enter=self._convert_datetime_to_str(enter),
            leave=self._convert_datetime_to_str(leave),
            space_id=space_id,
            user_email=user_email,
            subject=subject,
        )
        self._post("/booking/", data=data.model_dump(by_alias=True, exclude_none=True))

    def update_booking(
        self,
        booking_id: str,
        enter: datetime,
        leave: datetime,
        space_id: str,
        user_email: str,
    ):
        """Update an existing booking."""
        data = BookingCreateOrUpdateDTO(
            enter=self._convert_datetime_to_str(enter),
            leave=self._convert_datetime_to_str(leave),
            space_id=space_id,
            user_email=user_email,
        )
        self._put(f"/booking/{booking_id}", data=data.model_dump(by_alias=True))

    def delete_booking(self, booking_id: str):
        """Delete a booking using an ID."""
        self._delete(f"/booking/{booking_id}")
