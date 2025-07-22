import asyncio
import unittest

from gi.repository import GLib
from gi.repository import Gio
from gi.events import GLibEventLoopPolicy

from sbaid.model.database.project_sqlite import ProjectSQLite


class ProjectSQLiteTest(unittest.TestCase):

    def setUp(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectSQLiteTest().run_all_tests())
        loop.run_until_complete(task)

    async def run_all_tests(self) -> None:
        await self.test_meta_data()
        await self.test_algorithm_configuration()
        await self.test_parameters()
        await self.test_tag_and_parameter_tag()

    def on_delete_async(self, file, result, user_data):
        try:
            file.delete_finish(result)
        except GLib.Error as e:
            raise e

    async def test_meta_data(self) -> None:
        db = ProjectSQLite()
        file = Gio.File.new_for_path("test.db")
        await db.open(file)
        self.assertIsNotNone(await db.get_created_at())
        self.assertIsNotNone(await db.get_last_modified())
        self.assertNotEqual(await db.get_project_name(), "my_name")

        await db.set_project_name("my_project_name")
        self.assertIsNotNone(await db.get_created_at(), None)
        await db.set_last_modified(GLib.DateTime.new_now_local())
        created_at = await db.get_created_at()
        last_modified = await db.get_last_modified()
        self.assertTrue(GLib.DateTime.compare(created_at, last_modified) == -1)
        await db.set_project_name("my_project_name")
        self.assertEqual(await db.get_project_name(), "my_project_name")
        await db.set_last_modified(GLib.DateTime.new_now_local())
        new_last_modified = await db.get_last_modified()
        self.assertTrue(GLib.DateTime.compare(new_last_modified, created_at) == 1)

        file.delete_async(0, None, self.on_delete_async, None)

    async def test_algorithm_configuration(self):
        db = ProjectSQLite()
        file = Gio.File.new_for_path("test.db")
        await db.open(file)
        self.assertEqual(await db.get_all_algorithm_configuration_ids(), [])

        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id")
        await db.add_algorithm_configuration("my_algorithm_configuration_id_2",
                                             "my_algorithm_configuration_name", 1, 1, "my_path_2")
        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id_2")

        await db.remove_algorithm_configuration("my_algorithm_configuration_id_2")

        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "")

        await db.add_algorithm_configuration("my_algorithm_configuration_id_2",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        all_configs = await db.get_all_algorithm_configuration_ids()
        self.assertEqual(len(all_configs), 2)

        await db.set_selected_algorithm_configuration_id("my_algorithm_configuration_id")

        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id")

        file.delete_async(0, None, self.on_delete_async, None)

    async def test_parameters(self):
        db = ProjectSQLite()
        file = Gio.File.new_for_path("test.db")
        await db.open(file)

        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        value_to_be_inserted = GLib.Variant.new_boolean(True)
        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name",
                               None, value_to_be_inserted)

        self.assertEqual(await db.get_parameter_value("my_algorithm_configuration_id",
                                                      "my_parameter_name", None),
                         GLib.Variant.new_boolean(True))
        await db.remove_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertIsNone(await db.get_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None))

        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name", None, value_to_be_inserted)

        new_value = GLib.Variant.new_int64(161)
        await db.set_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None, new_value)

        self.assertEqual(await db.get_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None), new_value)

        file.delete_async(0, None, self.on_delete_async, None)


    async def test_cross_section(self):
        db = ProjectSQLite()
        file = Gio.File.new_for_path("test.db")
        await db.open(file)

        self.assertIsNone(await db.get_cross_section_name("my_nonexistent_cross_section_id"))
        await db.add_cross_section("my_cross_section_id", "my_cross_section_name")

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id"), "my_cross_section_name")

        await db.add_cross_section("my_cross_section_id_2", "my_cross_section_name_2")

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id_2"), "my_cross_section_name_2")

        await db.remove_cross_section("my_cross_section_id_2")

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id_2"), "")

        file.delete_async(0, None, self.on_delete_async, None)


    async def test_tag_and_parameter_tag(self):
        db = ProjectSQLite()
        file = Gio.File.new_for_path("test.db")
        await db.open(file)

        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        value_to_be_inserted = GLib.Variant.new_boolean(True)
        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name",
                               None, value_to_be_inserted)

        await db.add_tag("my_tag_id", "my_tag_name")

        await db.add_parameter_tag("my_parameter_tag_id", "my_parameter_name",
                                   "my_algorithm_configuration_id", None, "my_tag_id")
        all_parameter_tags = await db.get_all_tag_ids_for_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertEqual(len(all_parameter_tags), 1)

        # await db.remove_tag("my_tag_id")
        # updated_parameter_tags = await db.get_all_tag_ids_for_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        # self.assertEqual(len(updated_parameter_tags), 0)
        file.delete_async(0, None, self.on_delete_async, None)
