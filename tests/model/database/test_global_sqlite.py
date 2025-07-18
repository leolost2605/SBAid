import unittest

from gi.repository import Gio
from gi.repository.GLib import DateTime, TimeZone

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
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
        self.assertEqual(await db.get_result_name("my_result_id"), "my_result_name")
        await db.delete_result("my_result_id")
        all_results = await db.get_all_results()
        self.assertEqual(len(all_results), 0)


    async def test_snapshot(self):
        db = GlobalSQLite()
        file = Gio.File.new_for_path("/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/test.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.save_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))

        self.assertEqual(len(await db.get_all_snapshots("my_result_id")), 0)

        await db.save_snapshot("my_snapshot_id", DateTime.new_now(TimeZone.new("Europe/Berlin")),
                               "my_result_id")

        self.assertEqual(len(await db.get_all_snapshots("my_snapshot_id")), 1)

    async def test_cross_section_snapshot(self):
        db = GlobalSQLite()
        file = Gio.File.new_for_path("/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/test.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.save_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))
        await db.save_cross_section_snapshot("my_cross_section_snapshot_id",
                                             "my_cross_section_name", BDisplay.OFF,
                                             "my_snapshot_id")
        self.assertEqual(len(await db.get_all_cross_section_snapshots("my_snapshot_id")), 1)
        await db.save_cross_section_snapshot("my_cross_section_snapshot_id_2",
                                             "my_cross_section_name", BDisplay.OFF,
                                             "my_snapshot_id")
        self.assertEqual(len(await db.get_all_cross_section_snapshots("my_snapshot_id")), 2)

        # self.assertRaises(sqlite3.OperationalError, db.save_cross_section_snapshot, "my_cross_section_snapshot_id",
        #                                      "my_cross_section_name", BDisplay.OFF,
        #                                      "my_snapshot_id") # TODO should not work but does

    async def test_lane_snapshot(self):
        db = GlobalSQLite()
        file = Gio.File.new_for_path("/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/test.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.save_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))
        await db.save_cross_section_snapshot("my_cross_section_snapshot_id",
                                             "my_cross_section_name", BDisplay.OFF,
                                             "my_snapshot_id")
        await db.save_lane_snapshot("my_lane_snapshot_id", 1, "my_cross_section_snapshot_id", ADisplay.OFF)

        self.assertEqual(len(await db.get_all_lane_snapshots("my_cross_section_snapshot_id")), 1)
        cs_snapshot = await db.get_all_lane_snapshots("my_cross_section_snapshot_id")
        self.assertEqual(cs_snapshot[0][2], ADisplay.OFF)





# asyncio.run(GlobalSQLiteTest().test_remove())
# asyncio.run(GlobalSQLiteTest().test_result())
# asyncio.run(GlobalSQLiteTest().test_snapshot())
# asyncio.run(GlobalSQLiteTest().test_cross_section_snapshot())
# asyncio.run(GlobalSQLiteTest().test_lane_snapshot())


