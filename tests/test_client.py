from datetime import datetime
import os
import unittest

from dmi_open_data import DMIOpenDataClient, Parameter, microseconds2date


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = DMIOpenDataClient(api_key=os.getenv('DMI_API_KEY'))

    def test_stations(self):
        stations = self.client.get_stations()
        self.assertIsInstance(stations, list, 'Did not return a list of stations')
        self.assertGreater(len(stations), 0, 'Could not find any stations')

    def test_stations_limit(self):
        limit = 10
        stations = self.client.get_stations(limit=limit)
        self.assertLessEqual(len(stations), limit, 'Fetched too many stations')

    def test_observations(self):
        observations = self.client.get_observations()
        self.assertIsInstance(observations, list, 'Did not return a list of observations')
        self.assertGreater(len(observations), 0, 'Could not find any observations')

    def test_observations_limit(self):
        limit = 10
        observations = self.client.get_observations(limit=limit)
        self.assertLessEqual(len(observations), limit, 'Fetched too many observations')

    def test_observations_parameter(self):
        for parameter in Parameter:
            observations = self.client.get_observations(
                parameter=parameter,
                limit=10)
            self.assertTrue(
                all(
                    observation.get('parameterId') == parameter.value
                    for observation in observations
                ),
                'Parameter did not match')

    def test_observations_station(self):
        station_id = '06156'
        observations = self.client.get_observations(
            station_id=station_id,
            limit=10)
        self.assertTrue(
            all(
                observation.get('stationId') == station_id
                for observation in observations
            ),
            'Station did not match')

    def test_observations_time_interval(self):
        from_time = datetime(2020, 12, 20)
        to_time = datetime(2020, 12, 24)
        observations = self.client.get_observations(
            from_time=from_time,
            to_time=to_time,
            limit=1000)
        self.assertTrue(
            all(
                from_time <= microseconds2date(observation['timeObserved']) < to_time
                for observation in observations
            ),
            'Found observations outside time interval')

    def test_list_parameters(self):
        parameters = self.client.list_parameters()
        self.assertTrue(
            all(
                isinstance(Parameter(parameter['value']), Parameter)
                for parameter in parameters
            ),
            'Returned a wrong parameter')

    def test_get_parameter(self):
        parameter = self.client.get_parameter(parameter_id='temp_dry')
        self.assertIsInstance(parameter, Parameter, 'Returned value was not a Parameter object.')
        self.assertEqual(parameter, Parameter.TempDry, 'Wrong parameter returned.')

    def test_get_closest_station(self):
        station = self.client.get_closest_station(latitude=55.707722, longitude=12.562119)
        self.assertIsInstance(station, dict, 'Returned station was not a dict.')


if __name__ == '__main__':
    unittest.main()