import asyncio
import unittest
from unittest.mock import Mock, AsyncMock

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context
from sbaid.model.project import Project
from sbaid.model.results.result_manager import ResultManager


class ProjectTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:
        await self.create_via_context()
        await self.start_simulation()

    async def create_via_context(self) -> None:
        sim_type = SimulatorType("dummy_json", "Dummy Simulator")

        context = Context()
        await context.load()

        my_project_id = await context.create_project("my_cool_name", sim_type, "sim_file_path", "proj_file_path")
        project = context.projects.get_item(0)

        self.assertEqual(project.name, "my_cool_name")
        project.name = "my_cool_other_name"

        self.assertEqual(project.name, "my_cool_other_name")
        self.assertEqual(project.id, my_project_id)
        self.assertEqual(project.simulator_type, sim_type)
        self.assertEqual(project.simulation_file_path, "sim_file_path")
        self.assertEqual(project.project_file_path, "proj_file_path")

        result_manager = ResultManager()

        other_project = Project(my_project_id, sim_type, "sim_file_path", "proj_file_path", result_manager)
        await other_project.load_from_db()

        self.assertEqual(other_project.name, "my_cool_name")
        self.assertEqual(other_project.id, my_project_id)
        self.assertEqual(other_project.simulation_file_path, "sim_file_path")
        self.assertEqual(other_project.project_file_path, "proj_file_path")
        self.assertIsNotNone(other_project.network)
        self.assertIsNotNone(other_project.algorithm_configuration_manager)
        self.assertIsNotNone(other_project.simulator)

        await Gio.File.new_for_path("global_db").delete_async(0)

    async def start_simulation(self):
        sim_type = SimulatorType("dummy_json", "Dummy Simulator")

        project = Project("myid", sim_type, "sim_file_path", "proj_file_path", ResultManager())
        await project.algorithm_configuration_manager.create_algorithm_configuration()

        observer = Mock()

        await project.start_simulation(observer)

