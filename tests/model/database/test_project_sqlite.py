import sqlite3
import unittest

from gi.repository import GLib
from gi.repository import Gio

from sbaid.model.database.project_sqlite import ProjectSQLite


class ProjectSQLiteTest(unittest.IsolatedAsyncioTestCase):
    async def test_meta_data(self) -> None:
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

    async def test_algorithm_configuration(self):
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

        await db.set_selected_algorithm_configuration_id("my_algorithm_configuration_id")

        self.assertEqual(await db.get_selected_algorithm_configuration_id(), "my_algorithm_configuration_id")

        file.delete_async(0, None)

    async def test_parameters(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
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

        self.assertEqual(new_value, await db.get_parameter_value("my_algorithm_configuration_id", "my_parameter_name", None))

        file.delete_async(0, None)


    async def test_cross_section(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        self.assertEqual(await db.get_cross_section_name("my_nonexistent_cross_section_id"), None)
        await db.add_cross_section("my_cross_section_id", "my_cross_section_name", False, True)

        self.assertEqual(await db.get_cross_section_name("my_cross_section_id"), "my_cross_section_name")

        await db.add_cross_section("my_cross_section_id_2", "my_cross_section_name_2", False, True)

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


    async def test_tag_and_parameter_tag(self):
        file = Gio.File.new_for_path("./recursive/directories/test/apparently/successful/test.db")
        db = ProjectSQLite(file)
        await db.open()
        await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                             "my_algorithm_configuration_name", 1, 1, "my_path")
        value_to_be_inserted = GLib.Variant.new_boolean(True)
        await db.add_parameter("my_algorithm_configuration_id", "my_parameter_name",
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
        updated_parameter_tags = await db.get_all_tag_ids_for_parameter("my_algorithm_configuration_id", "my_parameter_name", None)
        self.assertEqual(len(updated_parameter_tags), 0)

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

    async def test_foreign_key_error(self):
        file = Gio.File.new_for_path("test.db")
        db = ProjectSQLite(file)
        await db.open()
        with self.assertRaises(sqlite3.IntegrityError):
            await db.add_parameter("my_nonexistent_algorithm_configuration_d",
                                   "my_parameter_name", None, GLib.Variant.new_boolean(True))
        with self.assertRaises(sqlite3.IntegrityError):
            await db.add_algorithm_configuration("my_algorithm_configuration_id",
                                                 "my_algorithm_configuration_name",
                                                 0, 0, "my_path")
            await db.add_parameter_tag("my_nonexistent_parameter_tag_id", "my_parameter_name",
                                       "my_algorithm_configuration_name",
                                       "my_nonexistent_cross_section_id", "my_tag_id")
        file.delete_async(0, None)
