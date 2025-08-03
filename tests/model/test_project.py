import asyncio
import unittest
from unittest.mock import Mock, AsyncMock

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context
from sbaid.model.project import Project


class ProjectTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:
        await self.load_from_db()
        await self.start_simulation()

    async def load_from_db(self) -> None:
        sim_type = SimulatorType("dummy_json", "Dummy Simulator")

        context = Context()
        await context.load()

        my_project_id = await context.create_project("my_cool_name", sim_type, "sim_file_path", "proj_file_path")
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

        db_mock = Mock()
        db_mock.get_project_name = AsyncMock(return_value="my loaded name")
        db_mock.get_created_at = AsyncMock(return_value=GLib.DateTime.new_now_local())
        db_mock.get_last_modified_at = AsyncMock(return_value=GLib.DateTime.new_now_local())

        project = Project("myid", sim_type, "sim_file_path", "proj_file_path", db_mock)
        await project.load_from_db()

        self.assertEqual(project.name, "my loaded name")
        self.assertEqual(project.id, "myid")
        self.assertEqual(project.simulation_file_path, "sim_file_path")

    async def start_simulation(self):
        sim_type = SimulatorType("dummy_json", "Dummy Simulator")

        project = Project("myid", sim_type, "sim_file_path", "proj_file_path", Mock())
        await project.algorithm_configuration_manager.create_algorithm_configuration()

        observer = Mock()

        await project.start_simulation(observer)

