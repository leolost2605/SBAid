import unittest

from gi.repository import GLib
from sbaid.model.results.result import Result
from sbaid.common.tag import Tag
from sbaid.model.results.snapshot import Snapshot


class ResultClassTestCase(unittest.TestCase):
    """This class tests the NetworkState class."""

    def test_add_tags(self):
        """Test adding tags"""
        now = GLib.DateTime.new_now_local()
        result = Result("random", "my_project", now)
        a = Tag("sorandom", "my_tag3")
        b = Tag("sosorandomstring1", "help_me")

        result.add_tag(a)
        result.add_tag(b)

        self.assertEqual(len(result.selected_tags), 2)
        self.assertIn(a, result.selected_tags)
        self.assertIn(b, result.selected_tags)

        result.remove_tag(a)

        self.assertEqual(len(result.selected_tags), 1)
        self.assertNotIn(a, result.selected_tags)
        self.assertIn(b, result.selected_tags)

    def test_add_snapshot(self):
        """Test to adding snapshot methods"""
        now = GLib.DateTime.new_now_local()
        result = Result("random", "my_project", now)

        my_snapshot = Snapshot("my_snapshot2", now)
        my_snapshot2 = Snapshot("my_snapshot2", now)

        result.add_snapshot(my_snapshot)
        result.add_snapshot(my_snapshot2)

        self.assertEqual(len(result.snapshots), 2)
        self.assertIn(my_snapshot, result.snapshots)
        self.assertIn(my_snapshot2, result.snapshots)


