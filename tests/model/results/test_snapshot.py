"""This module contains unittests for the Snapshot class"""
import unittest
import uuid

from gi.repository import GLib, Gio
from sbaid.common.b_display import BDisplay
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot


class SnapshotTestCase(unittest.TestCase):
    """Test class for the Snapshot class"""
    __gio_file = Gio.File.new_for_path("placeholder_path.db")
    __global_db = GlobalSQLite(__gio_file)

    def test_add_cross_section(self):
        """Test adding a cross-section snapshot."""
        now = GLib.DateTime.new_now_local()
        snapshot = Snapshot(GLib.uuid_string_random(), now, self.__global_db)

        # initialize and add cross-section snapshot
        cs_snapshot_1 = CrossSectionSnapshot(GLib.uuid_string_random(), GLib.uuid_string_random(), "Jake", str(uuid.uuid4()), BDisplay.SNOW, self.__global_db)
        snapshot.add_cross_section_snapshot(cs_snapshot_1)

        # assert length, added snapshot contained
        self.assertIn(cs_snapshot_1, snapshot.cross_section_snapshots)
        self.assertEqual(len(snapshot.cross_section_snapshots), 1)

        # initialize and add cross-section snapshot
        cs_snapshot_2 = CrossSectionSnapshot(GLib.uuid_string_random(), GLib.uuid_string_random(), "Eduardo", str(uuid.uuid4()), BDisplay.TRAFFIC_JAM, self.__global_db)
        snapshot.add_cross_section_snapshot(cs_snapshot_2)

        # assert length, contains added snapshot, first snapshot position
        self.assertEqual(len(snapshot.cross_section_snapshots), 2)
        self.assertIn(cs_snapshot_2, snapshot.cross_section_snapshots)
        self.assertEqual(snapshot.cross_section_snapshots[0], cs_snapshot_1)


