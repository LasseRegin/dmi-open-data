from datetime import datetime
import os
import unittest

from dmi_open_data import DMIOpenDataClient, ClimateDataParameter


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = DMIOpenDataClient(api_key=os.getenv("DMI_CLIMATE_DATA_API_KEY"))

    def test_observations(self):
        climate_data = self.client.get_climate_data(
            parameter=ClimateDataParameter.MeanTemp,
            station_id="06184",
            from_time=datetime(2021, 7, 20),
            to_time=datetime(2021, 7, 24),
            time_resolution="day",
            limit=1000,
        )
        self.assertIsInstance(
            climate_data, list, "Did not return a list of climate data"
        )
        self.assertGreater(len(climate_data), 0, "Could not find any climate data")


if __name__ == "__main__":
    unittest.main()
