"""This module contains unittests for the ResultManager class."""
import asyncio
import unittest
from unittest import mock
from gi.repository import GLib, Gio
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.results.result import Result

class ResultManagerTest(unittest.TestCase):
    """This class tests the ResultManager class. """
    __global_db = unittest.mock.AsyncMock()
    result_manager = ResultManager(__global_db)

    def test_add_and_remove_tag(self):
        """Test creating and removing tags to the list of available tags."""

        # create two tags
        self.result_manager.create_tag("test")
        self.result_manager.create_tag("test2")

        # assert length
        self.assertEqual(len(self.result_manager.available_tags), 2)

        # assert existence in list
        available_tag_one = self.result_manager.available_tags[0]
        available_tag_two = self.result_manager.available_tags[1]

        self.assertIn(available_tag_one, self.result_manager.available_tags)
        self.assertIn(available_tag_two, self.result_manager.available_tags)

        # delete tag
        self.result_manager.delete_tag(available_tag_one.tag_id)

        # assert length and non-existence in list
        self.assertEqual(len(self.result_manager.available_tags), 1)
        self.assertNotIn(available_tag_one, self.result_manager.available_tags)
        self.assertIn(available_tag_two, self.result_manager.available_tags)

    def test_add_and_remove_result(self):
        """Test creating and removing results to the list of results."""
        asyncio.run(self.__test_add_and_remove_result())

    async def __test_add_and_remove_result(self):
        """Test creating and removing results to the list of results."""

        # init result
        now = GLib.DateTime.new_now_local()
        test_id = GLib.uuid_string_random()
        test_name = "my_project"
        result = Result(test_id, test_name, now, self.__global_db)

        # register result
        await self.result_manager.register_result(result)

        # assert length, result in list, result initialized properly
        self.assertEqual(len(self.result_manager.results), 1)
        self.assertIn(result, self.result_manager.results)
        self.assertEqual(test_id, self.result_manager.results[0].id)
        self.assertEqual(result.id, self.result_manager.results[0].id)

        await self.result_manager.register_result(Result(GLib.uuid_string_random(), "test", now, self.__global_db))
        await self.result_manager.register_result(Result(GLib.uuid_string_random(), "test", now, self.__global_db))

        self.assertEqual(len(self.result_manager.results), 3)

        # delete first result
        self.result_manager.delete_result(test_id)

        # assert state of results list
        self.assertEqual(len(self.result_manager.results), 2)
        self.assertNotIn(result, self.result_manager.results)
