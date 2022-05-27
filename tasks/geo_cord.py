import requests
from decimal import Decimal
from django.core.exceptions import ValidationError
from typing import Tuple


class LocationService(object):
    """Abstraction for an external Geocoding API that we use for
    transforming addresses into coordinates.

    Example fixture for the return of `__request_get` method
    is contained on `domain.tests.fixtures` module.
    """

    def __init__(self, endpoint: str, apikey: str, timeout: float = 5.0) -> None:
        self.endpoint = endpoint
        self.apikey = apikey
        self.timeout = timeout

    def get_coordinates(self, address: str) -> Tuple[Decimal, Decimal]:
        """Handle requesting the address data from an external API
        and its response to be returned in the expected format."""
        params = {"address": address}
        data = self.__request_get(params)
        return self._extract_coordinates(data)

    def _extract_coordinates(self, data: dict) -> Tuple[Decimal, Decimal]:
        if data["status"] == "ZERO_RESULTS":
            raise ValidationError("Not found results to process.")

        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lng

    def __request_get(self, params: dict) -> dict:
        # See `domain.tests.fixtures` for example response.
        params["key"] = self.apikey
        response = requests.get(self.endpoint, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
