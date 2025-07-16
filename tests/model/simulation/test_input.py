"""This module contains unittests for the Display class."""

import unittest

from sbaid.common.vehicle_type import VehicleType
from sbaid.model.simulation.input import Input


class InputTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def test_empty_input(self):
        """Test an empty display, raising a KeyError when getter is called."""
        test_input = Input()
        self.assertIsNone(test_input.get_traffic_volume("my_cross_section_id", 0))
        self.assertIsNone(test_input.get_average_speed("my_cross_section_id", 0))
        self.assertEqual(test_input.get_all_vehicle_infos("my_cross_section_id", 0), [])

    def test_single_vehicle_input(self):
        """Test adding one vehicle info to an input,
        getting its properties and calculating secondary figures."""
        test_input = Input()
        test_input.add_vehicle_info("my_cross_section_id", 0, VehicleType.CAR, 129.53)
        self.assertEqual(test_input.get_traffic_volume("my_cross_section_id", 0), 1)
        self.assertEqual(test_input.get_average_speed("my_cross_section_id", 0), 129.53)
        self.assertTrue(len(test_input.get_all_vehicle_infos("my_cross_section_id", 0)) == 1)

        self.assertEqual(test_input.get_all_vehicle_infos("my_cross_section_id", 0)[0]
                        .vehicle_type, VehicleType.CAR)
        self.assertEqual(test_input.get_all_vehicle_infos("my_cross_section_id", 0)[0]
                        .speed, 129.53)

    def test_multiple_vehicle_input(self):
        """Test adding multiple vehicle infos to an input,
        getting its properties and calculating secondary figures
        also adding more infos after asserting."""
        test_input = Input()
        speed_sum = 0.0
        for i in range(10):
            test_input.add_vehicle_info("my_cross_section_id", 0, VehicleType.CAR, i)
            speed_sum += i
        avg = speed_sum / 10
        self.assertEqual(test_input.get_traffic_volume("my_cross_section_id", 0), 10)
        self.assertEqual(test_input.get_average_speed("my_cross_section_id", 0), avg)
        self.assertEqual(len(test_input.get_all_vehicle_infos("my_cross_section_id", 0)), 10)

        self.assertEqual(test_input.get_all_vehicle_infos("my_cross_section_id", 0)[0].vehicle_type,
                         VehicleType.CAR)
        self.assertEqual(test_input.get_all_vehicle_infos("my_cross_section_id", 0)[1].speed, 1)
        test_input.add_vehicle_info("my_cross_section_id", 0, VehicleType.LORRY, 10)

        new_sum = speed_sum + 10
        new_avg = new_sum / 11
        self.assertEqual(test_input.get_traffic_volume("my_cross_section_id", 0), 11)
        self.assertEqual(test_input.get_average_speed("my_cross_section_id", 0), new_avg)
        self.assertTrue(len(test_input.get_all_vehicle_infos("my_cross_section_id", 0)) == 11)

        self.assertEqual(test_input.get_all_vehicle_infos("my_cross_section_id", 0)[10]
                         .vehicle_type, VehicleType.LORRY)

    def test_different_lanes(self):
        test_input = Input()
        test_input.add_vehicle_info("my_cross_section_id", 0, VehicleType.LORRY, 100)
        test_input.add_vehicle_info("my_cross_section_id", 1, VehicleType.CAR, 130)

        self.assertEqual(test_input.get_traffic_volume("my_cross_section_id", 0), 1)
        self.assertEqual(test_input.get_traffic_volume("my_cross_section_id", 1), 1)
        self.assertIsNone(test_input.get_traffic_volume("my_cross_section_id", 2))

    def test_different_cross_sections(self):
        test_input = Input()
        test_input.add_vehicle_info("my_cross_section_id", 0, VehicleType.CAR, 100)
        test_input.add_vehicle_info("my_other_cross_section_id", 0, VehicleType.CAR, 130)

        self.assertEqual(test_input.get_average_speed("my_cross_section_id", 0), 100)
        self.assertEqual(test_input.get_average_speed("my_other_cross_section_id", 0), 130)
        self.assertIsNone(test_input.get_average_speed("my_nonexistent_cross_section_id", 0))
