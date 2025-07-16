import unittest

from gi.repository import GLib

from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.common.b_display import BDisplay
from sbaid.common.a_display import ADisplay




class CrossSectionSnapshotTest(unittest.TestCase):
    def test_add_lane_snapshot(self):
        """Testing addind a lane snapshot."""

        now = GLib.DateTime.new_now_local()
        cross_section_snapshot = CrossSectionSnapshot("random", "random", "Leonhard", BDisplay.SNOW)
        lane_snapshot_1 = LaneSnapshot("cross_section_snapshot_id",
                                       "lane_snapshot_id", 4,
                                       70.6, 9, ADisplay.SPEED_LIMIT_100)

        cross_section_snapshot.add_lane_snapshot(lane_snapshot_1)

        self.assertIn(lane_snapshot_1, cross_section_snapshot.lane_snapshots)


if __name__ == '__main__':
    unittest.main()
