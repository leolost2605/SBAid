import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import GLib, Gio

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.tag import Tag
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot
from sbaid.view_model.results.result import Result
from sbaid.model.results.result import Result as ModelResult


class ProjectDatabaseTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectDatabaseTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:

    async def result_nest(self):
        global_db_file = Gio.File.new_for_path("test_global_db")
        global_db = GlobalSQLite(global_db_file)
        await global_db.open()

        model_result = ModelResult("my_result_id",
                                   "my_project_name",
                                   GLib.DateTime.new_now_local(),
                                   global_db)

        vehicle_snapshot = VehicleSnapshot("lane_snapshot_id",
                                           VehicleType.CAR,
                                           0.0)

        lane_snapshot = LaneSnapshot("cross_section_snapshot_id",
                                     "lane_snapshot_id",
                                     0,
                                     0.0,
                                     1,
                                     ADisplay.OFF,
                                     global_db)

        lane_snapshot.add_vehicle_snapshot(vehicle_snapshot)

        cs_snapshot = CrossSectionSnapshot("snapshot_id",
                                           "cross_section_snapshot_id",
                                           "cross_section_name",
                                           "cross_section_id",
                                           BDisplay.OFF,
                                           global_db)

        cs_snapshot.add_lane_snapshot(lane_snapshot)

        snapshot = Snapshot("snapshot_id",
                            GLib.DateTime.new_now_local(),
                            global_db)
        snapshot.add_cross_section_snapshot(cs_snapshot)

        snapshot.add_cross_section_snapshot()


        model_result.add_snapshot(snapshot)


        result = Result(model_result, Gio.ListStore.new(Tag))


        new_model_result = ModelResult("")



