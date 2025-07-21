import asyncio
import unittest

from gi.repository import Gio
from gi.repository.GLib import DateTime, TimeZone
from gi.events import GLibEventLoopPolicy

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.database.global_sqlite import GlobalSQLite

def event_loop_instance(request):
    """ Add the event_loop as an attribute to the unittest style test class. """
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()

class GlobalSQLiteTest(unittest.TestCase):

    def setUp(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(GlobalSQLiteTest().run_all_tests())
        loop.run_until_complete(task)

    async def run_all_tests(self) -> None:
        await self.test_remove()
        await self.test_result()
        await self.test_snapshot()
        await self.test_cross_section_snapshot()
        await self.test_lane_snapshot()
        await self.test_times()
        await self.test_tags()

    async def test_remove(self) -> None:
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test.db")
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

        file.trash_async(0)

    async def test_result(self) -> None:
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test2.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"), "my_simulator_file_path",
                             "my_project_file_path")
        all_projects = await db.get_all_projects()
        self.assertEqual(len(all_projects), 1)
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))
        all_results = await db.get_all_results()
        self.assertEqual(len(all_results), 1)
        self.assertEqual(await db.get_result_name("my_result_id"), "my_result_name")
        await db.delete_result("my_result_id")
        all_results = await db.get_all_results()
        self.assertEqual(len(all_results), 0)

        file.trash_async(0)

    async def test_snapshot(self):
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test3.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))

        self.assertEqual(len(await db.get_all_snapshots("my_result_id")), 0)

        await db.add_snapshot("my_snapshot_id", "my_result_id",
         DateTime.new_now(TimeZone.new("Europe/Berlin")))

        self.assertEqual(len(await db.get_all_snapshots("my_snapshot_id")), 1)

        file.trash_async(0)

    async def test_cross_section_snapshot(self):
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test4.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))
        await db.add_cross_section_snapshot("my_cross_section_snapshot_id",
                                            "my_snapshot_id", "my_cross_section_name",
                                            BDisplay.OFF)
        self.assertEqual(len(await db.get_all_cross_section_snapshots("my_snapshot_id")), 1)
        await db.add_cross_section_snapshot("my_cross_section_snapshot_id_2",
                                            "my_snapshot_id", "my_cross_section_name",
                                            BDisplay.OFF)
        self.assertEqual(len(await db.get_all_cross_section_snapshots("my_snapshot_id")), 2)

        file.trash_async(0)

    async def test_lane_snapshot(self):
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test5.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name", DateTime.new_now(TimeZone.new("Europe/Berlin")))
        await db.add_cross_section_snapshot("my_cross_section_snapshot_id", "my_snapshot_id",
                                             "my_cross_section_name", BDisplay.OFF)
        await db.add_lane_snapshot("my_lane_snapshot_id", "my_cross_section_snapshot_id",
                                   1, 129.35, 25, ADisplay.OFF)

        self.assertEqual(len(await db.get_all_lane_snapshots("my_cross_section_snapshot_id")), 1)
        cs_snapshot = await db.get_all_lane_snapshots("my_cross_section_snapshot_id")
        self.assertEqual(cs_snapshot[0][4], ADisplay.OFF)

        file.trash_async(0)

    async def test_times(self):
        red_revo_date = DateTime.new_from_iso8601("1917-10-25T08:00:00.200000+02",
                                                       TimeZone.new("Europe/Berlin"))
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test6.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name",
                            red_revo_date)
        all_results = await db.get_all_results()
        result_time = all_results[0][1]
        self.assertEqual(result_time.format_iso8601(), red_revo_date.format_iso8601())

        file.trash_async(0)

    async def test_tags(self):
        red_revo_date = DateTime.new_from_iso8601("1917-10-25T08:00:00.200000+02",
                                                       TimeZone.new("Europe/Berlin"))
        db = GlobalSQLite()
        file = Gio.File.new_for_path("test7.db")
        await db.open(file)
        await db.add_project("my_project_id", SimulatorType("0", "Vissim"),
                             "my_simulator_file_path",
                             "my_project_file_path")
        await db.add_result("my_result_id", "my_result_name",
                             "my_project_name",
                            red_revo_date)

        await db.add_tag("my_tag_id", "my_tag_name")

        await db.add_result_tag("my_result_tag_id", "my_result_id", "my_tag_id")
        my_project_tags = await db.get_result_tags("my_result_id")
        self.assertEqual(len(my_project_tags), 1)
        self.assertEqual(my_project_tags[0][0], "my_tag_id")

        file.trash_async(0)
