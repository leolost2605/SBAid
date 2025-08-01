"""This module contains unittests for the CrossSection"""
import unittest
from gi.repository import GLib, Gio
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.common.b_display import BDisplay
from sbaid.common.a_display import ADisplay

class CrossSectionSnapshotTest(unittest.TestCase):
    """This class tests the CrossSectionSnapshot class."""

    gio_file = Gio.File.new_for_path("placeholder_path.db")
    global_db = GlobalSQLite(gio_file)

    cross_section_snapshot = CrossSectionSnapshot(GLib.uuid_string_random(),
                                                  GLib.uuid_string_random(),
                                                  "Julia",
                                                  BDisplay.SNOW, GlobalSQLite(gio_file))

    lane_snapshot_1 = LaneSnapshot(GLib.uuid_string_random(),
                                   GLib.uuid_string_random(), 0,
                                   70.6, 9, ADisplay.SPEED_LIMIT_100, GlobalSQLite(gio_file))
    lane_snapshot_2 = LaneSnapshot(GLib.uuid_string_random(),
                                   GLib.uuid_string_random(), 1,
                                   99.3, 5, ADisplay.SPEED_LIMIT_100, GlobalSQLite(gio_file))

    def test_add_lane_snapshot(self):
        """Tests adding lane snapshots."""
        self.assertEqual(len(self.cross_section_snapshot.lane_snapshots), 0) # assert length

        # add lane_snapshots then assert new state of the list
        self.cross_section_snapshot.add_lane_snapshot(self.lane_snapshot_1)

        self.assertIn(self.lane_snapshot_1, self.cross_section_snapshot.lane_snapshots)
        self.assertEqual(len(self.cross_section_snapshot.lane_snapshots), 1)

        self.cross_section_snapshot.add_lane_snapshot(self.lane_snapshot_2)

        self.assertIn(self.lane_snapshot_1, self.cross_section_snapshot.lane_snapshots)
        self.assertIn(self.lane_snapshot_2, self.cross_section_snapshot.lane_snapshots)
        self.assertEqual(len(self.cross_section_snapshot.lane_snapshots), 2)


    def test_calculate_average_speed(self):
        """Tests calculating the average speed."""
        self.assertIsNotNone(self.cross_section_snapshot.lane_snapshots)
        self.assertGreater(len(self.cross_section_snapshot.lane_snapshots), 0)
        calculated_speed = self.cross_section_snapshot.calculate_cs_average_speed()
        self.assertEqual(((70.6 + 99.3) / 2), calculated_speed)