from datetime import datetime
from typing import List, Dict, Optional, Any, Union

import requests
from tenacity import retry, stop_after_attempt, wait_random

from dmi_open_data.enums import Parameter, ClimateDataParameter
from dmi_open_data.utils import distance


class DMIOpenDataClient:
    _base_url = "https://dmigw.govcloud.dk/{version}/{api}"

    def __init__(self, api_key: str, version: str = "v2"):
        if api_key is None:
            raise ValueError(f"Invalid value for `api_key`: {api_key}")
        if version == "v1":
            raise ValueError(f"DMI metObs v1 not longer supported")
        if version not in ["v2"]:
            raise ValueError(f"API version {version} not supported")

        self.api_key = api_key
        self.version = version

    def base_url(self, api: str):
        if api not in ("climateData", "metObs"):
            raise NotImplementedError(f"Following api is not supported yet: {api}")
        return self._base_url.format(version=self.version, api=api)

    @retry(stop=stop_after_attempt(10), wait=wait_random(min=0.1, max=1.00))
    def _query(self, api: str, service: str, params: Dict[str, Any], **kwargs):
        res = requests.get(
            url=f"{self.base_url(api=api)}/{service}",
            params={
                "api-key": self.api_key,
                **params,
            },
            **kwargs,
        )
        data = res.json()
        http_status_code = data.get("http_status_code", 200)
        if http_status_code != 200:
            message = data.get("message")
            raise ValueError(
                f"Failed HTTP request with HTTP status code {http_status_code} and message: {message}"
            )
        return res.json()

    def get_stations(
        self, limit: Optional[int] = 10000, offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        """Get DMI stations.

        Args:
            limit (Optional[int], optional): Specify a maximum number of stations
                you want to be returned. Defaults to 10000.
            offset (Optional[int], optional): Specify the number of stations that should be skipped
                before returning matching objects. Defaults to 0.

        Returns:
            List[Dict[str, Any]]: List of DMI stations.
        """
        res = self._query(
            api="metObs",
            service="collections/station/items",
            params={
                "limit": limit,
                "offset": offset,
            },
        )
        return res.get("features", [])

    def get_observations(
        self,
        parameter: Optional[Parameter] = None,
        station_id: Optional[int] = None,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
    ) -> List[Dict[str, Any]]:
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
        res = self._query(
            api="metObs",
            service="collections/observation/items",
            params={
                "parameterId": None if parameter is None else parameter.value,
                "stationId": station_id,
                "datetime": _construct_datetime_argument(
                    from_time=from_time, to_time=to_time
                ),
                "limit": limit,
                "offset": offset,
            },
        )
        return res.get("features", [])

    def get_climate_data(
        self,
        parameter: Optional[ClimateDataParameter] = None,
        station_id: Optional[int] = None,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        time_resolution: Optional[str] = None,
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
    ) -> List[Dict[str, Any]]:
        """Get raw DMI climate data.

        Args:
            parameter_id (Optional[ClimateDataParameter], optional): Returns observations for a specific parameter.
                Defaults to None.
            station_id (Optional[int], optional): Search for a specific station using the stationID.
                Defaults to None.
            from_time (Optional[datetime], optional): Returns only objects with a "timeObserved" equal
                to or after a given timestamp. Defaults to None.
            to_time (Optional[datetime], optional): Returns only objects with a "timeObserved" before
                (not including) a given timestamp. Defaults to None.
            time_resolution (Optional[str], optional): Filter by time resolution (hour/day/month/year),
                ie. what type of time interval the station value represents
            limit (Optional[int], optional): Specify a maximum number of observations
                you want to be returned. Defaults to 10000.
            offset (Optional[int], optional): Specify the number of observations that should be skipped
                before returning matching objects. Defaults to 0.

        Returns:
            List[Dict[str, Any]]: List of raw DMI observations.
        """
        res = self._query(
            api="climateData",
            service="collections/stationValue/items",
            params={
                "parameterId": None if parameter is None else parameter.value,
                "stationId": station_id,
                "datetime": _construct_datetime_argument(
                    from_time=from_time, to_time=to_time
                ),
                "timeResolution": time_resolution,
                "limit": limit,
                "offset": offset,
            },
        )
        return res.get("features", [])

    def list_parameters(self) -> List[Dict[str, Union[str, Parameter]]]:
        """List available observation parameters.

        Returns:
            List[Dict[str, Union[str, Parameter]]]: List of dictionaries
                containing information about each available observations
                parameter.
        """
        return [
            {
                "name": parameter.name,
                "value": parameter.value,
                "enum": parameter,
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

    def get_closest_station(
        self, latitude: float, longitude: float
    ) -> List[Dict[str, Any]]:
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
            coordinates = station.get("geometry", {}).get("coordinates")
            if coordinates is None or len(coordinates) < 2:
                continue
            lat, lon = coordinates[1], coordinates[0]
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


def _construct_datetime_argument(
    from_time: Optional[datetime] = None, to_time: Optional[datetime] = None
) -> str:
    if from_time is None and to_time is None:
        return None
    if from_time is not None and to_time is None:
        return f"{from_time.isoformat()}Z"
    if from_time is None and to_time is not None:
        return f"{to_time.isoformat()}Z"
    return f"{from_time.isoformat()}Z/{to_time.isoformat()}Z"
