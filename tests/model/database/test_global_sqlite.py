import asyncio
import unittest
from time import tzset

from gi.repository import Gio
from gi.repository.GLib import DateTime, TimeZone

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.database.global_sqlite import GlobalSQLite


class GlobalSQLiteTest(unittest.TestCase):
    async def test_remove(self) -> None:
        db = GlobalSQLite()
        file = Gio.File.new_for_path("/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/test.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"), "my_simulator_file_path", "my_project_file_path")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 1)

        await db.remove_project("my_project_id")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 0)

        await db.add_project("my_project_id", SimulatorType("0", "Vissim"), "my_simulator_file_path", "my_project_file_path")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 1)

    async def test_result(self) -> None:
        db = GlobalSQLite()
        file = Gio.File.new_for_path("/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/test.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"), "my_simulator_file_path",
                             "my_project_file_path")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 1)
        await db.save_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))
        all_results = await db.get_all_results()
        self.assertEqual(len(all_results), 1)







asyncio.run(GlobalSQLiteTest().test_remove())
