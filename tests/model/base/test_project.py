"""TODO"""
import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context


class ProjectTestCase(unittest.TestCase):

    def on_delete_async(feld, file, result, user_data):
        file.delete_finish(result)


    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:
        # TODO test start_simulation (only works when dependencies are implemented
        await self.load_from_db()
        # load is not tested as it only delegates to network and
        # algorithm configuration manager loading


    async def load_from_db(self) -> None:
        sim_type = SimulatorType("dummy_json", "Dummy Simulator")
        context = Context()
        await context.load()
        my_project_id = await context.create_project(sim_type, "sim_file_path", "proj_file_path")
        project = context.projects.get_item(0)
        project.name = "my_cool_name"
        created_at = project.created_at

        self.assertEqual(project.name, "my_cool_name")
        self.assertEqual(project.id, my_project_id)
        self.assertEqual(project.simulator_type, sim_type)
        self.assertEqual(project.simulation_file_path, "sim_file_path")
        self.assertEqual(project.project_file_path, "proj_file_path")

        context2 = Context()
        await context2.load()
        project2 = context.projects.get_item(0)
        self.assertEqual("my_cool_name", project2.name)
        self.assertEqual(created_at, project2.created_at)

        await Gio.File.new_for_path("proj_file_path").delete_async(0)
        await Gio.File.new_for_path("global_db").delete_async(0)
