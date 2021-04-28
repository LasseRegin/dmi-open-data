"""Simple Python interface to the The Danish Meteorological Institute's (DMI) Open Data API."""

__version__ = "0.0.8"

from dmi_open_data.client import DMIOpenDataClient
from dmi_open_data.enums import Parameter
from dmi_open_data.utils import microseconds2date, date2microseconds


__all__ = [
    'DMIOpenDataClient',
    'Parameter',
    'microseconds2date',
    'date2microseconds',
]
