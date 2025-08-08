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
from tests import result_testing_utils


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
        result = await result_testing_utils.generate_result(snapshot_amount, cs_amount, lane_amount)

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
