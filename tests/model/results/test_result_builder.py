import asyncio
import unittest
import random
import uuid
from gi.repository import Gio, GLib
from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.vehicle_type import VehicleType
from unittest import mock
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.result import Result
from sbaid.model.results.result_builder import ResultBuilder, WrongOrderException
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.results.snapshot import Snapshot


class ResultBuilderTest(unittest.TestCase):

    __gio_file = Gio.File.new_for_path("placeholder_path.db")
    __global_mock_db = unittest.mock.AsyncMock()

    def test_build_with_random_values(self):
        asyncio.run(self.__test_build_with_random_values())

    async def __test_build_with_random_values(self):
        """Tests the result builder by calling the methods in the right order with random values."""
        snapshot_amount = 100
        cs_amount = 30
        lane_amount = 5
        result = await self.generate_result(snapshot_amount, cs_amount, lane_amount)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assertEqual(len(result.snapshots), snapshot_amount)

        random_snapshot = random.choice(list(result.snapshots))
        self.assertIsInstance(random_snapshot, Snapshot)
        self.assertEqual(len(random_snapshot.cross_section_snapshots), 30)

        random_cs_snapshot = random.choice(list(random_snapshot.cross_section_snapshots))
        self.assertIsInstance(random_cs_snapshot, CrossSectionSnapshot)
        self.assertEqual(len(random_cs_snapshot.lane_snapshots), lane_amount)


    def test_build_in_wrong_order(self):
        """Tests if the internal logic is robust enough to catch errors in the false building order."""
        with self.assertRaises(WrongOrderException):
            asyncio.run(self.__build_incomplete_cross_section())
            asyncio.run(self.__build_incomplete_lane())

    async def __build_incomplete_cross_section(self):
        """Starts building the result but does not add required values for the cross-section"""
        result_builder = ResultBuilder(ResultManager(self.__global_mock_db))
        result_builder.begin_result("randomized_result")

        time = GLib.DateTime.new(tz=GLib.TimeZone.new_local(), year=2025, month=8,
                                 day=3, hour=13, minute=35, seconds=4)
        result_builder.begin_snapshot(time)
        result_builder.begin_cross_section(str(uuid.uuid4()), "cross-section")
        result_builder.begin_lane(0)

    async def __build_incomplete_lane(self):
        result_builder = ResultBuilder(ResultManager(self.__global_mock_db))
        result_builder.begin_result("randomized_result")

        time = GLib.DateTime.new(tz=GLib.TimeZone.new_local(), year=2025, month=8,
                                 day=3, hour=13, minute=35, seconds=4)
        result_builder.begin_snapshot(time)
        result_builder.begin_cross_section(str(uuid.uuid4()), "cross-section")
        result_builder.add_b_display(random.choice(list(BDisplay)))
        result_builder.begin_lane(0)
        result_builder.add_a_display(random.choice(list(ADisplay)))
        result_builder.end_lane()

    async def generate_result(self, snapshot_amount: int, cs_amount: int, lane_amount: int) -> Result:
        """Generates a result with random values for testing purposes.
        The only thing not realistic is that the average speed calculated
        from the vehicles will not match the lane average.
        The next month is also not supported."""

        result_builder = ResultBuilder(ResultManager(self.__global_mock_db))
        result_builder.begin_result("randomized_result")
        random_ids = self.__generate_random_ids(cs_amount)
        for i in range(snapshot_amount):  # amount of snapshots
            minute = (30 + (i * 10)) % 60
            hour = ( 15 + ((30 + (i * 10)) // 60) ) % 24
            day = ( 24 + ((30 + (i * 10)) // 60)) // 24

            time = GLib.DateTime.new(tz=GLib.TimeZone.new_local(), year=2025, month=7,
                                     day=day, hour=hour, minute=minute, seconds=0)
            result_builder.begin_snapshot(time)
            for m in range(cs_amount):  # amount of cross-sections
                result_builder.begin_cross_section(random_ids[m], "cross-section " + str(m))
                result_builder.add_b_display(random.choice(list(BDisplay)))

                for p in range(lane_amount):  # amount of lanes
                    result_builder.begin_lane(p)
                    result_builder.add_a_display(random.choice(list(ADisplay)))
                    traffic_volume = random.randint(1, 50)
                    result_builder.add_traffic_volume(traffic_volume)
                    result_builder.add_average_speed(random.uniform(60.0, 140.0))

                    for k in range(traffic_volume):  # amount of vehicles
                        result_builder.begin_vehicle()
                        result_builder.add_vehicle_type(random.choice(list(VehicleType)))
                        # the average of all vehicles will not match the lane.average_speed
                        result_builder.add_vehicle_speed(random.uniform(60.0, 140.0))
                        result_builder.end_vehicle()
                    result_builder.end_lane()
                result_builder.end_cross_section()
            result_builder.end_snapshot()

        result = await result_builder.end_result()

        return result

    def __generate_random_ids(self, n: int):
        random_ids = []
        for i in range(n):
            random_ids.append(uuid.uuid4())
        return random_ids

