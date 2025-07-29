# author: Jan Tschada
# SPDX-License-Identifier: Apache-2.0

from georapid.client import GeoRapidClient
from georapid.factory import EnvironmentClientFactory
from geolocaltime.services import enrich, convert, time_of_day
from geolocaltime.types import OutputType
from requests.exceptions import HTTPError

import unittest


class TestGeoLocalTimeService(unittest.TestCase):

    def setUp(self):
        host = 'geolocaltime.p.rapidapi.com'
        self.client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        self.latitudes = [50.0088, 39.437, 66.0557, 71.0201, 39.6466, 37.0969, 70.4]
        self.longitudes = [8.2756, -31.542, -23.7033, 26.1334, 44.8109, 13.9381, -47.1]
        self.utc_times = ['2024-10-19T09:18:42.542819', '2024-10-19T15:30:00.000000', '2024-10-19T21:45:15.123456']

    def test_enrich(self):
        result = enrich(self.client, self.latitudes, self.longitudes, OutputType.LOCAL)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.latitudes))

        # Test direct enrichment to DTC        
        dtc_result = enrich(self.client, self.latitudes, self.longitudes, OutputType.DTC)
        self.assertIsInstance(dtc_result, list)
        self.assertEqual(len(dtc_result), len(self.latitudes))
        self.assertTrue(all(isinstance(item, str) for item in dtc_result))

    def test_convert(self):
        result = convert(self.client, self.latitudes, self.longitudes, self.utc_times, OutputType.LOCAL)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.latitudes))

        # Test direct conversion to DTC
        dtc_result = convert(self.client, self.latitudes, self.longitudes, self.utc_times, OutputType.DTC)
        self.assertIsInstance(dtc_result, list)
        self.assertEqual(len(dtc_result), len(self.latitudes))
        self.assertTrue(all(isinstance(item, str) for item in dtc_result))

    def test_time_of_day(self):
        # Test with invalid utc times
        with self.assertRaises(HTTPError) as context:
            time_of_day(self.client, self.latitudes, self.longitudes, self.utc_times)
        self.assertIn("Bad Request", str(context.exception))
        
        # Test with valid local times
        local_times = convert(self.client, self.latitudes, self.longitudes, self.utc_times, OutputType.LOCAL)
        result = time_of_day(self.client, self.latitudes, self.longitudes, local_times)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.latitudes))

    def test_enrich_input_validation(self):
        # Test mismatched array lengths
        with self.assertRaises(ValueError) as context:
            enrich(self.client, [50.0], [8.0, 9.0], OutputType.LOCAL)
        self.assertIn("must have the same length", str(context.exception))

    def test_convert_input_validation(self):
        # Test mismatched array lengths
        with self.assertRaises(ValueError) as context:
            convert(self.client, [50.0], [8.0, 9.0], ['2024-10-19T09:18:42.542819'], OutputType.LOCAL)
        self.assertIn("must have the same length", str(context.exception))

    def test_time_of_day_input_validation(self):
        # Test mismatched array lengths
        with self.assertRaises(ValueError) as context:
            time_of_day(self.client, [50.0], [8.0, 9.0], ['2024-10-19T09:18:42.542819'])
        self.assertIn("must have the same length", str(context.exception))

    def test_latitude_validation(self):
        # Test invalid latitude values
        with self.assertRaises(ValueError) as context:
            enrich(self.client, [91.0], [8.0], OutputType.LOCAL)
        self.assertIn("Invalid latitude value", str(context.exception))

        with self.assertRaises(ValueError) as context:
            enrich(self.client, [-91.0], [8.0], OutputType.LOCAL)
        self.assertIn("Invalid latitude value", str(context.exception))

    def test_longitude_validation(self):
        # Test invalid longitude values
        with self.assertRaises(ValueError) as context:
            enrich(self.client, [50.0], [181.0], OutputType.LOCAL)
        self.assertIn("Invalid longitude value", str(context.exception))

        with self.assertRaises(ValueError) as context:
            enrich(self.client, [50.0], [-181.0], OutputType.LOCAL)
        self.assertIn("Invalid longitude value", str(context.exception))

    def test_chunking_behavior(self):
        # Test with exactly 100 coordinates - should work normally
        lats_100 = [50.0] * 100
        lons_100 = [8.0] * 100
        times_100 = ['2024-10-19T09:18:42.542819'] * 100
        
        # These should not raise exceptions (though may fail due to missing API key)
        try:
            result = enrich(self.client, lats_100, lons_100, OutputType.LOCAL)
            self.assertIsInstance(result, list)
        except ValueError as e:
            if "x_rapidapi_key" in str(e):
                self.skipTest("API key not available for integration test")
            else:
                raise

    def test_large_batch_handling(self):
        # Test with more than 100 coordinates to verify chunking
        lats_150 = [50.0] * 150  
        lons_150 = [8.0] * 150
        times_150 = ['2024-10-19T09:18:42.542819'] * 150
        
        # These should not raise exceptions due to batch size (though may fail due to missing API key)
        try:
            result = enrich(self.client, lats_150, lons_150, OutputType.LOCAL)
            self.assertIsInstance(result, list)
            # Results should have same length as input when chunking works properly
            self.assertEqual(len(result), 150)
        except ValueError as e:
            if "x_rapidapi_key" in str(e):
                self.skipTest("API key not available for integration test")
            else:
                raise

    def test_empty_inputs(self):
        # Test with empty inputs
        result = enrich(self.client, [], [], OutputType.LOCAL)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        result = convert(self.client, [], [], [], OutputType.LOCAL)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        result = time_of_day(self.client, [], [], [])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)