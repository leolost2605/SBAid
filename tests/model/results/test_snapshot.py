"""This module contains unittests for the Snapshot class"""
import unittest
from gi.repository import GLib
from sbaid.common.b_display import BDisplay
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot


class SnapshotTestCase(unittest.TestCase):
    """Test class for the Snapshot class"""

    def test_add_cross_section(self):
        """Test adding a cross-section snapshot."""
        now = GLib.DateTime.new_now_local()
        snapshot = Snapshot(GLib.uuid_string_random(), now)

        # initialize and add cross-section snapshot
        cs_snapshot_1 = CrossSectionSnapshot(GLib.uuid_string_random(), GLib.uuid_string_random(), "Jake", BDisplay.SNOW)
        snapshot.add_cross_section_snapshot(cs_snapshot_1)

        # assert length, added snapshot contained
        self.assertIn(cs_snapshot_1, snapshot.cross_section_snapshots)
        self.assertEqual(len(snapshot.cross_section_snapshots), 1)

        # initialize and add cross-section snapshot
        cs_snapshot_2 = CrossSectionSnapshot(GLib.uuid_string_random(), GLib.uuid_string_random(), "Eduardo", BDisplay.TRAFFIC_JAM)
        snapshot.add_cross_section_snapshot(cs_snapshot_2)

        # assert length, contains added snapshot, first snapshot position
        self.assertEqual(len(snapshot.cross_section_snapshots), 2)
        self.assertIn(cs_snapshot_2, snapshot.cross_section_snapshots)
        self.assertEqual(snapshot.cross_section_snapshots[0], cs_snapshot_1)


