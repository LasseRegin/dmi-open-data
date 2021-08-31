# DMI Open Data API

Simple Python interface to the The Danish Meteorological Institute's (DMI) v2 [Open Data API](https://confluence.govcloud.dk/display/FDAPI/Danish+Meteorological+Institute+-+Open+Data).

Weather data from Denmark and Greenland are publicly available through DMI's Open Data API. Fetch raw weather observations from all available weather stations in Denmark and Greenland. Parameters available include _temperature_, _windspeed_, _humidity_, _pressure_, \_precipitation\_\_, and many more.

## Requirements

- Python 3.6+
- API Key for **metObs v2** from [DMI Open Data](https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476690)
- (Optional) API Key for **climateData v2** from [DMI Open Data](https://confluence.govcloud.dk/display/FDAPI/Climate+data?src=contextnavpagetreemode)

## Installation

```bash
$ pip install dmi-open-data
```

## Example

```python
from datetime import datetime
import os

from dmi_open_data import DMIOpenDataClient, Parameter, ClimateDataParameter


# Get 10 stations
client = DMIOpenDataClient(api_key=os.getenv('DMI_API_KEY'))
stations = client.get_stations(limit=10)

# Get all stations
stations = client.get_stations()

# Get DMI station
dmi_station = next(
    station
    for station in stations
    if station['properties']['name'].lower() == 'dmi')

# Get closest station
closest_station = client.get_closest_station(
    latitude=55.707722,
    longitude=12.562119)

# Get available parameters
parameters = client.list_parameters()

# Get temperature observations from DMI station in given time period
observations = client.get_observations(
    parameter=Parameter.TempDry,
    station_id=dmi_station['properties']['stationId'],
    from_time=datetime(2021, 7, 20),
    to_time=datetime(2021, 7, 24),
    limit=1000)

# Init climate data client
climate_data_client = DMIOpenDataClient(api_key=os.getenv('DMI_CLIMATE_DATA_API_KEY'))

# Get climate data
climate_data = climate_data_client.get_climate_data(
    parameter=ClimateDataParameter.MeanTemp,
    station_id=dmi_station['properties']['stationId'],
    from_time=datetime(2021, 7, 20),
    to_time=datetime(2021, 7, 24),
    time_resolution='day',
    limit=1000)
```

## API Key

API Key can be obtained for free at the [DMI Open Data](https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476690).

## Tests

Run tests

```bash
$ python -m unittest discover tests
```
