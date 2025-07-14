import unittest

from sbaid.model.simulation.vehicle_info import VehicleInfo
from sbaid.common.vehicle_type import VehicleType


class VehicleInfoTestCase(unittest.TestCase):
    def setUp(self):
        self.lorry = VehicleInfo(VehicleType.LORRY, 80)
        self.car = VehicleInfo(VehicleType.CAR, 130)
        self.speedster = VehicleInfo(VehicleType.CAR, 210.56)

    def test_properties(self):
        self.assertEqual(self.lorry.vehicle_type, VehicleType.LORRY)
        self.assertEqual(self.car.vehicle_type, VehicleType.CAR)
        self.assertEqual(self.lorry.speed, 80)
        self.assertEqual(self.speedster.speed, 210.56)

    def test_immutability(self):
        self.assertRaises(TypeError, self.set_speed, self.speedster)
        self.assertRaises(TypeError, self.set_speed, self.lorry)
        self.assertRaises(TypeError, self.set_type, self.lorry)

    def set_speed(self, vehicle):
        vehicle.speed = 90

    def set_type(self, vehicle):
        vehicle.vehicle_type = VehicleType.CAR

    def test_property_types(self):
        self.assertRaises(TypeError, self.construct_wrong_type)

    def construct_wrong_type(self):
        info = VehicleInfo("my vehicle", "80km/h")


if __name__ == '__main__':
    unittest.main()
