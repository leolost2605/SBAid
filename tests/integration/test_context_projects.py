import asyncio
import unittest
from typing import cast

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context as ModelContext
from sbaid.model.project import AlgorithmConfigurationException
from sbaid.view_model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
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
        # await self.test_start_simulation()

    async def simple(self) -> None:
        model_context = ModelContext()
        vm_context = Context(model_context)
        await vm_context.load()

        # TODO check for duplicate project id
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

        await context_2.delete_project(context_2.projects[0].id)

        self.assertEqual(1, model_context_2.projects.get_n_items())
        self.assertEqual(1, context_2.projects.get_n_items())

        # tear down
        global_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])
        await global_file.delete_async(0)


    async def test_start_simulation(self) -> None:
        model_context = ModelContext()
        vm_context = Context(model_context)
        await vm_context.create_project("project_name_1",
                                        SimulatorType("dummy_json", "JSON Dummy"),
                                        "sim_file_path",
                                        "project_file_path")
        vm_project = cast(Project, vm_context.projects[0])

        with self.assertRaises(AlgorithmConfigurationException):
            await vm_project.start_simulation()

        await vm_project.algorithm_configuration_manager.create_algorithm_configuration()
        algo_config = cast(AlgorithmConfiguration, vm_project.algorithm_configuration_manager.algorithm_configurations[0])
        algo_config.script_path = "algo.py"
        vm_project.algorithm_configuration_manager.algorithm_configurations.set_selected(0)
        await vm_project.start_simulation()
        self.assertEqual(1, len(vm_context.result_manager.results))
