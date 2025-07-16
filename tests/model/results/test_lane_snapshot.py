import unittest

from gi.repository import GLib
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot
from sbaid.common.a_display import ADisplay
from sbaid.common.vehicle_type import VehicleType


class LaneSnapshotTest(unittest.TestCase):

    def test_add_vehicle_snapshot(self):
        """Testing adding a vehicle snapshot."""
        now = GLib.DateTime.new_now_local()

        lane_snapshot = LaneSnapshot("cross_section_snapshot_id",
                                       "lane_snapshot_id", 4,
                                       70.6, 9, ADisplay.SPEED_LIMIT_100)

        vehicle_snapshot_1 = VehicleSnapshot("vehicle_snapshot_id", VehicleType.CAR, 80.324)

        lane_snapshot.add_vehicle_snapshot(vehicle_snapshot_1)

        self.assertIn(vehicle_snapshot_1, lane_snapshot.vehicle_snapshots)