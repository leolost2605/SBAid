import asyncio
import unittest

from gi.repository import Gio
from gi.repository.GLib import DateTime, TimeZone
from gi.events import GLibEventLoopPolicy

from sbaid.common.vehicle_type import VehicleType
from sbaid.model.database.foreign_key_error import ForeignKeyError
from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
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
        await self.result()
        await self.snapshot()
        await self.cross_section_snapshot()
        await self.lane_snapshot()
        await self.times()
        await self.tags()
        await self.foreign_key_error()
        await self.multiple_context_managers()

    def on_delete_async(feld, file, result, user_data):
        file.delete_finish(result)


    async def path(self):
        file = Gio.File.new_for_path("recursive/directories/test/apparently/successful/test.db")
        async with GlobalSQLite(file) as db:
            self.assertTrue(file.query_exists())
        file.delete_async(0, None, self.on_delete_async, None)

    async def remove(self) -> None:
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            self.assertEqual(len(await db.get_all_projects()), 0)
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"), "my_simulator_file_path", "my_project_file_path")
            all_projects = await db.get_all_projects()
            self.assertEqual(len(all_projects), 1)

            await db.remove_project("my_project_id")
            all_projects = await db.get_all_projects()
            self.assertEqual(len(all_projects), 0)

            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"), "my_simulator_file_path", "my_project_file_path")
            all_projects = await db.get_all_projects()
            self.assertEqual(len(all_projects), 1)

        file.delete_async(0, None, self.on_delete_async, None)

    async def result(self) -> None:
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            self.assertEqual(len(await db.get_all_projects()), 0)
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"), "my_simulator_file_path",
                                 "my_project_file_path")
            all_projects = await db.get_all_projects()
            self.assertEqual(len(all_projects), 1)
            await db.add_result("my_result_id", "my_result_name",
                                 "my_project_name", DateTime.new_now(TimeZone.new_utc()))
            all_results = await db.get_all_results()
            self.assertEqual(len(all_results), 1)
            self.assertEqual(await db.get_result_name("my_result_id"), "my_result_name")
            await db.delete_result("my_result_id")
            all_results = await db.get_all_results()
            self.assertEqual(len(all_results), 0)

        file.delete_async(0, None, self.on_delete_async, None)

    async def snapshot(self):
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"),
                                 "my_simulator_file_path",
                                 "my_project_file_path")
            await db.add_result("my_result_id", "my_result_name",
                                 "my_project_name", DateTime.new_now(TimeZone.new_utc()))

            self.assertEqual(len(await db.get_all_snapshots("my_result_id")), 0)

            await db.add_snapshot("my_snapshot_id", "my_result_id",
             DateTime.new_now(TimeZone.new_utc()))

            self.assertEqual(len(await db.get_all_snapshots("my_snapshot_id")), 1)

        file.delete_async(0, None, self.on_delete_async, None)

    async def cross_section_snapshot(self):
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"),
                                 "my_simulator_file_path",
                                 "my_project_file_path")
            await db.add_result("my_result_id", "my_result_name",
                                 "my_project_name", DateTime.new_now(TimeZone.new_utc()))
            await db.add_snapshot("my_snapshot_id", "my_result_id",
                                  DateTime.new_now(TimeZone.new_utc()))

            await db.add_cross_section_snapshot("my_cross_section_snapshot_id",
                                                "my_snapshot_id", "my_cross_section_name",
                                                BDisplay.OFF)
            self.assertEqual(len(await db.get_all_cross_section_snapshots("my_snapshot_id")), 1)
            await db.add_cross_section_snapshot("my_cross_section_snapshot_id_2",
                                                "my_snapshot_id", "my_cross_section_name",
                                                BDisplay.OFF)
            self.assertEqual(len(await db.get_all_cross_section_snapshots("my_snapshot_id")), 2)

        file.delete_async(0, None, self.on_delete_async, None)

    async def lane_snapshot(self):
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"),
                                 "my_simulator_file_path",
                                 "my_project_file_path")
            await db.add_result("my_result_id", "my_result_name",
                                 "my_project_name", DateTime.new_now(TimeZone.new_utc()))
            await db.add_snapshot("my_snapshot_id", "my_result_id",
                                  DateTime.new_now(TimeZone.new_utc()))
            await db.add_cross_section_snapshot("my_cross_section_snapshot_id", "my_snapshot_id",
                                                 "my_cross_section_name", BDisplay.OFF)
            await db.add_lane_snapshot("my_lane_snapshot_id", "my_cross_section_snapshot_id",
                                       1, 129.35, 25, ADisplay.OFF)

            self.assertEqual(len(await db.get_all_lane_snapshots("my_cross_section_snapshot_id")), 1)
            cs_snapshot = await db.get_all_lane_snapshots("my_cross_section_snapshot_id")
            self.assertEqual(cs_snapshot[0][4], ADisplay.OFF)

        file.delete_async(0, None, self.on_delete_async, None)

    async def times(self):
        revo_date = DateTime.new_from_iso8601("1917-10-25T08:00:00.200000+02",
                                                       TimeZone.new_utc())
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"),
                                 "my_simulator_file_path",
                                 "my_project_file_path")
            await db.add_result("my_result_id", "my_result_name",
                                 "my_project_name",
                                revo_date)
            all_results = await db.get_all_results()
            result_time = all_results[0][1]
            self.assertEqual(result_time.format_iso8601(), revo_date.format_iso8601())

        file.delete_async(0, None, self.on_delete_async, None)

    async def tags(self):
        revo_date = DateTime.new_from_iso8601("1917-10-25T08:00:00.200000+02",
                                                       TimeZone.new_utc())
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"),
                                 "my_simulator_file_path",
                                 "my_project_file_path")
            await db.add_result("my_result_id", "my_result_name",
                                 "my_project_name",
                                revo_date)

            await db.add_tag("my_tag_id", "my_tag_name")

            await db.add_result_tag("my_result_tag_id", "my_result_id", "my_tag_id")
            my_project_tags = await db.get_result_tags("my_result_id")
            self.assertEqual(len(my_project_tags), 1)
            self.assertEqual(my_project_tags[0][0], "my_tag_id")

        file.delete_async(0, None, self.on_delete_async, None)

    async def foreign_key_error(self):
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            with self.assertRaises(ForeignKeyError):
                await db.add_snapshot("my_snapshot_id", "my_nonexistent_result_id",
                                      DateTime.new_now(TimeZone.new_utc()))
            with self.assertRaises(ForeignKeyError):
                await db.add_cross_section_snapshot("my_cross_section_snapshot_id",
                                                    "my_nonexistent_snapshot_id",
                                                    "my_cross_section_name", BDisplay.OFF)
            with self.assertRaises(ForeignKeyError):
                await db.add_lane_snapshot("my_lane_snapshot_id",
                                           "my_nonexistent_snapshot_id", 0, 0.0, 0, ADisplay.OFF)
            with self.assertRaises(ForeignKeyError):
                await db.add_vehicle_snapshot("my_nonexistent_lane_snapshot_id",
                                              VehicleType.CAR, 100.0)
        file.delete_async(0, None, self.on_delete_async, None)

    async def multiple_context_managers(self):
        file = Gio.File.new_for_path("test.db")
        async with GlobalSQLite(file) as db:
            await db.add_project("my_project_id", "proj_name", SimulatorType("0", "Vissim"),
                                 "my_simulator_file_path", "my_project_file_path")

        async with GlobalSQLite(file) as db2:
            await db2.add_project("my_project_id_2", "proj_name", SimulatorType("0", "Vissim"),
                                  "my_simulator_file_path", "my_project_file_path")

        async with GlobalSQLite(file) as db3:
            self.assertEqual(len(await db3.get_all_projects()), 2)

        file.delete_async(0, None, self.on_delete_async, None)
