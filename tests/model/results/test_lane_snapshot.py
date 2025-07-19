"""This module contains unittests for the LaneSnapshot class."""
import unittest
from gi.repository import GLib
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot
from sbaid.common.a_display import ADisplay
from sbaid.common.vehicle_type import VehicleType


class LaneSnapshotTest(unittest.TestCase):
    """This class tests the LaneSnapshot class."""

    def test_add_vehicle_snapshot(self):
        """Test adding a vehicle snapshot."""

        # Initialize valid instance of LaneSnapshot and VehicleSnapshot
        now = GLib.DateTime.new_now_local()
        lane_snapshot = LaneSnapshot(GLib.uuid_string_random(),
                                     GLib.uuid_string_random(), 4,
                                       70.6, 9, ADisplay.SPEED_LIMIT_100)

        vehicle_snapshot_1 = VehicleSnapshot(GLib.uuid_string_random(), VehicleType.CAR, 80.324)

        # Add vehicle_snapshot to list in lane_snapshot
        lane_snapshot.add_vehicle_snapshot(vehicle_snapshot_1)

        # Assertions
        self.assertIn(vehicle_snapshot_1, lane_snapshot.vehicle_snapshots)
        self.assertEqual(len(lane_snapshot.vehicle_snapshots), 1)
