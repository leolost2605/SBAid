"""This module contains unittests for the Display class."""
import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio

from sbaid.common.location import Location
from sbaid.model.simulator.dummy.dummy_simulator import EndOfSimulationException
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.simulation.vehicle_info import VehicleInfo
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator


class DisplayTestCase(unittest.IsolatedAsyncioTestCase):
    """This class tests the display using pythons unittest."""

    async def test_simple(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("tests/model/dummy_simulator/test.json")

        await sim.init_simulation()
        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 131.9)
        await sim.continue_simulation(10)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 130.3)

        self.assertEqual(sim.route_points.get_item(0), Location(5.4, 8.8))
        self.assertEqual(sim.route_points.get_item(1), Location(2.5, 7.9))

    async def test_reset(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("tests/model/dummy_simulator/test.json")

        await sim.init_simulation()
        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 131.9)
        await sim.continue_simulation(10)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 130.3)

        await sim.stop_simulation()
        await sim.init_simulation()

        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 131.9)
        await sim.continue_simulation(10)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 130.3)

    async def test_load_different_file(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("tests/model/dummy_simulator/test.json")


        with self.assertRaises(FileNotFoundError):
            await sim.measure()

        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        await sim.continue_simulation(10)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        other_file = Gio.File.new_for_path("tests/model/dummy_simulator/test2.json")

        with self.assertRaises(RuntimeError):
            await sim.load_file(other_file)

    async def test_run_too_long(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("tests/model/dummy_simulator/test.json")

        await sim.init_simulation()
        await sim.load_file(cur_file)
        with self.assertRaises(EndOfSimulationException):
            await sim.continue_simulation(11)

    async def test_vehicle_infos(self):
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("test.json")

        await sim.init_simulation()
        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        veh_infos_cs1_lane0 = fetched_input.get_all_vehicle_infos("cs1", 0)
        veh_infos_cs1_lane1 = fetched_input.get_all_vehicle_infos("cs1", 1)
        veh_infos_cs2_lane0 = fetched_input.get_all_vehicle_infos("cs2", 0)
        veh_infos_cs2_lane1 = fetched_input.get_all_vehicle_infos("cs2", 1)

        self.assertEqual(veh_infos_cs1_lane0, [VehicleInfo(VehicleType.CAR, 130.2),
                                               VehicleInfo(VehicleType.CAR, 124.7),
                                               VehicleInfo(VehicleType.CAR, 130.2),
                                               VehicleInfo(VehicleType.CAR, 126.2)])
        self.assertEqual(veh_infos_cs1_lane1, [VehicleInfo(VehicleType.CAR, 131.6),
                                               VehicleInfo(VehicleType.LORRY, 120.2)])
        self.assertEqual(veh_infos_cs2_lane0, [VehicleInfo(VehicleType.CAR, 123.7),
                                               VehicleInfo(VehicleType.CAR, 140.1)])
        self.assertEqual(veh_infos_cs2_lane1, [VehicleInfo(VehicleType.CAR, 163.3),
                                               VehicleInfo(VehicleType.LORRY, 120.9)])

        await sim.continue_simulation(10)
        fetched_input = await sim.measure()

        veh_infos_cs1_lane0 = fetched_input.get_all_vehicle_infos("cs1", 0)
        veh_infos_cs1_lane1 = fetched_input.get_all_vehicle_infos("cs1", 1)
        veh_infos_cs2_lane0 = fetched_input.get_all_vehicle_infos("cs2", 0)
        veh_infos_cs2_lane1 = fetched_input.get_all_vehicle_infos("cs2", 1)

        self.assertEqual(veh_infos_cs1_lane0, [VehicleInfo(VehicleType.CAR, 130.2),
                                               VehicleInfo(VehicleType.CAR, 124.7)])
        self.assertEqual(veh_infos_cs1_lane1, [VehicleInfo(VehicleType.CAR, 131.6),
                                               VehicleInfo(VehicleType.LORRY, 120.2)])
        self.assertEqual(veh_infos_cs2_lane0, [VehicleInfo(VehicleType.CAR, 120.5),
                                               VehicleInfo(VehicleType.CAR, 140.1)])
        self.assertEqual(veh_infos_cs2_lane1, [VehicleInfo(VehicleType.CAR, 163.3),
                                               VehicleInfo(VehicleType.LORRY, 120.9)])
