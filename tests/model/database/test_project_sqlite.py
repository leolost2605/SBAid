import asyncio
import unittest

from gi.repository import GLib
from gi.repository import Gio
from gi.events import GLibEventLoopPolicy

from sbaid.model.database.foreign_key_error import ForeignKeyError
from sbaid.model.database.project_sqlite import ProjectSQLite, InvalidDatabaseError


class ProjectSQLiteTest(unittest.TestCase):

    def setUp(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectSQLiteTest().test())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def test(self) -> None:
        await self.meta_data()
        await self.algorithm_configuration()
        await self.parameters()
        await self.cross_section()
        await self.tag_and_parameter_tag()
        await self.already_existed()

    def on_delete_async(self, file, result, user_data):
        try:
            file.delete_finish(result)
        except GLib.Error as e:
            raise e

    async def meta_data(self) -> None:
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        self.assertIsNotNone(await db.get_created_at())
        self.assertIsNotNone(await db.get_last_opened())
        self.assertNotEqual(await db.get_project_name(), "my_name")

        await db.set_project_name("my_project_name")
        self.assertIsNotNone(await db.get_created_at(), None)
        await db.set_last_opened(GLib.DateTime.new_now_local())
        created_at = await db.get_created_at()
        last_opened = await db.get_last_opened()
        self.assertTrue(GLib.DateTime.compare(created_at, last_opened) == -1)
        await db.set_project_name("my_project_name")
        self.assertEqual(await db.get_project_name(), "my_project_name")
        await db.set_last_opened(GLib.DateTime.new_now_local())
        new_last_opened = await db.get_last_opened()
        self.assertTrue(GLib.DateTime.compare(new_last_opened, created_at) == 1)

        file.delete_async(0, None)

    async def algorithm_configuration(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        self.assertEqual(await db.get_all_algorithm_configuration_ids(), [])

        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id")
        await db.add_algorithm_configuration("my_algorithm_configuration_id_2",
                                             "my_algorithm_configuration_name", 1, 1, "my_path_2")
        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id_2")

        await db.remove_algorithm_configuration("my_algorithm_configuration_id_2")

        self.assertEqual(await db.get_selected_algorithm_configuration_id(), None)

        await db.add_algorithm_configuration("my_algorithm_configuration_id_2",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        all_configs = await db.get_all_algorithm_configuration_ids()
        self.assertEqual(len(all_configs), 2)

        await db.set_display_interval("my_algorithm_configuration_id", 123)
        await db.set_evaluation_interval("my_algorithm_configuration_id", 234)

        display_interval_1 = await db.get_display_interval("my_algorithm_configuration_id")
        eval_interval_1 = await db.get_evaluation_interval("my_algorithm_configuration_id")
        self.assertEqual(123, display_interval_1)
        self.assertEqual(234, eval_interval_1)

        await db.set_script_path("my_algorithm_configuration_id_2", "my/new/path")
        script_path_2 = await db.get_script_path("my_algorithm_configuration_id_2")
        self.assertEqual("my/new/path", script_path_2)

        await db.set_selected_algorithm_configuration_id("my_algorithm_configuration_id")

        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id")

        await db.set_algorithm_configuration_name("my_algorithm_configuration_id", "my_new_name")
        new_name = await db.get_algorithm_configuration_name("my_algorithm_configuration_id")
        self.assertEqual("my_new_name", new_name)
        algo_config = await db.get_algorithm_configuration("my_algorithm_configuration_id")
        self.assertIsNotNone(algo_config)

        file.delete_async(0, None)

    async def parameters(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        value_to_be_inserted = GLib.Variant.new_boolean(True)
        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name",
                               None)
        await db.set_parameter_value("my_algorithm_configuration_id", "my_parameter_name",
                                     None, value_to_be_inserted)

        self.assertEqual(await db.get_parameter_value("my_algorithm_configuration_id",
                                                      "my_parameter_name", None),
                         GLib.Variant.new_boolean(True))
        await db.remove_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertIsNone(await db.get_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None))

        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        await db.set_parameter_value("my_algorithm_configuration_id", "my_parameter_name",
                                     None, value_to_be_inserted)

        new_value = GLib.Variant.new_int64(161)
        await db.set_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None, new_value)

        self.assertEqual(new_value, await db.get_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None))

        file.delete_async(0, None)


    async def cross_section(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        self.assertEqual(await db.get_cross_section_name("my_nonexistent_cross_section_id"), None)
        await db.add_cross_section("my_cross_section_id")
        await db.set_cross_section_name("my_cross_section_id", "my_cross_section_name")
        await db.set_cross_section_hard_shoulder_active("my_cross_section_id", False)
        await db.set_cross_section_b_display_active("my_cross_section_id", True)

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id"), "my_cross_section_name")

        await db.add_cross_section("my_cross_section_id_2")
        await db.set_cross_section_name("my_cross_section_id_2", "my_cross_section_name_2")
        await db.set_cross_section_hard_shoulder_active("my_cross_section_id_2", False)
        await db.set_cross_section_b_display_active("my_cross_section_id_2", True)

        self.assertFalse(await db.get_cross_section_hard_shoulder_active("my_cross_section_id_2"))
        self.assertTrue(await db.get_cross_section_b_display_active("my_cross_section_id_2"))

        await db.set_cross_section_hard_shoulder_active("my_cross_section_id_2", True)
        await db.set_cross_section_b_display_active("my_cross_section_id_2", False)

        self.assertTrue(await db.get_cross_section_hard_shoulder_active("my_cross_section_id_2"))
        self.assertFalse(await db.get_cross_section_b_display_active("my_cross_section_id_2"))

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id_2"), "my_cross_section_name_2")

        await db.remove_cross_section("my_cross_section_id_2")

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id_2"), None)

        file.delete_async(0, None)


    async def tag_and_parameter_tag(self):
        file = Gio.File.new_for_path("./recursive/directories/test/apparently/successful/test.db")
        db = ProjectSQLite(file)
        await db.open()
        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        value_to_be_inserted = GLib.Variant.new_boolean(True)
        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name",
                               None)

        await db.set_parameter_value("my_algorithm_configuration_id", "my_parameter_name",
                                     None, value_to_be_inserted)

        await db.add_tag("my_tag_id", "my_tag_name")

        await db.add_parameter_tag("my_parameter_tag_id", "my_parameter_name",
                                   "my_algorithm_configuration_id", None, "my_tag_id")
        all_parameter_tag_ids = await db.get_all_tag_ids_for_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertEqual(len(all_parameter_tag_ids), 1)
        self.assertEqual(all_parameter_tag_ids[0], "my_tag_id")
        self.assertEqual("my_tag_name", await db.get_tag_name("my_tag_id"))

        await db.remove_tag("my_tag_id")
        await db.remove_parameter_tag("my_parameter_tag_id")

        await db.add_tag("my_tag_id", "my_tag_name")
        await db.add_parameter_tag("my_parameter_tag_id", "my_parameter_name",  # parameter_tag.id
                                   "my_algorithm_configuration_id", None, "my_tag_id")
        all_parameter_tag_ids = await db.get_all_tag_ids_for_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertEqual(len(all_parameter_tag_ids), 1)
        self.assertEqual(all_parameter_tag_ids[0], "my_tag_id")

        await db.remove_parameter("my_parameter_name", "my_algorithm_configuration_id", None)
        await db.remove_parameter_tag("my_parameter_tag_id")

        all_parameter_tag_ids = await db.get_all_tag_ids_for_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertEqual(len(all_parameter_tag_ids), 0)

        file.delete_async(0, None)

    async def foreign_key_error(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        async with ProjectSQLite(file) as db:
            try:
                await db.add_parameter("my_nonexistent_algorithm_configuration_d",
                                       "my_parameter_name", None, GLib.Variant.new_boolean(True))
            except ForeignKeyError:
                self.assertTrue(True)
            try:
                await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                                     "my_algorithm_configuration_name",
                                                     0, 0, "my_path")
                await db.add_parameter_tag("my_nonexistent_parameter_tag_id", "my_parameter_name",
                                           "my_algorithm_configuration_name",
                                           "my_nonexistent_cross_section_id", "my_tag_id")
            except ForeignKeyError:
                self.assertTrue(True)

                file.delete_async(0, None)
                return

            self.assertTrue(False)
        file.delete_async(0, None)

    async def already_existed(self) -> None:
        file = Gio.File.new_for_path("test.db")
        await file.make_directory_async(0)

        with self.assertRaises(InvalidDatabaseError):
            db = ProjectSQLite(file)
            await db.open()
        file.delete_async(0)
