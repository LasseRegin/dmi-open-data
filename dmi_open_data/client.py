from datetime import datetime
from typing import List, Dict, Optional, Any, Union

import requests
from tenacity import retry, stop_after_attempt, wait_random

from dmi_open_data.enums import Parameter
from dmi_open_data.utils import date2microseconds, distance


class DMIOpenDataClient:
    _base_url = 'https://dmigw.govcloud.dk/metObs'

    def __init__(self, api_key: str, version: str = 'v1'):
        if api_key is None:
            raise ValueError(f"Invalid value for `api_key`: {api_key}")

        self.api_key = api_key
        self.version = version

    @property
    def base_url(self):
        return f"{self._base_url}/{self.version}"

    @retry(stop=stop_after_attempt(10), wait=wait_random(min=0.01, max=0.10))
    def _query(self, service: str, params: Dict[str, Any], **kwargs):
        res = requests.get(
            url=f"{self.base_url}/{service}",
            params={
                'api-key': self.api_key,
                **params,
            },
            **kwargs,
        )
        return res.json()

    def get_stations(self,
                     limit: Optional[int] = 10000,
                     offset: Optional[int] = 0) -> List[Dict[str, Any]]:
        """Get DMI stations.

        Args:
            limit (Optional[int], optional): Specify a maximum number of stations
                you want to be returned. Defaults to 10000.
            offset (Optional[int], optional): Specify the number of stations that should be skipped
                before returning matching objects. Defaults to 0.

        Returns:
            List[Dict[str, Any]]: List of DMI stations.
        """
        return self._query(
            service='station',
            params={
                'limit': limit,
                'offset': offset,
            })

    def get_observations(self,
                         parameter: Optional[Parameter] = None,
                         station_id: Optional[int] = None,
                         from_time: Optional[datetime] = None,
                         to_time: Optional[datetime] = None,
                         limit: Optional[int] = 10000,
                         offset: Optional[int] = 0) -> List[Dict[str, Any]]:
        """Get raw DMI observation.

        Args:
            parameter_id (Optional[Parameter], optional): Returns observations for a specific parameter.
                Defaults to None.
            station_id (Optional[int], optional): Search for a specific station using the stationID.
                Defaults to None.
            from_time (Optional[datetime], optional): Returns only objects with a "timeObserved" equal
                to or after a given timestamp. Defaults to None.
            to_time (Optional[datetime], optional): Returns only objects with a "timeObserved" before
                (not including) a given timestamp. Defaults to None.
            limit (Optional[int], optional): Specify a maximum number of observations
                you want to be returned. Defaults to 10000.
            offset (Optional[int], optional): Specify the number of observations that should be skipped
                before returning matching objects. Defaults to 0.

        Returns:
            List[Dict[str, Any]]: List of raw DMI observations.
        """
        return self._query(
            service='observation',
            params={
                'parameterId': None if parameter is None else parameter.value,
                'stationId': station_id,
                'from': None if from_time is None else date2microseconds(from_time),
                'to': None if to_time is None else date2microseconds(to_time),
                'limit': limit,
                'offset': offset,
            })

    def list_parameters(self) -> List[Dict[str, Union[str, Parameter]]]:
        """List available observation parameters.

        Returns:
            List[Dict[str, Union[str, Parameter]]]: List of dictionaries
                containing information about each available observations
                parameter.
        """
        return [
            {
                'name': parameter.name,
                'value': parameter.value,
                'enum': parameter,
            }
            for parameter in Parameter
        ]

    @staticmethod
    def get_parameter(parameter_id: str) -> Parameter:
        """Get parameter enum from DMI parameter id.

        Args:
            parameter_id (int): Parameter id found on DMI API documentation.

        Returns:
            Parameter: Parameter enum object.
        """
        return Parameter(parameter_id)

    def get_closest_station(self, latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """Get closest weather station from given coordinates.

        Args:
            latitude (float): Latitude coordinate.
            longitude (float): Longitude coordinate.

        Returns:
            List[Dict[str, Any]]: Closest weather station.
        """
        stations = self.get_stations()
        closest_station, closests_dist = None, 1e10
        for station in stations:
            location = station.get('location', {})
            lat, lon = location.get('latitude'), location.get('longitude')
            if lat is None or lon is None:
                continue

            # Calculate distance
            dist = distance(
                lat1=latitude,
                lon1=longitude,
                lat2=lat,
                lon2=lon,
            )

            if dist < closests_dist:
                closests_dist, closest_station = dist, station
        return closest_station
