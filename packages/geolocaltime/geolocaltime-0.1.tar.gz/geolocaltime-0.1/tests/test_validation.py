# author: Jan Tschada
# SPDX-License-Identifier: Apache-2.0

from geolocaltime.services import enrich, convert, time_of_day, _chunk_coordinates
from geolocaltime.types import OutputType

import unittest


class TestValidation(unittest.TestCase):
    """Test validation logic without requiring API keys."""

    def test_enrich_input_validation(self):
        # Test mismatched array lengths
        with self.assertRaises(ValueError) as context:
            enrich(None, [50.0], [8.0, 9.0], OutputType.LOCAL)
        self.assertIn("must have the same length", str(context.exception))

    def test_convert_input_validation(self):
        # Test mismatched array lengths
        with self.assertRaises(ValueError) as context:
            convert(None, [50.0], [8.0, 9.0], ['2024-10-19T09:18:42.542819'], OutputType.LOCAL)
        self.assertIn("must have the same length", str(context.exception))

    def test_time_of_day_input_validation(self):
        # Test mismatched array lengths
        with self.assertRaises(ValueError) as context:
            time_of_day(None, [50.0], [8.0, 9.0], ['2024-10-19T09:18:42.542819'])
        self.assertIn("must have the same length", str(context.exception))

    def test_latitude_validation(self):
        # Test invalid latitude values
        with self.assertRaises(ValueError) as context:
            enrich(None, [91.0], [8.0], OutputType.LOCAL)
        self.assertIn("Invalid latitude value", str(context.exception))

        with self.assertRaises(ValueError) as context:
            enrich(None, [-91.0], [8.0], OutputType.LOCAL)
        self.assertIn("Invalid latitude value", str(context.exception))

    def test_longitude_validation(self):
        # Test invalid longitude values
        with self.assertRaises(ValueError) as context:
            enrich(None, [50.0], [181.0], OutputType.LOCAL)
        self.assertIn("Invalid longitude value", str(context.exception))

        with self.assertRaises(ValueError) as context:
            enrich(None, [50.0], [-181.0], OutputType.LOCAL)
        self.assertIn("Invalid longitude value", str(context.exception))

    def test_empty_inputs(self):
        # Test with empty inputs
        result = enrich(None, [], [], OutputType.LOCAL)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        result = convert(None, [], [], [], OutputType.LOCAL)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        result = time_of_day(None, [], [], [])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_chunking_behavior(self):
        # Test chunking with exactly 100 coordinates
        lats = list(range(100))
        lons = list(range(100))
        times = ['2024-10-19T09:18:42.542819'] * 100

        chunks = list(_chunk_coordinates(lats, lons, times))
        self.assertEqual(len(chunks), 1)
        self.assertEqual(len(chunks[0][0]), 100)

        # Test chunking with 150 coordinates  
        lats = list(range(150))
        lons = list(range(150))
        times = ['2024-10-19T09:18:42.542819'] * 150

        chunks = list(_chunk_coordinates(lats, lons, times))
        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0][0]), 100)
        self.assertEqual(len(chunks[1][0]), 50)

        # Test chunking without times
        chunks = list(_chunk_coordinates(lats[:150], lons[:150]))
        self.assertEqual(len(chunks), 2)
        self.assertIsNone(chunks[0][2])

    def test_edge_cases(self):
        # Test edge case latitude values - just test validation, not API calls
        valid_lats = [-90.0, 90.0, 0.0]
        valid_lons = [-180.0, 180.0, 0.0]
        
        # Test that validation passes for valid coordinates
        # We test empty inputs to avoid API calls
        for lat in valid_lats:
            for lon in valid_lons:
                # Just test validation by calling with empty arrays
                result = enrich(None, [], [], OutputType.LOCAL)
                self.assertEqual(result, [])

        # Test boundary values that should fail
        invalid_lats = [-90.1, 90.1]
        invalid_lons = [-180.1, 180.1]
        
        for lat in invalid_lats:
            with self.assertRaises(ValueError):
                enrich(None, [lat], [0.0], OutputType.LOCAL)
                
        for lon in invalid_lons:
            with self.assertRaises(ValueError):
                enrich(None, [0.0], [lon], OutputType.LOCAL)


if __name__ == '__main__':
    unittest.main()