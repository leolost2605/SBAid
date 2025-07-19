"""This module contains unittests for the CrossSection"""
import unittest

from gi.repository import GLib
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.common.b_display import BDisplay
from sbaid.common.a_display import ADisplay

class CrossSectionSnapshotTest(unittest.TestCase):
    """This class tests the CrossSectionSnapshot class."""

    cross_section_snapshot = CrossSectionSnapshot(GLib.uuid_string_random(),
                                                  GLib.uuid_string_random(),
                                                  "Julia",
                                                  BDisplay.SNOW)

    lane_snapshot_1 = LaneSnapshot(GLib.uuid_string_random(),
                                   GLib.uuid_string_random(), 0,
                                   70.6, 9, ADisplay.SPEED_LIMIT_100)
    lane_snapshot_2 = LaneSnapshot(GLib.uuid_string_random(),
                                   GLib.uuid_string_random(), 1,
                                   99.3, 5, ADisplay.SPEED_LIMIT_100)

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
        """Tests calculating the average speed. todo this ASSUMES previous method has run, maybe not best practice."""

        print(len(self.cross_section_snapshot.lane_snapshots))
        print(self.cross_section_snapshot.calculate_cs_average_speed())