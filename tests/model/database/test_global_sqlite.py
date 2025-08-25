import asyncio
import unittest

from gi.repository import Gio, GLib
from gi.repository.GLib import DateTime, TimeZone
from gi.events import GLibEventLoopPolicy

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.database.global_sqlite import GlobalSQLite

class GlobalSQLiteTest(unittest.TestCase):

    def setUp(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(GlobalSQLiteTest().test())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def test(self) -> None:
        await self.path()
        await self.remove()
        await self.add_entire_result()
        await self.multiple_dbs()


    async def path(self):
        file = Gio.File.new_for_path("recursive/directories/test/apparently/successful/test.db")
        db = GlobalSQLite(file)
        await db.open()
        self.assertTrue(file.query_exists())
        await file.delete_async(0, None)

    async def remove(self) -> None:
        file = Gio.File.new_for_path("test.db")
        db = GlobalSQLite(file)
        await db.open()
        self.assertEqual(len(await db.get_all_projects()), 0)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"), "my_simulator_file_path", "my_project_file_path")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 1)

        await db.remove_project("my_project_id")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 0)

        await db.add_project("my_project_id", SimulatorType("0", "Vissim"), "my_simulator_file_path", "my_project_file_path")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 1)

        await file.delete_async(0, None)

    async def times(self):
        revo_date = DateTime.new_from_iso8601("1917-10-25T08:00:00.200000+02",
                                                       TimeZone.new_utc())
        file = Gio.File.new_for_path("test.db")
        db = GlobalSQLite(file)
        await db.open()
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name",
                            revo_date)
        all_results = await db.get_all_results()
        self.assertEqual(all_results[0][0], "my_result_id")
        self.assertEqual(all_results[0][1], "my_result_name")
        self.assertEqual(all_results[0][2], "my_project_name")
        self.assertEqual(all_results[0][3].format_iso8601(), revo_date.format_iso8601())

        await file.delete_async(0, None)

    async def tags(self):
        revo_date = DateTime.new_from_iso8601("1917-10-25T08:00:00.200000+02",
                                                       TimeZone.new_utc())
        file = Gio.File.new_for_path("test.db")
        db = GlobalSQLite(file)
        await db.open()
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name",
                            revo_date)

        await db.add_tag("my_tag_id", "my_tag_name")

        await db.add_result_tag("my_result_tag_id", "my_result_id", "my_tag_id")
        my_project_tags = await db.get_result_tag_ids("my_result_id")
        self.assertEqual(len(my_project_tags), 1)
        self.assertEqual(my_project_tags[0][0], "my_tag_id")
        self.assertEqual("my_tag_name", await db.get_tag_name("my_tag_id"))

        await file.delete_async(0, None)

    async def foreign_key_error(self):
        file = Gio.File.new_for_path("test.db")
        db = GlobalSQLite(file)
        await db.open()
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path", "my_project_file_path")

        veh_sn = [("lane_sn_id", 0, 120.0)]
        lane_sn = [("lane_sn_id", "cs_sn_id", 0, 120.0, 5, 0, veh_sn)]
        cs_sn = [("cs_sn_id", "sn_id", "cs_id", "cs_name", 0, lane_sn)]
        snapshot_data = [("sn_id", "my_res_id", GLib.DateTime.new_now_local().format_iso8601(), cs_sn)]
        await db.add_entire_result("my_res_id", "my_res_name", "my_project_name",
                                   GLib.DateTime.new_now_local(), snapshot_data)

        self.assertEqual(1, len(await db.get_all_results()))
        self.assertEqual(1, len(await db.get_all_snapshots("my_res_id")))
        self.assertEqual(1, len(await db.get_all_lane_snapshots("cs_sn_id")))
        self.assertEqual(1, len(await db.get_all_vehicle_snapshots("lane_sn_id")))

        vehs = await db.get_all_vehicle_snapshots("lane_sn_id")
        self.assertEqual(120.0, vehs[0][1])

        await file.delete_async(0, None)

    async def multiple_dbs(self):
        file = Gio.File.new_for_path("test.db")
        db = GlobalSQLite(file)
        await db.open()
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path", "my_project_file_path")

        db2 = GlobalSQLite(file)
        await db2.open()
        await db2.add_project("my_project_id_2", SimulatorType("0", "Vissim"),
                              "my_simulator_file_path", "my_project_file_path")

        db3 = GlobalSQLite(file)
        await db3.open()
        self.assertEqual(len(await db3.get_all_projects()), 2)

        await file.delete_async(0, None)

    async def add_entire_result(self):
        file = Gio.File.new_for_path("test.db")
        db = GlobalSQLite(file)
        await db.open()
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path", "my_project_file_path")

        veh_sn = [("lane_sn_id", 0, 120.0)]
        lane_sn = [("lane_sn_id", "cs_sn_id", 0, 120.0, 5, 0, veh_sn)]
        cs_sn = [("cs_sn_id", "sn_id", "cs_id", "cs_name", 0, lane_sn)]
        snapshot_data = [("sn_id", "my_res_id", GLib.DateTime.new_now_local().format_iso8601(), cs_sn)]
        await db.add_entire_result("my_res_id", "my_res_name", "my_project_name",
                                   GLib.DateTime.new_now_local(), snapshot_data)

        self.assertEqual(1, len(await db.get_all_results()))
        self.assertEqual(1, len(await db.get_all_snapshots("my_res_id")))
        self.assertEqual(1, len(await db.get_all_lane_snapshots("cs_sn_id")))
        self.assertEqual(1, len(await db.get_all_vehicle_snapshots("lane_sn_id")))

        vehs = await db.get_all_vehicle_snapshots("lane_sn_id")
        self.assertEqual(120.0, vehs[0][1])

        await file.delete_async(0, None)
