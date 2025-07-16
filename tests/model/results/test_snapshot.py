import unittest
from gi.repository import GLib
from sbaid.common.b_display import BDisplay
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot


class SnapshotTestCase(unittest.TestCase):

    def test_add_cross_section(self):
        """Test adding a cross section snapshot."""
        now = GLib.DateTime.new_now_local()
        snapshot = Snapshot("snapshot_id", now)

        cs_snapshot_1 = CrossSectionSnapshot("random", "random", "Leonhard", BDisplay.SNOW)
        snapshot.add_cross_section_snapshot(cs_snapshot_1)

        self.assertIn(cs_snapshot_1, snapshot.cross_section_snapshots)



if __name__ == '__main__':
    unittest.main()
