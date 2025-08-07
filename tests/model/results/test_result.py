"""This module contains unittests for the Result class."""
import unittest
from gi.repository import GLib, Gio
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.model.results.result import Result
from sbaid.common.tag import Tag
from sbaid.model.results.snapshot import Snapshot


class ResultClassTestCase(unittest.TestCase):
    """This class tests the Result class."""
    __gio_file = Gio.File.new_for_path("placeholder_path.db")
    __global_db = GlobalSQLite(__gio_file)

    def test_tags(self):
        """Test adding and removing tags"""
        now = GLib.DateTime.new_now_local()

        # initialize tags
        result = Result(GLib.uuid_string_random(), "my_project", now, self.__global_db)
        a = Tag(GLib.uuid_string_random(), "my_tag3")
        b = Tag(GLib.uuid_string_random(), "help_me")

        # add tags
        result.add_tag(a)
        result.add_tag(b)

        # assert length and containment of tags
        self.assertEqual(len(result.selected_tags), 2)
        self.assertIn(a, result.selected_tags)
        self.assertIn(b, result.selected_tags)

        # remove tag
        result.remove_tag(a)

        # assert new length and containment of tags
        self.assertEqual(len(result.selected_tags), 1)
        self.assertNotIn(a, result.selected_tags)
        self.assertIn(b, result.selected_tags)

    def test_add_snapshot(self):
        """Test adding snapshot methods"""
        now = GLib.DateTime.new_now_local()
        result = Result(GLib.uuid_string_random(), "my_project", now, self.__global_db)

        my_snapshot = Snapshot(GLib.uuid_string_random(), now, self.__global_db)
        my_snapshot2 = Snapshot(GLib.uuid_string_random(), now, self.__global_db)

        result.add_snapshot(my_snapshot)
        result.add_snapshot(my_snapshot2)

        self.assertEqual(len(result.snapshots), 2)
        self.assertIn(my_snapshot, result.snapshots)
        self.assertIn(my_snapshot2, result.snapshots)

    def test_name_setting(self):
        datetime = GLib.DateTime.new_now_local()
        result = Result(GLib.uuid_string_random(), "project_name", datetime, self.__global_db)
        self.assertEqual(result.result_name, "project_name_" + datetime.format("%F"))
