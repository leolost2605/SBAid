import asyncio
import unittest
from typing import cast

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context as ModelContext
from sbaid.model.project import AlgorithmConfigurationException
from sbaid.view_model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.view_model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager
from sbaid.view_model.context import Context
from sbaid.view_model.project import Project


class ContextProjectsTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ContextProjectsTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:
        await self.simple()
        # await self.simulate()

    async def simple(self) -> None:
        model_context = ModelContext()
        vm_context = Context(model_context)
        await vm_context.load()

        await vm_context.create_project("project_name_1",
                                  SimulatorType("dummy_json", "JSON Dummy"),
                                  "sim_file_path",
                                  "project_file_path")


        self.assertEqual(1, len(vm_context.projects))
        self.assertEqual(1, len(model_context.projects))

        await vm_context.create_project("project_name_2",
                                  SimulatorType("dummy_json", "JSON Dummy"),
                                  "sim_file_path",
                                  "project_file_path")

        self.assertEqual(2, len(model_context.projects))
        self.assertEqual(2, len(vm_context.projects))

        # create new instances in order to mimic app restart
        model_context_2 = ModelContext()
        context_2 = Context(model_context_2)
        await context_2.load()

        self.assertEqual(2, context_2.projects.get_n_items())

        await context_2.delete_project(context_2.projects[1].id)

        self.assertEqual(1, model_context_2.projects.get_n_items())
        self.assertEqual(1, context_2.projects.get_n_items())

        # tear down
        global_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])
        project_file = Gio.File.new_for_path("project_file_path")
        await global_file.delete_async(0)
        await project_file.delete_async(0)

    async def simulate(self) -> None:
        model_context = ModelContext()
        context = Context(model_context)
        await context.load()
        await context.create_project("project_name",
                                     SimulatorType("dummy_json", "JSON Dummy"),
                                     "tests/integration/test_dummy.json",
                                     "project_file")
        project = cast(Project, context.projects.get_item(0))

        with self.assertRaises(AlgorithmConfigurationException):
            await project.start_simulation()

        alcom = cast(AlgorithmConfigurationManager, project.algorithm_configuration_manager)
        assert alcom is not None
        await alcom.create_algorithm_configuration()
        selected_alco = cast(AlgorithmConfiguration, alcom.algorithm_configurations.get_item(0))
        selected_alco.script_path = "tests/integration/algo.py"
        simulation = await project.start_simulation()
        self.assertEqual(1, context.result_manager.results.get_n_items())

        # cleanup:
        global_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])
        project_file = Gio.File.new_for_path("project_file/db")
        project_directory = Gio.File.new_for_path("project_file")
        await global_file.delete_async(0)
        await project_file.delete_async(0)
        await project_directory.delete_async(0)
